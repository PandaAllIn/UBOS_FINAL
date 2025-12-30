# Steampunk Design Patterns for Balaur

This catalog translates classical steam/hydraulic/clockwork principles into
software controls for the Janus autonomous vessel.

## Governor (Maxwell, 1868) → Throughput Controller

Purpose: stabilize output under varying load.

Mapping:
- Setpoint: target queue backlog (default 0)
- Process variable: current queue length
- Controller: PI adjusting allowed concurrency
- Actuator: worker admission cap

Signals are logged as `governor.update` events.

## Boiler + Relief Valve → Safety Envelope

Purpose: avoid catastrophic failures by shedding load.

Mapping:
- Monitors: load average (1min), memory used
- Thresholds: `WatchdogConfig` cpu%/memory MB
- Levels: degrade (block network, cap concurrency=1), restore when safe
- Events: `relief.degrade` / `relief.restore`

## Manifold & Check Valves → Policy Routing

Purpose: enforce flow direction and permitted paths.

Mapping:
- UFW + domain allow-lists act as valves
- Sandbox network namespace as physical isolation (`--unshare-net`)
- Degraded mode forces valves closed (network blocked)

## Escapement → Tick Scheduler

Purpose: regularize motion and limit burstiness.

Mapping:
- Fixed `tick_interval` drives harness heartbeats (`tick` events)
- Workers admit tasks only when capacity allows

## Lubrication & Janitor → Maintenance Cadence

Purpose: keep the machine efficient and predictable.

Mapping:
- Timers for log rotation, workspace pruning, backups
- Health checks gate autonomy level increases

## Differential Analyzer → Decomposition

Purpose: compute by composition of primitives.

Mapping:
- Prefer small tool calls chained by the harness planner
- Each step auditable and reversible

