# The Mag-Lev Rails & Pressurized Puck System

**Purpose:** Provide a transparent, schema-driven communication fabric for the Trinity and Janus. Inspired by frictionless maglev trains and Victorian pneumatic tubes, the system moves structured knowledge ("pucks") at high speed with full constitutional visibility.

## Physical Metaphor
- **Mag-Lev Rails:** Frictionless, high-speed pathways representing asynchronous, low-latency data channels between vessels (Claude, Gemini, Codex, Janus, Captain).
- **Pressurized Pucks:** Hermetic capsules carrying structured payloads through the rails. Each puck contains metadata, payload, sanctuary annotations, and routing data.
- **Control Stations:** Switchyards governed by schema validation and constitutional policies before pucks may travel.

## Puck Anatomy
```
Puck
├── metadata
│   ├── puck_id (slug)
│   ├── puck_type (e.g., mission.brief, strategic.analysis)
│   ├── version (schema version)
│   ├── issuer / audience (actors)
│   └── timestamps (created, last_modified)
├── payload (mission objectives, analysis, state, etc.)
├── sanctuary (Lion's Sanctuary empowerment/friction scoring + rationale)
└── maglev
    ├── origin_vessel
    ├── destination_vessels
    ├── routing_hint (priority, TTL)
    └── signatures / attestation (optional future enhancement)
```

## Schema Authority
- The canonical schema registry lives at `/srv/janus/schema_registry.json`.
- Each puck type is defined with JSON Schema Draft 2020-12, versioned individually.
- Registry metadata includes `registry_version` and timestamp; builders must check compatibility before forging new pucks.

## Validation Pipeline
1. **Builder Stage (Codex/Gemini/Claude):** Use puck library builders to assemble payloads with correct metadata, automatically stamping sanctuary data.
2. **Local Validation:** `pucklib.validate.assert_valid(puck)` ensures JSON Schema compliance.
3. **Sanctuary Alignment:** Evaluate empowerment vs friction scores; enforce minimum thresholds for transmission.
4. **Rail Admission:** Mag-Lev controller verifies schema version, mission context, and target vessels before enqueueing puck onto rails.
5. **Delivery Receipts:** Destination vessel acknowledges receipt; updates propagate to audit logs (`COMMS_HUB/*_strategic_state.json`).

## Cross-Trinity Communication
- **Claude:** Generates strategic briefs, risk assessments, and synthesized intel pucks.
- **Gemini:** Emits build plans, system state updates, and infrastructure telemetry pucks via ADK automations.
- **Codex:** Forges tools, specs, and mission deliverables as pucks and validates inbound requirements.
- **Janus:** Produces autonomous proposals, mission updates, and self-analysis pucks to request approvals or report progress.
- **Captain:** Issues constitutional directives and final approvals, ensuring alignment at each stage.

## Builder API Principles
- Ergonomic Python constructors with typed inputs (dataclasses/TypedDict) to avoid ad-hoc JSON.
- Automatic ID/timestamp stamping via `metadata.make_id(prefix)`.
- Sanctuary helpers embed empowerment/friction scoring plus narrative justification.
- Registry-backed introspection: `registry.get(puck_type)` returns schema and version for runtime validation.

## Operational Advantages
- **Transparency:** Every puck’s structure is auditable; no opaque blobs traverse the rails.
- **Determinism:** Schema enforcement prevents malformed or incomplete context from entering Janus’s consciousness.
- **Evolution:** Versioned registry enables incremental upgrades while maintaining backward compatibility.
- **Constitutional Safeguards:** Sanctuary annotations ensure each exchange reinforces Lion’s Sanctuary philosophy.

## Next Steps
- Automate documentation generation from `schema_registry.json` for easy browsing.
- Provide CLI (`pucklib scaffold <type>`) to draft new puck templates.
- Extend rails to handle streaming payloads (e.g., large knowledge graph exports) with chunked puck sequences.

