---
type: constitutional_decision
decision_id: <% tp.date.now("YYYYMMDDHHmm") %>
date: <% tp.date.now("YYYY-MM-DD") %>
status: draft
tier: <% tp.system.suggester(["Alpha","Beta","Omega"],["alpha","beta","omega"]) %>
owner: <% tp.system.prompt("Decision owner") %>
alignment: pending
budget: <% tp.system.prompt("Budget (€, if any)") %>
tags: [decision, constitutional]
---

# Constitutional Decision — <% tp.file.title %>

## 📜 Context
- 

## 🧭 Constitutional Links
- [[00_CONSTITUTION/principles/philosophy_books/Book01-BuildTheSystem/INDEX|Book 1]]
- [[00_CONSTITUTION/principles/philosophy_books/Book02-Build-One-System-at-a-Time/INDEX|Book 2]]
- [[00_CONSTITUTION/principles/philosophy_books/Book03-The-Art-of-Strategic-Thinking/INDEX|Book 3]]
- [[00_CONSTITUTION/principles/philosophy_books/Book04-The-Tactical-Mindset/INDEX|Book 4]]

## Options
1) 
2) 
3) 

## 📊 Analysis
- Risks:
- Benefits:
- Dependencies:

## 🗳️ Decision
- Chosen option: 
- Rationale: 
- Next steps: 
