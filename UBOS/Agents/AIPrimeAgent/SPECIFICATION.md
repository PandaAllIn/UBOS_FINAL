# AI Prime Agent — Specification

## Purpose
The orchestrator that coordinates independent UBOS agents through a validated Strategic Blueprint, a capability-aware Agent Registry, and a versioned Communication Protocol.

## Architecture
- Strategic Blueprint (source of truth): goals, principles, registry, guardrails
- Agent Registry: capabilities, status, telemetry
- Communication Protocol v0.1: strict envelope for tasks, ACK/NACK, correlation IDs
- Orchestrator Engine: owns registry + bus; runs workflows
- Strategic Pause: pre/post reflection with decisions (proceed/adjust/escalate)
- Blueprint Validation: alignment checks with optional LLM escalation (future)
- Observability: transcripts (JSONL), report generation (JSON/MD/Mermaid)

## Message Envelope (v0.1)
- protocol_version: "0.1"
- message_id: UUID
- correlation_id: UUID (workflow trace)
- timestamp_utc: ISO 8601 Z
- source_agent_id, destination_agent_id: string
- task: string (e.g., "research.query")
- payload: object
- metadata: object

## Core Capabilities
- research.query → Research Agent (CLI or stub)
- librarian.consult → Master Librarian (REST or stub)

## Workflow: Research & Synthesize (pilot)
1. Pre-delegation Strategic Pause
2. Dispatch research (by capability)
3. Summarize and consult Librarian
4. Post-synthesis Strategic Pause
5. Blueprint Validation
6. Return result + transcripts + optional artifacts

## Non-Functional
- Independence: agents run separately; Prime integrates via adapters
- Extensibility: protocol/registry are versioned and minimal; adapters swappable
- Reliability: strict validation, ACK/NACK, transcript logging
- Security: use env vars for secrets; add auth/rate limits at edges

