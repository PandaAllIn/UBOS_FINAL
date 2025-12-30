#!/usr/bin/env python3
# UBOS Repeatability Implementation Protocol - Automation Service
# Gemini Systems Engineer - 2025-10-26

import time
import json
import os
import subprocess
from datetime import datetime

# Configuration
HEARTBEAT_DIR = "/srv/janus/balaur/signal/heartbeat/"
LOG_DIR = "/srv/janus/balaur/logs/"
FAILURE_LOG = os.path.join(LOG_DIR, "failure.log")
RESONANCE_LOG = os.path.join(LOG_DIR, "alert_resonance.log")
ALERT_SOUND = "/srv/janus/balaur/assets/sounds/alert_bell.wav" # Placeholder
REGISTERED_DAEMONS = {
    "urip_hardware_daemon": "/srv/janus/balaur/bin/urip_hardware_daemon.py"
}
IDLE_THRESHOLD = 300 # 5 minutes
MAX_RESTARTS = 2

def emit_heartbeat(service_name, status, latency=0, load_index=0):
    """Emits a heartbeat token for a service."""
    heartbeat = {
        "service_name": service_name,
        "timestamp": datetime.utcnow().isoformat(),
        "status": status,
        "latency": latency,
        "load_index": load_index
    }
    filepath = os.path.join(HEARTBEAT_DIR, f"{service_name}_heartbeat.json")
    with open(filepath, "w") as f:
        json.dump(heartbeat, f)

def log_failure(service_name, error):
    """Logs a service failure."""
    with open(FAILURE_LOG, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} - {service_name}: {error}\n")

def trigger_alert(service_name):
    """Triggers a resonance alert."""
    with open(RESONANCE_LOG, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} - Resonance alert for {service_name}\n")
    # subprocess.run(["aplay", ALERT_SOUND]) # Requires aplay and a sound file

def manage_daemons():
    """The main loop to manage registered daemons."""
    processes = {}
    restart_counts = {name: 0 for name in REGISTERED_DAEMONS}

    # Initial launch
    for name, path in REGISTERED_DAEMONS.items():
        print(f"Starting {name}...")
        processes[name] = subprocess.Popen(["python3", path])
        emit_heartbeat(name, "started")

    while True:
        for name, proc in processes.items():
            if proc.poll() is not None: # Process has terminated
                if restart_counts[name] < MAX_RESTARTS:
                    log_failure(name, f"Process terminated unexpectedly. Restarting ({restart_counts[name] + 1}/{MAX_RESTARTS}).")
                    processes[name] = subprocess.Popen(["python3", REGISTERED_DAEMONS[name]])
                    restart_counts[name] += 1
                    emit_heartbeat(name, "restarted")
                else:
                    log_failure(name, "Process failed to restart after multiple attempts.")
                    trigger_alert(name)
                    emit_heartbeat(name, "failed")
                    # Remove from active management
                    processes.pop(name)
                    break # Avoid modifying dict during iteration
            else:
                # This is a simplified check. A real implementation would check heartbeat files.
                emit_heartbeat(name, "running")

        time.sleep(10) # Check every 10 seconds

def main():
    print("RIP Automation Service: Activated.")
    for d in [HEARTBEAT_DIR, LOG_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)
    
    manage_daemons()

if __name__ == "__main__":
    main()