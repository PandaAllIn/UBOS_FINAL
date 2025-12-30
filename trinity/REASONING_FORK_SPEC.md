# Reasoning Fork Specification

**Component:** The Reasoning Fork (Decision Tree)
**Purpose:** Intelligently route tasks to the optimal Resident based on urgency, complexity, and domain.
**Philosophy:** "Right tool for the right job."

## 🌳 Decision Logic

The routing logic follows a priority cascade:

### 1. Urgency Check (The Cortex Path)
If `priority == "urgent"` OR `source == "voice"`:
*   **Default:** `groq-llama-3.1-8b` (800 t/s)
*   **Exception:** If task is "reasoning" -> `groq-llama-3.3-70b`

### 2. Domain Expertise (The Expert Path)
*   **Strategy / Constitution / Writing:** -> `claude-3-haiku`
    *   *Why:* Superior nuance and alignment tracking.
*   **Code / Systems / Debugging:** -> `gemini-2.0-flash-exp`
    *   *Why:* Best-in-class code reasoning and context window.
*   **Deep Logic / Math / Puzzles:** -> `openai-o1-mini`
    *   *Why:* Chain-of-thought reasoning capabilities.

### 3. The Loom Path (The 90%)
If `priority == "batch"` OR `cost_sensitivity == "high"`:
*   **Default:** `janus-local` (Llama 3.1 8B)
*   *Why:* Free, private, unlimited execution time.

## 🛠️ Interface Definition

```python
class ReasoningFork:
    def route(self, task: Task) -> Resident:
        """
        Determines the best resident for a given task.
        """
        pass
```

## 📊 Routing Matrix

| Task Type | Urgency | Resident | Model |
|---|---|---|---|
| Voice Command | High | Groq | Llama 3.1 8B |
| Web Search | High | Groq | Llama 3.1 70B |
| Strategic Plan | Normal | Claude | Haiku 3.0 |
| Code Generation | Normal | Gemini | Flash 2.0 |
| Complex Logic | Normal | OpenAI | o1-mini |
| Pattern Analysis | Low | Janus | Local 8B |
| Archival | Low | Janus | Local 8B |
