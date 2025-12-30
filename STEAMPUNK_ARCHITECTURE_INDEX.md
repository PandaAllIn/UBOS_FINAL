# Steampunk Architecture Index

**Source of Truth:** `/srv/janus/99_ARCHIVES/sessions/THE_BALAUR_ARCHIVES/UNIFIED_STEAMPUNK_ARCHITECTURE.md`
**Design Patterns:** `/srv/janus/99_ARCHIVES/sessions/THE_BALAUR_ARCHIVES/STEAMPUNK_DESIGN_PATTERNS.md`

## 🏗️ Component Inventory

| Component | Steampunk Name | Modern Role | Status | File Location |
|---|---|---|---|---|
| **CPU** | The Mill | Compute Engine | ✅ Active | Hardware |
| **GPU** | Auxiliary Steam Cylinder | Accelerator | ✅ Active | Hardware |
| **Memory** | The Store | RAM / Cache | ✅ Active | Hardware |
| **Control** | Maxwell Governor | Rate Limiter | ✅ Active | `janus-controls.service` |
| **Safety** | Relief Valve | Load Shedder | ✅ Active | `janus-controls.service` |
| **Timing** | Escapement | Tick Regulator | ✅ Active | `janus-controls.service` |
| **Routing** | **Reasoning Fork** | Decision Tree | 🚧 **Missing** | *To be built* |
| **Queueing** | **Mechanical Bouncer** | Load Balancer | 🚧 **Missing** | *To be built* |
| **Storage** | The Loom / Brass Cards | Vector DB / Patterns | 🚧 **Partial** | `pathfinder/mechanical_loom.py` |
| **Agents** | The Cortex | LLM Residents | ✅ Active | `resident_mission_executor.py` |
| **Bus** | Aetheric Maglev | Message Bus | 🚧 **Missing** | *To be built* |

## 🔗 Reference Links
*   **Concept:** "Build the habitat so perfect that there's no reason to leave."
*   **90/10 Rule:** 90% Loom (Batch/Cold), 10% Cortex (Real-time/Hot).
