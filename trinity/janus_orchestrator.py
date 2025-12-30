from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DelegationPlan:
    mode: str  # 'override' | 'oracle' | 'keyword'
    target: str  # 'claude' | 'gemini' | 'groq' | 'openai' | 'perplexity' | 'wolfram' | 'fast'
    query: str
    model: Optional[str] = None
    tool_args: Optional[list[str]] = None


def parse_use_command(text: str) -> Optional[DelegationPlan]:
    stripped = (text or "").strip()
    if not stripped.lower().startswith("/use "):
        return None
    remainder = stripped[5:].strip()
    if not remainder:
        return None
    parts = remainder.split(None, 1)
    head = parts[0]
    query = parts[1].strip() if len(parts) > 1 else ""
    if not query:
        return None
    if ":" in head:
        target, model = head.split(":", 1)
    else:
        target, model = head, None
    target_norm = target.lower()
    if target_norm not in {"claude", "gemini", "groq", "openai"}:
        return None
    return DelegationPlan(mode="override", target=target_norm, query=query, model=model)


def parse_mention_command(text: str) -> Optional[DelegationPlan]:
    stripped = (text or "").strip()
    if not stripped.startswith("@"):
        return None
    try:
        head, query = stripped.split(None, 1)
    except ValueError:
        return None
    head = head[1:]
    if not head or not query:
        return None
    model: Optional[str] = None
    if ":" in head:
        target, model = head.split(":", 1)
    else:
        target = head
    target_norm = target.lower()
    if target_norm in {"perplexity", "px", "ppx", "sonar"}:
        return DelegationPlan(mode="oracle", target="perplexity", query=query)
    if target_norm in {"wolfram", "wa", "wf"}:
        return DelegationPlan(mode="oracle", target="wolfram", query=query)
    if target_norm in {"fast", "think", "groqfast"}:
        return DelegationPlan(mode="oracle", target="fast", query=query)
    if target_norm in {"claude", "gemini", "groq", "openai"}:
        return DelegationPlan(mode="override", target=target_norm, query=query, model=model)
    return None


def parse_oracle_command(text: str) -> Optional[DelegationPlan]:
    stripped = (text or "").strip()
    if not stripped.lower().startswith("/oracle "):
        return None
    remainder = stripped[8:].strip()
    if not remainder:
        return None
    parts = remainder.split(None, 1)
    oracle = parts[0].lower()
    query = parts[1].strip() if len(parts) > 1 else ""
    if not query:
        return None
    if oracle in {"perplexity", "wolfram", "fast"}:
        return DelegationPlan(mode="oracle", target=oracle, query=query)
    if oracle in {"px", "ppx", "sonar"}:
        return DelegationPlan(mode="oracle", target="perplexity", query=query)
    if oracle in {"wf", "wa"}:
        return DelegationPlan(mode="oracle", target="wolfram", query=query)
    if oracle in {"groq", "think", "fast_think"}:
        return DelegationPlan(mode="oracle", target="fast", query=query)
    return None


def keyword_route(text: str) -> DelegationPlan:
    t = (text or "").lower()
    if any(w in t for w in ("latest", "news", "source", "citation", "market", "docs")):
        return DelegationPlan(mode="keyword", target="perplexity", query=text)
    if any(w in t for w in ("equation", "integral", "derivative", "formula", "compute")):
        return DelegationPlan(mode="keyword", target="wolfram", query=text)
    if any(w in t for w in ("deep research", "multi-step", "reason about", "chain of thought", "prove")):
        return DelegationPlan(mode="keyword", target="openai", query=text, model="o4-mini-deep-research")
    if any(w in t for w in ("deploy", "configure", "systemd", "service", "shell", "script", "pipeline")):
        return DelegationPlan(mode="keyword", target="gemini", query=text)
    if any(w in t for w in ("code", "implement", "refactor", "bug", "patch", "pull request", "pr ")):
        return DelegationPlan(mode="keyword", target="openai", query=text, model="gpt-5-codex")
    if any(w in t for w in ("strategy", "plan", "roadmap", "policy", "principle", "constitution")):
        return DelegationPlan(mode="keyword", target="claude", query=text)
    if any(w in t for w in ("quick", "scout", "draft", "sanity", "summary")):
        return DelegationPlan(mode="keyword", target="groq", query=text)
    return DelegationPlan(mode="keyword", target="openai", query=text, model="gpt-5-mini")


def plan_from_text(text: str) -> DelegationPlan:
    return (
        parse_mention_command(text)
        or parse_use_command(text)
        or parse_oracle_command(text)
        or keyword_route(text)
    )

