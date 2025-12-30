# Agent Exports

Lightweight JSON exports for agents that need quick access to the book contents:

- `summary.json` — chapter metadata plus the global topic index.
- `ideas_quick.json` — flattened list of idea records.
- `practices_quick.json` — flattened list of practice records.
- `quotes_quick.json` — flattened list of quotes.

Regenerate these files with `tools/export_for_agents.py`.
