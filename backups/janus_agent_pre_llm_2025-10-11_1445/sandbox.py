"""Sandbox execution helpers for Janus harness."""
from __future__ import annotations

import os
import shlex
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Mapping, Optional

from .config import SandboxPolicy, ToolConfig
from .tools import ToolResult


@dataclass(slots=True)
class SandboxConfig:
    """Concrete sandbox runtime configuration."""

    policy: SandboxPolicy
    workspace_root: Path
    bubblewrap_path: Path = Path("/usr/bin/bwrap")
    shell_path: Path = Path("/bin/bash")
    dynamic_user: str = "janus"

    def ensure(self) -> None:
        self.workspace_root.mkdir(parents=True, exist_ok=True)


class SandboxExecutor:
    """Executes tool commands inside a bind-mounted namespace via bubblewrap.

    The implementation intentionally stays simple: no long-running daemons, just a
    subprocess wrapper to be invoked per tool call. This keeps the harness portable
    across development and Balaur environments.
    """

    def __init__(self, config: SandboxConfig) -> None:
        self.config = config
        self.config.ensure()
        # When set, the sandbox will always block network irrespective of tool/policy
        self.force_block_network: bool = False

    def __call__(self, command: List[str], tool_config: ToolConfig) -> ToolResult:
        policy = self.config.policy
        workspace = self._allocate_workspace(tool_config.name)
        env = self._prepare_env(tool_config.environment)

        if self.config.bubblewrap_path.exists():
            args = self._build_bwrap_args(policy, workspace, command, tool_config)

            try:
                completed = subprocess.run(
                    args,
                    check=False,
                    capture_output=True,
                    text=True,
                    env=env,
                )
                return ToolResult(
                    ok=completed.returncode == 0,
                    stdout=completed.stdout,
                    stderr=completed.stderr,
                    metadata={
                        "returncode": completed.returncode,
                        "workspace": str(workspace),
                        "command": command,
                    },
                )
            finally:
                self._cleanup_workspace(workspace)

        # Fallback: bubblewrap not available; execute directly in place.
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                env=env,
                cwd=str(tool_config.working_directory) if tool_config.working_directory else None,
            )
            return ToolResult(
                ok=completed.returncode == 0,
                stdout=completed.stdout,
                stderr=completed.stderr,
                metadata={
                    "returncode": completed.returncode,
                    "workspace": str(workspace),
                    "command": command,
                    "sandboxed": False,
                },
            )
        finally:
            self._cleanup_workspace(workspace)

    def _allocate_workspace(self, tool_name: str) -> Path:
        workspace = Path(
            tempfile.mkdtemp(prefix=f"janus-{tool_name}-", dir=self.config.workspace_root)
        )
        return workspace

    def _cleanup_workspace(self, workspace: Path) -> None:
        # We intentionally leave workspace files for auditing unless empty. Auditors
        # can configure logrotate or janitor jobs to prune directories later.
        if not any(workspace.iterdir()):
            workspace.rmdir()

    def _prepare_env(self, overrides: Optional[Mapping[str, str]]) -> Mapping[str, str]:
        env = {key: os.environ[key] for key in self.config.policy.preserved_env if key in os.environ}
        if overrides:
            env.update(overrides)
        return env

    def _build_bwrap_args(
        self,
        policy: SandboxPolicy,
        workspace: Path,
        command: List[str],
        tool_config: ToolConfig,
    ) -> List[str]:
        args: List[str] = [str(self.config.bubblewrap_path)]

        args.extend(["--unshare-pid", "--unshare-ipc", "--unshare-uts"])
        args.extend(["--ro-bind", "/", "/"])

        for ro_path in policy.read_only_paths:
            args.extend(["--ro-bind", str(ro_path), str(ro_path)])

        # Writable workspace and explicit writable paths
        args.extend(["--bind", str(workspace), str(workspace)])
        for writable in policy.writable_paths:
            args.extend(["--bind", str(writable), str(writable)])

        # Proc and dev mounts
        args.extend(["--dev", "/dev"])
        args.extend(["--proc", "/proc"])

        # Network
        if self.force_block_network or not (policy.allow_network or tool_config.allow_network):
            args.append("--unshare-net")

        # Working directory
        workdir = tool_config.working_directory or workspace
        args.extend(["--chdir", str(workdir)])

        # Command invocation via shell for compatibility
        shell_command = shlex.join(command)
        args.extend(["--", str(self.config.shell_path), "-lc", shell_command])

        return args
