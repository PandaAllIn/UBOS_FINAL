# Dataview Test

type: test
category: dashboard

## All Missions
```dataview
TABLE status, budget, deadline
FROM "03_OPERATIONS"
WHERE type = "mission"
SORT deadline ASC
```

## DataviewJS Test
```dataviewjs
const pages = dv.pages('"03_OPERATIONS"');
dv.paragraph(`Found ${pages.length} files in operations folder`);
if (pages.length > 0) {
  dv.paragraph("✅ DataviewJS working!");
} else {
  dv.paragraph("⚠️ No files found - check folder path");
}
```
