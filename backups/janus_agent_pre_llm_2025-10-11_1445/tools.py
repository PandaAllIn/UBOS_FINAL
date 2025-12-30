"""Tool abstraction layer for Janus agent harness."""
from __future__ import annotations

import shlex
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Protocol

from .config import ToolConfig


class Tool(Protocol):
    """Runtime protocol that every tool implementation must satisfy."""

    name: str

    async def run(self, *args: str, **kwargs: Any) -> "ToolResult":  # pragma: no cover - interface
        ...


@dataclass(slots=True)
class ToolResult:
    """Success/failure payload returned by tools."""

    ok: bool
    stdout: str = ""
    stderr: str = ""
    metadata: Dict[str, Any] | None = None

    def __bool__(self) -> bool:
        return self.ok


class ToolRegistry:
    """Registry for dynamically adding/removing tools."""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool

    def register_from_config(
        self,
        config: Iterable[ToolConfig],
        factory: Callable[[ToolConfig], Tool],
    ) -> None:
        for tool_config in config:
            self.register(factory(tool_config))

    def unregister(self, name: str) -> None:
        self._tools.pop(name, None)

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:  # pragma: no cover - defensive
            raise KeyError(f"Unknown tool '{name}'") from exc

    def list_tools(self) -> list[str]:
        return sorted(self._tools)


class ShellTool:
    """Shell command tool executed via sandboxed executor."""

    def __init__(
        self,
        config: ToolConfig,
        executor: "Callable[[list[str], ToolConfig], ToolResult]",
    ) -> None:
        self.config = config
        self._executor = executor
        self.name = config.name

    async def run(self, *args: str, **_: Any) -> ToolResult:
        command = list(self.config.command)
        if args:
            command.extend(args)
        return self._executor(command, self.config)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"ShellTool(name={self.name!r}, command={shlex.join(self.config.command)})"
