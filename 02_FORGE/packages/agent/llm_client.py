"""
LLM Client for Janus Agent
Connects to the local llama.cpp binary (The Mill) to generate text.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None  # type: ignore

from .config import APIKeys

log = logging.getLogger(__name__)

@dataclass(slots=True)
class LLMConfig:
    """Configuration for the LLM client."""
    model_path: Path
    llama_cli_path: Path
    missions_dir: Path = Path("/srv/janus/03_OPERATIONS/vessels/balaur/runtime/controls/missions")
    default_temp: float = 0.7
    default_n_predict: int = 1024
    threads: int = 8


@dataclass(slots=True)
class LLMHealthStatus:
    ok: bool
    details: str
    resolved_cli_path: Path | None = None


class LLMClient:
    """A client for interacting with the llama.cpp binary."""

    def __init__(self, config: LLMConfig):
        self.config = config

    def _get_active_mission(self) -> Optional[dict]:
        """Best-effort: load an active mission YAML from missions_dir.

        This is a fallback when upstream does not inject mission into the context.
        """
        missions_dir = self.config.missions_dir
        if not missions_dir.exists() or yaml is None:
            return None
        try:
            for mission_file in sorted(missions_dir.glob("*.yaml")):
                data = yaml.safe_load(mission_file.read_text(encoding="utf-8")) or {}
                if str(data.get("status", "")).lower() == "active":
                    return data
        except Exception:
            return None
        return None

    async def generate(
        self,
        prompt: str,
        temperature: float | None = None,
        n_predict: int | None = None,
    ) -> str:
        """Generate text from a prompt using the llama.cpp binary."""
        if not self.config.llama_cli_path.exists():
            raise FileNotFoundError(f"llama.cpp binary not found at {self.config.llama_cli_path}")
        if not self.config.model_path.exists():
            raise FileNotFoundError(f"Model weights not found at {self.config.model_path}")

        temp = temperature if temperature is not None else self.config.default_temp
        n_predict_val = n_predict if n_predict is not None else self.config.default_n_predict

        args = [
            str(self.config.llama_cli_path),
            "-m", str(self.config.model_path),
            "-p", prompt,
            "-n", str(n_predict_val),
            "--temp", str(temp),
            "--threads", str(self.config.threads),
            "--simple-io",  # Use simple I/O for easier parsing
            "--no-display-prompt",
        ]

        log.info(f"Executing LLM generation with {n_predict_val} tokens...")
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode().strip()
            log.error(f"LLM generation failed with code {process.returncode}: {error_msg}")
            raise RuntimeError(f"LLM generation failed: {error_msg}")

        response = stdout.decode().strip()
        log.info(f"LLM generation complete. Response length: {len(response)}")
        return response

    async def generate_proposal_json(self, context: str) -> dict:
        """
        Generate a structured JSON proposal from a context string.
        This is a specialized method for the thinking cycle.
        """
        # A carefully crafted prompt to guide the LLM to produce JSON
        # Optional mission enrichment via fallback directory scan
        mission_segment = ""
        active = self._get_active_mission()
        if active and yaml is not None:
            mission_segment = (
                "\nMISSION CONTEXT (active):\n---\n"
                + yaml.dump(active, indent=2)
                + "---\n"
            )

        prompt = f"""
You are Janus, a constitutional AI operating under Mode Beta (supervised autonomy).
Using the mission context and study materials provided below, generate a single, valid JSON object representing one action proposal that advances the mission.

AVAILABLE TOOLS (you MUST use one of these):
- shell: Execute safe shell commands for analysis, system queries, file operations
- llama-cli: Run local LLM inference for text analysis and synthesis
- node_generator: Generate knowledge graph nodes from study materials
- file_chunker: Split large files into processable chunks

Constraints:
- Output must be ONLY a JSON object, no extra text.
- Keys required: "action_type", "rationale", "expected_outcome", "risk_level", "tool_name", "tool_args".
- "tool_name" MUST be one of: shell, llama-cli, node_generator, file_chunker
- DO NOT invent new tools or use tools not in the list above
- "risk_level" must be one of: "low", "medium", "high".
- "tool_args" must be a list of strings (command arguments)
- Prefer mission-relevant analyses and studies over generic maintenance unless the mission explicitly calls for it.

{mission_segment}
Context:
{context}

JSON Proposal:
"""
        response = await self.generate(prompt, temperature=0.2, n_predict=512)

        try:
            # Clean up the response to find the JSON object
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON object found in LLM response")

            json_str = response[json_start:json_end]
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError) as e:
            log.error(f"Failed to parse JSON from LLM response: {e}")
            log.error(f"Raw response was: {response}")
            raise ValueError("Failed to generate a valid JSON proposal") from e

    # ------------------------------------------------------------------ Health checks
    def health_check(self, *, timeout_seconds: int = 5) -> LLMHealthStatus:
        """Validate llama-cli availability and model readiness."""
        cli_path = self._resolve_cli_path()
        if cli_path is None:
            return LLMHealthStatus(
                ok=False,
                details="Unable to locate llama-cli binary; searched default locations and PATH.",
            )

        if cli_path != self.config.llama_cli_path:
            log.info(
                "Resolved llama-cli path override: %s -> %s",
                self.config.llama_cli_path,
                cli_path,
            )
            self.config.llama_cli_path = cli_path

        if not self.config.model_path.exists():
            return LLMHealthStatus(
                ok=False,
                details=f"Model weights missing at {self.config.model_path}",
                resolved_cli_path=cli_path,
            )

        try:
            completed = subprocess.run(
                [str(self.config.llama_cli_path), "--help"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout_seconds,
                check=False,
            )
        except OSError as exc:
            return LLMHealthStatus(
                ok=False,
                details=f"Failed to execute llama-cli: {exc}",
                resolved_cli_path=cli_path,
            )

        if completed.returncode != 0:
            return LLMHealthStatus(
                ok=False,
                details=f"llama-cli returned non-zero status ({completed.returncode}) during health check.",
                resolved_cli_path=cli_path,
            )

        return LLMHealthStatus(ok=True, details="llama-cli ready", resolved_cli_path=cli_path)

    # ------------------------------------------------------------------ Helpers
    def _resolve_cli_path(self) -> Path | None:
        """Attempt to resolve the llama-cli binary path."""
        candidates: list[Path] = []

        configured = self.config.llama_cli_path
        candidates.append(configured)

        env_path = os.environ.get("LLAMA_CLI_PATH")
        if env_path:
            candidates.append(Path(env_path))

        # Known forge paths documented in the architecture playbooks
        candidates.extend(
            [
                Path("/srv/janus/bin/llama-cli"),
                Path("/opt/llama.cpp/build/bin/llama-cli"),
                Path("/opt/llama.cpp/build-vk/bin/llama-cli"),
            ]
        )

        which_path = shutil.which("llama-cli")
        if which_path:
            candidates.append(Path(which_path))

        seen: set[Path] = set()
        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            if candidate.exists() and candidate.is_file():
                return candidate
        return None


class OracleBridge:
    """Bridge to external Oracle services (Gemini, etc.) via API keys."""
    
    def __init__(self, api_keys: APIKeys):
        self.api_keys = api_keys
        self.enabled = bool(api_keys.gemini_api_key or api_keys.openai_api_key)
        if self.enabled:
            log.info("OracleBridge initialized with available API keys.")
        else:
            log.warning("OracleBridge initialized without API keys. External oracle services unavailable.")

    async def query(self, prompt: str, service: str = "gemini") -> str:
        """Placeholder for external oracle query execution."""
        if not self.enabled:
            raise RuntimeError("OracleBridge is not enabled (missing API keys).")
        
        # In a real implementation, this would call the respective API
        log.info(f"Simulating Oracle query to {service}: {prompt[:50]}...")
        return f"Oracle response from {service} (simulated)"
