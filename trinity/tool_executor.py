from __future__ import annotations

import asyncio
import subprocess
from dataclasses import dataclass
from types import SimpleNamespace


@dataclass
class ToolExecutor:
    async def execute_shell(self, command: str):
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await proc.communicate()
        return SimpleNamespace(ok=proc.returncode == 0, stdout=(out or b"").decode(), stderr=(err or b"").decode(), returncode=proc.returncode)

    async def execute_python_script(self, script_path: str):
        try:
            proc = await asyncio.create_subprocess_exec(
                "python3", script_path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            out, err = await proc.communicate()
            return SimpleNamespace(ok=proc.returncode == 0, stdout=(out or b"").decode(), stderr=(err or b"").decode(), returncode=proc.returncode)
        except FileNotFoundError as e:
            return SimpleNamespace(ok=False, stdout="", stderr=str(e), returncode=127)

