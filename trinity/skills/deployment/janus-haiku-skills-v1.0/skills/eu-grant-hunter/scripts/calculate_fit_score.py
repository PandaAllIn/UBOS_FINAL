from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from utils import (  # type: ignore
    Opportunity,
    SkillPaths,
    format_euro,
    load_pipeline_state,
    normalise_criteria,
    resolve_paths,
)


@dataclass(frozen=True)
class Capability:
    name: str
    summary: str
    keywords: frozenset[str]


@dataclass(frozen=True)
class ProjectProfile:
    name: str
    summary: str
    keywords: frozenset[str]
    budget_min: int | None
    budget_max: int | None
    priority: str


@dataclass(frozen=True)
class FitResult:
    fit_score: float
    explanation: list[str]
    matched_project: str | None
    matched_keywords: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "fit_score": self.fit_score,
            "explanation": self.explanation,
            "matched_project": self.matched_project,
            "matched_keywords": self.matched_keywords,
        }


class FitAnalyzer:
    """Deterministic fit scoring against reference knowledge."""

    def __init__(self, paths: SkillPaths | None = None) -> None:
        self.paths = paths or resolve_paths()
        references = self.paths.skill_root / "references"
        self.capabilities = tuple(_parse_capabilities(references / "ubos_capabilities.md"))
        self.projects = tuple(_parse_projects(references / "ubos_projects.md"))

    def analyse(self, opportunity: Opportunity) -> FitResult:
        tokens = _tokenize(
            " ".join(
                [
                    opportunity.title,
                    opportunity.program,
                    opportunity.description,
                    " ".join(opportunity.criteria),
                ]
            )
        )
        capability_score, capability_hits, capability_explanations = _score_capabilities(tokens, self.capabilities)
        best_project, project_score, project_explanation = _score_projects(tokens, self.projects)
        budget_score = _score_budget(opportunity, best_project)

        explanation: list[str] = []
        explanation.extend(capability_explanations)
        if project_explanation:
            explanation.append(project_explanation)
        explanation.append(
            f"Budget fit contribution: {budget_score:.1f}/1.0 ({_describe_budget(opportunity, best_project)})"
        )

        total_score = round(min(5.0, capability_score + project_score + budget_score), 1)

        return FitResult(
            fit_score=total_score,
            explanation=explanation,
            matched_project=best_project.name if best_project else None,
            matched_keywords=sorted(capability_hits),
        )


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[A-Za-z0-9]+", text.lower()) if len(token) > 2}


def _keyword_tokens(raw: str) -> set[str]:
    tokens: set[str] = set()
    for fragment in raw.split(","):
        tokens.update(_tokenize(fragment))
    return tokens


def _parse_sections(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Reference file not found: {path}")
    sections: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("## "):
            if current:
                sections.append(current)
            current = {"name": stripped[3:].strip()}
            continue
        if current is None:
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip().lower()] = value.strip()

    if current:
        sections.append(current)
    return sections


def _parse_capabilities(path: Path) -> Iterable[Capability]:
    for section in _parse_sections(path):
        name = section.get("name")
        if not name:
            continue
        keywords = frozenset(_keyword_tokens(section.get("keywords", "")))
        yield Capability(
            name=name,
            summary=section.get("summary", ""),
            keywords=keywords,
        )


def _parse_projects(path: Path) -> Iterable[ProjectProfile]:
    for section in _parse_sections(path):
        name = section.get("name")
        if not name:
            continue
        keywords = frozenset(_keyword_tokens(section.get("keywords", "")))
        budget_range = section.get("budget range") or section.get("budget")
        budget_min = budget_max = None
        if budget_range:
            try:
                lower, upper = budget_range.replace("€", "").split("-")
                budget_min = int(lower)
                budget_max = int(upper)
            except ValueError:
                pass
        yield ProjectProfile(
            name=name,
            summary=section.get("summary", ""),
            keywords=keywords,
            budget_min=budget_min,
            budget_max=budget_max,
            priority=section.get("priority", "medium"),
        )


def _score_capabilities(tokens: set[str], capabilities: Sequence[Capability]) -> tuple[float, set[str], list[str]]:
    score = 0.0
    hits: set[str] = set()
    explanations: list[str] = []

    for capability in capabilities:
        overlap = capability.keywords & tokens
        if not overlap:
            continue
        coverage = len(overlap) / max(1, len(capability.keywords))
        increment = min(1.75, 0.75 + coverage * 2.0)
        score = min(2.5, score + increment)
        hits.update(overlap)
        explanations.append(
            f"Capability '{capability.name}' coverage {coverage:.0%} ({', '.join(sorted(overlap))})"
        )

    return score, hits, explanations


def _score_projects(tokens: set[str], projects: Sequence[ProjectProfile]) -> tuple[ProjectProfile | None, float, str | None]:
    best_project: ProjectProfile | None = None
    best_score = 0.0
    best_explanation: str | None = None

    for project in projects:
        overlap = project.keywords & tokens
        if not overlap:
            continue
        coverage = len(overlap) / max(1, len(project.keywords))
        score = min(2.0, 1.0 + coverage * 1.5)
        if project.priority.lower() == "critical":
            score = min(2.0, score + 0.25)
        if score > best_score:
            best_score = score
            best_project = project
            best_explanation = (
                f"Project alignment: {project.name} ({score:.1f}/2.0) via {', '.join(sorted(overlap))}"
            )

    return best_project, best_score, best_explanation


def _score_budget(opportunity: Opportunity, project: ProjectProfile | None) -> float:
    if opportunity.budget_min is None and opportunity.budget_max is None:
        return 0.5
    if project is None or project.budget_min is None or project.budget_max is None:
        return 0.5
    opp_min = opportunity.budget_min or opportunity.budget_max or project.budget_min
    opp_max = opportunity.budget_max or opportunity.budget_min or project.budget_max
    if opp_max < project.budget_min or opp_min > project.budget_max:
        return 0.0
    return 1.0


def _describe_budget(opportunity: Opportunity, project: ProjectProfile | None) -> str:
    if project is None:
        return "no project selected"
    return (
        f"opportunity €{format_euro(opportunity.budget_min)}-€{format_euro(opportunity.budget_max)} vs "
        f"project target €{format_euro(project.budget_min)}-€{format_euro(project.budget_max)}"
    )


def calculate_fit_score(opportunity: Opportunity, analyzer: FitAnalyzer | None = None) -> FitResult:
    analyzer = analyzer or FitAnalyzer()
    opportunity.criteria = normalise_criteria(opportunity.criteria)
    return analyzer.analyse(opportunity)


def _update_pipeline(entries: Sequence[Opportunity], analyzer: FitAnalyzer) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for entry in entries:
        fit = calculate_fit_score(entry, analyzer)
        entry.fit_score = fit.fit_score
        entry.fit_explanation = fit.explanation
        entry.ubos_project_match = fit.matched_project
        entry.matched_keywords = fit.matched_keywords
        results.append(fit.to_dict() | {"opportunity_id": entry.opportunity_id})
    return results


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Calculate UBOS fit scores for grant opportunities.")
    parser.add_argument("--opportunity-id", help="Specific opportunity ID to score", default=None)
    parser.add_argument("--pipeline", help="Optional pipeline JSON path", default=None)
    parser.add_argument("--output", help="Write results to JSON file", default=None)
    args = parser.parse_args(argv)

    paths = resolve_paths()
    analyzer = FitAnalyzer(paths)

    if args.pipeline:
        pipeline_path = Path(args.pipeline)
        payload = json.loads(pipeline_path.read_text(encoding="utf-8"))
        opportunities = [Opportunity.from_dict(item) for item in payload.get("opportunities", [])]
    else:
        payload = load_pipeline_state(paths)
        opportunities = payload.get("opportunities", [])

    if args.opportunity_id:
        opportunities = [op for op in opportunities if op.opportunity_id == args.opportunity_id]
        if not opportunities:
            parser.error(f"Opportunity '{args.opportunity_id}' not found in pipeline")

    results = _update_pipeline(opportunities, analyzer)

    if args.output:
        Path(args.output).write_text(json.dumps(results, indent=2), encoding="utf-8")
    else:
        sys.stdout.write(json.dumps(results, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
