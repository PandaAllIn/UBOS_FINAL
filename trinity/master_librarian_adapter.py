from __future__ import annotations

import os
import re
import shlex
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from config import TrinityPaths, load_configuration
from tool_audit_logger import audit_tool_call


@dataclass(slots=True)
class SandboxConfig:
    """Concrete sandbox runtime configuration."""

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

    def __call__(self, command: List[str], tool_config) -> Dict:
        workspace = self._allocate_workspace(tool_config.name)
        env = self._prepare_env(tool_config.environment)

        if self.config.bubblewrap_path.exists():
            args = self._build_bwrap_args(workspace, command, tool_config)

            try:
                completed = subprocess.run(
                    args,
                    check=False,
                    capture_output=True,
                    text=True,
                    env=env,
                )
                return {
                        "ok": completed.returncode == 0,
                        "stdout": completed.stdout,
                        "stderr": completed.stderr,
                        "returncode": completed.returncode,
                    }
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
            return {
                    "ok": completed.returncode == 0,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                    "returncode": completed.returncode,
                }
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
        env = {key: os.environ[key] for key in [] if key in os.environ}
        if overrides:
            env.update(overrides)
        return env

    def _build_bwrap_args(
        self,
        workspace: Path,
        command: List[str],
        tool_config,
    ) -> List[str]:
        args: List[str] = [str(self.config.bubblewrap_path)]

        args.extend(["--unshare-pid", "--unshare-ipc", "--unshare-uts"])
        args.extend(["--ro-bind", "/", "/"])

        # Writable workspace and explicit writable paths
        args.extend(["--bind", str(workspace), str(workspace)])

        # Proc and dev mounts
        args.extend(["--dev", "/dev"])
        args.extend(["--proc", "/proc"])

        # Network
        if self.force_block_network:
            args.append("--unshare-net")

        # Working directory
        workdir = tool_config.working_directory or workspace
        args.extend(["--chdir", str(workdir)])

        # Command invocation via shell for compatibility
        shell_command = shlex.join(command)
        args.extend(["--", str(self.config.shell_path), "-lc", shell_command])

        return args

@dataclass
class MasterLibrarianAdapter:
    paths: TrinityPaths

    def __init__(self, paths: TrinityPaths | None = None) -> None:
        self.paths = paths or load_configuration()[0]
        self._allowed_roots: tuple[Path, ...] = self._initialise_allowed_roots()
        self._alias_map: Dict[str, Path] = {root.name: root for root in self._allowed_roots}
        sandbox_config = SandboxConfig(workspace_root=self.paths.base_dir / "sandbox_workspace")
        self.sandbox = SandboxExecutor(sandbox_config)


    async def consult(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"query": query, "context": context, "summary": "Consultation recorded (stub)."}

    # ------------------------------------------------------------------ file access
    @audit_tool_call("librarian.read_file")
    def read_file(self, path: str | Path) -> str:
        """Read a text file from an approved directory."""
        file_path = self._resolve_path(path, expect_directory=False)
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return file_path.read_text(encoding="utf-8", errors="ignore")

    @audit_tool_call("librarian.write_file")
    def write_file(self, path: str | Path, content: str) -> str:
        """Write a text file to an approved directory."""
        file_path = self._resolve_path(path, expect_directory=False, must_exist=False)
        file_path.write_text(content, encoding="utf-8")
        return f"Successfully wrote to {self._display_path(file_path)}"

    @audit_tool_call("librarian.list_files")
    def list_files(self, directory: str | Path) -> List[str]:
        """List entries within an approved directory."""
        dir_path = self._resolve_path(directory, expect_directory=True)
        return sorted(self._display_path(entry) for entry in dir_path.iterdir())

    @audit_tool_call("librarian.search_content")
    def search_content(self, pattern: str, directory: str | Path) -> Dict[str, List[str]]:
        """Search recursively within an approved directory for a regex pattern."""
        dir_path = self._resolve_path(directory, expect_directory=True)
        regex = re.compile(pattern)
        results: Dict[str, List[str]] = {}

        for file_path in dir_path.rglob("*"):
            if not file_path.is_file():
                continue
            try:
                text = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = file_path.read_text(encoding="utf-8", errors="ignore")

            matches: List[str] = []
            for line_number, line in enumerate(text.splitlines(), start=1):
                if regex.search(line):
                    matches.append(f"{line_number}: {line.strip()}")

            if matches:
                results[self._display_path(file_path)] = matches

        return results

    @audit_tool_call("librarian.execute_shell")
    def execute_shell(self, command: str) -> Dict:
        """Execute a shell command in a sandboxed environment."""
        tool_config = type("ToolConfig", (), {"name": "shell", "environment": {}, "working_directory": self.paths.base_dir, "allow_network": False})
        return self.sandbox(shlex.split(command), tool_config)

    # ------------------------------------------------------------------ helpers
    def _initialise_allowed_roots(self) -> tuple[Path, ...]:
        roots = [
            self.paths.master_librarian_root,
            Path("/srv/janus/00_CONSTITUTION"),
            Path("/srv/janus/01_STRATEGY"),
            self.paths.base_dir / "skills",
            self.paths.log_dir,
            Path("/srv/janus/logs"),
        ]

        normalised: list[Path] = []
        for root in roots:
            resolved = root.expanduser().resolve()
            if resolved not in normalised:
                normalised.append(resolved)
        return tuple(normalised)

    def _resolve_path(self, raw: str | Path, *, expect_directory: bool, must_exist: bool = True) -> Path:
        candidate = Path(raw).expanduser()
        if candidate.is_absolute():
            base_candidates = [candidate]
        else:
            parts = candidate.parts
            if parts and parts[0] in self._alias_map:
                relative = Path(*parts[1:]) if len(parts) > 1 else Path()
                base_candidates = [self._alias_map[parts[0]] / relative]
            else:
                base_candidates = [root / candidate for root in self._allowed_roots]

        found_within = False
        for possible in base_candidates:
            resolved = possible.resolve()
            if not self._is_within_allowed(resolved):
                continue
            found_within = True
            if not must_exist:
                return resolved
            if expect_directory:
                if resolved.is_dir():
                    return resolved
            else:
                if resolved.is_file():
                    return resolved

        if found_within:
            if expect_directory:
                raise FileNotFoundError(f"Directory not found: {raw}")
            raise FileNotFoundError(f"File not found: {raw}")

        raise PermissionError(f"Path '{raw}' is outside permitted Master Librarian directories.")

    def _is_within_allowed(self, path: Path) -> bool:
        for root in self._allowed_roots:
            try:
                path.relative_to(root)
                return True
            except ValueError:
                continue
        return False

    def _display_path(self, path: Path) -> str:
        resolved = path.resolve()
        for root in self._allowed_roots:
            try:
                rel = resolved.relative_to(root)
                rel_display = rel.as_posix()
                if rel_display == ".":
                    return root.name
                return f"{root.name}/{rel_display}"
            except ValueError:
                continue
        return resolved.as_posix()
