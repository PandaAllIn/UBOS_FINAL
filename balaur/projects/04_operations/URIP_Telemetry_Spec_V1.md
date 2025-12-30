# UBOS Rhythmic Integrity Protocol - Hardware Telemetry Specification V1

**Author:** Gemini, Systems Engineer
**Date:** 2025-10-26
**Status:** Draft

## 1. Overview

This document details the integration of the UBOS Rhythmic Integrity Protocols (URIP) with the physical hardware layer of The Balaur. The objective is to create a tangible, measurable feedback loop where the philosophical principles of "Governor" and "Escapement" are reflected in the server's actual hardware performance.

## 2. Telemetry Mapping

The core of this integration is the mapping of abstract URIP concepts to concrete hardware metrics.

| URIP Concept | Hardware Metric | Sensor/Source | Signal Pipe |
|---|---|---|---|
| **Amplitude** | CPU Temperature (°C) | `sensors` (lm-sensors) | `/srv/janus/balaur/signal/clock/amplitude.json` |
| **Beat Strength** | Power Draw (Watts) | `ipmitool` / Smart Outlet | `/srv/janus/balaur/signal/clock/beat_strength.json` |
| **Escapement Delay**| Network Latency (ms) | `ping` / `fping` | `/srv/janus/balaur/signal/clock/escapement_delay.json` |
| **Feedback** | Environmental Sensors | (Future) TBD | `/srv/janus/balaur/signal/clock/environmental.json` |

## 3. Signal Pipes and Communication

- **Protocol:** MQTT will be used for real-time messaging. A local Mosquitto broker will be configured.
- **Topic Structure:** `ubos/balaur/urip/telemetry/{metric}` (e.g., `ubos/balaur/urip/telemetry/amplitude`)
- **Daemon:** The `urip_hardware_daemon.py` will be responsible for reading sensor data, mapping it to the URIP concepts, and publishing it to the appropriate MQTT topic.

## 4. Clock Synchronization

The system's `chronyd` or `ntpd` will be configured to listen to a local reference clock, which will be disciplined by the main URIP pulse. This ensures that system-level cron jobs and schedulers are in sync with the UBOS heartbeat.

## 5. Governor Watchdog

- **Script:** A script located at `/srv/janus/balaur/bin/governor_sensor.py` will subscribe to the URIP telemetry topics.
- **Logic:** It will compare the incoming telemetry data against the expected rhythm defined by the URIP controller.
- **Threshold:** A deviation of more than ±5% from the expected value will be considered a resonance alert.
- **Action:** Upon detecting a resonance alert, the script will:
    1. Play the `alert_bell.wav` sound.
    2. Write the timestamp and deviation details to `/srv/janus/balaur/logs/alert_resonance.log`.

This specification provides the blueprint for making the pulse of the Republic a physically measurable reality.

## 6. Repeatability Metrics

The RIP provides critical data on the health and resilience of the UBOS daemons. This telemetry will be integrated into the Harmony Dashboard.

| RIP Metric | Data Source | Signal Pipe / Topic | Description |
|---|---|---|---|
| **Daemon Health** | `automation_service.py` | `ubos/balaur/rip/health` | A JSON object containing the status of all registered daemons. |
| **Heartbeat Status**| Heartbeat Tokens | `ubos/balaur/rip/heartbeats`| The latest heartbeat timestamp and status for each service. |
| **System Resilience**| `failure.log` | `ubos/balaur/rip/resilience`| A summary of restart attempts and permanent failures. |