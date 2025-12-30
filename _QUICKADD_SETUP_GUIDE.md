---
type: runbook
category: quickadd
created: 2025-11-20
tags: [quickadd, workflow, captain]
---

# ⚡ QuickAdd Setup (Captain)

**Goal:** Configure 5 macros + hotkeys in 10 minutes. Run from **Settings → Community Plugins → QuickAdd**.

## Macro 1 – Captain's Log (`Cmd/Ctrl + Shift + L`)
1. Manage Macros → `Add Macro` → name `Captain's Log`.
2. Add Choice → `Capture`.
3. Template: `_TEMPLATES/automation/captain_log.md`.
4. Capture to file → `03_OPERATIONS/MALAGA_EMBASSY/field_insights/`.
5. Filename: `{{DATE:YYYY-MM-DD}}-{{VALUE:title}}`.
6. Prompts (QuickAdd fields):
   - `title` – short label (<4 words).
   - `location` – default `Málaga, ES`.
   - `notes` – dictation-friendly text area.
   - `priority` – suggester [critical, high, medium, low].
7. Disable "Open file after creation" for fastest capture.
8. Assign hotkey `Cmd/Ctrl + Shift + L`.

## Macro 2 – New Mission (`Cmd/Ctrl + Shift + M`)
- Template: `_TEMPLATES/operations/mission_creation.md`.
- Folder: `03_OPERATIONS/missions/`.
- Filename: `{{DATE:YYYY-MM-DD}}-{{VALUE:mission_name}}`.
- Turn on "Open file" to refine details immediately.

## Macro 3 – Constitutional Decision (`Cmd/Ctrl + Shift + D`)
- Template: `_TEMPLATES/strategy/constitutional_decision.md`.
- Folder: `03_OPERATIONS/decisions/`.
- Filename: `{{DATE:YYYYMMDDHHmm}}-decision`.
- Keep `Open file` enabled for Trinity review.

## Macro 4 – Partner Profile (`Cmd/Ctrl + Shift + P`)
- Template: `_TEMPLATES/strategy/partner_contact.md`.
- Folder: `03_OPERATIONS/MALAGA_EMBASSY/partners/`.
- Filename: `{{VALUE:name}}`.
- Prompt fields: `name`, `category`, `relationship_strength`.

## Macro 5 – Pattern Documentation (`Cmd/Ctrl + Shift + T`)
- Template: `_TEMPLATES/knowledge/pattern_documentation.md`.
- Folder: `CONCEPTS/patterns/`.
- Filename: `{{DATE:YYYY-MM-DD}}-{{VALUE:pattern_name}}`.
- Prompts: `pattern_name`, `signal_source`, `impact`.

### Verification Steps
1. Use command palette to run each macro once.
2. Confirm files land in correct folders/follow naming rules.
3. Delete test files when satisfied.
4. Sync mobile (iPad) and repeat `Cmd+Shift+L` test.

_Macros remain UI-managed per Captain's request; this guide keeps reconfiguration trivial._
