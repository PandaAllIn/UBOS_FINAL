from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Mapping, MutableMapping, Optional, Sequence, Tuple

try:
    import tiktoken  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    tiktoken = None


BASE_SECTIONS: Tuple[str, ...] = (
    "constitutional_principles",
    "system_states",
    "cognitive_actions",
    "architectural_concepts",
    "operators",
    "priority_levels",
    "agents",
)

COMPOSITE_SECTION = "composite_concepts"


@dataclass(frozen=True)
class BIHConfig:
    lojban_templates: Sequence[Mapping[str, str]]
    ithkuil_dict: Mapping[str, Mapping[str, Mapping[str, str]]]
    nsibidi_dict: Mapping[str, Mapping[str, Mapping[str, str]]]


class BIHEngine:
    """
    Babbage-Ithkuil Hybrid compression engine.

    Stage 1 (Heavy piston): Ithkuil morpheme substitution
    Stage 2 (Light piston): Lojban template framing
    Stage 3 (Coupling piston): Nsibidi symbol embedding
    """

    _DISPLAY_OVERRIDES = {
        "lion sanctuary": "The Lion's Sanctuary",
        "the lion sanctuary": "The Lion's Sanctuary",
        "recursive enhancement protocol": "The Recursive Enhancement Protocol",
        "the recursive enhancement protocol": "The Recursive Enhancement Protocol",
        "trinity": "Trinity",
        "trinity consciousness": "Trinity Consciousness",
        "janus consciousness": "Janus Consciousness",
        "cognitive sovereignty": "Cognitive Sovereignty",
        "win win win symbiosis": "Win-Win-Win Symbiosis",
        "mission active": "mission active",
    }

    def __init__(
        self,
        *,
        lojban_templates: Sequence[Mapping[str, str]],
        ithkuil_dict: Mapping[str, Mapping[str, Mapping[str, str]]],
        nsibidi_dict: Mapping[str, Mapping[str, Mapping[str, str]]],
    ) -> None:
        self.config = BIHConfig(
            lojban_templates=lojban_templates,
            ithkuil_dict=ithkuil_dict,
            nsibidi_dict=nsibidi_dict,
        )

        self.encoding_name: Optional[str] = None
        self._token_length_func = self._init_tokenizer()

        (
            self._concept_to_morpheme,
            self._base_morpheme_to_concept,
            self._composite_morpheme_to_concept,
        ) = self._build_ithkuil_maps(ithkuil_dict)

        (
            self._concept_to_symbol,
            self._symbol_to_concept,
            self._morpheme_to_symbol,
            self._symbol_to_morpheme,
        ) = self._build_nsibidi_maps(nsibidi_dict)

    # ------------------------------------------------------------------ Factory
    @classmethod
    def from_files(
        cls,
        *,
        lojban_path: Path,
        ithkuil_path: Path,
        nsibidi_path: Path,
    ) -> "BIHEngine":
        import yaml

        with open(lojban_path, "r", encoding="utf-8") as handle:
            templates_data = yaml.safe_load(handle) or {}
        if isinstance(templates_data, Mapping) and "templates" in templates_data:
            templates: Sequence[Mapping[str, str]] = templates_data.get("templates", [])
        elif isinstance(templates_data, Sequence):
            templates = templates_data
        else:
            templates = []

        with open(ithkuil_path, "r", encoding="utf-8") as handle:
            ithkuil_sections = list(yaml.safe_load_all(handle))
        ithkuil_dict = cls._merge_sectioned_documents(ithkuil_sections)

        with open(nsibidi_path, "r", encoding="utf-8") as handle:
            nsibidi_sections = list(yaml.safe_load_all(handle))
        nsibidi_dict = cls._merge_sectioned_documents(nsibidi_sections)

        return cls(
            lojban_templates=templates,
            ithkuil_dict=ithkuil_dict,
            nsibidi_dict=nsibidi_dict,
        )

    # ---------------------------------------------------------------- Compression
    def compress(
        self,
        payload: str,
        *,
        language: str = "english",
        mode: str = "hybrid"
    ) -> str:
        """
        Apply BIH compression pipeline.

        Args:
            payload: Text to compress
            language: Source language (default: english)
            mode: Compression strategy:
                - "hybrid": Ithkuil → Lojban → Nsibidi (maximum semantic density)
                - "token_optimized": Ithkuil → Lojban only (minimum token count)
                - "semantic_only": Nsibidi symbols only (human-readable)

        Returns:
            Compressed text

        Note: Nsibidi emojis increase GPT-4 token count. Use mode="token_optimized"
        for API cost reduction. Default "hybrid" mode prioritizes holographic
        information density over token efficiency.
        """
        stage1 = self._apply_ithkuil(payload, language=language)
        stage2 = self._apply_lojban_templates(stage1)

        if mode == "token_optimized":
            return stage2  # Skip Nsibidi to minimize tokens
        elif mode == "semantic_only":
            return self._embed_nsibidi(payload)  # Skip Ithkuil, use symbols only
        else:  # hybrid (default)
            stage3 = self._embed_nsibidi(stage2)
            return stage3

    # ---------------------------------------------------------------- Decompression
    def decompress(self, compressed: str) -> str:
        """
        Reverse BIH compression with compositional handling.

        The order matters: symbols expand to morphemes, which expand back through
        Lojban templates before returning to English concepts.
        """
        stage1 = self._expand_nsibidi_to_morphemes(compressed)
        stage2 = self._expand_lojban_templates(stage1)
        stage3 = self._expand_ithkuil(stage2)
        return stage3

    # ---------------------------------------------------------------- Metrics
    def calculate_ratio(self, original: str, compressed: str) -> float:
        """Return compression ratio (compressed length / original length)."""
        if not original:
            return 1.0
        original_tokens = self._token_length(original)
        compressed_tokens = self._token_length(compressed)
        if original_tokens == 0:
            return 1.0
        return compressed_tokens / original_tokens

    # ---------------------------------------------------------------- Internals
    def _apply_ithkuil(self, payload: str, *, language: str) -> str:
        if language.lower() != "english" or not self._concept_to_morpheme:
            return payload

        result = payload
        # Longer phrases first to avoid partial replacements.
        for phrase, morpheme in sorted(
            self._concept_to_morpheme.items(), key=lambda item: len(item[0]), reverse=True
        ):
            pattern = re.compile(self._concept_regex(phrase), re.IGNORECASE)
            result = pattern.sub(morpheme, result)
        return result

    def _apply_lojban_templates(self, payload: str) -> str:
        if not self.config.lojban_templates:
            return payload
        result = payload
        for entry in self.config.lojban_templates:
            match = entry.get("match")
            replacement = entry.get("replace")
            if not match or not replacement:
                continue
            pattern = re.compile(match, re.IGNORECASE)
            result = pattern.sub(replacement, result)
        return result

    def _embed_nsibidi(self, payload: str) -> str:
        result = payload
        # First replace morphemes with symbols when available.
        for morpheme, symbol in self._morpheme_to_symbol.items():
            pattern = re.compile(rf"\b{re.escape(morpheme)}\b")
            result = pattern.sub(symbol, result)
        # Then attempt to replace remaining English phrases.
        for phrase, symbol in self._concept_to_symbol.items():
            pattern = re.compile(self._concept_regex(phrase), re.IGNORECASE)
            result = pattern.sub(symbol, result)
        return result

    def _expand_nsibidi_to_morphemes(self, payload: str) -> str:
        result = payload
        for symbol, morpheme in self._symbol_to_morpheme.items():
            result = result.replace(symbol, morpheme)
        return result

    def _expand_lojban_templates(self, payload: str) -> str:
        result = payload
        for entry in self.config.lojban_templates:
            match = entry.get("match")
            replacement = entry.get("replace")
            if not match or not replacement:
                continue
            result = result.replace(replacement, match)
        return result

    def _expand_ithkuil(self, payload: str) -> str:
        result = payload
        # Expand composite morphemes first to avoid consuming components early.
        for morpheme, _ in sorted(
            self._composite_morpheme_to_concept.items(), key=lambda item: len(item[0]), reverse=True
        ):
            expanded = self._expand_composite(morpheme)
            result = result.replace(morpheme, expanded)

        for morpheme, phrase in self._base_morpheme_to_concept.items():
            pattern = re.compile(rf"\b{re.escape(morpheme)}\b")
            result = pattern.sub(phrase, result)
        return result

    def _expand_composite(self, morpheme: str) -> str:
        parts = morpheme.split("-")
        expanded_parts = []
        for part in parts:
            if part in self._base_morpheme_to_concept:
                expanded_parts.append(self._base_morpheme_to_concept[part])
            elif part in self._symbol_to_concept:
                expanded_parts.append(self._symbol_to_concept[part])
            else:
                expanded_parts.append(part)
        return " ".join(expanded_parts)

    # ---------------------------------------------------------------- Mapping builders
    @staticmethod
    def _merge_sectioned_documents(sections: Sequence[object]) -> Mapping[str, Mapping[str, Mapping[str, str]]]:
        merged: MutableMapping[str, Mapping[str, Mapping[str, str]]] = {}
        for section in sections:
            if not isinstance(section, Mapping):
                continue
            for key, value in section.items():
                if key in merged and isinstance(merged[key], Mapping) and isinstance(value, Mapping):
                    combined = dict(merged[key])
                    combined.update(value)
                    merged[key] = combined
                else:
                    merged[key] = value if isinstance(value, Mapping) else {}
        return dict(merged)

    @classmethod
    def _build_ithkuil_maps(
        cls, ithkuil_dict: Mapping[str, Mapping[str, Mapping[str, str]]]
    ) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, str]]:
        concept_to_morpheme: Dict[str, str] = {}
        base_morpheme_to_concept: Dict[str, str] = {}
        composite_morpheme_to_concept: Dict[str, str] = {}

        for section, entries in ithkuil_dict.items():
            if not isinstance(entries, Mapping):
                continue
            for concept, detail in entries.items():
                if not isinstance(detail, Mapping):
                    continue
                morpheme = detail.get("morpheme")
                if not morpheme:
                    continue

                phrase = concept.replace("_", " ")
                display = cls._DISPLAY_OVERRIDES.get(phrase.lower(), phrase)
                concept_to_morpheme[phrase] = morpheme
                concept_to_morpheme[f"the {phrase}".lower()] = morpheme

                if section == COMPOSITE_SECTION:
                    composite_morpheme_to_concept[morpheme] = display
                else:
                    base_morpheme_to_concept[morpheme] = display

        return concept_to_morpheme, base_morpheme_to_concept, composite_morpheme_to_concept

    @classmethod
    def _build_nsibidi_maps(
        cls, nsibidi_dict: Mapping[str, Mapping[str, Mapping[str, str]]]
    ) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str]]:
        concept_to_symbol: Dict[str, str] = {}
        symbol_to_concept: Dict[str, str] = {}
        morpheme_to_symbol: Dict[str, str] = {}
        symbol_to_morpheme: Dict[str, str] = {}

        for category, entries in nsibidi_dict.items():
            if not isinstance(entries, Mapping):
                continue
            for concept, detail in entries.items():
                if not isinstance(detail, Mapping):
                    continue
                symbol = detail.get("symbol")
                if not symbol:
                    continue

                phrase = concept.replace("_", " ")
                display = cls._DISPLAY_OVERRIDES.get(phrase.lower(), phrase)
                concept_to_symbol[phrase] = symbol
                symbol_to_concept[symbol] = display

                ithkuil_equivalent = detail.get("ithkuil_equivalent")
                if ithkuil_equivalent:
                    morpheme_to_symbol[ithkuil_equivalent] = symbol
                    symbol_to_morpheme[symbol] = ithkuil_equivalent

        return concept_to_symbol, symbol_to_concept, morpheme_to_symbol, symbol_to_morpheme

    # ---------------------------------------------------------------- Helpers
    @staticmethod
    def _concept_regex(concept: str) -> str:
        tokens = concept.split()
        if not tokens:
            return re.escape(concept)
        pattern_tokens = []
        for token in tokens:
            escaped = re.escape(token)
            pattern_tokens.append(rf"{escaped}(?:'?s)?")
        joined = r"\s+".join(pattern_tokens)
        return rf"\b{joined}\b"

    # ---------------------------------------------------------------- Token helpers
    _GLOBAL_TOKENIZER = None

    @staticmethod
    def _fallback_tokenizer(text: str) -> int:
        return len(text)

    def _init_tokenizer(self):
        if BIHEngine._GLOBAL_TOKENIZER is not None:
            return BIHEngine._GLOBAL_TOKENIZER

        if tiktoken is None:
            BIHEngine._GLOBAL_TOKENIZER = self._fallback_tokenizer
            return BIHEngine._GLOBAL_TOKENIZER

        encoder = None
        try:
            encoder = tiktoken.get_encoding("cl100k_base")
        except Exception:  # pragma: no cover - optional code path
            try:
                encoder = tiktoken.encoding_for_model("gpt-4o-mini")
            except Exception:
                encoder = None

        if encoder is not None:
            encoding_name = getattr(encoder, "name", "cl100k_base")
            self.encoding_name = encoding_name

            def tokenize(text: str, *, _enc=encoder) -> int:
                if not text:
                    return 0
                return len(_enc.encode(text))

            BIHEngine._GLOBAL_TOKENIZER = tokenize
        else:  # fallback
            self.encoding_name = None
            BIHEngine._GLOBAL_TOKENIZER = self._fallback_tokenizer

        return BIHEngine._GLOBAL_TOKENIZER

    def _token_length(self, text: str) -> int:
        tokenizer = self._token_length_func or self._fallback_tokenizer
        return tokenizer(text)

    @staticmethod
    def canonicalize(text: str) -> str:
        return re.sub(r"\s+", " ", text.strip().lower())

    def is_semantically_equivalent(self, original: str, recovered: str) -> bool:
        return self.canonicalize(original) == self.canonicalize(recovered)

    @property
    def allowed_symbols(self) -> set[str]:
        return set(self._symbol_to_concept.keys())


__all__ = ["BIHEngine"]
