# Trinity Orchestrator Quickstart

This guide explains how to interact with the Trinity Orchestrator, the central routing system for AI model interactions.

## Interaction Patterns

There are three primary ways to direct your requests to a specific model or service:

1.  **`/use` Overrides (Manual Selection):** For precise control, use the `/use` command to target a specific resident and model.
2.  **`@mentions` (Service Routing):** For specialized services like web searches or document retrieval, use `@mentions`.
3.  **Keyword Routing (Automatic Selection):** For general queries, the orchestrator automatically selects the best model based on keywords in your prompt.

---

## 1. `/use` Overrides

The `/use` command gives you direct control over which AI resident and model processes your request. This is useful for testing, comparing models, or when you know exactly which tool you need.

**Syntax:** `/use <resident>:<model_id>`

### Examples

-   **Target a specific OpenAI model:**
    ```
    /use openai:gpt-5-mini What are the key principles of the Lion's Sanctuary?
    ```

-   **Use a high-speed Groq model for quick answers:**
    ```
    /use groq:llama-3.1-8b-instant Summarize the latest STATE_OF_THE_REPUBLIC.md in three bullet points.
    ```

-   **Engage Gemini for a systems engineering task:**
    ```
    /use gemini:gemini-2.5-pro Design a high-level architecture for the Living Scroll MCP.
    ```

---

## 2. `@mentions`

`@mentions` are used to invoke specialized services that are not standard chat models. This is the preferred way to access tools for web searches, database queries, and other integrated services.

**Syntax:** `@<service_name> <query>`

### Examples

-   **Perform a web search with Perplexity:**
    ```
    @perplexity What is the current status of the Falcon 9 launch?
    ```

-   **Query the UBOS document index:**
    ```
    @retriever Find documents related to the "Steampunk Doctrine".
    ```

-   **Access a custom tool via MCP:**
    ```
    @custom_tool --arg1 value1 Run diagnostics on the janus-agent service.
    ```

---

## 3. Keyword Routing

If you don't specify a resident or service, the orchestrator analyzes your prompt for keywords and routes it to the most appropriate default model. This is the most common way to interact with the system for general tasks.

### How it Works

The orchestrator maintains a routing table that maps keywords and phrases to specific AI tasks and models.

-   **"plan", "strategy", "roadmap"** → Routes to a strategic model like `openai:gpt-5`.
-   **"code", "refactor", "bug"** → Routes to a coding model like `openai:gpt-5-codex`.
-   **"fast", "quick", "summarize"** → Routes to a high-speed model like `groq:llama-3.1-8b-instant`.
-   **"image", "diagram", "see"** → Routes to a vision-capable model like `openai:gpt-5`.

### Examples

-   **Plain text query for general chat:**
    ```
    What's the difference between the Mill and the Studio in the Balaur architecture?
    ```
    *(This would likely be routed to a general-purpose chat model.)*

-   **A query implying a need for speed:**
    ```
    Quickly, what are the three main components of the Autonomous Vessel Protocol?
    ```
    *(This would likely be routed to a Groq model.)*

-   **A request for code:**
    ```
    Write a python script to parse the trinity_events.jsonl file.
    ```
    *(This would be routed to a specialized coding model.)*

---

This combination of explicit commands, service mentions, and intelligent routing provides a flexible and powerful interface for interacting with the full suite of UBOS AI capabilities.