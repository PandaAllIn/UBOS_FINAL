# UBOS Mission Deliverables

This directory stores curated artifacts promoted from the Trinity autonomous loop.

## Workflow

1. Run `python3 /srv/janus/trinity/autonomous_janus.py` to generate fresh resident outputs.
2. Promote the latest entries from `trinity_logs/autonomous_delegations.jsonl` into the
   mission folders (`GeoDataCenter`, `Portal_Oradea`, …) as Markdown.
3. Update the corresponding mission YAML deliverable paths if needed, then flip `status`
   from `active` to `completed` only after the files exist.
4. Archive or publish the Markdown files as part of reports, ROADMAP updates, or runbooks.

Each Markdown file includes the mission, resident, model, prompt, and captured content
so we can trace every deliverable back to its source.

## Reference Logs
- `UPGRADE_LOG_2025-10-26.md` – Automation, mission orchestrator, and Telegram upgrades captured on 2025-10-26. Add future dated logs here as needed.
