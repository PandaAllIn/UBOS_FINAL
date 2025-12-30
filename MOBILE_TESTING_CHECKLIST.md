---
type: testing_checklist
device: iPad (Obsidian Mobile)
created: 2025-11-20
tags: [mobile, qa, malaga]
---

# 📱 Mobile Testing Checklist

## Pre-Test Setup
- [ ] Obsidian mobile synced (iCloud/Obsidian Sync)
- [ ] QuickAdd + Dataview + Templater enabled on mobile
- [ ] Plug in or ensure >40% battery
- [ ] Toggle airplane mode handy for offline test

## Test 1 – Quick Capture (No Keyboard)
- [ ] Open vault → Command palette (☰)
- [ ] Search "Captain's Log"
- [ ] Pick macro, dictate via iOS mic
- [ ] Tap `Done` → file saved under `field_insights/`
- [ ] Measure elapsed time (<15 s target)

## Test 2 – Quick Capture (Keyboard)
- [ ] Connect Magic Keyboard (or BT keyboard)
- [ ] Press `Cmd+Shift+L`
- [ ] Template renders with prompts already focused
- [ ] Fill fields → `Cmd+S`
- [ ] Time under 10 s ✅

## Test 3 – Dashboard View
- [ ] Open `_DASHBOARDS/MISSION_STATUS`
- [ ] Verify Dataview tables render and scroll smoothly
- [ ] Tap links to missions → open correctly
- [ ] Back gesture returns to dashboard

## Test 4 – Graph Filters
- [ ] Open [[_VIEWS/PHILOSOPHY_GRAPH]] instructions
- [ ] Launch Graph View, apply filter `path:03_OPERATIONS/MALAGA_EMBASSY`
- [ ] Confirm taps open notes without lag

## Test 5 – Offline Resilience
- [ ] Disable Wi-Fi ➜ repeat Quick Capture
- [ ] Note saves locally
- [ ] Re-enable Wi-Fi ➜ sync completes

## Test 6 – Search
- [ ] Use mobile search for `#mission`
- [ ] Confirm filters + previews display properly

## Test 7 – Task Review
- [ ] Open `_DASHBOARDS/TASKS_TODAY`
- [ ] Tasks plugin renders checkboxes
- [ ] Toggle a sample task → sync completes once online

## Issues Found
_Log any device-specific issues here with screenshots if possible._

## Improvements / Follow-ups
- Add hardware keyboard shortcuts discovered
- Document any plugin toggles needed for performance
- Capture App Store/OS updates required

_Use this checklist before Málaga departure and after every major plugin change._
