---
type: dashboard
category: constitutional_audit
auto_refresh: true
created: 2025-11-16
tags: [dashboard, constitution, decisions, audit]
---

# ⚖️ CONSTITUTIONAL AUDIT DASHBOARD

*Automatic compliance checks for Trinity decisions*

---

## 🧭 DECISION STATUS

```dataviewjs
const decisions = dv.pages('"03_OPERATIONS/decisions"')
  .where(p => (p.type ?? "").toLowerCase() === "constitutional_decision");
const pending = decisions.where(p => (p.vote_status ?? "").toLowerCase() === "pending");
const approved = decisions.where(p => (p.vote_status ?? "").toLowerCase() === "approved");
const rejected = decisions.where(p => (p.vote_status ?? "").toLowerCase() === "rejected");
dv.paragraph(`**Decisions Indexed:** ${decisions.length} | **Pending:** ${pending.length} | **Approved:** ${approved.length} | **Rejected:** ${rejected.length}`);
if (decisions.length === 0) {
  dv.paragraph("_No decisions recorded. Use `_TEMPLATES/strategy/constitutional_decision.md` when logging Trinity locks._");
}
```

---

## 🚨 DECISIONS WITHOUT FOUR BOOKS LINKS

```dataviewjs
const missingLinks = decisions.where(d =>
  !(d.links_to_books && d.links_to_books.length));
if (missingLinks.length === 0) {
  dv.paragraph("✅ All decisions link back to the Four Books.");
} else {
  dv.paragraph("⚠️ Decisions missing Four Books references:");
  dv.list(missingLinks.map(d => d.file.link));
}
```

---

## 🔐 TRINITY LOCK DISTRIBUTION

```dataview
TABLE trinity_lock_tier AS Tier, status, date, budget
FROM "03_OPERATIONS/decisions"
WHERE type = "constitutional_decision"
SORT date DESC
LIMIT 20
```

### Tier Counts

```dataviewjs
const tiers = {};
decisions.forEach(d => {
  const tier = (d.trinity_lock_tier ?? "unspecified").toLowerCase();
  tiers[tier] = (tiers[tier] ?? 0) + 1;
});
dv.table(["Tier","Count"],
  Object.entries(tiers).map(([tier,count]) => [tier, count]));
```

---

## 🧮 ALIGNMENT SCORE

```dataviewjs
const aligned = decisions.where(d => (d.constitutional_alignment ?? "").toLowerCase() === "verified");
const pendingAlign = decisions.length ? Math.round((aligned.length / decisions.length) * 100) : 0;
dv.paragraph(`**Constitutional Alignment:** ${pendingAlign}%`);
```

> _Alignment increases automatically when decisions are marked `constitutional_alignment: verified`._

---

## 📥 PENDING VOTES

```dataview
LIST file.link
FROM "03_OPERATIONS/decisions"
WHERE type = "constitutional_decision" AND vote_status = "pending"
```

---

## 🔗 CONSTITUTIONAL LINEAGE

To trace a decision back to its originating principles:

1. Open the decision note → **More options → Open local graph**.
2. In the graph search bar, filter with `tag:#constitutional OR path:00_CONSTITUTION/principles/philosophy_books`.
3. Expand neighbors until you see Four Books references and any linked concept hubs.
4. Use [[_VIEWS/PHILOSOPHY_GRAPH|Philosophy Graph View]] presets for a vault-wide perspective.

This workflow surfaces alignment gaps immediately—add missing `links_to_books` fields before approving a Trinity lock.

---

## 🔗 LINKS

- [[00_CONSTITUTION/principles/philosophy_books/README|Four Books (Philosophy Core)]]
- [[03_OPERATIONS/decisions/|Decision Archive]]
- [[_DASHBOARDS/MISSION_STATUS|Mission Control]]
- [[OBSERVATORY_INDEX|Observatory Home]]

---

*Dashboard updates when decision notes are created via QuickAdd → Constitutional Decision.*
