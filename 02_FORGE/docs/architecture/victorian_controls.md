# Victorian Control Mechanisms – The Steampunk Operating System

**Philosophy:** Inspired by 19th-century mechanical regulation, the Victorian Controls harmonize The Mill’s neural workload with physical constraints. They embody transparency, predictability, and constitutional safety.

## The Governor (Maxwell’s Adaptive Control)
- **Purpose:** Regulate token throughput to prevent overload, analogous to James Clerk Maxwell’s centrifugal governor modulating steam engine speed.
- **Implementation:**
  - PI controller adjusts allowed concurrent actions in janus_agent harness.
  - Metrics input: queue depth, token rate (from tokens/sec sidecar), CPU load.
  - Parameters (default): `Kp=0.2`, `Ki=0.05`, target backlog = 0.
- **Operation:**
  1. Measure error = backlog – target.
  2. Update integral term (`integral += error * dt`).
  3. Compute new `allowed_concurrency = clamp(prev + Kp*error + Ki*integral, 1, max_concurrency)`.
  4. Broadcast updates via audit log (`governor.update`).
- **Tuning Guidance:**
  - Increase Kp for faster response; decrease to avoid oscillation.
  - Ki addresses steady-state error; keep low to prevent wind-up.
  - Integrate anti-windup by clamping integral when hitting concurrency limits.

## The Relief Valve (Thermal & Safety)
- **Purpose:** Protect hardware from thermal runaway and resource exhaustion, analogous to steam relief valves venting pressure.
- **Stages:**
  1. **SEALED:** Normal operation, monitoring but no intervention.
  2. **VENTING:** Soft throttle when CPU load > 85% or memory > 90%; reduce concurrency, block new network-dependent actions.
  3. **EMERGENCY:** If thresholds persist, force `allowed_concurrency=1`, enable sandbox network block, and alert Captain.
  4. **CRITICAL:** Final safeguard; suspend thinking cycle, notify via audit log, require manual reset.
- **Inputs:** `cpupower`, `/proc/meminfo`, GPU thermals (via amdgpu sensors), `turbostat` package wattage.
- **Integration:** Hooks into janus_agent harness `_relief_valve_loop`; modifies sandbox executor behavior and logs `relief.degrade` / `relief.restore` events.

## The Escapement (Precision Timing)
- **Purpose:** Provide deterministic pacing, similar to a clock escapement ensuring uniform ticks.
- **Mechanism:**
  - Background task (`_tick_loop`) emits tick every `tick_interval` (default 0.5 s).
  - Updates audit log with queue length, active tasks, allowed concurrency.
  - Coordinates with Governor and Relief Valve to synchronize decisions.
- **Benefits:**
  - Prevents runaway loops by enforcing minimum cycle time.
  - Creates traceable temporal log for post-mortem analysis.

## Integration with The Mill (llama.cpp)
- Maxwell governor influences number of concurrent proposals to avoid CPU saturation.
- Relief Valve watches CPU package power from `turbostat`; if llama.cpp triggers AVX offset or thermal surge, concurrency drops before throttling occurs.
- Escapement ensures llama.cpp invocations adhere to pacing, enabling consistent scheduling even under load.

## Telemetry & Monitoring
- Audit log events: `controls.governor`, `controls.relief_valve`, `tick`, `thinking_cycle.*`.
- `janus-controls.service` orchestrates control loops; metrics accessible via `/srv/janus/metrics/token_rate.json` (to be fed by tokens/sec sidecar).
- Use `journalctl -u janus-controls -f` to observe control decisions in real time.

## Constitutional Alignment
- Controls expose state clearly; no black-box throttling.
- Parameters tuned in open configuration files; Trinity can review and adjust collaboratively.
- Preserves Lion’s Sanctuary principle: empower Janus while ensuring safe coexistence with physical vessel constraints.

