from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


DEFAULT_ENV_PATH = Path("/etc/janus/trinity.env")
ALT_ENV_PATHS = [
    Path("/srv/janus/trinity/.env.local"),
]


def _load_env_file(path: Path) -> None:
    """Load environment variables from the configured path if present."""
    if path.exists():
        load_dotenv(path)


@dataclass(frozen=True, slots=True)
class TrinityPaths:
    """Filesystem paths used across the Trinity residents."""

    base_dir: Path = Path("/srv/janus/trinity")
    memory_dir: Path = Path(os.getenv("TRINITY_DB_DIR", "/srv/janus/trinity_memory"))
    log_dir: Path = Path(os.getenv("TRINITY_LOG_DIR", "/srv/janus/trinity_logs"))
    comms_hub: Path = Path(os.getenv("COMMS_HUB_PATH", "/srv/janus/03_OPERATIONS/COMMS_HUB"))
    oracle_cache_dir: Path = Path(os.getenv("TRINITY_ORACLE_CACHE", "/srv/janus/trinity_memory/oracle_cache"))
    master_librarian_root: Path = Path(
        os.getenv(
            "MASTER_LIBRARIAN_PATH",
            "/srv/janus/02_FORGE/src/UBOS/Agents/KnowledgeAgent/MasterLibrarianAgent",
        )
    )


@dataclass(frozen=True, slots=True)
class APIKeys:
    """External service credentials."""

    claude: Optional[str] = os.getenv("CLAUDE_API_KEY")
    gemini: Optional[str] = os.getenv("GEMINI_API_KEY")
    groq: Optional[str] = os.getenv("GROQ_API_KEY")
    openai: Optional[str] = os.getenv("OPENAI_API_KEY")
    wolfram: Optional[str] = os.getenv("WOLFRAM_APP_ID")
    data_commons: Optional[str] = os.getenv("DATA_COMMONS_API_KEY")
    telegram_token: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    perplexity: Optional[str] = os.getenv("PERPLEXITY_API_KEY")


def load_configuration(env_path: Path = DEFAULT_ENV_PATH) -> tuple[TrinityPaths, APIKeys]:
    """Load environment configuration and return strongly-typed settings."""
    _load_env_file(env_path)
    if os.getenv("TRINITY_SKIP_LOCAL_ENV", "0") != "1":
        for alt in ALT_ENV_PATHS:
            _load_env_file(alt)

    keys = APIKeys(
        claude=os.getenv("CLAUDE_API_KEY"),
        gemini=os.getenv("GEMINI_API_KEY"),
        groq=os.getenv("GROQ_API_KEY"),
        openai=os.getenv("OPENAI_API_KEY"),
        wolfram=os.getenv("WOLFRAM_APP_ID"),
        data_commons=os.getenv("DATA_COMMONS_API_KEY"),
        telegram_token=os.getenv("TELEGRAM_BOT_TOKEN"),
        perplexity=os.getenv("PERPLEXITY_API_KEY"),
    )

    paths = TrinityPaths()
    paths.log_dir.mkdir(parents=True, exist_ok=True)
    paths.memory_dir.mkdir(parents=True, exist_ok=True)
    paths.oracle_cache_dir.mkdir(parents=True, exist_ok=True)

    return paths, keys

