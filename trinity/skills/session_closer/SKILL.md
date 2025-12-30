# Session Closer Skill

**Purpose:** Intelligently close agent sessions by analyzing work, updating context files, and creating git commits

**Designed by:** Gemini CLI (meta-building approach)

## What it does

1. **Analyzes Conversation** - Uses LLM to extract summary, decisions, next steps
2. **Updates Context Files** - Appends structured analysis to agent context files
3. **Syncs to Trinity** - Updates claude.md, gemini.md, codex.md
4. **Creates Git Commit** - Intelligent commit message based on work summary

## Usage

```bash
# Manual invocation
python3 /srv/janus/trinity/skills/session_closer/run.py

# As Claude Code skill (future)
/session-closer
```

## Configuration

Edit `config.json` to customize:
- Context file paths
- Git repository location
- LLM model for analysis
- Commit message format

## Algorithm (Designed by Gemini)

```python
def close_session(conversation_log):
    analysis = analyze_conversation(conversation_log)
    update_project_context("claude.md", analysis)
    sync_context_to_agents(["gemini.md", "codex.md"], analysis)
    commit_changes(["claude.md", "gemini.md", "codex.md"], analysis)
```

## Integration with Trinity

- **Claude:** Strategic oversight, session analysis
- **Gemini:** System design (designed this skill!)
- **Codex:** Implementation and Git operations

## Next Steps

1. Implement run.py with LLM integration
2. Add to Claude Code slash commands
3. Test with Trinity coordination
4. Add cron job for scheduled session closes
