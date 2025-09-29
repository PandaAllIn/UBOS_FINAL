# UBOS Standard Agent Protocol (SAP) V2.0 — “The Brass Fitting”

Version: 2.0  
Status: Draft for implementation  
Scope: Normative object model and behaviors for inter‑agent tasking across all UBOS transports (in‑proc bus, HTTP, MCP, queues)

## 1. Purpose and Philosophy
SAP V2.0 standardizes how agents exchange intent and results under constitutional governance. It encodes:
- Constitutional alignment up front (context, constraints, objectives)
- Deterministic execution envelopes (ids, timestamps, schemas)
- Auditable outcomes with explicit constitutional evidence
- Hydraulic efficiency via caching and continuous learning

The protocol is transport‑agnostic. Transports adapt framing, not semantics.

## 2. Versioning and Compatibility
- Field `protocolVersion` MUST be "2.0" for SAP V2 messages.
- Producers MUST NOT emit breaking changes without bumping the version.
- Consumers SHOULD ignore unknown fields for forward compatibility.

## 3. Core Identifiers and Time
- All ids (`taskId`, `parentTaskId`, `correlationId`) MUST be RFC‑4122 UUID strings.
- All timestamps MUST be ISO‑8601 UTC in `YYYY-MM-DDTHH:MM:SSZ` format.

---

## 4. Objects

### 4.1 Task Object
Canonical envelope for a unit of work issued to an agent or capability.

Required fields are marked MUST; optional are SHOULD/MAY.

- `protocolVersion` (string, MUST): "2.0".
- `taskId` (string, MUST): UUID for this task.
- `parentTaskId` (string, MAY): UUID of parent task (for hierarchies).
- `correlationId` (string, MUST): UUID for cross‑message tracing.
- `issuedAt` (string, MUST): ISO UTC timestamp when issued.
- `issuer` (object, MUST): Who issues the task.
  - `agentId` (string, MUST): Logical id of the issuing agent or user.
  - `agentKind` (string, MUST): `"user" | "system" | "agent"`.
  - `name` (string, MAY): Friendly name.
- `target` (object, MUST): Where/how to execute.
  - `agentId` (string, SHOULD): Specific agent id (if direct addressing).
  - `capability` (string, MUST): Namespaced capability (e.g., `"consult.align"`).
  - `routingHints` (object, MAY): e.g., `priority`, `shard`, `affinity`.
- `constitutionalContext` (object, MUST): Alignment inputs.
  - `pressureLevel` (string, MUST): Hydraulic decision level `"instant" | "consulted" | "deliberated"`.
  - `principles` (array<string>, SHOULD): Symbolic principle keys.
  - `pressure` (object, SHOULD): Map principle -> number (PSI 0..100).
  - `objectives` (array<string>, SHOULD): Desired outcomes.
  - `constraints` (array<string>, SHOULD): Hard rules/guardrails.
  - `riskTolerance` (string, SHOULD): `"low" | "medium" | "high"`.
  - `territory` (string, SHOULD): Domain/space (e.g., `"EUFM"`).
  - `references` (array<string>, MAY): URIs/IDs for grounding.
  - `cachePolicy` (object, SHOULD): See §6.
    - `mode` (string): `"prefer" | "only" | "bypass"`.
    - `maxAgeSec` (integer, ≥0): Acceptable staleness.
    - `mustAlign` (boolean): Require alignment check on cache hit.
- `payload` (object, MUST): Capability‐specific inputs.
- `outputContract` (object, SHOULD): Declared output schema/spec.
  - `schema` (object): JSON Schema or contract descriptor.
  - `format` (string): e.g., `"json" | "markdown" | "text"`.
- `telemetry` (object, MAY): Execution controls.
  - `priority` (string): `"low" | "normal" | "high" | "urgent"`.
  - `deadline` (string): ISO UTC deadline.
  - `budget` (object): e.g., `{ "tokens": 5000, "seconds": 30 }`.
  - `trace` (boolean): Request deep tracing.
- `replyTo` (object, MAY): Transport return route or channel.
  - `endpoint` (string): URI or channel key.
  - `expectAck` (boolean): Default true; see §5.
- `attachments` (array<object>, MAY): External payload references.
  - `uri` (string), `kind` (string), `digest` (string)
- `tags` (array<string>, MAY): Freeform labeling.
- `meta` (object, MAY): Extensible metadata.

Example — Task
```json
{
  "protocolVersion": "2.0",
  "taskId": "7fbb32b6-0d2c-4c1a-9b75-2a4b3b0b6c0a",
  "parentTaskId": null,
  "correlationId": "a7f5d5b2-13a8-4a0d-9ba2-6b1e3c6f9d11",
  "issuedAt": "2025-09-28T10:15:23Z",
  "issuer": { "agentId": "A-prime", "agentKind": "agent", "name": "AI Prime" },
  "target": { "agentId": "A-ml-001", "capability": "consult.align" },
  "constitutionalContext": {
    "principles": ["systems_over_willpower", "blueprint_thinking", "strategic_pause"],
    "pressure": { "systems_over_willpower": 52, "blueprint_thinking": 41, "strategic_pause": 28 },
    "objectives": ["Outline SAP V2 spec"],
    "constraints": ["No PII", "Cite constitutional sources"],
    "riskTolerance": "low",
    "territory": "EUFM",
    "references": ["ubos://constitution/books"],
    "cachePolicy": { "mode": "prefer", "maxAgeSec": 86400, "mustAlign": true }
  },
  "payload": { "topic": "UBOS SAP V2", "depth": "detailed" },
  "outputContract": { "format": "json", "schema": {"type": "object"} },
  "telemetry": { "priority": "high", "deadline": "2025-09-28T11:00:00Z", "budget": {"tokens": 8000} },
  "replyTo": { "endpoint": "bus:inproc:prime", "expectAck": true },
  "tags": ["spec", "protocol"],
  "meta": { "clientVersion": "ubos/1.7.0" }
}
```

---

### 4.2 Result Object
Canonical outcome envelope for a processed Task.

- `protocolVersion` (string, MUST): "2.0".
- `taskId` (string, MUST): UUID matching the Task.
- `correlationId` (string, MUST): Propagated from the Task.
- `reportedAt` (string, MUST): ISO UTC when produced.
- `producer` (object, MUST): Who produced this result.
  - `agentId` (string, MUST)
  - `agentKind` (string, MUST): `"agent" | "system"`.
- `status` (string, MUST): One of `"QUEUED" | "RUNNING" | "SUCCEEDED" | "FAILED" | "CANCELLED" | "ESCALATED" | "PARTIAL"`.
- `output` (any, SHOULD): Data per `outputContract`.
- `artifacts` (array<object>, MAY): External outputs (URIs, digests).
- `metrics` (object, MAY): Resource use (e.g., tokens, latency, cost).
- `constitutionalEvidence` (object, MUST): Alignment proof (see below).
- `error` (object, MAY): On failure.
  - `code` (string), `message` (string), `details` (object)
- `nextActions` (array<object>, MAY): Proposed follow‑ups (task snippets).
- `meta` (object, MAY): Extensible metadata.

Constitutional Evidence (required)
- `alignment` (string, MUST): `"VALID" | "NON_CONSTITUTIONAL" | "ESCALATE"`.
- `pressureReadings` (object, SHOULD): Principle -> number used at decision time.
- `policyChecks` (array<object>, SHOULD): Per principle findings.
  - `principle` (string), `status` (string), `notes` (string)
- `violations` (array<object>, MAY): Any detected issues.
  - `principle` (string), `severity` (string), `evidence` (string)
- `citations` (array<string>, MAY): Sources/IDs grounding the output.
- `cache` (object, MAY): See §6 (`hit`, `cacheKey`, `ageSec`).

Example — Result
```json
{
  "protocolVersion": "2.0",
  "taskId": "7fbb32b6-0d2c-4c1a-9b75-2a4b3b0b6c0a",
  "correlationId": "a7f5d5b2-13a8-4a0d-9ba2-6b1e3c6f9d11",
  "reportedAt": "2025-09-28T10:29:12Z",
  "producer": { "agentId": "A-ml-001", "agentKind": "agent" },
  "status": "SUCCEEDED",
  "output": { "sections": ["Purpose", "Objects", "Learning"] },
  "artifacts": [{ "uri": "file://reports/UBOS_SAP_V2.spec.md", "kind": "md" }],
  "metrics": { "latencyMs": 842, "tokensIn": 2100, "tokensOut": 600 },
  "constitutionalEvidence": {
    "alignment": "VALID",
    "pressureReadings": { "systems_over_willpower": 52, "blueprint_thinking": 41, "strategic_pause": 28 },
    "policyChecks": [
      { "principle": "systems_over_willpower", "status": "PASS", "notes": "Protocolized behavior over ad‑hoc calls" },
      { "principle": "blueprint_thinking", "status": "PASS", "notes": "Clear object model and schemas" }
    ],
    "citations": ["ubos://constitution/books", "ubos://sap/v1"],
    "cache": { "hit": false }
  },
  "meta": { "versionHint": "sap/2.0" }
}
```

---

### 4.3 Ack/Nack (Transport‑level)
Transports MAY deliver synchronous acknowledgments separate from Result.
- `Ack`: Confirms the task envelope was accepted for processing.
- `Nack`: Rejects invalid or unroutable tasks early with a reason.
Ack/Nack carry `messageId`/`correlationId` at the transport layer; SAP V2 does not redefine their wire shape, only requires that Task→Result correlation remains intact.

---

## 5. Processing Semantics
- Producers MUST validate required fields before dispatch.
- Consumers MUST either emit an `Ack` (if transport supports it) or transition to a `Result` with `status` reflecting progress.
- `status` transitions SHOULD follow: `QUEUED → RUNNING → {SUCCEEDED|FAILED|ESCALATED|CANCELLED}`; `PARTIAL` indicates partial fulfillment with `nextActions`.
- `Result.taskId` MUST equal `Task.taskId`; `correlationId` MUST be preserved.
- `constitutionalEvidence.alignment` MUST be present in all Results.

---

## 6. ConstitutionalCache System
Purpose: hydraulic efficiency by reusing constitutionally vetted outcomes.

Cache Policy (Task `constitutionalContext.cachePolicy`)
- `mode`:
  - `prefer`: Use cache if valid and aligned; otherwise compute.
  - `only`: Use cache only; if miss/invalid, return `FAILED` with error `CACHE_MISS`.
  - `bypass`: Ignore cache.
- `maxAgeSec`: Accept entries younger than this age.
- `mustAlign`: On hit, re‑check alignment against Task context.

Cache Record Shape
- `cacheKey` (string): Deterministic hash over `{capability, payload essence, territory, principles, outputContract, sapVersion}`.
- `storedAt` (ISO UTC), `ageSec` (int), `producer` (string), `alignment` (string), `output` (any), `citations` (array), `fingerprint` (string for payload essence derivation).

Behavior
- On hit meeting policy, consumers SHOULD return a `Result` with the cached `output` and include `constitutionalEvidence.cache` = `{hit:true, cacheKey, ageSec}`.
- On miss or stale, compute fresh output, validate alignment, then write a new record.
- Cache entries MUST be immutable (WORM) and versioned by `sapVersion` to preserve auditability.

---

## 7. ConstitutionalLearningLoop
Purpose: continuous improvement of constitutional decision quality.

Signals
- From `Result` producers: `policyChecks`, `violations`, `metrics`, `nextActions`.
- From humans/operators: outcome rating, corrective notes, approvals.

Mechanics
- Aggregate signals keyed by `{capability, territory, fingerprint}`.
- Derive updated heuristics: improved payload essence extraction, refined `pressure` thresholds, enriched `policyChecks` catalogs.
- Emit new knowledge artifacts (e.g., playbooks, punch‑cards) into the Master Librarian for reuse.
- Learning MUST NOT retroactively alter prior cache records; it influences future cache writes and alignments only.

---

## 8. Error Model
- `error.code` SHOULD be one of: `INVALID_TASK`, `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `UNPROCESSABLE`, `TIMEOUT`, `RATE_LIMIT`, `INTERNAL`, `CACHE_MISS`, `NON_CONSTITUTIONAL`.
- `FAILED` Results MUST include `error.message`.
- `ESCALATED` Results SHOULD include `nextActions` with a recommended escalation path.

---

## 9. JSON Schemas (abridged)
These minimal shapes are informative. Implementations MAY publish full JSON Schema.

Task (informative)
```json
{
  "type": "object",
  "required": ["protocolVersion", "taskId", "correlationId", "issuedAt", "issuer", "target", "constitutionalContext", "payload"],
  "properties": {
    "protocolVersion": {"const": "2.0"},
    "taskId": {"type": "string", "format": "uuid"},
    "parentTaskId": {"type": ["string", "null"], "format": "uuid"},
    "correlationId": {"type": "string", "format": "uuid"},
    "issuedAt": {"type": "string", "format": "date-time"},
    "issuer": {"type": "object"},
    "target": {"type": "object"},
    "constitutionalContext": {"type": "object"},
    "payload": {"type": "object"}
  }
}
```

Result (informative)
```json
{
  "type": "object",
  "required": ["protocolVersion", "taskId", "correlationId", "reportedAt", "producer", "status", "constitutionalEvidence"],
  "properties": {
    "protocolVersion": {"const": "2.0"},
    "taskId": {"type": "string", "format": "uuid"},
    "correlationId": {"type": "string", "format": "uuid"},
    "reportedAt": {"type": "string", "format": "date-time"},
    "producer": {"type": "object"},
    "status": {"enum": ["QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "CANCELLED", "ESCALATED", "PARTIAL"]},
    "constitutionalEvidence": {"type": "object"}
  }
}
```

---

### ConstitutionalContext (informative)
```json
{
  "type": "object",
  "required": ["pressureLevel"],
  "properties": {
    "pressureLevel": {"enum": ["instant", "consulted", "deliberated"]},
    "principles": {"type": "array", "items": {"type": "string"}},
    "pressure": {"type": "object", "additionalProperties": {"type": "integer", "minimum": 0, "maximum": 100}},
    "objectives": {"type": "array", "items": {"type": "string"}},
    "constraints": {"type": "array", "items": {"type": "string"}},
    "riskTolerance": {"enum": ["low", "medium", "high"]},
    "territory": {"type": "string"},
    "references": {"type": "array", "items": {"type": "string"}},
    "cachePolicy": {
      "type": "object",
      "properties": {
        "mode": {"enum": ["prefer", "only", "bypass"]},
        "maxAgeSec": {"type": "integer", "minimum": 0},
        "mustAlign": {"type": "boolean"}
      }
    }
  }
}
```

---

## 10. Transport Guidance
- In‑process bus: envelope maps 1:1 to Python dataclasses; Ack/Nack as lightweight classes; transcript logging MUST persist Task and Result.
- HTTP: Task/Result map to JSON bodies; `correlationId` SHOULD propagate via headers (e.g., `X‑Correlation‑Id`).
- MCP/Queue: Preserve `taskId`/`correlationId`; Ack/Nack capability recommended for backpressure.

---

## 11. Security and Integrity
- Producers MUST avoid embedding secrets in `payload`; use `attachments` with secure URIs where required.
- Consumers SHOULD validate issuer authorization for the target capability.
- All stores (cache, transcripts) MUST be append‑only with tamper‑evident digests when feasible.

---

## 12. Conformance Checklist
- [ ] Valid ids and timestamps
- [ ] Required fields present
- [ ] Constitutional context provided
- [ ] Result includes constitutional evidence
- [ ] Cache policy honored
- [ ] Learning signals emitted
- [ ] Transport preserves correlation

---

Adopted wholesale from the Robust Protocol design cadence and extended with constitutional cache and learning primitives to embody the Hydraulic Heart.

*** End of SAP V2.0 ***
