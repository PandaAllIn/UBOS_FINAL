#!/usr/bin/env bash
set -euo pipefail

# Pull files from a Mac over a reverse SSH tunnel (Mac -> Balaur).
#
# Usage (once the reverse tunnel is up on Balaur localhost:2222):
#   export MAC_USER=macuser
#   export MAC_ROOT="/Users/macuser/Projects/janus"   # adjust
#   /srv/janus/02_FORGE/scripts/pull_from_mac.sh docs-dryrun
#   /srv/janus/02_FORGE/scripts/pull_from_mac.sh docs
#   /srv/janus/02_FORGE/scripts/pull_from_mac.sh full-dryrun
#   /srv/janus/02_FORGE/scripts/pull_from_mac.sh full
#
# Environment:
#   MAC_USER   - macOS username (required)
#   MAC_ROOT   - root folder on the Mac to sync from (required)
#   PORT       - reverse tunnel port on Balaur (default: 2222)
#   DEST       - destination root on Balaur (default: /srv/janus)

PORT="${PORT:-2222}"
DEST="${DEST:-/srv/janus}"
: "${MAC_USER:?Set MAC_USER}"
: "${MAC_ROOT:?Set MAC_ROOT}"

ssh_cmd=(ssh -p "${PORT}" -o BatchMode=yes -o ConnectTimeout=5)
rsync_cmd=(rsync -av --progress --human-readable --protect-args -e "ssh -p ${PORT}")

filter_docs=(
  --include='*/'
  --include='*.md'
  --exclude='*'
)

filter_full=(
  --exclude='**/.git/'
  --exclude='**/.DS_Store'
  --exclude='**/node_modules/'
  --exclude='**/.venv/'
  --exclude='**/__pycache__/'
)

case "${1:-}" in
  docs-dryrun)
    echo "[DRY-RUN] Pull docs (*.md) from ${MAC_USER}@localhost:${MAC_ROOT} -> ${DEST}"
    "${rsync_cmd[@]}" --dry-run "${filter_docs[@]}" "${MAC_USER}@localhost:${MAC_ROOT}/" "${DEST}/"
    ;;
  docs)
    echo "Pulling docs (*.md) from ${MAC_USER}@localhost:${MAC_ROOT} -> ${DEST}"
    "${rsync_cmd[@]}" "${filter_docs[@]}" "${MAC_USER}@localhost:${MAC_ROOT}/" "${DEST}/"
    ;;
  full-dryrun)
    echo "[DRY-RUN] Full sync (filtered) from ${MAC_USER}@localhost:${MAC_ROOT} -> ${DEST}"
    "${rsync_cmd[@]}" --dry-run "${filter_full[@]}" "${MAC_USER}@localhost:${MAC_ROOT}/" "${DEST}/"
    ;;
  full)
    echo "Full sync (filtered) from ${MAC_USER}@localhost:${MAC_ROOT} -> ${DEST}"
    "${rsync_cmd[@]}" "${filter_full[@]}" "${MAC_USER}@localhost:${MAC_ROOT}/" "${DEST}/"
    ;;
  pull-missing-core)
    # Pull specific critical files that are missing on Balaur
    echo "Pulling core missing files (ROADMAP, STATE_OF_THE_REPUBLIC, GEMINI.md) if present on Mac..."
    declare -a files=(
      "01_STRATEGY/ROADMAP.md"
      "03_OPERATIONS/STATE_OF_THE_REPUBLIC.md"
      "trinity/GEMINI.md"
    )
    for rel in "${files[@]}"; do
      src="${MAC_ROOT}/${rel}"
      dst="${DEST}/${rel}"
      mkdir -p "$(dirname "${dst}")"
      echo "- Trying ${src} -> ${dst}"
      scp -P "${PORT}" -o BatchMode=yes "${MAC_USER}@localhost:${src}" "${dst}" 2>/dev/null || true
    done
    ;;
  *)
    cat <<USAGE
Usage:
  MAC_USER=<macuser> MAC_ROOT=/Users/<macuser>/Projects/janus \
    ${0} docs-dryrun | docs | full-dryrun | full | pull-missing-core

Examples:
  export MAC_USER=bro
  export MAC_ROOT=/Users/bro/Projects/janus
  ${0} docs-dryrun
  ${0} docs
  ${0} pull-missing-core
USAGE
    exit 1
    ;;
esac

echo "Done."

