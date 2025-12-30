# APT/DPKG Deadlock Recovery (Balaur)
 
Status: Operational Playbook
Audience: Gemini (onsite/console), Codex (ops scripts), Captain (runbook)
 
---
 
## Symptoms
- `apt`/`apt-get` fails with lock held: `/var/lib/dpkg/lock(-frontend)`
- No `apt` process visible, but a watcher script is waiting on a finished `apt install`
- `dpkg --configure -a` suggests partially installed packages
 
## Safety First
- Do NOT reboot to “clear” locks; finish recovery to avoid partial state
- Only clear locks when no package manager process is running
 
## Quick Fix (Console)
```bash
# 0) Verify no package managers running
sudo pgrep -xa 'apt|apt-get|aptitude|dpkg|unattended'

# 1) Stop background updaters (ignore errors)
sudo systemctl stop apt-daily.service apt-daily-upgrade.service packagekit || true

# 2) Remove stale locks
sudo rm -f /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock \
  /var/cache/apt/archives/lock /var/lib/apt/lists/lock

# 3) Repair dpkg and dependencies
sudo DEBIAN_FRONTEND=noninteractive dpkg --configure -a
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::=--force-confnew -f install

# 4) Refresh indexes + install required packages
sudo apt-get update
sudo apt-get install -y mesa-opencl-icd ocl-icd-libopencl1 clinfo

# 5) Validate OpenCL visibility
clinfo | head -n 50
```
 
## Automated Path (Recommended)
```bash
# Copy helper and run as root
scp scripts/recover_apt_lock.sh balaur:/tmp/
ssh balaur 'sudo bash /tmp/recover_apt_lock.sh --timeout 900 --kill-watchers \
  mesa-opencl-icd ocl-icd-libopencl1 clinfo'
```
- Logs: `/var/log/ubos_apt_recover.log`
 
## Post-Recovery Validation
- `dpkg --audit` shows no problems
- `apt-get check` returns success
- `clinfo` shows platform/device; for Mesa/Rusticl: `RUSTICL_ENABLE=radeonsi clinfo`
 
## If Issues Persist
- Remove a broken pkg: `sudo dpkg --remove --force-remove-reinstreq <pkg>` then rerun steps 3–4
- Inspect apt logs: `/var/log/apt/`, `/var/log/dpkg.log`
 
## Preventing Future Deadlocks (Watchers)
- Use a timeout around apt operations
- Avoid infinite `wait` loops; detect child exit and fail fast
- Prefer `flock` for single-instance guards; don’t rely on dpkg lock as a signal
 
Minimal wrapper pattern:
```bash
#!/usr/bin/env bash
set -euo pipefail
PKGS=(mesa-opencl-icd ocl-icd-libopencl1 clinfo)
TIMEOUT=${TIMEOUT:-900}

# Single instance guard (not the dpkg lock!)
exec 9>/var/run/apt-watcher.lock
flock -n 9 || { echo "Another watcher running"; exit 0; }

# Abort if another package manager is active
pgrep -xa 'apt|apt-get|aptitude|dpkg|unattended' && { echo "Busy"; exit 1; } || true

# Time-bounded install
if command -v timeout >/dev/null; then
  timeout "$TIMEOUT" sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "${PKGS[@]}"
else
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "${PKGS[@]}"
fi
```
 
This pattern ensures:
- No indefinite waiting
- Safe concurrency gating
- Clear exit codes for supervisors
 
---
 
Owner: Codex (ops tooling) | Reviewed by: Gemini (infra), Claude (governance)
Version: 1.0

