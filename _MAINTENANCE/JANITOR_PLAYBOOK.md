---
type: maintenance
category: janitor
created: 2025-11-20
tags: [maintenance, janitor, cleanup]
---

# 🧹 Janitor Schedule

| Task | Frequency | Command | Output |
| --- | --- | --- | --- |
| Orphan/unused files | Weekly (Mon 08:00) | `Janitor: Scan vault` → Enable Orphans | `_MAINTENANCE/orphans.md` |
| Empty notes | Weekly (Mon 08:00) | Same scan (Empty enabled) | `_MAINTENANCE/empty_notes.md` |
| Broken links | Daily (20:00) | After Janitor scan run [[OBSERVATORY_INDEX#Link QA]] checklist | `_MAINTENANCE/broken_links.md` |
| Unused attachments | Monthly (1st 09:00) | Janitor with “Big files” filter | `_MAINTENANCE/attachments.md` |
| Expired notes | Weekly | Janitor “Expired attribute” check | `_MAINTENANCE/expired_notes.md` |

**How to run:**
1. Command palette → `Janitor: Scan vault`.
2. Choose operation `Send to Obsidian trash` (default) and confirm prompt.
3. Copy summary into the appropriate report above (append timestamp + action).

_Janitor respects `.trash`, `_MAINTENANCE`, and `99_ARCHIVES` so production records stay safe._
