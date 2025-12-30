from __future__ import annotations

import argparse
import hashlib
import json
import logging
import time
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator

from trinity.config import load_configuration, TrinityPaths
from trinity.intelligence_tools import IntelligenceDatabase, IntelligenceNode

LOGGER = logging.getLogger("trinity.intelligence_collector")

CATEGORY_BY_TEMPLATE = {
    "grant_hunter_daily": "grant",
    "grant_followup": "grant",
    "innovation_scout_daily": "insight",
    "market_intel_daily": "insight",
    "malaga_network_daily": "contact",
    "malaga_network_outreach": "contact",
    "monetization_analysis_daily": "revenue",
    "oradea_outreach": "revenue",
    "ops_hardening": "operational",
    "pipeline_ops": "operational",
    "eu_remote_opportunity_scout_daily": "revenue",
    "romanian_market_scout_daily": "revenue",
    "content_monetization_weekly": "revenue",
    "fast_grant_hunter_daily": "grant",
    "ubos_productization_weekly": "revenue",
}

CATEGORY_BY_MESSAGE = {
    "grant_opportunity": "grant",
    "grant_followup": "grant",
    "innovation_brief": "insight",
    "market_insight": "insight",
    "contact_profile": "contact",
    "malaga_contact": "contact",
    "revenue_signal": "revenue",
    "monetization_report": "revenue",
    "ops_report": "operational",
    "pipeline_ops_report": "operational",
    "remote_revenue_signals": "revenue",
    "romanian_revenue_signals": "revenue",
    "content_revenue_strategy": "revenue",
    "fast_grant_opportunity": "grant",
    "productization_revenue_signals": "revenue",
}

CACHE_DIR = Path("/srv/janus/03_OPERATIONS/vessels/balaur/intel_cache/intelligence")
STATE_FILE = CACHE_DIR / "collector_state.json"
NODE_DIR = CACHE_DIR / "nodes"


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _safe_write_json(path: Path, payload: dict[str, Any]) -> None:
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    tmp.replace(path)


@dataclass(slots=True)
class CollectorConfig:
    missions_dir: Path
    archive_root: Path
    cache_dir: Path
    node_dir: Path
    state_path: Path
    log_path: Path
    poll_interval: int


class IntelligenceCollector:
    """Transforms mission deliverables into structured intelligence nodes."""

    def __init__(
        self,
        *,
        missions_dir: Path | None = None,
        archive_root: Path | None = None,
        cache_dir: Path | None = None,
        log_path: Path | None = None,
        poll_interval: int = 300,
        db_path: Path | None = None,
    ) -> None:
        paths, _ = load_configuration()
        missions = missions_dir or (paths.comms_hub / "missions" / "completed")
        archive = archive_root or paths.comms_hub
        cache_base = cache_dir or CACHE_DIR
        self.config = CollectorConfig(
            missions_dir=Path(missions).resolve(),
            archive_root=Path(archive).resolve(),
            cache_dir=Path(cache_base).resolve(),
            node_dir=Path(cache_base).resolve() / "nodes",
            state_path=(Path(cache_base).resolve() / "collector_state.json"),
            log_path=Path(log_path or (paths.log_dir / "intelligence_collector.jsonl")).resolve(),
            poll_interval=poll_interval,
        )
        self.config.cache_dir.mkdir(parents=True, exist_ok=True)
        self.config.node_dir.mkdir(parents=True, exist_ok=True)
        self.config.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()
        self.db = IntelligenceDatabase(db_path=db_path)
        self.paths: TrinityPaths = paths

    def collect_once(self, *, force_rescan: bool = False) -> list[IntelligenceNode]:
        nodes: list[IntelligenceNode] = []
        mission_files = sorted(self.config.missions_dir.glob("*.json"))
        for mission_file in mission_files:
            mission_mtime = mission_file.stat().st_mtime
            if not force_rescan and self.state.get(str(mission_file)) == mission_mtime:
                continue
            try:
                mission_payload = _read_json(mission_file)
            except json.JSONDecodeError as exc:
                self._log("error", {"mission_file": str(mission_file), "error": f"invalid json: {exc}"})
                continue
            extracted = self._process_mission(mission_payload, mission_file)
            if extracted:
                nodes.extend(extracted)
            self.state[str(mission_file)] = mission_mtime
        if nodes:
            self._write_state()
        return nodes

    def run_loop(self) -> None:
        LOGGER.info("Starting intelligence collector loop (interval=%ss)", self.config.poll_interval)
        while True:
            try:
                collected = self.collect_once()
                if collected:
                    LOGGER.info("Collected %d nodes", len(collected))
            except Exception as exc:  # pragma: no cover - defensive daemon guard
                LOGGER.exception("Collector iteration failed: %s", exc)
            time.sleep(self.config.poll_interval)

    # ------------------------------------------------------------------ mission processing
    def _process_mission(self, mission: dict[str, Any], mission_path: Path) -> list[IntelligenceNode]:
        category = self._infer_category(mission)
        if category is None:
            self._log("skip", {"mission_id": mission.get("mission_id"), "reason": "unsupported_category"})
            return []

        payload = self._load_deliverable_payload(mission)
        nodes = list(self._normalise_nodes(category, mission, payload))
        stored: list[IntelligenceNode] = []
        for node in nodes:
            content_hash = self._hash_node(node)
            cache_file = self.config.node_dir / f"{content_hash}.json"
            if cache_file.exists():
                continue
            self.db.store_node(node)
            cache_file.write_text(
                json.dumps(
                    {
                        "id": node.id,
                        "category": node.category,
                        "timestamp": node.timestamp,
                        "source_mission": node.source_mission,
                        "data": node.data,
                        "relevance_score": node.relevance_score,
                        "tags": node.tags,
                    },
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            stored.append(node)
        if stored:
            self._log(
                "collected",
                {
                    "mission_id": mission.get("mission_id"),
                    "category": category,
                    "count": len(stored),
                    "mission_file": str(mission_path),
                },
            )
        return stored

    def _infer_category(self, mission: dict[str, Any]) -> str | None:
        template = (mission.get("source_template") or "").lower()
        if template in CATEGORY_BY_TEMPLATE:
            return CATEGORY_BY_TEMPLATE[template]
        deliverable = mission.get("deliverable", {})
        message_type = (deliverable.get("message_type") or "").lower()
        if message_type in CATEGORY_BY_MESSAGE:
            return CATEGORY_BY_MESSAGE[message_type]
        objective = (mission.get("objective") or "").lower()
        if "grant" in objective:
            return "grant"
        if "market" in objective or "insight" in objective:
            return "insight"
        if "contact" in objective:
            return "contact"
        if "revenue" in objective or "monetization" in objective:
            return "revenue"
        if "ops" in objective or "operational" in objective:
            return "operational"
        return None

    def _load_deliverable_payload(self, mission: dict[str, Any]) -> dict[str, Any]:
        deliverable = mission.get("deliverable") or {}
        recipient = deliverable.get("recipient")
        mission_id = mission.get("mission_id")
        if not recipient or not mission_id:
            return {}
        archive_dir = self.config.archive_root / recipient / "archive"
        if not archive_dir.exists():
            return {}
        candidates = sorted(archive_dir.glob(f"*{mission_id}*.json"))
        for candidate in reversed(candidates):
            try:
                payload = _read_json(candidate)
                payload["_source_file"] = str(candidate)
                return payload
            except json.JSONDecodeError:
                continue
        return {}

    def _normalise_nodes(
        self,
        category: str,
        mission: dict[str, Any],
        payload: dict[str, Any],
    ) -> Iterator[IntelligenceNode]:
        if category == "grant":
            yield from self._normalise_grants(mission, payload)
        elif category == "insight":
            yield self._build_node(category, mission, payload or {"summary": mission.get("objective")})
        elif category == "contact":
            yield from self._normalise_contacts(mission, payload)
        elif category == "revenue":
            yield from self._normalise_revenue(mission, payload)
        elif category == "operational":
            yield self._build_node(category, mission, payload or {"metric_type": "mission_success_rate"})

    # ------------------------------------------------------------------ normalisers
    def _normalise_grants(self, mission: dict[str, Any], payload: dict[str, Any]) -> Iterator[IntelligenceNode]:
        opportunities = payload.get("opportunities") or payload.get("summary", {}).get("opportunities")
        if isinstance(opportunities, list) and opportunities:
            for opportunity in opportunities:
                data = {
                    "title": opportunity.get("title"),
                    "program": opportunity.get("program"),
                    "deadline": opportunity.get("deadline"),
                    "budget": opportunity.get("budget"),
                    "fit_score": opportunity.get("fit_score"),
                    "status": opportunity.get("status", "new"),
                    "summary": opportunity,
                }
                yield self._build_node("grant", mission, data)
        else:
            data = {
                "summary": payload.get("summary") or payload,
                "title": (payload.get("summary") or {}).get("top_titles", ["Grant opportunity"])[0]
                if isinstance((payload.get("summary") or {}).get("top_titles"), list)
                else payload.get("title") or "Grant opportunity",
            }
            yield self._build_node("grant", mission, data)

    def _normalise_contacts(self, mission: dict[str, Any], payload: dict[str, Any]) -> Iterator[IntelligenceNode]:
        contacts = payload.get("contacts") or payload.get("network") or []
        if isinstance(contacts, list) and contacts:
            for contact in contacts:
                data = {
                    "name": contact.get("name"),
                    "organization": contact.get("organization"),
                    "role": contact.get("role"),
                    "connection_strength": contact.get("connection_strength") or contact.get("connection"),
                    "location": contact.get("location"),
                    "last_contact": contact.get("last_contact"),
                    "notes": contact.get("notes"),
                    "tags": contact.get("tags"),
                }
                yield self._build_node("contact", mission, data)
        else:
            yield self._build_node("contact", mission, payload or {})

    def _normalise_revenue(self, mission: dict[str, Any], payload: dict[str, Any]) -> Iterator[IntelligenceNode]:
        signals = payload.get("signals") or payload.get("leads") or []
        if isinstance(signals, list) and signals:
            for signal in signals:
                data = {
                    "channel": signal.get("channel"),
                    "value_estimate": signal.get("value_estimate"),
                    "probability": signal.get("probability"),
                    "stage": signal.get("stage"),
                    "tags": signal.get("tags"),
                }
                yield self._build_node("revenue", mission, data)
        else:
            yield self._build_node("revenue", mission, payload or {})

    def _build_node(self, category: str, mission: dict[str, Any], data: dict[str, Any]) -> IntelligenceNode:
        mission_id = mission.get("mission_id", "unknown")
        timestamp = mission.get("completed_at") or mission.get("queued_at") or _utc_now().isoformat()
        tags = self._collect_tags(mission, data)
        relevance = self._calculate_relevance(mission, data)
        base_payload = {
            "category": category,
            "mission_id": mission_id,
            "data": data,
            "tags": tags,
        }
        content_hash = hashlib.sha256(json.dumps(base_payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()
        node_id = str(uuid.uuid5(uuid.NAMESPACE_URL, content_hash))
        return IntelligenceNode(
            id=node_id,
            category=category,
            timestamp=timestamp,
            source_mission=mission_id,
            data=data,
            relevance_score=relevance,
            tags=tags,
        )

    def _calculate_relevance(self, mission: dict[str, Any], data: dict[str, Any]) -> float:
        if "fit_score" in data and data["fit_score"] is not None:
            try:
                return max(0.0, min(1.0, float(data["fit_score"]) / 10))
            except (TypeError, ValueError):
                pass
        priority = mission.get("priority")
        if priority is not None:
            try:
                return max(0.1, min(1.0, float(priority) / 5))
            except (TypeError, ValueError):
                pass
        return 0.5

    def _collect_tags(self, mission: dict[str, Any], data: dict[str, Any]) -> list[str]:
        tags: set[str] = set()
        for value in (mission.get("source_template"), mission.get("deliverable", {}).get("message_type"), mission.get("assigned_to")):
            if value:
                tags.add(str(value).lower())
        for entry in data.get("tags", []) if isinstance(data.get("tags"), list) else []:
            tags.add(str(entry).lower())
        objective = mission.get("objective")
        if objective:
            tags.update(word.strip(".,").lower() for word in objective.split() if len(word) > 4)
        return sorted(tags)

    def _hash_node(self, node: IntelligenceNode) -> str:
        payload = {
            "id": node.id,
            "category": node.category,
            "source_mission": node.source_mission,
            "data": node.data,
            "tags": node.tags,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()

    # ------------------------------------------------------------------ state + logging
    def _load_state(self) -> dict[str, float]:
        if self.config.state_path.exists():
            try:
                return json.loads(self.config.state_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _write_state(self) -> None:
        _safe_write_json(self.config.state_path, self.state)

    def _log(self, event: str, payload: dict[str, Any]) -> None:
        record = {"timestamp": _utc_now().isoformat(), "event": event, **payload}
        try:
            with self.config.log_path.open("a", encoding="utf-8") as handle:
                json.dump(record, handle)
                handle.write("\n")
        except OSError:
            LOGGER.exception("Failed to append intelligence collector log")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect structured intelligence from completed missions.")
    parser.add_argument("--collect-all", action="store_true", help="Process all missions ignoring cached state.")
    parser.add_argument("--once", action="store_true", help="Run a single collection pass and exit.")
    parser.add_argument("--poll-interval", type=int, default=300, help="Daemon poll interval in seconds.")
    parser.add_argument("--db", type=Path, help="Override intelligence database path (testing).")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    collector = IntelligenceCollector(poll_interval=args.poll_interval, db_path=args.db)
    if args.once or args.collect_all:
        collector.collect_once(force_rescan=args.collect_all)
    else:
        collector.run_loop()


if __name__ == "__main__":
    main()
