#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/srv/janus"
SYSTEMD_DIR="/etc/systemd/system"
UNITS_DIR="$REPO_ROOT/trinity/deployment/systemd"

if [[ $EUID -ne 0 ]]; then
  echo "This installer must be run as root." >&2
  exit 1
fi

install -m 644 "$UNITS_DIR/janus-mission-scheduler.service" "$SYSTEMD_DIR/janus-mission-scheduler.service"
install -m 644 "$UNITS_DIR/janus-mission-scheduler@.service" "$SYSTEMD_DIR/janus-mission-scheduler@.service"
install -m 644 "$UNITS_DIR/mission-scheduler-failure@.service" "$SYSTEMD_DIR/mission-scheduler-failure@.service"
install -m 644 "$UNITS_DIR/janus-grant-hunter.timer" "$SYSTEMD_DIR/janus-grant-hunter.timer"
install -m 644 "$UNITS_DIR/janus-malaga-briefing.timer" "$SYSTEMD_DIR/janus-malaga-briefing.timer"
install -m 644 "$UNITS_DIR/janus-monetization.timer" "$SYSTEMD_DIR/janus-monetization.timer"
install -m 644 "$UNITS_DIR/janus-innovation-scout.timer" "$SYSTEMD_DIR/janus-innovation-scout.timer"
install -m 644 "$UNITS_DIR/janus-mission-dispatcher.service" "$SYSTEMD_DIR/janus-mission-dispatcher.service"
install -m 644 "$UNITS_DIR/janus-mission-executor@.service" "$SYSTEMD_DIR/janus-mission-executor@.service"

systemctl daemon-reload

systemctl enable --now janus-grant-hunter.timer
systemctl enable --now janus-malaga-briefing.timer
systemctl enable --now janus-monetization.timer
systemctl enable --now janus-innovation-scout.timer
systemctl enable --now janus-mission-dispatcher.service

RESIDENTS=("claude" "gemini" "groq" "openai")
for resident in "${RESIDENTS[@]}"; do
  systemctl enable --now "janus-mission-executor@${resident}.service"
done

systemctl list-timers --all | grep "janus-"
systemctl status janus-mission-dispatcher.service --no-pager
systemctl list-units "janus-mission-executor@*.service" --no-pager
