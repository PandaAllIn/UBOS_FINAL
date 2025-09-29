from __future__ import annotations

"""
Constitutional Query Engine (CQE)

get_constitutional_guidance(task: str, orrery: networkx.Graph) -> dict

Purpose
  Given a simple task string and the Hydraulic Constitution graph (NetworkX
  DiGraph as produced by scripts/unify_constitution.py), infer a
  constitutionalContext block compliant with SAP V2.0:
    {
      principles: [string],
      pressure: { principle_id: number },
      objectives: [string],
      constraints: [string],
      riskTolerance: string,
      territory: string?,
      references: [string]?,
      cachePolicy: { mode, maxAgeSec, mustAlign }
    }

Design
  - Resonance: token-based similarity between task and node text fields
    (id, title, one_liner, description, topics, etc.).
  - Importance weighting: boost `kind=principle`; smaller boost for
    practices/checklists; quotes/chapters get lower weight.
  - Conflict detection: identify presence of opposing conceptual axes in the
    top resonant nodes (e.g., speed vs. caution, risk vs. safety) and craft
    constraints accordingly.
  - Pressure: map resonance scores for the top principles to a 0..100 scale.
  - Directives: synthesize clear objectives from top relevant nodes’ titles
    and descriptions.

Dependencies
  - networkx required; no heavy NLP dependencies by design.
"""

import math
import re
import time
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple, Optional

import networkx as nx


# Small, pragmatic English stopword list (extend as needed)
STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "of",
    "in",
    "for",
    "on",
    "with",
    "at",
    "by",
    "from",
    "is",
    "are",
    "be",
    "can",
    "will",
    "it",
    "that",
    "this",
    "as",
    "into",
    "your",
    "you",
    "we",
}


KIND_WEIGHTS = {
    "principle": 1.30,
    "practice": 1.10,
    "checklist": 1.10,
    "idea": 1.05,
    "quote": 0.80,
    "chapter": 0.70,
    "book": 0.60,
}


AXES = {
    "speed_vs_caution": {
        "speed": {"speed", "fast", "quick", "accelerate", "rapid", "now", "immediate", "urgent"},
        "caution": {"patience", "wait", "slow", "caution", "careful", "deliberate", "respond", "24-hour"},
    },
    "risk_vs_safety": {
        "risk": {"risk", "aggressive", "bold", "venture"},
        "safety": {"safe", "safety", "secure", "conservative"},
    },
    "breadth_vs_focus": {
        "breadth": {"breadth", "broad", "explore", "divergent", "survey"},
        "focus": {"focus", "narrow", "converge", "refine", "specific"},
    },
    # Blueprint-aligned extensions
    "speed_vs_thoroughness": {
        "speed": {"speed", "fast", "quick", "rapid", "now", "asap"},
        "thoroughness": {"thorough", "thoroughness", "comprehensive", "deep", "complete", "meticulous"},
    },
    "innovation_vs_reliability": {
        "innovation": {"innovate", "innovation", "novel", "experimental", "new"},
        "reliability": {"reliable", "reliability", "stable", "stability", "robust", "consistent"},
    },
    "individual_vs_team": {
        "individual": {"individual", "solo", "autonomous", "independent"},
        "team": {"team", "collaborate", "collaboration", "consensus", "together"},
    },
}


def _tokenize(text: str) -> List[str]:
    toks = re.findall(r"[a-zA-Z0-9\-]+", text.lower())
    return [t for t in toks if t not in STOPWORDS and len(t) > 1]


def _gather_node_text(attrs: Dict[str, Any]) -> str:
    parts: List[str] = []
    for key in (
        "id",
        "title",
        "one_liner",
        "description",
        "prompt",
        "expected_outcome",
    ):
        val = attrs.get(key)
        if isinstance(val, str) and val.strip():
            parts.append(val)

    # topics, steps as text too
    topics = attrs.get("topics")
    if isinstance(topics, list):
        parts.extend(str(x) for x in topics)
    steps = attrs.get("steps")
    if isinstance(steps, list):
        parts.extend(str(x) for x in steps)

    return "\n".join(parts)


@dataclass
class Resonance:
    node_id: str
    score: float
    kind: str
    title: str | None
    description: str | None
    tokens: List[str]
    path: str | None


def _score_nodes(task: str, G: nx.DiGraph) -> List[Resonance]:
    task_tokens = _tokenize(task)
    if not task_tokens:
        return []

    task_set = set(task_tokens)
    out: List[Resonance] = []

    for n, data in G.nodes(data=True):
        text = _gather_node_text(data)
        if not text:
            continue
        ntoks = _tokenize(text)
        nset = set(ntoks)
        if not nset:
            continue

        # basic overlap score
        overlap = task_set & nset
        if not overlap:
            base = 0.0
        else:
            base = len(overlap) / max(1.0, len(task_set))

        # topic boost
        topic_boost = 0.0
        topics = data.get("topics")
        if isinstance(topics, list):
            tset = {str(x).lower() for x in topics}
            topic_boost = 0.1 * len(task_set & tset)

        # kind weighting
        kind = str(data.get("kind", "")).lower()
        weight = KIND_WEIGHTS.get(kind, 1.0)

        score = (base + topic_boost) * weight

        # light path for zero scores: skip
        if score <= 0.0:
            continue

        out.append(
            Resonance(
                node_id=str(data.get("id", n)),
                score=score,
                kind=kind,
                title=(data.get("title") if isinstance(data.get("title"), str) else None),
                description=(
                    data.get("one_liner")
                    if isinstance(data.get("one_liner"), str)
                    else (data.get("description") if isinstance(data.get("description"), str) else None)
                ),
                tokens=list(nset),
                path=(data.get("path") if isinstance(data.get("path"), str) else None),
            )
        )

    out.sort(key=lambda r: r.score, reverse=True)
    return out


def _detect_conflicts(resonants: List[Resonance]) -> List[str]:
    # Look across the top resonant items for opposing axis terms
    k = min(12, len(resonants))
    top = resonants[:k]

    # Flatten tokens from titles/descriptions for naive detection
    all_tokens = set()
    for r in top:
        all_tokens.update(r.tokens)
        if r.title:
            all_tokens.update(_tokenize(r.title))
        if r.description:
            all_tokens.update(_tokenize(r.description))

    constraints: List[str] = []
    for axis_name, poles in AXES.items():
        left_name, right_name = list(poles.keys())
        left, right = poles[left_name], poles[right_name]
        left_hit = bool(all_tokens & left)
        right_hit = bool(all_tokens & right)
        if left_hit and right_hit:
            # Craft a balancing constraint for this tension
            if axis_name == "speed_vs_caution":
                constraints.append(
                    "Balance urgency with a deliberate response window (apply the 24‑hour rule when emotions run hot)."
                )
            elif axis_name == "risk_vs_safety":
                constraints.append(
                    "Pursue calculated risk with explicit safeguards; require a pre‑mortem before committing resources."
                )
            elif axis_name == "breadth_vs_focus":
                constraints.append(
                    "Begin broad to discover options, then converge to a focused plan with acceptance criteria."
                )

    return constraints


def _map_pressure(principle_hits: List[Tuple[str, float]]) -> Dict[str, int]:
    # Normalize scores to 0..100 (floor at 10 to avoid zero guidance)
    if not principle_hits:
        return {}
    max_s = max(s for _, s in principle_hits) or 1e-9
    pressure: Dict[str, int] = {}
    for pid, s in principle_hits:
        scaled = int(round(15 + 85 * (s / max_s)))
        scaled = max(0, min(100, scaled))
        pressure[pid] = scaled
    return pressure


def _risk_tolerance(task: str, resonants: List[Resonance]) -> str:
    task_toks = set(_tokenize(task))
    high_signals = {"urgent", "now", "immediate", "must", "deadline", "crisis"}
    low_signals = {"patience", "wait", "caution", "careful", "deliberate"}

    high = len(task_toks & high_signals)
    low = len(task_toks & low_signals)

    # Nudge by resonance context
    for r in resonants[:8]:
        if r.kind == "principle" and r.title:
            rtoks = set(_tokenize(r.title + " " + (r.description or "")))
            high += len(rtoks & high_signals)
            low += len(rtoks & low_signals)

    if high >= low + 1:
        return "medium" if high < 2 else "high"
    if low >= high + 1:
        return "low"
    return "medium"


def _synthesize_objectives(resonants: List[Resonance], limit: int = 5) -> List[str]:
    objs: List[str] = []
    for r in resonants[:limit]:
        if r.kind in {"principle", "idea"} and r.title:
            objs.append(f"Apply principle: {r.title}")
        elif r.kind in {"practice", "checklist"} and r.title:
            objs.append(f"Execute practice: {r.title}")
        elif r.title:
            objs.append(f"Incorporate insight: {r.title}")
        elif r.description:
            objs.append(f"Incorporate insight: {r.description[:80]}…")
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for o in objs:
        if o not in seen:
            seen.add(o)
            deduped.append(o)
    return deduped


# --- V2: Task classification and tiered matching ---------------------------------

INTENT_KEYWORDS = {
    "plan": {"plan", "design", "architect", "outline", "strategy", "strategize", "map"},
    "execute": {"execute", "build", "implement", "ship", "run", "deploy", "do", "write", "compose"},
    "research": {"research", "analyze", "investigate", "explore", "survey"},
    "summarize": {"summarize", "summarise", "condense", "review"},
    "respond": {"respond", "reply", "wait", "cool", "pause", "defer"},
}

INTENT_TO_BOOK = {
    # Book01: Systems Over Willpower — architecture & identity
    "architect": "Book01",
    "plan": "Book03",  # strategic thinking
    "research": "Book03",
    "execute": "Book04",  # tactical mindset
    "respond": "Book04",
}

# Constitutional situation → book mapping
SITUATION_TO_BOOK = {
    "REACTIVE_DECISION": "Book04",
    "INTERPERSONAL_CONFLICT": "Book04",
    "SYSTEM_CREATION": "Book01",
}

DOMAIN_KEYWORDS = {
    "xf": {"xf", "xylella", "olive", "agriculture"},
    "funding": {"funding", "proposal", "grant", "horizon", "eufm", "eu"},
    "energy": {"geothermal", "energy", "renewable"},
    "agents": {"agent", "summoner", "knowledge", "graph", "orrery"},
    "timing": {"timing", "24-hour", "respond", "wait", "pause", "impulsive"},
    "leverage": {"leverage", "less", "effort", "outsized"},
    "clarity": {"clarity", "endgame", "define", "outcome"},
    "legal": {"regulation", "compliance", "policy", "law", "article", "section"},
}


def _classify_task(task: str, situations: Optional[List[str]] = None) -> Dict[str, Any]:
    toks = set(_tokenize(task))
    intents: List[str] = []
    for name, vocab in INTENT_KEYWORDS.items():
        if toks & vocab:
            intents.append(name)
    if not intents:
        # heuristic: presence of words implying plan or execute
        if {"proposal", "plan", "strategy"} & toks:
            intents.append("plan")
        elif {"build", "implement", "run", "deploy"} & toks:
            intents.append("execute")

    domains: List[str] = []
    for name, vocab in DOMAIN_KEYWORDS.items():
        if toks & vocab:
            domains.append(name)

    urgency = "low"
    if {"urgent", "now", "immediate", "asap", "deadline"} & toks:
        urgency = "high"
    elif {"soon", "quick"} & toks:
        urgency = "medium"

    complexity = "medium"
    if len(toks) > 14 or {"comprehensive", "detailed", "end-to-end", "deep", "thorough"} & toks:
        complexity = "high"
    elif len(toks) < 6:
        complexity = "low"

    # map intents to books
    book_targets: List[str] = []
    for intent in intents:
        key = "architect" if intent == "plan" and {"architecture", "architect"} & toks else intent
        book = INTENT_TO_BOOK.get(key)
        if book and book not in book_targets:
            book_targets.append(book)

    situation_books: List[str] = []
    for s in (situations or []):
        b = SITUATION_TO_BOOK.get(s)
        if b and b not in situation_books:
            situation_books.append(b)

    return {
        "intents": intents,
        "domains": domains,
        "urgency": urgency,
        "complexity": complexity,
        "books": book_targets,
        "situation_books": situation_books,
        "situations": situations or [],
    }


def _book_of_node(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    m = re.search(r"Book0([1-4])", path)
    if not m:
        return None
    return f"Book0{m.group(1)}"


def _tiered_match(task: str, G: nx.DiGraph, cls: Dict[str, Any]) -> List[Resonance]:
    # Base resonance
    base = _score_nodes(task, G)
    if not base:
        return []

    toks = set(_tokenize(task))

    # Primary: boost nodes from targeted books
    targeted_books = set(cls.get("books") or [])
    situation_books = set(cls.get("situation_books") or [])
    boosted: List[Resonance] = []
    for r in base:
        b = _book_of_node(r.path)
        mult = 1.0
        if b and b in situation_books:
            mult *= 1.60  # strong boost from constitutional situation
        elif b and b in targeted_books:
            mult *= 1.25
        boosted.append(dataclass_replace(r, score=r.score * mult))

    boosted.sort(key=lambda x: x.score, reverse=True)

    # Secondary: emphasize domain-specific practice/checklist nodes
    domain_hits = set(cls.get("domains") or [])
    if domain_hits:
        def is_practice(res: Resonance) -> bool:
            kid = res.node_id or ""
            return res.kind in {"practice", "checklist"} or kid.startswith("practice-")

        dom_boosted = []
        for r in boosted:
            mult = 1.0
            if is_practice(r):
                # If node topics overlap domains, increase
                if r.title:
                    rtoks = set(_tokenize(r.title + " " + (r.description or "")))
                else:
                    rtoks = set(r.tokens)
                # approximate domain match using keywords sets
                has_domain = False
                for d in domain_hits:
                    if rtoks & DOMAIN_KEYWORDS.get(d, set()):
                        has_domain = True
                        break
                if has_domain:
                    mult *= 1.25
            dom_boosted.append(dataclass_replace(r, score=r.score * mult))
        boosted = dom_boosted
        boosted.sort(key=lambda x: x.score, reverse=True)

    # Tertiary: pull in neighbors of top-N nodes
    topN = boosted[:8]
    neighbor_scores: Dict[str, float] = {}
    for r in topN:
        if r.node_id in G:
            for nbr in G.successors(r.node_id):
                neighbor_scores[nbr] = neighbor_scores.get(nbr, 0.0) + 0.15 * r.score
            for nbr in G.predecessors(r.node_id):
                neighbor_scores[nbr] = neighbor_scores.get(nbr, 0.0) + 0.10 * r.score

    # merge neighbors into the list
    index = {res.node_id: res for res in boosted}
    for nid, bonus in neighbor_scores.items():
        if nid in index:
            index[nid] = dataclass_replace(index[nid], score=index[nid].score + bonus)
        else:
            data = G.nodes[nid]
            index[nid] = Resonance(
                node_id=nid,
                score=bonus,
                kind=str(data.get("kind", "")).lower(),
                title=(data.get("title") if isinstance(data.get("title"), str) else None),
                description=(data.get("one_liner") if isinstance(data.get("one_liner"), str) else (data.get("description") if isinstance(data.get("description"), str) else None)),
                tokens=_tokenize(_gather_node_text(data)),
                path=(data.get("path") if isinstance(data.get("path"), str) else None),
            )

    merged = list(index.values())
    merged.sort(key=lambda x: x.score, reverse=True)
    return merged


def dataclass_replace(r: Resonance, **changes: Any) -> Resonance:
    return Resonance(
        node_id=changes.get("node_id", r.node_id),
        score=changes.get("score", r.score),
        kind=changes.get("kind", r.kind),
        title=changes.get("title", r.title),
        description=changes.get("description", r.description),
        tokens=changes.get("tokens", r.tokens),
        path=changes.get("path", r.path),
    )


def _conflict_severity(resonants: List[Resonance], G: nx.DiGraph) -> Tuple[str, List[str]]:
    constraints = _detect_conflicts(resonants)
    severity = "NONE"

    if constraints:
        # Both poles present in top-5 => MAJOR
        topTokens = set()
        for r in resonants[:5]:
            topTokens.update(r.tokens)
        major = False
        for poles in AXES.values():
            left, right = list(poles.values())
            if (topTokens & left) and (topTokens & right):
                major = True
                break
        severity = "MAJOR_CONFLICT" if major else "MINOR_CONFLICT"

    # Dependency conflicts: selected principles depend on nodes not present or conflicting
    window_ids = {r.node_id for r in resonants[:10]}
    dep_conflict = False
    common_parent_hint: Optional[str] = None
    for r in resonants[:6]:
        if r.node_id in G:
            deps = []
            for _, tgt, edata in G.out_edges(r.node_id, data=True):
                if edata.get("type") == "depends_on":
                    deps.append(tgt)
            for tgt in deps:
                if tgt not in window_ids:
                    dep_conflict = True
                # Attempt common parent hint across predecessors
                preds_r = set(G.predecessors(r.node_id))
                preds_t = set(G.predecessors(tgt))
                inter = preds_r & preds_t
                if inter and not common_parent_hint:
                    # Prefer a titled/common node
                    nid = next(iter(inter))
                    title = G.nodes[nid].get("title")
                    common_parent_hint = str(title or nid)
            if dep_conflict and "Ensure prerequisites" not in constraints:
                msg = "Ensure prerequisites are met before execution (resolve dependencies explicitly)."
                if common_parent_hint:
                    msg += f" Align on common parent principle: {common_parent_hint}."
                constraints.append(msg)
        if dep_conflict:
            break

    if dep_conflict:
        severity = "DEPENDENCY_CONFLICT"

    return severity, constraints


# --- Constitutional situation classification (Solution #1) -----------------------

def classify_constitutional_situation(task: str) -> List[str]:
    """Detect constitutional situation categories in the task string.

    Returns a list of situation codes like ["REACTIVE_DECISION", "INTERPERSONAL_CONFLICT"].
    """
    s = task.lower()
    situations: List[str] = []

    reactive_indicators = [
        "right now",
        "immediately",
        "urgent",
        "asap",
        "just happened",
        "respond to",
    ]
    if any(ind in s for ind in reactive_indicators):
        situations.append("REACTIVE_DECISION")

    conflict_indicators = [
        "argument",
        "disagreement",
        "stole",
        "unfair",
        "angry",
        "frustrated",
    ]
    if any(ind in s for ind in conflict_indicators):
        situations.append("INTERPERSONAL_CONFLICT")

    building_indicators = [
        "create",
        "build",
        "design",
        "implement",
        "establish",
    ]
    if any(ind in s for ind in building_indicators):
        situations.append("SYSTEM_CREATION")

    return situations


_TASK_CACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
_CACHE_TTL_SEC = 3600  # 1 hour


def get_constitutional_guidance(task: str, orrery: nx.DiGraph) -> Dict[str, Any]:
    """Return a SAP V2 constitutionalContext derived from a task and the graph.

    Parameters
    - task: natural language request (short phrase or sentence)
    - orrery: DiGraph created by unify_constitution.py (nodes carry YAML attrs)
    """

    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")
    if not isinstance(orrery, nx.DiGraph):
        raise TypeError("orrery must be a networkx.DiGraph")

    # Cache fast path
    now = time.time()
    cached = _TASK_CACHE.get(task)
    if cached and now - cached[0] <= _CACHE_TTL_SEC:
        return cached[1]

    # V2: classification + constitutional situation check, then tiered matching
    situations = classify_constitutional_situation(task)
    cls = _classify_task(task, situations)
    resonants = _tiered_match(task, orrery, cls)
    if not resonants:
        # Minimal guidance if nothing matches
        res = {
            "pressureLevel": "consulted",
            "principles": ["systems_over_willpower"],
            "pressure": {"systems_over_willpower": 70},
            "objectives": [
                "Architect the system before action (Build the System).",
                "Define environment and routines to reduce reliance on willpower.",
            ],
            "constraints": [
                "Avoid impulsive decisions; apply the 24‑hour rule if stakes are high.",
            ],
            "riskTolerance": "medium",
            "references": [],
            "cachePolicy": {"mode": "prefer", "maxAgeSec": 86400, "mustAlign": True},
        }
        _TASK_CACHE[task] = (now, res)
        return res

    # Pick a dynamic cut: top 10 or scores within 50% of the best
    best = resonants[0].score
    window = [r for r in resonants if r.score >= 0.5 * best][:10]

    # Principles among the window
    principles = [r for r in window if r.kind == "principle"]
    # If none tagged as principle, allow ideas to stand in
    if not principles:
        principles = [r for r in window if r.kind in {"idea"}]

    # Top principle ids and pressures
    top_principles = [(r.node_id, r.score) for r in principles[:5]]
    pressure = _map_pressure(top_principles)
    principle_ids = [pid for pid, _ in top_principles]

    severity, constraints = _conflict_severity(window, orrery)
    objectives = _synthesize_objectives(window, limit=5)
    risk_tol = _risk_tolerance(task, window)

    # References: prefer ubos://node/<id> if id present; else use file path
    refs: List[str] = []
    for r in window[:6]:
        if r.node_id:
            refs.append(f"ubos://node/{r.node_id}")
        elif r.path:
            refs.append(r.path)

    # Compose constitutionalContext per SAP V2.0
    # Determine overall pressure level from matches, domain, conflicts, complexity
    num_principles = len(principle_ids)
    domain_familiar = len(cls.get("domains") or []) > 0
    complexity = cls.get("complexity", "medium")
    if (
        severity == "MAJOR_CONFLICT"
        or complexity == "high"
        or (not domain_familiar and num_principles <= 1)
    ):
        pressure_level = "deliberated"
    elif severity in {"MINOR_CONFLICT", "DEPENDENCY_CONFLICT"} or num_principles <= 2 or not domain_familiar:
        pressure_level = "consulted"
    else:
        pressure_level = "instant"

    ctx: Dict[str, Any] = {
        "pressureLevel": pressure_level,
        "principles": principle_ids,
        "pressure": pressure,
        "objectives": objectives,
        "constraints": constraints,
        "riskTolerance": risk_tol,
        "references": refs,
        "cachePolicy": {"mode": "prefer", "maxAgeSec": 86400, "mustAlign": True},
    }
    _TASK_CACHE[task] = (now, ctx)
    _log_decision(task, cls, ctx)
    return ctx


_ORRERY_CACHE: Optional[Tuple[float, nx.DiGraph]] = None


def load_constitutional_orrery(root: Optional[Path] = None, run_scan: bool = True) -> nx.DiGraph:
    """Load or re-use the Hydraulic Constitution graph.

    - Attempts to import and build via scripts/unify_constitution.GraphBuilder.
    - Optionally invokes the unify_constitution.py script as a subprocess to run a scan
      (helps surface parse/log errors in CI) before importing and building the graph in-process.
    - Caches the built graph in-memory.
    """
    global _ORRERY_CACHE

    if _ORRERY_CACHE and (time.time() - _ORRERY_CACHE[0] < _CACHE_TTL_SEC):
        return _ORRERY_CACHE[1]

    default_root = Path("/Users/apple/Desktop/UBOS/UBOS/SystemFundamentals/Books")
    scan_root = (root or default_root).resolve()

    if run_scan:
        try:
            subprocess.run(
                ["python3", "scripts/unify_constitution.py", "--root", str(scan_root), "--quiet"],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
        except Exception:
            pass  # non-fatal; we still try to import and build

    # Import and build in-process
    import importlib.util
    spec = importlib.util.spec_from_file_location("unify_constitution", str(Path("scripts/unify_constitution.py").resolve()))
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load scripts/unify_constitution.py module")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore

    builder = mod.GraphBuilder(quiet=True)
    import yaml
    for path in mod.iter_yaml_files(scan_root):
        builder.stats["files"] += 1
        try:
            with open(path, "r", encoding="utf-8") as f:
                docs = list(yaml.safe_load_all(f))
        except Exception:
            builder.stats["errors"] += 1
            continue
        if not docs:
            builder.add_document({}, path, 0)
            continue
        for i, d in enumerate(docs):
            builder.add_document(d, path, i)
    builder.forge_edges()

    G = builder.G
    # Basic structural validation
    if G.number_of_nodes() == 0:
        raise RuntimeError("Orrery graph has zero nodes after load; check root path")
    # Ensure a sample node has expected attributes
    any_node = next(iter(G.nodes))
    nd = G.nodes[any_node]
    for req in ("path",):
        if req not in nd:
            raise RuntimeError(f"Orrery nodes missing required attribute: {req}")
    _ORRERY_CACHE = (time.time(), G)
    return G


def _log_decision(task: str, cls: Dict[str, Any], ctx: Dict[str, Any]) -> None:
    """Append a JSON decision record for future analysis (best-effort)."""
    try:
        import json, os
        from datetime import datetime, timezone
        reports = Path("reports")
        reports.mkdir(parents=True, exist_ok=True)
        rec = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "task": task,
            "classification": cls,
            "context": ctx,
        }
        with open(reports / "constitutional_decisions.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


__all__ = ["get_constitutional_guidance", "load_constitutional_orrery"]
