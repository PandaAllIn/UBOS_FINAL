# Mechanical Bouncer Specification

**Component:** The Mechanical Bouncer (Load Balancer)
**Purpose:** Protect Resident APIs from rate-limit exhaustion and manage traffic flow.
**Philosophy:** "Order amidst chaos."

## 🛡️ Protection Mechanisms

### 1. Rate Limited Queues
Each resident has a dedicated queue with strict emission limits matching their API tier.

| Resident | Rate Limit (RPM) | Burst (RPM) | Daily Limit (TPD) |
|---|---|---|---|
| **Groq** | 30 | 50 | 14,400 |
| **Gemini** | 15 | 20 | 1,000,000 (TPM) |
| **Claude** | 50 | 60 | Unlimited (Paid) |
| **OpenAI** | 500 | 600 | Unlimited (Paid) |
| **Janus** | ∞ | ∞ | ∞ |

### 2. Circuit Breakers
If a resident fails (500/503 errors) > 3 times in 1 minute:
1.  **Trip:** Stop sending requests to that resident.
2.  **Cooldown:** Wait 60 seconds.
3.  **Probe:** Send 1 test request.
4.  **Reset:** If successful, resume normal flow.

### 3. Failover Routing
If a resident's queue is full or circuit is open:
*   Groq -> Failover to Gemini Flash
*   Claude -> Failover to OpenAI GPT-4o-mini
*   Gemini -> Failover to Claude Haiku
*   OpenAI -> Failover to Claude Haiku

## 🛠️ Interface Definition

```python
class MechanicalBouncer:
    def submit(self, task, target_resident):
        """
        Enqueues task. Returns future/promise.
        Raises RateLimitExceeded if queue full.
        """
        pass
```
