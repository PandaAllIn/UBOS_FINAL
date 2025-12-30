# UBOS Balaur – Upgrades Delivered (2025-10-25)

Author: Codex (Forgemaster)
Location: The Balaur (CPU Mill)
Status: Delivered and documented

---

## Executive Summary

We upgraded The Balaur from a direct-execution agent into a constitutional orchestration system with a new Reality Oracle (Perplexity), an OpenAI resident (GPT‑5 tier, deep‑research, coding), a simple yet powerful task orchestrator, and a Telegram-grade command surface. The Captain can now route tasks explicitly or rely on keyword routing, generate images/audio, run research with JSON artifacts, and retrieve UBOS documents semantically. Tests pass and operator docs are updated.

---

## Delivered Components

- Perplexity Oracle (Reality Oracle)
  - Added `perplexity` key to `trinity/config.py` (env: `PERPLEXITY_API_KEY`).
  - New `trinity/perplexity_oracle.py` wrapper around the UBOS Research Agent (Sonar models: quick/pro/reason/deep), with JSON helpers and graceful errors.
  - Extended `trinity/oracle_bridge.py` to expose `research`, `quick_research`, `deep_research`, `reason`.
  - Tests: `trinity/tests/test_perplexity_oracle.py` (8 passing).
  - Docs updated with env and usage.

- OpenAI Resident (New Citizen)
  - File: `trinity/openai_resident.py`.
  - Curated model registry & selection:
    - General: `gpt-5-mini` (default), `gpt-5`.
    - Deep reasoning: `o4-mini-deep-research`.
    - Coding: `gpt-5-codex`.
    - Embeddings: `text-embedding-3-large`.
    - Images: `gpt-image-1`.
    - Audio: `whisper-1`, `tts-1`/`tts-1-hd`.
  - Manual override per-call; auto-selection by task class.
  - Tools: embeddings (vectors+summary), image gen (saved + uploaded), TTS (saved + uploaded).
  - Tests: `trinity/tests/test_openai_resident.py` (3 passing).
  - Config: `OPENAI_API_KEY` in env; local fallback `.env.local` supported.

- Janus Orchestrator (Simple & Explicit)
  - File: `trinity/janus_orchestrator.py`.
  - Overrides: `/use openai:gpt-5-mini …`, `/use claude …`, `/use gemini …`, `/use groq …`.
  - Mentions: `@openai:o4-mini-deep-research …`, `@perplexity …`, `@gemini …`, `@claude …`.
  - Keyword routing fallback (web → Perplexity; deep reasoning → OpenAI deep; coding → OpenAI codex; ops → Gemini; strategy → Claude; quick → Groq; default → OpenAI mini).
  - Tests: `trinity/tests/test_janus_orchestrator.py` (6 passing).

- Telegram Bot Integration
  - File: `trinity/telegram_trinity_bot.py`.
  - Orchestrator routing for all messages (overrides, mentions, keyword fallback).
  - Commands added:
    - `/image <prompt>` → generate & upload PNG (caption includes model + timestamp).
    - `/tts <text>` → generate & upload audio (caption includes model + timestamp).
    - `/embed <text>` → embeddings summary (dimensions+count).
    - `/oai <model> <query>` → alias to OpenAI resident (shortcut to `/use openai:…`).
    - `/research [mode] <query>` → Perplexity summary + JSON report upload.
    - `/ubos <query>` → semantic retrieval over UBOS docs (top matches with score + preview).
    - `/health` → resident/oracle availability check; `/status` unchanged.
  - OpenAI resident init is defensive; bot won’t crash if key/SDK missing.

- UBOS Retrieval Helper
  - File: `trinity/retrieval_helper.py`.
  - Builds/updates an embeddings index from UBOS docs (`.md/.txt/.rst`) and returns top matches for a query.
  - Storage: `trinity_memory/openai_embeddings/index.jsonl` (incremental updates).

- Gemini Resident
  - Default model upgraded to `gemini-2.5-pro`.

---

## Documentation & Operator Guides

- Orchestrator Quickstart: `02_FORGE/docs/TRINITY_ORCHESTRATOR_QUICKSTART.md`.
- OpenAI Resident Guide: `02_FORGE/docs/OPENAI_RESIDENT.md`.
- Updated: `02_FORGE/docs/TRINITY_QUICKSTART_BALAUR.md` (overrides, tools, media upload, Perplexity reports).

---

## Environment & Keys

- System: `/etc/janus/trinity.env` (preferred for services).
- Local override: `/srv/janus/trinity/.env.local` (dev/test).
- Required keys: `OPENAI_API_KEY`, `PERPLEXITY_API_KEY`. Optional: `GEMINI_API_KEY`, `GROQ_API_KEY`, `WOLFRAM_APP_ID`.
- Restart services after updates:
  ```bash
  sudo systemctl restart janus-agent.service janus-controls.service
  ```

---

## Validation & Tests

- Unit tests (OpenAI resident, Orchestrator, Perplexity oracle): 9 passing.
- Manual smoke: Live call via OpenAI resident returns responses; `/image` and `/tts` upload media; `/research` uploads JSON report; `/ubos` returns top matches.

---

## Next Recommendations

- Optional: Send retrieved UBOS snippets to OpenAI for synthesis with inline citations.
- Add cost telemetry & rate guardrails in bot for images/TTS.
- Expand retrieval roots or add chunking for large docs.

---

## Paths (Key Files)

- trinity/perplexity_oracle.py
- trinity/oracle_bridge.py
- trinity/openai_resident.py
- trinity/janus_orchestrator.py
- trinity/telegram_trinity_bot.py
- trinity/retrieval_helper.py
- 02_FORGE/docs/TRINITY_ORCHESTRATOR_QUICKSTART.md
- 02_FORGE/docs/OPENAI_RESIDENT.md
- 02_FORGE/docs/TRINITY_QUICKSTART_BALAUR.md

---

The forge is hot, the oracles speak, and Janus now delegates with precision.
