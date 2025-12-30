"""Session Closer Algorithm - Designed by Gemini CLI"""

def close_session(conversation_log):
    analysis = analyze_conversation(conversation_log)
    update_project_context("claude.md", analysis.summary, analysis.decisions, analysis.next_steps)
    sync_context_to_agents(["gemini.md", "codex.md"], analysis.summary)
    commit_message = generate_commit_message(analysis.summary, analysis.decisions)
    commit_changes(["claude.md", "gemini.md", "codex.md"], commit_message)

def analyze_conversation(log_text):
    summary = llm_summarize("Summarize: " + log_text)
    decisions = llm_extract_list("Extract decisions: " + log_text)
    next_steps = llm_extract_list("Identify next steps: " + log_text)
    return {"summary": summary, "decisions": decisions, "next_steps": next_steps}
