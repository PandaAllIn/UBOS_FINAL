---
type: dashboard
category: vault_health
created: 2025-11-20
tags: [dashboard, metrics]
---

# 📊 Vault Statistics

## Key Metrics

```dataviewjs
const pages = dv.pages();
const total = pages.length; 
const words = pages.array().reduce((sum,p)=>sum + (p.file.wordCount ?? 0),0);
const today = moment();
const weekStart = moment().startOf('week');
const monthStart = moment().startOf('month');
const createdThisWeek = pages.where(p => moment(p.file.ctime).isSameOrAfter(weekStart));
const createdThisMonth = pages.where(p => moment(p.file.ctime).isSameOrAfter(monthStart));
dv.table(["Metric","Value"], [
  ["Total notes", total.toLocaleString()],
  ["Total words", words.toLocaleString()],
  ["Created this week", createdThisWeek.length],
  ["Created this month", createdThisMonth.length]
]);
```

## Most Linked Notes

```dataview
TABLE file.link AS Note, length(file.inlinks) AS Inlinks
FROM ""
SORT length(file.inlinks) DESC
LIMIT 10
```

## Orphan Notes (no backlinks)

```dataview
LIST file.link
FROM ""
WHERE length(file.inlinks) = 0 AND file.path !~ "^99_ARCHIVES/"
LIMIT 50
```

## Tag Usage (Top 20)

```dataviewjs
const tags = {};
pages.forEach(p => {
  (p.file.tags ?? []).forEach(tag => {
    tags[tag] = (tags[tag] ?? 0) + 1;
  });
});
const rows = Object.entries(tags)
  .sort((a,b)=>b[1]-a[1])
  .slice(0,20)
  .map(([tag,count])=>[tag,count]);
dv.table(["Tag","Count"], rows);
```

---

_Run this dashboard after large imports to verify Observatory health._
