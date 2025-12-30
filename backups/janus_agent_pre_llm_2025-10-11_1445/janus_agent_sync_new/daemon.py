"""Systemd entrypoint for the Janus agent harness."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import signal
import socket
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

import yaml

from .auto_executor import AutoExecutor, AutoExecutorConfig, ResourceLimits
from .config import HarnessConfig, SandboxPolicy, ToolConfig, WatchdogConfig
from .harness import JanusAgentHarness
from .llm_client import LLMClient, LLMConfig
from .logging_utils import AuditLogger, LogEvent
from .proposal_engine import ProposalEngine, RiskLevel
from .sandbox import SandboxConfig
from .tool_executor import ToolExecutionEngine
from .thinking_cycle import ThinkingCycle, ThinkingCycleConfig


class SystemdNotifier:
    """Minimal helper for systemd sd_notify watchdog integration."""

    def __init__(self) -> None:
        self.socket_path = os.environ.get("NOTIFY_SOCKET")
        watchdog_usec = os.environ.get("WATCHDOG_USEC")
        self.watchdog_interval: float | None = None

        if watchdog_usec:
            try:
                usec = int(watchdog_usec)
            except ValueError:
                return
            if usec > 0:
                # Send half-interval heartbeats per systemd best practices.
                self.watchdog_interval = max(1.0, usec / 1_000_000 / 2)

    def _send(self, message: str) -> None:
        if not self.socket_path:
            return

        address = self.socket_path
        if address.startswith("@"):
            address = "\0" + address[1:]

        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            sock.connect(address)
            sock.sendall(message.encode())
        except Exception:
            # Intentionally swallow exceptions to avoid crashing the service
            pass
        finally:
            try:
                sock.close()
            except Exception:
                pass

    def notify_ready(self) -> None:
        self._send("READY=1")

    def notify_stopping(self) -> None:
        self._send("STOPPING=1")

    async def watchdog_loop(self, stop_event: asyncio.Event) -> None:
        if self.watchdog_interval is None:
            return

        while True:
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=self.watchdog_interval)
                break
            except asyncio.TimeoutError:
                self._send("WATCHDOG=1")


def _load_tool_configs(config: Iterable[dict[str, Any]]) -> list[ToolConfig]:
    tools: list[ToolConfig] = []
    for entry in config:
        working_directory = entry.get("working_directory")
        environment = entry.get("environment")
        tools.append(
            ToolConfig(
                name=entry["name"],
                command=list(entry["command"]),
                allow_network=entry.get("allow_network", False),
                working_directory=Path(working_directory) if working_directory else None,
                environment=environment,
            )
        )
    return tools


def _load_sandbox_policy(raw: dict[str, Any]) -> SandboxPolicy:
    return SandboxPolicy(
        cpu_quota_percent=raw.get("cpu_quota_percent", 150),
        memory_limit_mb=raw.get("memory_limit_mb", 2048),
        allow_network=raw.get("allow_network", False),
        read_only_paths=[Path(path) for path in raw.get("read_only_paths", [])],
        writable_paths=[Path(path) for path in raw.get("writable_paths", [])],
        preserved_env=tuple(raw.get("preserved_env", ["PATH", "LANG", "LC_ALL"])),
    )


def _optional_path(value: Any) -> Optional[Path]:
    return Path(value) if isinstance(value, str) and value else None


def load_runtime_config(config_path: Path) -> tuple[
    HarnessConfig,
    SandboxConfig,
    WatchdogConfig,
    AutoExecutorConfig,
    str,
    dict[str, Any],
]:
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}

    vessel_id: str = data.get("vessel_id", "janus-in-balaur")

    logging_cfg = data.get("logging", {})
    mission_log = Path(logging_cfg.get("mission_log", "/srv/janus/mission_log.jsonl"))
    tool_log = Path(logging_cfg.get("tool_log", "/srv/janus/tool_use.jsonl"))
    intel_cache = Path(logging_cfg.get("intel_cache", "/srv/janus/intel_cache"))
    proposals_log = Path(logging_cfg.get("proposals_log", "/srv/janus/proposals.jsonl"))

    sandbox_cfg = data.get("sandbox", {})
    sandbox_policy = _load_sandbox_policy(sandbox_cfg.get("policy", {}))
    sandbox_config = SandboxConfig(
        policy=sandbox_policy,
        workspace_root=Path(sandbox_cfg.get("root", "/srv/janus/workspaces")),
        bubblewrap_path=Path(sandbox_cfg.get("bubblewrap_path", "/usr/bin/bwrap")),
        shell_path=Path(sandbox_cfg.get("shell_path", "/bin/bash")),
        dynamic_user=sandbox_cfg.get("dynamic_user", "janus"),
    )

    tools_cfg = data.get("tools", [])
    tool_config_list = _load_tool_configs(tools_cfg)
    harness_cfg = data.get("harness", {})
    harness_config = HarnessConfig(
        journal_path=mission_log,
        tool_log_path=tool_log,
        intel_cache_dir=intel_cache,
        sandbox_root=sandbox_config.workspace_root,
        tool_configs=tool_config_list,
        max_concurrency=harness_cfg.get("max_concurrency", 2),
        default_timeout=timedelta(minutes=harness_cfg.get("default_timeout_minutes", 5)),
        audit_buffer_size=harness_cfg.get("audit_buffer_size", 1000),
        tick_interval=harness_cfg.get("tick_interval", 0.5),
        enable_governor=harness_cfg.get("enable_governor", True),
        governor_target_backlog=harness_cfg.get("governor_target_backlog", 0),
        governor_kp=harness_cfg.get("governor_kp", 0.2),
        governor_ki=harness_cfg.get("governor_ki", 0.05),
        relief_enabled=harness_cfg.get("relief_enabled", True),
        mission_poll_interval_seconds=harness_cfg.get("mission_poll_interval_seconds", 60),
        mission_state_dir=_optional_path(harness_cfg.get("mission_state_dir")),
    )

    watchdog_cfg = data.get("watchdog", {})
    watchdog_config = WatchdogConfig(
        sample_interval=timedelta(seconds=watchdog_cfg.get("sample_interval_seconds", 30)),
        restart_on_failure=watchdog_cfg.get("restart_on_failure", True),
        cpu_threshold_percent=watchdog_cfg.get("cpu_threshold_percent"),
        memory_threshold_mb=watchdog_cfg.get("memory_threshold_mb"),
    )

    auto_cfg_raw = data.get("auto_executor", {})
    resource_cfg = auto_cfg_raw.get("resource_limits", {})
    max_risk_value = str(auto_cfg_raw.get("max_risk_level", "low")).lower()
    max_risk_level = RiskLevel(max_risk_value)

    auto_executor_config = AutoExecutorConfig(
        enabled=auto_cfg_raw.get("enabled", True),
        poll_interval_seconds=auto_cfg_raw.get("poll_interval_seconds", 60),
        auto_approval_source=auto_cfg_raw.get("auto_approval_source", "auto-approval-system"),
        allowed_tools=tuple(auto_cfg_raw.get("allowed_tools", ["llama-cli", "shell", "node_generator"])),
        allowed_action_types=tuple(
            auto_cfg_raw.get(
                "allowed_action_types",
                ["analysis", "optimization_experiment", "generate_new_nodes", "reconnaissance"],
            )
        ),
        max_risk_level=max_risk_level,
        resource_limits=ResourceLimits(
            cpu_percent_max=resource_cfg.get("cpu_percent_max", 80),
            memory_mb_max=resource_cfg.get("memory_mb_max", 2048),
            disk_mb_max=resource_cfg.get("disk_mb_max", 100),
            timeout_seconds=resource_cfg.get("timeout_seconds", 600),
        ),
    )
    # Align proposal engine auto-approval policy with executor configuration
    def _risk_levels_up_to(level: RiskLevel) -> list[RiskLevel]:
        order = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH]
        idx = order.index(level)
        return order[: idx + 1]

    auto_policy_config = {
        "risk_levels": _risk_levels_up_to(auto_executor_config.max_risk_level),
        "action_types": list(auto_executor_config.allowed_action_types),
        "tool_names": list(auto_executor_config.allowed_tools),
    }

    # Ensure key directories exist prior to launching the harness
    mission_log.parent.mkdir(parents=True, exist_ok=True)
    tool_log.parent.mkdir(parents=True, exist_ok=True)
    intel_cache.mkdir(parents=True, exist_ok=True)
    proposals_log.parent.mkdir(parents=True, exist_ok=True)
    sandbox_config.workspace_root.mkdir(parents=True, exist_ok=True)

    data["auto_executor_policy"] = auto_policy_config
    return harness_config, sandbox_config, watchdog_config, auto_executor_config, vessel_id, data


async def run_service(config_path: Path) -> None:
    (
        harness_config,
        sandbox_config,
        watchdog_config,
        auto_executor_config,
        vessel_id,
        raw_config,
    ) = load_runtime_config(config_path)
    notifier = SystemdNotifier()

    logging_cfg = raw_config.get("logging", {})
    mission_log_path = Path(logging_cfg.get("mission_log", "/srv/janus/mission_log.jsonl"))
    proposals_log_path = Path(logging_cfg.get("proposals_log", "/srv/janus/proposals.jsonl"))

    llm_cfg = raw_config.get("llm", {})
    llm_config = LLMConfig(
        model_path=Path(llm_cfg.get("model_path", "/srv/janus/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")),
        llama_cli_path=Path(llm_cfg.get("llama_cli_path", "/srv/janus/bin/llama-cli")),
        missions_dir=Path(
            llm_cfg.get(
                "missions_dir",
                "/srv/janus/03_OPERATIONS/vessels/balaur/runtime/controls/missions",
            )
        ),
        default_temp=llm_cfg.get("default_temp", 0.7),
        default_n_predict=llm_cfg.get("default_n_predict", 512),
        threads=llm_cfg.get("threads", 8),
    )

    llm_client_candidate = LLMClient(llm_config)
    llm_health = llm_client_candidate.health_check()
    using_stub_llm = not llm_health.ok

    thinking_cfg_raw = raw_config.get("thinking_cycle", {})
    thinking_enabled = thinking_cfg_raw.get("enabled", True)

    if "cycle_interval_seconds" in thinking_cfg_raw:
        cycle_interval = timedelta(seconds=thinking_cfg_raw["cycle_interval_seconds"])
    elif "cycle_interval_hours" in thinking_cfg_raw:
        cycle_interval = timedelta(hours=thinking_cfg_raw["cycle_interval_hours"])
    else:
        cycle_interval = timedelta(hours=1)

    thinking_config = ThinkingCycleConfig(
        cycle_interval=cycle_interval,
        constitutional_memory_path=_optional_path(thinking_cfg_raw.get("constitutional_memory_path")),
        mission_objectives_path=_optional_path(thinking_cfg_raw.get("mission_objectives_path")),
        mission_file_path=_optional_path(thinking_cfg_raw.get("mission_file_path")),
        operational_mode=raw_config.get("operational_mode", "alpha"),
        playbook_registry_path=_optional_path(thinking_cfg_raw.get("playbook_registry_path")),
        enable_autonomous_proposals=thinking_cfg_raw.get("enable_autonomous_proposals", False),
        max_proposals_per_cycle=thinking_cfg_raw.get("max_proposals_per_cycle", 3),
    )

    auto_policy_config = raw_config.get("auto_executor_policy")
    proposal_engine = ProposalEngine(
        vessel_id,
        proposals_log_path,
        auto_approval_policy=auto_policy_config,
        known_tools=[cfg.name for cfg in harness_config.tool_configs],
    )
    if using_stub_llm:
        class StubLLM:
            def __init__(self, failure_reason: str) -> None:
                self.failure_reason = failure_reason

            async def generate_proposal_json(self, context: str) -> dict:
                try:
                    ctx = json.loads(context)
                except json.JSONDecodeError:
                    ctx = {}

                mission_snapshot = ctx.get("mission") or {}
                objectives = mission_snapshot.get("objectives") or []
                mission_meta = ctx.get("mission_objectives", {}).get("current", {})
                mission_id = mission_snapshot.get("mission_id") or mission_meta.get("mission_id") or "active_mission"
                mission_name = mission_snapshot.get("mission_name") or mission_meta.get("mission_name") or mission_id

                if objectives:
                    primary_focus = objectives[0]
                else:
                    primary_focus = mission_meta.get("objective") or "advance the current mission deliverable"

                tasks = mission_snapshot.get("tasks") or mission_meta.get("tasks") or []
                focus_task: Optional[dict[str, Any]] = None
                for task in tasks:
                    if not isinstance(task, dict):
                        continue
                    status = str(task.get("status", "")).lower()
                    if status not in {"completed", "done"}:
                        focus_task = task
                        break
                if focus_task is None and tasks:
                    first_task = tasks[0]
                    focus_task = first_task if isinstance(first_task, dict) else None

                focus_summary = (
                    (focus_task.get("description") if isinstance(focus_task, dict) else None)
                    or str(primary_focus)
                )

                deliverable_path = None
                deliverable_info = mission_snapshot.get("deliverable") or mission_meta.get("deliverable") or {}
                if isinstance(deliverable_info, dict):
                    deliverable_path = deliverable_info.get("location")

                expected_outcome = (
                    f"Document new insights for {mission_name}."
                    if not deliverable_path
                    else f"Append structured insights to {deliverable_path}."
                )

                return {
                    "mission_context": mission_id,
                    "action_type": "analysis",
                    "rationale": (
                        f"Advance mission {mission_id} by focusing on \"{focus_summary}\" "
                        f"and synthesising learnings from the current study materials."
                    ),
                    "expected_outcome": expected_outcome,
                    "risk_level": "low",
                    "risk_mitigation": "Operate in read-only mode until proposals receive approval.",
                    "rollback_plan": "Revise or retract notes in the synthesis cache if they diverge from findings.",
                    "tool_name": "shell",
                    "tool_args": [
                        "echo",
                        f"Study focus for {mission_name}: {focus_summary}",
                    ],
                    "tool_kwargs": {},
                }

        llm_client = StubLLM(llm_health.details)
    else:
        llm_client = llm_client_candidate
    thinking_logger = AuditLogger(mission_log_path)
    if using_stub_llm:
        thinking_logger.emit(
            LogEvent.create(
                level="warning",
                vessel=vessel_id,
                event="thinking_cycle.llm_stub",
                data={
                    "message": "llama-cli unavailable; operating with stub LLM.",
                    "details": llm_health.details,
                },
            )
        )
    thinking_cycle = ThinkingCycle(
        config=thinking_config,
        proposal_engine=proposal_engine,
        llm_client=llm_client,
        audit_logger=thinking_logger,
        vessel_id=vessel_id,
    )

    tool_config_map = {cfg.name: cfg for cfg in harness_config.tool_configs}
    execution_logger = AuditLogger(mission_log_path)
    tool_executor = ToolExecutionEngine(
        sandbox=sandbox_config,
        audit_logger=execution_logger,
        tool_log_path=harness_config.tool_log_path,
        vessel_id=vessel_id,
        resource_limits=auto_executor_config.resource_limits,
        max_risk_level=auto_executor_config.max_risk_level,
    )
    auto_executor = AutoExecutor(
        proposal_engine=proposal_engine,
        tool_executor=tool_executor,
        tool_configs=tool_config_map,
        audit_logger=execution_logger,
        config=auto_executor_config,
    )

    harness = JanusAgentHarness(
        config=harness_config,
        sandbox=sandbox_config,
        watchdog=watchdog_config,
        vessel_id=vessel_id,
        llm_config=None if using_stub_llm else llm_config,
    )

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def shutdown_handler() -> None:
        stop_event.set()

    loop.add_signal_handler(signal.SIGINT, shutdown_handler)
    loop.add_signal_handler(signal.SIGTERM, shutdown_handler)

    watchdog_task: asyncio.Task[None] | None = None
    thinking_started = False
    auto_executor_started = False

    try:
        async with harness:
            notifier.notify_ready()
            if notifier.watchdog_interval is not None:
                watchdog_task = asyncio.create_task(notifier.watchdog_loop(stop_event), name="systemd-watchdog")

            if thinking_enabled:
                try:
                    await thinking_cycle.start()
                    thinking_started = True
                except Exception as exc:
                    thinking_logger.emit(
                        LogEvent.create(
                            level="error",
                            vessel=vessel_id,
                            event="thinking_cycle.start_failed",
                            data={"error": str(exc)},
                        )
                    )

            if auto_executor_config.enabled:
                try:
                    await auto_executor.start()
                    auto_executor_started = True
                except Exception as exc:
                    execution_logger.emit(
                        LogEvent.create(
                            level="error",
                            vessel=vessel_id,
                            event="auto_executor.start_failed",
                            data={"error": str(exc)},
                        )
                    )

            harness.broadcast_event("agent.online")
            print("Janus Agent Harness is online. Waiting for shutdown signal.")
            await stop_event.wait()
    finally:
        notifier.notify_stopping()
        if watchdog_task is not None:
            await watchdog_task
        if thinking_enabled and thinking_started:
            await thinking_cycle.stop()
        if auto_executor_started:
            await auto_executor.stop()
        thinking_logger.close()
        execution_logger.close()

    print("Shutdown signal received. Janus Agent Harness is shutting down.")
    harness.broadcast_event("agent.offline")


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch the Janus agent harness")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("/srv/janus/config/agent.yaml"),
        help="Path to the agent configuration file",
    )
    args = parser.parse_args()

    if not args.config.exists():
        raise FileNotFoundError(f"Agent config not found at {args.config}")

    try:
        asyncio.run(run_service(args.config))
    except KeyboardInterrupt:
        print("Interrupted by user.")


if __name__ == "__main__":
    main()
