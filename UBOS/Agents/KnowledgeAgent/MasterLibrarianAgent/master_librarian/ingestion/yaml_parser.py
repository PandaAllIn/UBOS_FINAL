"""Helpers for parsing UBOS YAML concept files."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Optional

import yaml

from master_librarian.models import Concept, ConceptType

LOGGER = logging.getLogger(__name__)


def parse_concept_yaml(
    path: Path | str,
    *,
    concept_type_hint: ConceptType,
    chapter: Optional[str] = None,
    book: Optional[str] = None,
) -> Concept:
    """Parse a YAML file into a :class:`Concept`."""

    yaml_path = Path(path)
    if not yaml_path.exists():
        raise FileNotFoundError(f"Concept YAML file not found: {yaml_path}")

    with yaml_path.open("r", encoding="utf-8") as fh:
        try:
            payload: Dict[str, object] = yaml.safe_load(fh) or {}
        except yaml.YAMLError as exc:
            raise ValueError(f"Failed to parse YAML {yaml_path}") from exc

    concept = Concept.from_yaml(
        payload,
        concept_type=concept_type_hint,
        source_path=str(yaml_path.relative_to(yaml_path.parents[3]) if len(yaml_path.parents) >= 3 else yaml_path),
        chapter=chapter,
        book=book,
    )

    return concept


__all__ = ["parse_concept_yaml"]
