"""Configuration models for the Janus agent harness."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass(slots=True)
class ToolConfig:
    """Configuration for a single tool made available to the agent."""

    name: str
    command: List[str]
    allow_network: bool = False
    working_directory: Optional[Path] = None
    environment: Optional[dict[str, str]] = None


@dataclass(slots=True)
class HarnessConfig:
    """Top-level harness configuration."""

    journal_path: Path
    tool_log_path: Path
    intel_cache_dir: Path
    sandbox_root: Path
    tool_configs: Iterable[ToolConfig]
    max_concurrency: int = 2
    default_timeout: timedelta = timedelta(minutes=5)
    audit_buffer_size: int = 1000
    # Steampunk execution controls
    tick_interval: float = 0.5
    enable_governor: bool = True
    governor_target_backlog: int = 0
    governor_kp: float = 0.2
    governor_ki: float = 0.05
    relief_enabled: bool = True
    mission_poll_interval_seconds: float = 60.0
    mission_state_dir: Optional[Path] = None


@dataclass(slots=True)
class SandboxPolicy:
    """Sandbox execution policy.

    Properties map onto Linux primitive settings used by the sandbox executor. By
    keeping the schema here we can serialize it and ship to Balaur during
    deployment.
    """

    cpu_quota_percent: int = 150
    memory_limit_mb: int = 2048
    allow_network: bool = False
    read_only_paths: Iterable[Path] = field(
        default_factory=lambda: [
            Path("/usr"),
            Path("/bin"),
            Path("/lib"),
            Path("/lib64"),
            Path("/etc"),
        ]
    )
    writable_paths: Iterable[Path] = field(
        default_factory=lambda: [
            Path("/srv/janus/workspaces"),
        ]
    )
    preserved_env: Iterable[str] = field(
        default_factory=lambda: [
            "PATH",
            "LANG",
            "LC_ALL",
        ]
    )


@dataclass(slots=True)
class WatchdogConfig:
    """Resource monitoring parameters for the harness."""

    sample_interval: timedelta = timedelta(seconds=30)
    restart_on_failure: bool = True
    cpu_threshold_percent: Optional[int] = 90
    memory_threshold_mb: Optional[int] = 28_000


@dataclass(slots=True)
class APIKeys:
    """API keys for external services."""
    
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None

    @classmethod
    def load(cls) -> APIKeys:
        """Load API keys from environment variables."""
        return cls(
            gemini_api_key=os.environ.get("GEMINI_API_KEY"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
            groq_api_key=os.environ.get("GROQ_API_KEY"),
        )
