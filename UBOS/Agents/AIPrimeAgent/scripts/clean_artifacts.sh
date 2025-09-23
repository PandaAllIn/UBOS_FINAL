#!/usr/bin/env bash
set -euo pipefail

# Prune AI Prime artifacts older than N days (default: 14)
# Usage: bash UBOS/Agents/AIPrimeAgent/scripts/clean_artifacts.sh [DAYS]

DAYS="${1:-14}"
ART_DIR="UBOS/Agents/AIPrimeAgent/artifacts"

if [ ! -d "$ART_DIR" ]; then
  echo "Artifacts directory not found: $ART_DIR" >&2
  exit 0
fi

echo "Pruning artifacts older than $DAYS days in $ART_DIR ..."
find "$ART_DIR" -type f -mtime +"$DAYS" -print -delete || true
echo "Done."

