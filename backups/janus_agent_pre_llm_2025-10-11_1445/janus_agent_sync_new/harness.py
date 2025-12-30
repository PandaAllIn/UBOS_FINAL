"""Core Janus agent harness implementation."""
from __future__ import annotations

import asyncio
import json
import os
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING

from .config import HarnessConfig, WatchdogConfig
from .logging_utils import AuditLogger, LogEvent, log_exception
from .sandbox import SandboxConfig, SandboxExecutor
from .tools import ShellTool, ToolRegistry, ToolResult


@dataclass(slots=True)
class ActionRequest:
    """Container describing an action to be executed."""

    action_id: str
    tool_name: str
    args: tuple[str, ...]
    kwargs: dict[str, Any]
    metadata: dict[str, Any]


@dataclass(slots=True)
class ActionResult:
    """Response emitted upon completion of an action."""

    action_id: str
    ok: bool
    stdout: str
    stderr: str
    metadata: dict[str, Any]


if TYPE_CHECKING:
    from .llm_client import LLMConfig


class JanusAgentHarness(AbstractAsyncContextManager["JanusAgentHarness"]):
    """Asynchronous execution harness for Janus autonomous vessel."""

    DEFAULT_STATE_DIR = Path("/srv/janus/runtime/state")

    def __init__(
        self,
        config: HarnessConfig,
        sandbox: SandboxConfig,
        watchdog: Optional[WatchdogConfig] = None,
        vessel_id: str = "janus-in-balaur",
        llm_config: "LLMConfig | None" = None,
    ) -> None:
        self.config = config
        self.watchdog_config = watchdog or WatchdogConfig()
        self.vessel_id = vessel_id
        self.audit_logger = AuditLogger(config.journal_path)
        self.tool_logger = AuditLogger(config.tool_log_path)
        self.registry = ToolRegistry()
        self.executor = SandboxExecutor(sandbox)
        self.llm_config = llm_config
        self._action_queue: "asyncio.Queue[ActionRequest]" = asyncio.Queue()
        self._results: "asyncio.Queue[ActionResult]" = asyncio.Queue()
        self._workers: list[asyncio.Task[None]] = []
        self._shutdown = asyncio.Event()
        # Governor / relief valve state
        self._active_tasks = 0
        self._allowed_concurrency = max(1, self.config.max_concurrency)
        self._integral_error = 0.0
        self._tick_task: Optional[asyncio.Task[None]] = None
        self._monitor_task: Optional[asyncio.Task[None]] = None
        self._mission_watch_task: Optional[asyncio.Task[None]] = None
        self._admission_lock = asyncio.Lock()
        self._degraded = False
        self._mission_poll_interval = max(5.0, float(config.mission_poll_interval_seconds))
        self._mission_context: dict[str, Any] | None = None
        self._state_dir = Path(config.mission_state_dir) if config.mission_state_dir else self.DEFAULT_STATE_DIR
        self._current_mission_path = self._state_dir / "current_mission.json"
        self._next_mission_path = self._state_dir / "next_mission.json"
        self._transition_signal_path = self._state_dir / "mission_transition_signal"
        self._ack_path = self._state_dir / "mission_ack.json"

        # Pre-register tools from configuration
        self.registry.register_from_config(
            config.tool_configs,
            lambda tool_config: ShellTool(tool_config, self.executor),
        )

    async def __aenter__(self) -> "JanusAgentHarness":
        self._start_workers()
        # Start escapement (tick) and relief valve monitors
        self._tick_task = asyncio.create_task(self._tick_loop(), name="janus-escapement")
        if self.watchdog_config and self.config.relief_enabled:
            self._monitor_task = asyncio.create_task(self._relief_valve_loop(), name="janus-relief")
        self._mission_watch_task = asyncio.create_task(self._mission_watch_loop(), name="janus-mission-watch")
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        await self.stop()

    def _start_workers(self) -> None:
        for index in range(self.config.max_concurrency):
            task = asyncio.create_task(self._worker_loop(index), name=f"janus-worker-{index}")
            self._workers.append(task)

    async def _worker_loop(self, worker_index: int) -> None:
        while not self._shutdown.is_set():
            try:
                request = await asyncio.wait_for(self._action_queue.get(), timeout=0.5)
            except asyncio.TimeoutError:
                continue

            # Admission control: respect current allowed_concurrency
            await self._admission_wait()
            self._active_tasks += 1

            self.audit_logger.emit(
                LogEvent.create(
                    level="info",
                    vessel=self.vessel_id,
                    event="action.started",
                    data={
                        "worker": worker_index,
                        "action_id": request.action_id,
                        "tool": request.tool_name,
                    },
                )
            )

            try:
                tool = self.registry.get(request.tool_name)
                result = await tool.run(*request.args, **request.kwargs)
            except Exception as exc:  # pragma: no cover - defensive
                log_exception(self.audit_logger, self.vessel_id, "action.error", exc)
                result = ToolResult(ok=False, stderr=str(exc))

            action_result = ActionResult(
                action_id=request.action_id,
                ok=result.ok,
                stdout=result.stdout,
                stderr=result.stderr,
                metadata=result.metadata or {},
            )

            self._results.put_nowait(action_result)
            self.tool_logger.emit(
                LogEvent.create(
                    level="info" if result.ok else "error",
                    vessel=self.vessel_id,
                    event="action.completed",
                    data={
                        "action_id": request.action_id,
                        "tool": request.tool_name,
                        "ok": result.ok,
                        "metadata": result.metadata or {},
                    },
                )
            )

            self._action_queue.task_done()
            # Release admission slot
            async with self._admission_lock:
                self._active_tasks = max(0, self._active_tasks - 1)

    async def stop(self) -> None:
        if self._shutdown.is_set():
            return
        self._shutdown.set()
        for task in self._workers:
            task.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)
        if self._tick_task:
            self._tick_task.cancel()
            await asyncio.gather(self._tick_task, return_exceptions=True)
        if self._monitor_task:
            self._monitor_task.cancel()
            await asyncio.gather(self._monitor_task, return_exceptions=True)
        if self._mission_watch_task:
            self._mission_watch_task.cancel()
            await asyncio.gather(self._mission_watch_task, return_exceptions=True)
        self.audit_logger.close()
        self.tool_logger.close()

    async def enqueue_action(
        self,
        action_id: str,
        tool_name: str,
        *args: str,
        metadata: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        request = ActionRequest(
            action_id=action_id,
            tool_name=tool_name,
            args=args,
            kwargs=kwargs,
            metadata=metadata or {},
        )
        await self._action_queue.put(request)

    async def next_result(self, timeout: float | None = 30.0) -> Optional[ActionResult]:
        try:
            return await asyncio.wait_for(self._results.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    def list_tools(self) -> list[str]:
        return self.registry.list_tools()

    def broadcast_event(self, event: str, payload: Optional[dict[str, Any]] = None) -> None:
        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event=event,
                data=payload or {},
            )
        )

    async def _mission_watch_loop(self) -> None:
        """Poll for mission transition signals and reload mission context."""
        interval = self._mission_poll_interval
        # Ensure the state directory exists so that touch/write operations succeed.
        try:
            self._state_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass

        while not self._shutdown.is_set():
            try:
                await self._check_for_mission_transition()
            except Exception as exc:  # pragma: no cover - defensive logging
                log_exception(self.audit_logger, self.vessel_id, "mission.transition.error", exc)
            try:
                await asyncio.wait_for(self._shutdown.wait(), timeout=interval)
                break
            except asyncio.TimeoutError:
                continue

    async def _check_for_mission_transition(self) -> None:
        """Detect staged missions and perform acknowledgment handshake."""
        signal_path = self._transition_signal_path
        if not signal_path.exists():
            return

        mission_data = self._load_next_mission()
        if mission_data is None:
            return

        mission_id = mission_data.get("mission_id", "unknown")
        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="mission.transition.detected",
                data={"mission_id": mission_id},
            )
        )

        self._mission_context = mission_data
        self._write_current_mission(mission_data)
        self._write_acknowledgment(mission_id)
        self._cleanup_transition_files()

        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="mission.transition.applied",
                data={"mission_id": mission_id},
            )
        )

    def _load_next_mission(self) -> Optional[dict[str, Any]]:
        """Load mission payload staged by the orchestrator."""
        try:
            raw = self._next_mission_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            self.audit_logger.emit(
                LogEvent.create(
                    level="error",
                    vessel=self.vessel_id,
                    event="mission.transition.missing_payload",
                    data={"path": str(self._next_mission_path)},
                )
            )
            return None
        except OSError as exc:
            log_exception(self.audit_logger, self.vessel_id, "mission.transition.read_failed", exc)
            return None

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            log_exception(self.audit_logger, self.vessel_id, "mission.transition.invalid_payload", exc)
            return None

    def _write_current_mission(self, mission_data: dict[str, Any]) -> None:
        """Persist mission context for other vessel components."""
        try:
            self._current_mission_path.parent.mkdir(parents=True, exist_ok=True)
            with self._current_mission_path.open("w", encoding="utf-8") as handle:
                json.dump(mission_data, handle, indent=2)
            os.chmod(self._current_mission_path, 0o644)
        except OSError as exc:
            log_exception(self.audit_logger, self.vessel_id, "mission.transition.write_current_failed", exc)

    def _write_acknowledgment(self, mission_id: str) -> None:
        """Emit mission acknowledgment for orchestrator handshake."""
        ack_payload = {
            "mission_id": mission_id,
            "transition_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "acknowledged",
        }
        try:
            self._ack_path.parent.mkdir(parents=True, exist_ok=True)
            with self._ack_path.open("w", encoding="utf-8") as handle:
                json.dump(ack_payload, handle, indent=2)
            os.chmod(self._ack_path, 0o644)
        except OSError as exc:
            log_exception(self.audit_logger, self.vessel_id, "mission.transition.write_ack_failed", exc)

    def _cleanup_transition_files(self) -> None:
        """Remove semaphore artifacts once the mission has been loaded."""
        for path in (self._transition_signal_path, self._next_mission_path):
            try:
                if path.exists():
                    path.unlink()
            except OSError as exc:
                log_exception(self.audit_logger, self.vessel_id, "mission.transition.cleanup_failed", exc)

    async def _admission_wait(self) -> None:
        """Block until there is capacity under governor limits."""
        while not self._shutdown.is_set():
            async with self._admission_lock:
                if self._active_tasks < self._allowed_concurrency:
                    return
            await asyncio.sleep(self.config.tick_interval)

    async def _tick_loop(self) -> None:
        """Escapement ticker + PI governor adjusting concurrency."""
        interval = max(0.05, float(self.config.tick_interval))
        while not self._shutdown.is_set():
            await asyncio.sleep(interval)
            qsize = self._action_queue.qsize()
            # Emit tick event (low volume)
            self.audit_logger.emit(
                LogEvent.create(
                    level="debug",
                    vessel=self.vessel_id,
                    event="tick",
                    data={"queue": qsize, "active": self._active_tasks, "allowed": self._allowed_concurrency},
                )
            )

            if not self.config.enable_governor or self._degraded:
                continue

            error = float(qsize - int(self.config.governor_target_backlog))
            self._integral_error += error * interval
            delta = self.config.governor_kp * error + self.config.governor_ki * self._integral_error
            new_allowed = int(round(self._allowed_concurrency + delta))
            new_allowed = max(1, min(self.config.max_concurrency, new_allowed))
            if new_allowed != self._allowed_concurrency:
                self._allowed_concurrency = new_allowed
                self.audit_logger.emit(
                    LogEvent.create(
                        level="info",
                        vessel=self.vessel_id,
                        event="governor.update",
                        data={"allowed": new_allowed, "error": error},
                    )
                )

    async def _relief_valve_loop(self) -> None:
        """Monitor system load/memory to degrade or restore operation."""
        interval = max(1.0, float(self.watchdog_config.sample_interval.total_seconds()))
        while not self._shutdown.is_set():
            await asyncio.sleep(interval)
            try:
                load1 = os.getloadavg()[0]
            except OSError:
                load1 = 0.0

            mem_total = 0
            mem_available = 0
            try:
                with open("/proc/meminfo", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("MemTotal:"):
                            mem_total = int(line.split()[1])  # kB
                        elif line.startswith("MemAvailable:"):
                            mem_available = int(line.split()[1])
                used_mb = max(0, (mem_total - mem_available) // 1024)
            except FileNotFoundError:
                used_mb = 0

            exceed_cpu = self.watchdog_config.cpu_threshold_percent is not None and (load1 * 100 / max(1, os.cpu_count() or 1)) > self.watchdog_config.cpu_threshold_percent
            exceed_mem = self.watchdog_config.memory_threshold_mb is not None and used_mb > self.watchdog_config.memory_threshold_mb

            if (exceed_cpu or exceed_mem) and not self._degraded:
                self._degraded = True
                self.executor.force_block_network = True
                self._allowed_concurrency = 1
                self.audit_logger.emit(
                    LogEvent.create(
                        level="warn",
                        vessel=self.vessel_id,
                        event="relief.degrade",
                        data={"load1": load1, "used_mb": used_mb},
                    )
                )
            elif not exceed_cpu and not exceed_mem and self._degraded:
                self._degraded = False
                self.executor.force_block_network = False
                self._allowed_concurrency = max(1, min(self._allowed_concurrency, self.config.max_concurrency))
                self.audit_logger.emit(
                    LogEvent.create(
                        level="info",
                        vessel=self.vessel_id,
                        event="relief.restore",
                        data={"load1": load1, "used_mb": used_mb},
                    )
                )
