---
type: mission
mission_id: <% tp.date.now("YYYYMMDDHHmm") %>
title: <% tp.system.prompt("Mission title") %>
status: planning
priority: <% tp.system.suggester(["critical","high","medium","low"],["critical","high","medium","low"]) %>
owner: <% tp.system.prompt("Owner") %>
budget: <% tp.system.prompt("Budget (€, numeric)") %>
deadline: <% tp.date.now("YYYY-MM-DD") %>
tags: [mission]
---

# <% tp.file.title %>

## 🎯 Objective
- 

## 🗺️ Scope
- In scope:
- Out of scope:

## 📅 Milestones
- [ ] Milestone / date

## 🚧 Risks / Mitigations
- 

## 📡 Links
- Strategy: [[01_STRATEGY/ROADMAP|Roadmap]]
- Constitution: [[00_CONSTITUTION/principles/philosophy_books/README|Four Books]]
- Ops Index: [[OPERATIONS_INDEX|Operations Index]]
