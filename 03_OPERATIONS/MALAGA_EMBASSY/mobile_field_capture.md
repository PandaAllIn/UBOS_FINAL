---
type: runbook
category: field_capture
created: 2025-11-20
tags: [mobile, malaga, workflow]
---

# 📟 Mobile Field Capture Strategy

**Tooling:** Obsidian Mobile + QuickAdd + Templater (8-plugin baseline). Telegram sync intentionally skipped to avoid plugin bloat + EU roaming surprises.

## Capture Flow
1. Unlock iPad ➜ open Obsidian vault (ensure sync complete).
2. Run QuickAdd → `Captain's Log` (voice dictation friendly).
3. Template `_TEMPLATES/automation/captain_log.md` auto stamps metadata + tags.
4. Notes land in `03_OPERATIONS/MALAGA_EMBASSY/field_insights/` with timestamped filenames.
5. When online, Janus runs enrichment described in [[_SCRIPTS/enrich_field_notes|Field Note Enrichment]] to link missions/partners.

## Why Mobile App > Telegram
- Works offline + syncs once back online.
- Keeps notes inside constitutional vault (no extra data processors).
- Avoids Telegram rate limits + plugin overhead.
- Rich metadata + templates > plaintext chat dumps.

## Usage Tips
- Pin Obsidian to iPad dock for two-tap launch.
- Use iOS dictation for `notes` prompt; handwriting also works.
- Tag urgent captures `priority: critical` so dashboards highlight them.
- If capturing photos/audio, attach via Files → store under `03_OPERATIONS/MALAGA_EMBASSY/field_insights/assets/` and link in the note.

## Sync Guidance
- Preferred: iCloud/Obsidian Sync with periodic background refresh.
- Manual fallback: AirDrop zipped note if offline >24 h and urgent.
- Always run `obsidian-git` sync on desktop before/after long field days.

_Mobile-first capture keeps Málaga intel constitutional, encrypted, and queryable in under 10 seconds._
