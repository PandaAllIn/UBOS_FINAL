# UBOS Repeatability Implementation Protocol (RIP) Specification V1

**Author:** Gemini, Systems Engineer
**Date:** 2025-10-26
**Status:** Draft

## 1. Overview

The Repeatability Implementation Protocol (RIP) is a system-wide service designed to ensure that all UBOS daemons and modules operate with resilience, autonomy, and effortless continuity. It is the implementation of the philosophical directive: "Simplicity breathes endlessly when systems renew themselves."

## 2. Core Components

### 2.1. Automation Service (`automation_service.py`)

- **Location:** `/srv/janus/balaur/projects/05_software/repeatability/automation_service.py`
- **Function:** This service is the heart of RIP. It is responsible for:
    - **Auto-launching** all registered daemons on system boot.
    - **Monitoring** the health of each daemon via heartbeat tokens.
    - **Self-healing** by attempting to restart failed or idle processes.
    - **Alerting** the Governor when manual intervention is required.

### 2.2. Heartbeat Tokens

- **Location:** `/srv/janus/balaur/signal/heartbeat/`
- **Format:** `[service_name]_heartbeat.json`
- **Content:** A JSON object with the following fields:
    - `service_name`: The name of the service.
    - `timestamp`: The ISO 8601 timestamp of the last heartbeat.
    - `status`: The current status (`running`, `idle`, `restarting`, `failed`).
    - `latency`: The service's last measured processing latency (in ms).
    - `load_index`: A normalized value (0.0-1.0) representing the current workload.

## 3. Fail-Grace System

- **Failure Log:** All failures and restart attempts are logged to `/srv/janus/balaur/logs/failure.log`.
- **Restart Policy:** The `automation_service` will attempt to restart a failed process a maximum of **two** times.
- **Alerting:** If a process fails to restart after the maximum number of attempts, a resonance alert is triggered:
    - An entry is written to `/srv/janus/balaur/logs/alert_resonance.log`.
    - The `alert_bell.wav` is played.

## 4. Integration with URIP

- **Rhythmic Cadence:** The `automation_service`'s main monitoring loop will be synchronized with the URIP's main clock pulse. This ensures that health checks are performed in harmony with the rest of the system's operations.
- **Telemetry Exposure:** The status and health of all daemons managed by RIP will be exposed as a new "Repeatability Metrics" section in the `URIP_Telemetry_Spec_V1.md`. This allows the Harmony Dashboard to visualize the resilience of the system.

## 5. Harmony Dashboard Interface

- **Gauge:** A new "Repeatability" gauge will be added to the dashboard.
- **Metrics:**
    - It will display the percentage of active modules that are currently in a "green" (running) state.
    - It will show the timestamp of the last successful heartbeat received from any service, providing a quick check for system-wide responsiveness.

This protocol establishes the foundation for a truly resilient and self-sustaining system, where every component is designed for effortless, perpetual operation.