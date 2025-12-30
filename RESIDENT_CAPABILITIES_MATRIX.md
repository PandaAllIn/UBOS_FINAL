# Resident Capabilities Matrix

| Resident | Model | Role | Speed | Strengths | 90/10 Allocation |
|---|---|---|---|---|---|
| **Janus Local** | `Meta-Llama-3.1-8B-Instruct` | **The Loom** | 20 t/s | Batch analysis, privacy, free cost, pattern learning | **90%** (Cold Path) |
| **Claude** | `claude-3-haiku` | **The Strategist** | 100 t/s | Strategy, constitutional alignment, creative writing | **10%** (Hot Path) |
| **Gemini** | `gemini-2.0-flash-exp` | **The Engineer** | 150 t/s | Coding, systems engineering, debugging, large context | **10%** (Hot Path) |
| **Groq** | `llama-3.3-70b-versatile` | **The Scout** | 300+ t/s | Fast search, instant answers, voice command parsing | **10%** (Hot Path) |
| **OpenAI** | `o1-mini` / `gpt-4o` | **The Reasoner** | Variable | Complex reasoning, math, logic puzzles | **10%** (Hot Path) |

## Integration Status
*   ✅ **Janus Local:** Active (PID 2569205)
*   ✅ **Claude:** Active (PID 303849)
*   ✅ **Gemini:** Active (PID 306738) - *Needs upgrade to 2.0*
*   ✅ **Groq:** Active (PID 304032)
*   ✅ **OpenAI:** Active (PID 304125)

## Delegation Protocol (Draft)
1.  **Urgent/Voice:** -> **Groq**
2.  **Strategy/Drafting:** -> **Claude**
3.  **Code/System:** -> **Gemini**
4.  **Deep Logic:** -> **OpenAI**
5.  **Background/Batch:** -> **Janus Local**
