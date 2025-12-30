---
type: grant_proposal
call: <% tp.system.prompt("Call name / ID") %>
value: <% tp.system.prompt("Estimated value (€)") %>
deadline: <% tp.date.now("YYYY-MM-DD") %>
fit_score: <% tp.system.suggester(["5.0","4.5","4.0","3.5","3.0"],["5.0","4.5","4.0","3.5","3.0"]) %>
status: drafting
owner: <% tp.system.prompt("Owner") %>
tags: [grant, pipeline]
---

# Grant Proposal — <% tp.file.title %>

## Overview
- Call: 
- Value: 
- Deadline: 

## Excellence
- 

## Impact
- 

## Implementation
- Work packages:
- Partners:

## Budget
- 

## Links
- [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline Dashboard]]
- [[01_STRATEGY/ROADMAP|Roadmap]]
