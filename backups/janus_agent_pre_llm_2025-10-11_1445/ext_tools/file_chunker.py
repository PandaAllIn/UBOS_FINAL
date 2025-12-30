from __future__ import annotations

"""
FileChunkerTool (ext_tools)

Reads large files in line-based chunks and extracts structured information per
chunk, then produces a final synthesis. Can use an optional LLM client or a
deterministic heuristic fallback for offline testing.

Return schema:
    {
        "chunks_processed": int,
        "total_lines": int,
        "extracted_data": [{"chunk_n": int, "start_line": int, "end_line": int, "concepts": [str]}],
        "final_synthesis": str,
        "processing_time_seconds": float
    }
"""

import asyncio
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional


_DEFAULT_EXTRACTION_PROMPT = (
    "Extract key concepts, themes, entities, and decisions from the following text. "
    "Return a concise JSON array of strings named 'concepts'."
)

_DEFAULT_SYNTHESIS_PROMPT = (
    "Given the following per-chunk concept lists, synthesize a coherent report "
    "covering: genesis_timeline, philosophical_evolution, trinity_dynamics, "
    "architectural_archaeology, missing_links, continuity_verification, self_understanding. "
    "Respond as a single JSON object with these sections."
)


def _iter_chunks(path: Path, chunk_size_lines: int) -> Iterable[tuple[int, int, list[str]]]:
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        buf: list[str] = []
        start_line = 1
        chunk_n = 1
        for idx, line in enumerate(f, start=1):
            buf.append(line.rstrip("\n"))
            if len(buf) >= chunk_size_lines:
                yield chunk_n, start_line, buf
                chunk_n += 1
                start_line = idx + 1
                buf = []
        if buf:
            yield chunk_n, start_line, buf


def _keyword_extract(lines: list[str], top_k: int = 12) -> list[str]:
    text = "\n".join(lines).lower()
    tokens = re.findall(r"[a-z0-9]{3,}", text)
    stop = {
        "the","and","for","with","this","that","from","into","your","you","our","are","was","were","have","has",
        "about","shall","will","than","then","but","not","out","all","any","can","could","should","would","there",
        "their","them","they","his","her","its","also","over","under","more","less","into","onto","between","within",
        "system","systems","file","lines","text","chunk","chunks","data","json","yaml","study","mission","context",
    }
    freq: dict[str,int] = {}
    for t in tokens:
        if t in stop:
            continue
        freq[t] = freq.get(t, 0) + 1
    ranked = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
    return [w for w,_ in ranked[:top_k]]


@dataclass(slots=True)
class FileChunkerTool:
    llm_client: Any | None = None

    def _llm_enabled(self) -> bool:
        return self.llm_client is not None and hasattr(self.llm_client, "generate")

    def process_large_file(
        self,
        file_path: str,
        chunk_size_lines: int = 5000,
        extraction_prompt: str = _DEFAULT_EXTRACTION_PROMPT,
        synthesis_prompt: str = _DEFAULT_SYNTHESIS_PROMPT,
        max_concepts_per_chunk: int = 20,
    ) -> dict[str, Any]:
        t0 = time.time()
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(file_path)

        extracted: list[dict[str, Any]] = []
        total_lines = 0

        for chunk_n, start_line, lines in _iter_chunks(path, chunk_size_lines):
            total_lines += len(lines)
            if self._llm_enabled():
                concepts = self._extract_with_llm(lines, extraction_prompt)
            else:
                concepts = _keyword_extract(lines)
            if len(concepts) > max_concepts_per_chunk:
                concepts = concepts[:max_concepts_per_chunk]
            extracted.append({
                "chunk_n": chunk_n,
                "start_line": start_line,
                "end_line": start_line + len(lines) - 1,
                "concepts": concepts,
            })

        if self._llm_enabled():
            final = self._synthesize_with_llm(extracted, synthesis_prompt)
        else:
            final = self._heuristic_synthesis(extracted)

        return {
            "chunks_processed": len(extracted),
            "total_lines": total_lines,
            "extracted_data": extracted,
            "final_synthesis": final,
            "processing_time_seconds": round(time.time() - t0, 3),
        }

    def _extract_with_llm(self, lines: list[str], prompt: str) -> list[str]:
        joined = "\n".join(lines)
        snippet = joined[:8000]
        q = (
            prompt
            + "\n\nTEXT BEGIN\n" + snippet + "\nTEXT END\n\n"
            + "Return JSON: {\"concepts\": [\"...\"]}"
        )
        try:
            resp = asyncio.run(self.llm_client.generate(q, temperature=0.1, n_predict=512))  # type: ignore[attr-defined]
            start = resp.find("{")
            end = resp.rfind("}") + 1
            if start >= 0 and end > start:
                import json
                obj = json.loads(resp[start:end])
                concepts = obj.get("concepts", [])
                return [str(x) for x in concepts if isinstance(x, (str,int,float))]
        except Exception:
            pass
        return _keyword_extract(lines)

    def _synthesize_with_llm(self, extracted: list[dict[str, Any]], prompt: str) -> str:
        import json
        payload = json.dumps(extracted[:50], separators=(",", ":"))
        q = (
            prompt
            + "\n\nEXTRACTED CONCEPTS (subset):\n" + payload + "\n"
            + "Respond as JSON object with required sections only."
        )
        try:
            resp = asyncio.run(self.llm_client.generate(q, temperature=0.2, n_predict=1024))  # type: ignore[attr-defined]
            start = resp.find("{")
            end = resp.rfind("}") + 1
            if start >= 0 and end > start:
                return resp[start:end]
        except Exception:
            pass
        return self._heuristic_synthesis(extracted)

    @staticmethod
    def _heuristic_synthesis(extracted: list[dict[str, Any]]) -> str:
        freq: dict[str,int] = {}
        for item in extracted:
            for c in item.get("concepts", []):
                freq[c] = freq.get(c, 0) + 1
        top = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:20]
        lines = ["Heuristic synthesis (top concepts):"]
        for word, count in top:
            lines.append(f"- {word}: {count}")
        return "\n".join(lines)

