# Control Theory Primer (For Victorian Controls)

## PID (PI) Control Refresher
- Error e(t) = setpoint − measurement. PI output u(t) = Kp·e + Ki·∫e dt.
- Kp: responsiveness; Ki: steady‑state error removal; Kd: overshoot damping (not used currently).

## Tokens‑per‑Second Governor
- Measurement: tokens/sec from llama sidecar; setpoint chosen for stability vs throughput.
- Actuator: allowed_concurrency in harness.
- Anti‑windup: clamp integral term when at concurrency limits.

## Safety Interlocks
- Relief Valve overrides governor if CPU watts/temps exceed thresholds.
- Escapement sets minimum cycle time to prevent aliasing and runaway loops.

Sources: Åström & Murray, Maxwell “On Governors” (1868).
