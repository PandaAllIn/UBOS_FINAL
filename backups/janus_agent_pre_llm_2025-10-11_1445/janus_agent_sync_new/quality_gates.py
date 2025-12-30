"""Mission quality gate evaluation helpers."""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence


class MissionQualityError(RuntimeError):
    """Raised when Tier 1 mission quality gates are violated."""

    def __init__(self, message: str, *, code: str = "quality_violation") -> None:
        super().__init__(message)
        self.code = code


@dataclass(slots=True)
class MissionQualityGates:
    MINIMUM_NODE_COUNT_RATIO: float = 0.5
    MAXIMUM_STUB_RATIO: float = 0.1
    MINIMUM_RELATIONSHIP_DENSITY: float = 0.3


@dataclass(slots=True)
class QualityWarningsConfig:
    TARGET_NODE_COUNT_RATIO: float = 0.8
    TARGET_CONFIDENCE_AVG: float = 0.75
    TARGET_SOURCE_DENSITY: float = 2.0


@dataclass(slots=True)
class ExcellenceMetricsConfig:
    RICH_PRACTICE_RATIO: float = 0.4
    CROSS_BOOK_RATIO: float = 0.5
    SYNTHESIS_NODE_RATIO: float = 0.3


@dataclass(slots=True)
class NodeGenerationQuality:
    summary: Dict[str, Any]
    quality: Dict[str, Any]
    warnings: List[str]
    excellence: Dict[str, float]


def evaluate_node_generation_quality(stdout: str) -> NodeGenerationQuality:
    """Parse node generator output and enforce quality gates."""
    payload = _parse_json_document(stdout)
    nodes: Sequence[dict[str, Any]] = ()
    summary = payload
    if isinstance(payload, dict) and "summary" in payload:
        summary = payload["summary"]
        nodes = payload.get("nodes") or ()

    if not isinstance(summary, dict):
        raise MissionQualityError("Node generator summary missing or malformed.", code="missing_summary")

    quality = summary.get("quality")
    if not isinstance(quality, dict):
        raise MissionQualityError("Node generator quality metrics missing from output.", code="missing_quality")

    generated = int(quality.get("generated", summary.get("generated", 0)))
    target_min = int(quality.get("target_min", 0))
    target_max = int(quality.get("target_max", 0))
    if target_min <= 0:
        raise MissionQualityError("Quality summary missing target_min.", code="missing_target_min")
    min_required = math.ceil(target_min * MissionQualityGates.MINIMUM_NODE_COUNT_RATIO)
    if generated < min_required:
        raise MissionQualityError(
            f"Generated {generated} nodes; Tier 1 minimum is {min_required} ("
            f"{MissionQualityGates.MINIMUM_NODE_COUNT_RATIO:.0%} of target_min {target_min}).",
            code="insufficient_node_count",
        )

    stub_ratio = float(quality.get("stub_ratio", 0.0))
    if stub_ratio > MissionQualityGates.MAXIMUM_STUB_RATIO:
        raise MissionQualityError(
            f"Stub ratio {stub_ratio:.2%} exceeds Tier 1 maximum "
            f"{MissionQualityGates.MAXIMUM_STUB_RATIO:.0%}.",
            code="stub_ratio",
        )

    relationship_density = float(quality.get("relationship_density", 0.0))
    if relationship_density < MissionQualityGates.MINIMUM_RELATIONSHIP_DENSITY:
        raise MissionQualityError(
            f"Relationship density {relationship_density:.2f} below Tier 1 minimum "
            f"{MissionQualityGates.MINIMUM_RELATIONSHIP_DENSITY:.2f}.",
            code="relationship_density",
        )

    average_confidence = float(quality.get("average_confidence", 0.0))
    source_density = float(quality.get("source_density", 0.0))
    warnings: List[str] = list(quality.get("warnings", []))

    warnings_config = QualityWarningsConfig()
    if generated < math.ceil(target_min * warnings_config.TARGET_NODE_COUNT_RATIO):
        warnings.append(
            f"Generated {generated} nodes; Tier 2 ambition is "
            f"{math.ceil(target_min * warnings_config.TARGET_NODE_COUNT_RATIO)}."
        )

    if average_confidence < warnings_config.TARGET_CONFIDENCE_AVG:
        warnings.append(
            f"Average confidence {average_confidence:.2f} below Tier 2 target "
            f"{warnings_config.TARGET_CONFIDENCE_AVG:.2f}."
        )

    if source_density and source_density < warnings_config.TARGET_SOURCE_DENSITY:
        warnings.append(
            f"Average source density {source_density:.2f} below Tier 2 target "
            f"{warnings_config.TARGET_SOURCE_DENSITY:.2f}."
        )

    excellence = dict(quality.get("excellence") or {})
    if nodes and not excellence:
        excellence = _compute_excellence(nodes)

    return NodeGenerationQuality(
        summary=summary,
        quality={**quality, "target_max": target_max, "average_confidence": average_confidence, "source_density": source_density},
        warnings=warnings,
        excellence=excellence,
    )


def _parse_json_document(text: str) -> Any:
    stripped = text.strip()
    if not stripped:
        raise MissionQualityError("Node generator emitted empty output.", code="empty_output")
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        last_index = stripped.rfind("{")
        while last_index != -1:
            candidate = stripped[last_index:]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                last_index = stripped.rfind("{", 0, last_index)
        raise MissionQualityError("Unable to parse JSON summary from node generator output.", code="parse_error")


def _compute_excellence(nodes: Sequence[dict[str, Any]]) -> Dict[str, float]:
    if not nodes:
        return {}
    total = len(nodes)
    richness = sum(1 for node in nodes if node.get("practices"))
    cross_book = 0
    synthesis = 0
    for node in nodes:
        sources = node.get("sources") or ()
        unique_books = {src.get("book") for src in sources if isinstance(src, dict)}
        if len(unique_books) >= 2:
            cross_book += 1
        if str(node.get("type", "")).lower() == "synthesis":
            synthesis += 1
    return {
        "rich_practice_ratio": richness / total,
        "cross_book_ratio": cross_book / total,
        "synthesis_node_ratio": synthesis / total,
    }
