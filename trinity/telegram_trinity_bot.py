"""Trinity Telegram Bot

Reconstructed with defensive initialization and orchestrator routing.

Commands (per UPGRADE_LOG_2025-10-25.md):
  /image <prompt>             → OpenAI image gen + upload
  /tts <text>                 → OpenAI TTS + upload
  /embed <text>               → OpenAI embeddings summary
  /oai <model> <query>        → OpenAI resident call
  /claude <prompt>            → Claude resident override (optional model as first word)
  /gemini <prompt>            → Gemini resident override
  /groq <prompt>              → Groq resident override
  /research [mode] <query>    → Perplexity + JSON report upload
  /ubos <query>               → semantic UBOS doc retrieval (fallback keyword scan)
  /health                     → resident/oracle availability
  /status                     → unchanged (status summary)
  /now                        → live Balaur mission snapshot

All non-command messages route through janus_orchestrator plan_from_text
to choose a resident/oracle based on overrides, mentions, or keyword fallback.

The bot does not crash if any resident/oracle is missing. Each feature
degrades gracefully with a helpful message.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import APIKeys, TrinityPaths, load_configuration
from janus_orchestrator import DelegationPlan, plan_from_text
from openai_resident import ResidentOpenAI
from oracle_bridge import OracleBridge
from orchestrator_executor import execute_plan

# Claude resident is optional; import defensively
try:
    from claude_resident import ResidentClaude
except Exception:  # pragma: no cover
    ResidentClaude = None  # type: ignore


LOGGER = logging.getLogger("trinity.telegram_bot")


@dataclass
class BotState:
    paths: TrinityPaths
    keys: APIKeys
    oracle: OracleBridge
    oai: ResidentOpenAI | None
    claude: Any | None
    mission_state_path: Path
    mission_log_path: Path


def _ensure_logging() -> None:
    level = os.getenv("TRINITY_BOT_LOG", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def _build_state() -> BotState:
    paths, keys = load_configuration()

    # Residents: defensive initialization
    oai: ResidentOpenAI | None = None
    try:
        oai = ResidentOpenAI()
    except Exception as exc:  # pragma: no cover - keys/SDK may be missing
        LOGGER.warning("OpenAI resident unavailable: %s", exc)
        oai = None

    claude = None
    if ResidentClaude is not None:
        try:
            claude = ResidentClaude()
        except Exception as exc:  # pragma: no cover
            LOGGER.warning("Claude resident unavailable: %s", exc)
            claude = None

    oracle = OracleBridge(keys)
    mission_state_path = Path("/srv/janus/03_OPERATIONS/vessels/balaur/state/mission_orchestrator_state.json")
    mission_log_path = Path("/srv/janus/03_OPERATIONS/vessels/balaur/logs/mission_transitions.log")
    return BotState(
        paths=paths,
        keys=keys,
        oracle=oracle,
        oai=oai,
        claude=claude,
        mission_state_path=mission_state_path,
        mission_log_path=mission_log_path,
    )


async def _send_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    if not update.effective_chat:
        return
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text[:4096])


def _conversation_id(update: Update) -> str:
    chat_id = update.effective_chat.id if update.effective_chat else 0
    user_id = update.effective_user.id if update.effective_user else 0
    return f"tg:{chat_id}:{user_id}"


def _execute_plan(plan: DelegationPlan, state: BotState) -> str:
    try:
        return execute_plan(plan, state.paths, state.keys)
    except Exception as exc:  # pragma: no cover - defensive
        LOGGER.error("Plan execution failed: %s", exc)
        return f"Delegation error: {exc}"


def _mission_snapshot(state: BotState) -> str:
    lines = []
    if state.mission_state_path.exists():
        try:
            data = json.loads(state.mission_state_path.read_text(encoding="utf-8"))
            current = data.get("current_mission")
            lines.append(f"Current mission: {current or 'none'}")
        except json.JSONDecodeError:
            lines.append("Current mission: [state file corrupted]")
    else:
        lines.append("Current mission: [state file missing]")

    if state.mission_log_path.exists():
        try:
            tail = state.mission_log_path.read_text(encoding="utf-8").strip().splitlines()
            if tail:
                lines.append(f"Last event: {tail[-1]}")
        except Exception:
            lines.append("Last event: [log unreadable]")
    else:
        lines.append("Last event: [log missing]")
    return "\n".join(lines)


def _parse_tail(text: str, *, min_parts: int = 2) -> Optional[str]:
    parts = (text or "").strip().split(None, min_parts - 1)
    if len(parts) < min_parts:
        return None
    return parts[-1].strip()


def _extract_file_path_from_message(msg: str) -> Optional[Path]:
    # Expect formats like:
    #   "Image generated: /path/to/file | model=..."
    #   "Audio generated: /path/to/file | model=..."
    if ": " in msg:
        after = msg.split(": ", 1)[1]
        path_s = after.split(" | ", 1)[0].strip()
        p = Path(path_s)
        return p if p.exists() else None
    return None


# ------------------------------- command handlers ------------------------------


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Trinity Telegram Bot online.\n"
        "Use /health, /status, or try: /image, /tts, /embed, /oai, /research, /ubos.\n"
        "Messages are routed via the Janus Orchestrator."
    )
    await _send_text(update, context, text)


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    flags = [
        f"OpenAI: {'ok' if state.oai is not None else 'unavailable'}",
        f"Claude: {'ok' if (state.claude and getattr(state.claude, 'is_available', lambda: False)()) else 'unavailable'}",
        f"Perplexity: {'ok' if getattr(state.oracle, 'perplexity_client', None) else 'unavailable'}",
        f"Groq: {'ok' if getattr(state.oracle, 'client', None) else 'unavailable'}",
    ]
    text = (
        "Trinity Status\n"
        f"Time: {now}\n"
        f"Paths: memory={state.paths.memory_dir}, logs={state.paths.log_dir}\n"
        + "\n".join(f"- {f}" for f in flags)
        + "\n"
        + _mission_snapshot(state)
    )
    await _send_text(update, context, text)


async def cmd_health(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    statuses = []

    # Telegram token presence
    statuses.append({"service": "telegram", "available": bool(state.keys.telegram_token)})

    # OpenAI
    statuses.append({"service": "openai_resident", "available": state.oai is not None})

    # Claude
    claude_ok = bool(state.claude and getattr(state.claude, "is_available", lambda: False)())
    statuses.append({"service": "claude_resident", "available": claude_ok})

    # Oracles
    statuses.append({"service": "perplexity", "available": getattr(state.oracle, "perplexity_client", None) is not None})
    statuses.append({"service": "groq", "available": getattr(state.oracle, "client", None) is not None})

    lines = ["Health Check"]
    for s in statuses:
        lines.append(f"- {s['service']}: {'ok' if s['available'] else 'unavailable'}")
    await _send_text(update, context, "\n".join(lines))


async def cmd_now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    await _send_text(update, context, _mission_snapshot(state))


async def cmd_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    prompt = _parse_tail(update.message.text, min_parts=2) if update.message else None
    if not prompt:
        await _send_text(update, context, "Usage: /image <prompt>")
        return
    if not state.oai:
        await _send_text(update, context, "OpenAI resident unavailable (image generation requires OpenAI).")
        return
    msg = state.oai.generate_image(prompt)
    p = _extract_file_path_from_message(msg)
    if p and p.exists():
        try:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
            with p.open("rb") as fh:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=fh, caption=msg[:1024])
        except Exception as exc:
            await _send_text(update, context, f"Generated but failed to upload image: {exc}\n{msg}")
    else:
        await _send_text(update, context, msg)


async def cmd_tts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    text = _parse_tail(update.message.text, min_parts=2) if update.message else None
    if not text:
        await _send_text(update, context, "Usage: /tts <text>")
        return
    if not state.oai:
        await _send_text(update, context, "OpenAI resident unavailable (TTS requires OpenAI).")
        return
    msg = state.oai.text_to_speech(text)
    p = _extract_file_path_from_message(msg)
    if p and p.exists():
        try:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_VOICE)
            with p.open("rb") as fh:
                await context.bot.send_audio(chat_id=update.effective_chat.id, audio=fh, caption=msg[:1024])
        except Exception as exc:
            await _send_text(update, context, f"Generated but failed to upload audio: {exc}\n{msg}")
    else:
        await _send_text(update, context, msg)


async def cmd_embed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    text = _parse_tail(update.message.text, min_parts=2) if update.message else None
    if not text:
        await _send_text(update, context, "Usage: /embed <text>")
        return
    if not state.oai:
        await _send_text(update, context, "OpenAI resident unavailable (embeddings require OpenAI).")
        return
    result = state.oai.create_embeddings(text)
    await _send_text(update, context, result)


async def cmd_oai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    if not state.oai:
        await _send_text(update, context, "OpenAI resident unavailable.")
        return
    raw = (update.message.text or "").strip()
    parts = raw.split(None, 2)
    if len(parts) < 3:
        await _send_text(update, context, "Usage: /oai <model> <query>")
        return
    _, model, query = parts[0], parts[1], parts[2]
    conv_id = _conversation_id(update)
    await _send_text(update, context, state.oai.generate_response(conv_id, query, model=model))


def _research_summary_from_json(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if not isinstance(payload, dict):
        return "Perplexity returned an unexpected payload."
    content = payload.get("content") or ""
    model = payload.get("model_used") or "sonar"
    rid = payload.get("research_id") or ""
    header = f"Perplexity ({model})"
    if rid:
        header += f"\nResearch ID: {rid}"
    return (header + "\n\n" + (content.strip() or "[No content] ")).strip()


async def cmd_research(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    raw = (update.message.text or "").strip()
    # Forms:
    #   /research <query>
    #   /research <mode> <query>
    parts = raw.split(None, 2)
    if len(parts) < 2:
        await _send_text(update, context, "Usage: /research [mode] <query>")
        return
    if len(parts) == 2:
        mode, query = "auto", parts[1]
    else:
        mode, query = parts[1], parts[2]

    # JSON report
    payload = state.oracle.perplexity_client and state.oracle.perplexity_client.research_json(query, mode=mode)  # type: ignore[attr-defined]
    if not payload:
        await _send_text(update, context, "Perplexity oracle unavailable (missing API key or integration).")
        return

    # Save JSON artifact
    out_dir = state.paths.memory_dir / "perplexity_reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"research_{ts}.json"
    try:
        with out_path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=True, indent=2)
    except Exception as exc:
        LOGGER.warning("Failed to write research JSON: %s", exc)

    # Send summary and upload JSON
    summary = _research_summary_from_json(payload)
    await _send_text(update, context, summary)
    try:
        if out_path.exists():
            with out_path.open("rb") as fh:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=fh, filename=out_path.name)
    except Exception as exc:  # pragma: no cover
        await _send_text(update, context, f"Saved report but failed to upload JSON: {exc}")


def _scan_text_files(root: Path, pattern: str) -> list[tuple[Path, str]]:
    results: list[tuple[Path, str]] = []
    try:
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".md", ".txt", ".rst"}:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if re.search(pattern, text, flags=re.IGNORECASE):
                # Grab a small preview around the first match
                m = re.search(pattern, text, flags=re.IGNORECASE)
                start = max(0, (m.start() if m else 0) - 80)
                end = min(len(text), (m.end() if m else 0) + 80)
                preview = text[start:end].replace("\n", " ")
                results.append((p, preview))
                if len(results) >= 8:
                    break
    except Exception:
        pass
    return results


async def cmd_ubos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    query = _parse_tail(update.message.text, min_parts=2) if update.message else None
    if not query:
        await _send_text(update, context, "Usage: /ubos <query>")
        return

    # Simple fallback: keyword scan over repo docs
    # Prefer janus root if present; otherwise scan /srv/janus
    roots = [Path("/srv/janus")] if Path("/srv/janus").exists() else [state.paths.base_dir.parent]
    hits: list[tuple[Path, str]] = []
    for root in roots:
        hits = _scan_text_files(root, re.escape(query))
        if hits:
            break

    if not hits:
        await _send_text(update, context, "No UBOS documents matched your query (fallback scan).")
        return

    lines = ["UBOS retrieval (fallback scan):"]
    for i, (path, preview) in enumerate(hits[:5], start=1):
        lines.append(f"{i}. {path} \n   … {preview[:200]} …")
    await _send_text(update, context, "\n".join(lines))


# ------------------------------- message routing -------------------------------


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    text = (update.message.text or "").strip()
    if not text:
        return

    plan: DelegationPlan = plan_from_text(text)
    result = _execute_plan(plan, state)
    await _send_text(update, context, f"[{plan.target}] {result}")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    if not state.oai:
        await _send_text(update, context, "OpenAI resident unavailable (voice transcription requires OpenAI).")
        return
    audio = update.message.voice or update.message.audio
    if not audio:
        return
    file = await context.bot.get_file(audio.file_id)
    out_dir = state.paths.memory_dir / "telegram_voice"
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = ".oga"
    if getattr(audio, "mime_type", "").endswith("mpeg"):
        suffix = ".mp3"
    path = out_dir / f"voice_{int(time.time())}{suffix}"
    await file.download_to_drive(custom_path=str(path))
    transcript = await asyncio.to_thread(state.oai.transcribe_audio, path)
    await _send_text(update, context, f"[Voice transcription]\n{transcript}")
    if transcript.startswith("OpenAI transcription error"):
        return
    plan = plan_from_text(transcript)
    result = _execute_plan(plan, state)
    await _send_text(update, context, f"[{plan.target}] {result}")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state: BotState = context.application.bot_data.get("state")
    if not state.oai:
        await _send_text(update, context, "OpenAI resident unavailable (vision requires OpenAI).")
        return
    photos = update.message.photo or []
    if not photos:
        return
    photo = photos[-1]
    file = await context.bot.get_file(photo.file_id)
    out_dir = state.paths.memory_dir / "telegram_images"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"photo_{int(time.time())}.jpg"
    await file.download_to_drive(custom_path=str(path))
    prompt = update.message.caption or "Describe this image in the context of UBOS operations."
    analysis = await asyncio.to_thread(state.oai.analyze_image, path, prompt)
    await _send_text(update, context, f"[Image analysis]\n{analysis}")


async def _handle_override_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    resident: str,
    allow_model: bool = False,
) -> None:
    state: BotState = context.application.bot_data.get("state")
    text = (update.message.text or "").strip()
    parts = text.split(None, 1)
    if len(parts) < 2:
        await _send_text(update, context, f"Usage: /{resident} {'<model> ' if allow_model else ''}<prompt>")
        return
    remainder = parts[1].strip()
    model = None
    query = remainder
    if allow_model:
        tokens = remainder.split(None, 1)
        if len(tokens) == 2:
            model = tokens[0]
            query = tokens[1]
    if not model and resident == "claude":
        model = "claude-3-haiku-20240307"
    if not model and resident == "openai":
        model = "gpt-5"
    if not model and resident == "gemini":
        model = "gemini-2.5-pro"
    if not model and resident == "groq":
        model = "llama-3.3-70b-versatile"
    plan = DelegationPlan(mode="override", target=resident, query=query, model=model)
    result = _execute_plan(plan, state)
    await _send_text(update, context, f"[{resident}] {result}")


async def cmd_openai_override(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _handle_override_command(update, context, resident="openai", allow_model=True)


async def cmd_claude_override(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _handle_override_command(update, context, resident="claude", allow_model=True)


async def cmd_gemini_override(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _handle_override_command(update, context, resident="gemini", allow_model=True)


async def cmd_groq_override(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _handle_override_command(update, context, resident="groq", allow_model=True)


# ----------------------------------- main -------------------------------------


def build_application(state: BotState) -> Application:
    token = state.keys.telegram_token
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured (set in /etc/janus/trinity.env or .env.local)")

    app = ApplicationBuilder().token(token).build()
    app.bot_data["state"] = state

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("health", cmd_health))
    app.add_handler(CommandHandler("now", cmd_now))
    app.add_handler(CommandHandler("image", cmd_image))
    app.add_handler(CommandHandler("tts", cmd_tts))
    app.add_handler(CommandHandler("embed", cmd_embed))
    app.add_handler(CommandHandler("oai", cmd_oai))
    app.add_handler(CommandHandler("openai", cmd_openai_override))
    app.add_handler(CommandHandler("claude", cmd_claude_override))
    app.add_handler(CommandHandler("gemini", cmd_gemini_override))
    app.add_handler(CommandHandler("groq", cmd_groq_override))
    app.add_handler(CommandHandler("research", cmd_research))
    app.add_handler(CommandHandler("ubos", cmd_ubos))

    # Non-command messages → orchestrator
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return app


def main() -> None:
    _ensure_logging()
    state = _build_state()
    app = build_application(state)
    LOGGER.info("Starting Trinity Telegram bot…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
