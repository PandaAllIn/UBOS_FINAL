from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from trinity.config import load_configuration
from trinity.intelligence_db_init import initialise_database
from trinity.tool_audit_logger import audit_tool_call

ALLOWED_CATEGORIES = {"grants", "insights", "contacts", "revenue", "operational"}


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _json_dump(value: Iterable[str] | None) -> str:
    if not value:
        return "[]"
    return json.dumps(sorted(set(str(item) for item in value)))


def _serialise_timestamp(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC).isoformat()
    return str(value)


def _parse_numeric(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@dataclass(slots=True)
class IntelligenceNode:
    id: str
    category: str
    timestamp: str
    source_mission: str
    data: dict[str, Any]
    relevance_score: float
    tags: list[str]


class IntelligenceDatabase:
    """Thin wrapper around the SQLite intelligence database."""

    def __init__(self, db_path: Path | None = None) -> None:
        paths, _ = load_configuration()
        self.db_path = (db_path if db_path is not None else paths.memory_dir / "intelligence.db").resolve()
        initialise_database(self.db_path)

    def store_node(self, node: IntelligenceNode) -> None:
        match node.category:
            case "grant":
                self._insert_grant(node)
            case "insight":
                self._insert_insight(node)
            case "contact":
                self._insert_contact(node)
            case "revenue":
                self._insert_revenue(node)
            case "operational":
                self._insert_operational(node)
            case _:
                raise ValueError(f"Unsupported intelligence category '{node.category}'")

    def query(
        self,
        category: str,
        filters: dict[str, Any] | None,
        query: str | None,
        limit: int,
        sort_by: str,
    ) -> list[dict[str, Any]]:
        category = category.lower()
        if category not in ALLOWED_CATEGORIES:
            raise ValueError(f"Unknown intelligence category '{category}'")

        sql, params = self._build_select(category, filters or {}, query, sort_by, limit)
        with self._connection() as connection:
            cursor = connection.execute(sql, params)
            rows = [dict(row) for row in cursor.fetchall()]
        return rows

    def _connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.execute("PRAGMA busy_timeout = 5000;")
        return connection

    def _insert_grant(self, node: IntelligenceNode) -> None:
        title = node.data.get("title") or node.data.get("name") or node.data.get("summary") or "Untitled opportunity"
        program = node.data.get("program")
        deadline = _serialise_timestamp(node.data.get("deadline"))
        budget = _parse_numeric(node.data.get("budget"))
        fit_score = _parse_numeric(node.data.get("fit_score"))
        status = node.data.get("status") or "new"
        tags = _json_dump(node.tags or node.data.get("tags"))

        with self._connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO grants (id, title, program, deadline, budget, fit_score, status,
                                              source_mission, discovered_at, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    node.id,
                    title,
                    program,
                    deadline,
                    budget,
                    fit_score,
                    status,
                    node.source_mission,
                    node.timestamp,
                    tags,
                ),
            )

    def _insert_insight(self, node: IntelligenceNode) -> None:
        summary = node.data.get("summary") or node.data.get("title") or "Untitled insight"
        details = node.data.get("details") or node.data.get("body")
        category = node.data.get("insight_category") or node.data.get("category") or "market"
        source = node.data.get("source")
        tags = _json_dump(node.tags or node.data.get("tags"))
        relevance = node.data.get("relevance_score", node.relevance_score)
        relevance_value = _parse_numeric(relevance)

        with self._connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO insights (id, category, summary, details, source,
                                                source_mission, discovered_at, relevance_score, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    node.id,
                    category,
                    summary,
                    details,
                    source,
                    node.source_mission,
                    node.timestamp,
                    relevance_value,
                    tags,
                ),
            )

    def _insert_contact(self, node: IntelligenceNode) -> None:
        name = node.data.get("name") or "Unknown contact"
        organization = node.data.get("organization")
        role = node.data.get("role")
        connection_strength = node.data.get("connection_strength") or node.data.get("connection")
        location = node.data.get("location")
        last_contact = _serialise_timestamp(node.data.get("last_contact"))
        notes = node.data.get("notes")
        tags = _json_dump(node.tags or node.data.get("tags"))

        with self._connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO contacts (id, name, organization, role, connection_strength,
                                                location, last_contact, tags, notes, source_mission, discovered_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    node.id,
                    name,
                    organization,
                    role,
                    connection_strength,
                    location,
                    last_contact,
                    tags,
                    notes,
                    node.source_mission,
                    node.timestamp,
                ),
            )

    def _insert_revenue(self, node: IntelligenceNode) -> None:
        channel = node.data.get("channel")
        value_estimate = _parse_numeric(node.data.get("value_estimate"))
        probability = _parse_numeric(node.data.get("probability"))
        stage = node.data.get("stage") or "lead"
        tags = _json_dump(node.tags or node.data.get("tags"))

        with self._connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO revenue_signals (id, channel, value_estimate, probability,
                                                       stage, source_mission, created_at, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    node.id,
                    channel,
                    value_estimate,
                    probability,
                    stage,
                    node.source_mission,
                    node.timestamp,
                    tags,
                ),
            )

    def _insert_operational(self, node: IntelligenceNode) -> None:
        metric_type = node.data.get("metric_type") or node.data.get("name") or "metric"
        value = _parse_numeric(node.data.get("value"))
        timestamp = _serialise_timestamp(node.data.get("timestamp") or node.timestamp)

        with self._connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO operational_metrics (id, metric_type, value, timestamp, source_mission)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    node.id,
                    metric_type,
                    value,
                    timestamp,
                    node.source_mission,
                ),
            )

    def _build_select(
        self,
        category: str,
        filters: dict[str, Any],
        query: str | None,
        sort_by: str,
        limit: int,
    ) -> tuple[str, tuple[Any, ...]]:
        table = {
            "grants": "grants",
            "insights": "insights",
            "contacts": "contacts",
            "revenue": "revenue_signals",
            "operational": "operational_metrics",
        }[category]

        clauses: list[str] = []
        params: list[Any] = []

        filter_handlers = {
            "grants": self._grant_filters,
            "insights": self._insight_filters,
            "contacts": self._contact_filters,
            "revenue": self._revenue_filters,
            "operational": self._operational_filters,
        }
        clauses.extend(filter_handlers[category](filters, params))

        order_clause = self._order_clause(category, sort_by)

        if query:
            fts_table = f"{table}_fts"
            clauses.append(f"rowid IN (SELECT rowid FROM {fts_table} WHERE {fts_table} MATCH ?)")
            params.append(query)

        where_clause = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"SELECT * FROM {table}{where_clause}{order_clause} LIMIT ?"
        params.append(limit)
        return sql, tuple(params)

    def _order_clause(self, category: str, sort_by: str) -> str:
        sort = sort_by.lower()
        if sort == "recency":
            column = {
                "grants": "discovered_at",
                "insights": "discovered_at",
                "contacts": "discovered_at",
                "revenue": "created_at",
                "operational": "timestamp",
            }[category]
            return f" ORDER BY ({column} IS NULL), {column} DESC"
        if sort == "score" and category == "grants":
            return " ORDER BY (fit_score IS NULL), fit_score DESC"
        if sort == "score" and category == "insights":
            return " ORDER BY (relevance_score IS NULL), relevance_score DESC"
        if category == "grants":
            return " ORDER BY (fit_score IS NULL), fit_score DESC, (deadline IS NULL), deadline ASC"
        if category == "insights":
            return " ORDER BY (relevance_score IS NULL), relevance_score DESC, discovered_at DESC"
        if category == "revenue":
            return " ORDER BY (probability IS NULL), probability DESC, created_at DESC"
        if category == "contacts":
            return " ORDER BY (last_contact IS NULL), last_contact DESC, discovered_at DESC"
        if category == "operational":
            return " ORDER BY (timestamp IS NULL), timestamp DESC"
        return " ORDER BY discovered_at DESC"

    def _grant_filters(self, filters: dict[str, Any], params: list[Any]) -> list[str]:
        clauses: list[str] = []
        for key, value in filters.items():
            if key == "fit_score":
                op, val = _parse_operator(value)
                clauses.append(f"fit_score {op} ?")
                params.append(_parse_numeric(val))
            elif key == "status":
                clauses.append("status = ?")
                params.append(str(value))
            elif key == "deadline":
                op, val = _parse_deadline(value)
                clauses.append(f"deadline {op} ?")
                params.append(val)
            elif key == "tags":
                clauses.append("tags LIKE ?")
                params.append(f"%{value}%")
        return clauses

    def _insight_filters(self, filters: dict[str, Any], params: list[Any]) -> list[str]:
        clauses: list[str] = []
        for key, value in filters.items():
            if key == "category":
                clauses.append("category = ?")
                params.append(str(value))
            elif key == "relevance_score":
                op, val = _parse_operator(value)
                clauses.append(f"relevance_score {op} ?")
                params.append(_parse_numeric(val))
            elif key == "tags":
                clauses.append("tags LIKE ?")
                params.append(f"%{value}%")
        return clauses

    def _contact_filters(self, filters: dict[str, Any], params: list[Any]) -> list[str]:
        clauses: list[str] = []
        for key, value in filters.items():
            if key == "location":
                clauses.append("location = ?")
                params.append(str(value))
            elif key in {"connection", "connection_strength"}:
                clauses.append("connection_strength = ?")
                params.append(str(value))
            elif key == "days_since_contact":
                op, threshold = _parse_operator(value)
                days = float(threshold)
                clauses.append(f"(last_contact IS NOT NULL AND (julianday('now') - julianday(last_contact)) {op} ?)")
                params.append(days)
        return clauses

    def _revenue_filters(self, filters: dict[str, Any], params: list[Any]) -> list[str]:
        clauses: list[str] = []
        for key, value in filters.items():
            if key == "stage":
                clauses.append("stage = ?")
                params.append(str(value))
            elif key == "probability":
                op, val = _parse_operator(value)
                clauses.append(f"probability {op} ?")
                params.append(_parse_numeric(val))
            elif key == "channel":
                clauses.append("channel = ?")
                params.append(str(value))
        return clauses

    def _operational_filters(self, filters: dict[str, Any], params: list[Any]) -> list[str]:
        clauses: list[str] = []
        for key, value in filters.items():
            if key == "metric_type":
                clauses.append("metric_type = ?")
                params.append(str(value))
            elif key == "since":
                op, val = _parse_operator(value)
                clauses.append(f"timestamp {op} ?")
                params.append(_serialise_timestamp(val))
        return clauses


def _parse_operator(value: Any) -> tuple[str, Any]:
    if isinstance(value, str):
        value = value.strip()
        for op in (">=", "<=", "!=", ">", "<"):
            if value.startswith(op):
                return op, value[len(op) :].strip()
    return "=", value


def _parse_deadline(value: Any) -> tuple[str, str]:
    op, operand = _parse_operator(value)
    operand = str(operand)
    if operand.endswith("d"):
        try:
            days = int(float(operand[:-1]))
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError(f"Invalid deadline filter '{value}'") from exc
        target = (_utc_now() + timedelta(days=days)).date().isoformat()
        return op, target
    return op, operand


_INTEL_DB = IntelligenceDatabase()


@audit_tool_call("intelligence.lookup")
def intel_lookup(
    category: str,
    filters: dict[str, Any] | None = None,
    query: str | None = None,
    limit: int = 10,
    sort_by: str = "relevance",
) -> List[Dict[str, Any]]:
    """
    Query intelligence database.

    Examples:
        # High-fit grants due soon
        intel_lookup("grants", {"fit_score": ">4.5", "deadline": "<45d"})

        # Recent market insights about EU funding
        intel_lookup("insights", query="EU digital infrastructure", limit=5)

        # Warm contacts in Malaga
        intel_lookup("contacts", {"location": "Malaga", "connection": "warm"})

    Returns: List of intelligence nodes matching criteria.
    """

    filters = filters or {}
    limit = max(1, min(limit, 100))
    sort_map = {"relevance", "recency", "score"}
    if sort_by not in sort_map:
        raise ValueError(f"Unsupported sort order '{sort_by}'")
    return _INTEL_DB.query(category, filters, query, limit, sort_by)


__all__ = ["IntelligenceDatabase", "IntelligenceNode", "intel_lookup"]
