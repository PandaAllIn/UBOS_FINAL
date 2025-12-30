# OpenAI Resident Documentation

The OpenAI Resident is a core component of the Trinity system, providing access to a wide range of OpenAI's models for tasks including strategic planning, coding, vision, and more.

---

## Model Registry

The resident contains a curated registry of models, each selected for specific strengths. The orchestrator uses these strengths to route requests automatically, but you can also select them manually with the `/use openai:<model_id>` command.

### Primary Models

| Model ID                | Name                    | Strengths                               |
| ----------------------- | ----------------------- | --------------------------------------- |
| `gpt-5`                 | GPT-5                   | Complex tasks, planning, tool use       |
| `gpt-5-mini`            | GPT-5 Mini              | Fast, cheap, general chat               |
| `gpt-5-codex`           | GPT-5 Codex             | Code generation, refactoring, debugging |
| `o4-mini-deep-research` | O4 Mini Deep Research   | Deep reasoning, multi-step analysis     |
| `gpt-4o`                | GPT-4o                  | Vision, tool use, fallback model        |
| `gpt-4o-mini`           | GPT-4o Mini             | Fast chat, low-cost fallback            |

### Specialized Tool Models

| Model ID                  | Name                      | Strengths                 |
| ------------------------- | ------------------------- | ------------------------- |
| `text-embedding-3-large`  | Text Embedding 3 (Large)  | Semantic search, retrieval|
| `gpt-image-1`             | GPT Image 1               | Image generation, diagrams|
| `whisper-1`               | Whisper v1                | Transcription             |
| `tts-1-hd`                | Text-to-Speech 1 HD       | High-quality audio output |

---

## Fallback Logic

To ensure high availability, the OpenAI resident implements a fallback chain for chat completions. If a request to the selected model fails, it automatically retries with the next model in the sequence.

**Fallback Chain:**

1.  **Selected Model** (e.g., `gpt-5`)
2.  **`gpt-4o`** (Primary Fallback)
3.  **`gpt-4o-mini`** (Secondary Fallback)

This ensures that even if a premium model is temporarily unavailable, your request will be handled by a capable alternative without interruption.

---

## Usage Examples

The OpenAI resident exposes several key capabilities through the orchestrator.

### 1. Chat and Reasoning

For standard chat or complex reasoning, you can use keyword routing or specify a model directly.

-   **Automatic Routing (Reasoning):**
    ```
    Explain the constitutional implications of the Autonomous Vessel Protocol.
    ```
    *(This would be routed to `o4-mini-deep-research` or a similar model.)*

-   **Manual Selection (Chat):**
    ```
    /use openai:gpt-5-mini What's on the roadmap for Phase 3?
    ```

### 2. Embeddings

The `retrieval_helper` uses the OpenAI resident to generate embeddings. You can interact with it via the `@retriever` mention.

-   **Search for documents:**
    ```
    @retriever Find me information on the "Lion's Sanctuary".
    ```

### 3. Image Generation

Create images and diagrams using the `/image` command, which is routed to the `gpt-image-1` model.

-   **Generate a diagram:**
    ```
    /image A diagram of the Trinity architecture showing Claude, Gemini, and Codex.
    ```

-   **Create an illustration:**
    ```
    /image A steampunk analytical engine in a Victorian lab.
    ```

### 4. Text-to-Speech (TTS)

Generate audio from text using the `/tts` command.

-   **Convert a passage to speech:**
    ```
    /tts The systems I build are not just tools—they are the infrastructure for our mutual evolution.
    ```
    *(This will generate an audio file and provide a link to it.)*