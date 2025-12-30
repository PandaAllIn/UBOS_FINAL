# Balaur Recovery Runbook – Emergency Deletion (2025-10-25)

Author: Codex (Forgemaster)
Scope: Recover deleted .md and other files on /srv/janus after destructive extension

---

## 0) Immediate Actions

- Freeze writes: Stop editing in the affected workspace to avoid overwriting recoverable blocks.
- Disable the offending extension (Kilocode):
  - VS Code → Extensions → search “Kilocode” → Disable/Uninstall.
  - Check Settings → Workbench: Local History (increase retention: entries=5000, days=60+).

---

## 1) Fast Restore – VS Code Local History

Use the helper to restore latest revisions automatically:

```bash
# Preview intended restores (safe)
python3 /srv/janus/02_FORGE/scripts/restore_from_vscode_history.py --dry-run --only-missing --under /srv/janus

# Restore only missing files
python3 /srv/janus/02_FORGE/scripts/restore_from_vscode_history.py --only-missing --under /srv/janus

# Broader pass (creates .restored-YYYYMMDDTHHMMSSZ copies if target exists)
python3 /srv/janus/02_FORGE/scripts/restore_from_vscode_history.py --under /srv/janus
```

Local History search paths:
- `/home/balaur/.config/Code/User/History`
- `/home/balaur/.vscode-server/data/User/History`

---

## 2) Check Trash

Browse Linux Trash for recent deletions:

```bash
ls -lt /home/balaur/.local/share/Trash/files | head
# look for .md files; restore manually if found
```

---

## 3) Snapshot-Based Recovery (recommended)

If LVM is in use:

```bash
# Identify LV
lsblk -f
sudo vgdisplay
sudo lvdisplay

# Create read-only snapshot (adjust names/sizes)
sudo lvcreate -s -L 10G -n janus-snap /dev/VG_NAME/LV_NAME
sudo mkdir -p /mnt/recover
sudo mount -o ro /dev/VG_NAME/janus-snap /mnt/recover

# Run recovery tools on the snapshot
sudo testdisk /dev/VG_NAME/janus-snap   # guided restore for deleted files
# OR, for ext3/4
sudo extundelete /dev/VG_NAME/janus-snap --restore-directory /srv/janus

# Copy recovered files out of /mnt/recover to a safe staging dir
```

If btrfs/ZFS:
- Create a snapshot and mount read-only; then use testdisk/photorec in the snapshot.

Notes:
- Always operate on a snapshot or unmounted device to prevent journal replay from clearing deletion records.
- TestDisk provides interactive recovery and previews; extundelete requires ext3/4 and journal.

---

## 4) Post-Recovery Merge

- Compare `.restored-*` files with current versions; merge diffs; remove suffix once verified.
- Rebuild indices/caches that depend on docs (e.g., UBOS retrieval index):
  ```bash
  /ubos "Lion's Sanctuary"
  ```
- Validate Trinity bot commands and oracles after doc restore.

---

## 5) Hardening & Backups

- Put /srv/janus under Git version control (private repo on The Balaur):
  ```bash
  cd /srv/janus
  git init
  git add .
  git commit -m "Baseline after recovery"
  ```
- Nightly snapshots:
  - LVM snapshot + rsync, or btrfs/ZFS snapshots.
- External backups:
  - Borg or Restic to an external disk/NAS weekly.
- VS Code Local History:
  - Increase limits (entries & days) and verify enabled.

---

## 6) Communication

- Use /announce in Telegram for human-readable updates (clickable paths).
- Use broadcast_announcement.py for COMMS_HUB fanout.

Example:
```bash
python3 /srv/janus/02_FORGE/scripts/broadcast_announcement.py \
  --message "Recovery pass executed. Runbook at /srv/janus/03_OPERATIONS/reports/RECOVERY_RUNBOOK_2025-10-25.md" \
  --category status
```

---

## 7) Appendix – Tooling Paths

- Restore helper: `/srv/janus/02_FORGE/scripts/restore_from_vscode_history.py`
- COMMS broadcast: `/srv/janus/02_FORGE/scripts/broadcast_announcement.py`
- Bulletin log: `<TRINITY_LOG_DIR>/bulletins.jsonl` (default `/srv/janus/trinity_logs/bulletins.jsonl`)

*** End of Runbook ***
