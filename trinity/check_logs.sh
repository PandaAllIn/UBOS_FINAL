#!/bin/bash
echo "📊 Recent Mallorca Checks"
tail -20 /srv/janus/logs/mallorca_checks.log | grep -E "STREAM|PASS|FAIL|€|Stage"
