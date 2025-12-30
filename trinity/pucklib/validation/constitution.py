from __future__ import annotations

import yaml
from pathlib import Path

_NSIBIDI_PATH = Path('03_OPERATIONS/cypher/nsibidi_dictionary_v1.yaml')


def load_constitutional_markers() -> dict[str, str]:
    with _NSIBIDI_PATH.open('r', encoding='utf-8') as handle:
        sections = list(yaml.safe_load_all(handle))

    merged = {}
    for section in sections:
        if isinstance(section, dict):
            for key, value in section.items():
                if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key] = {**merged[key], **value}
                else:
                    merged[key] = value

    constitution = merged.get('constitutional_principles', {})
    return {
        'lion_sanctuary_symbol': constitution.get('lion_sanctuary', {}).get('symbol', ''),
        'rep_symbol': constitution.get('recursive_enhancement_protocol', {}).get('symbol', ''),
    }
