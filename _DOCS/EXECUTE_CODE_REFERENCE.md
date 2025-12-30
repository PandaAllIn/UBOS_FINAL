---
type: reference
category: automation
created: 2025-11-20
tags: [execute-code, automation, analytics]
---

# ⚙️ Execute Code Plugin Reference

**Enabled Languages:** `python`, `javascript`, `shell` (bash). Run code blocks directly inside notes via Execute Code.

## Example 1 – Financial Projections (Python)

````run-python
import json
from pathlib import Path

with open(Path('03_OPERATIONS/MALAGA_EMBASSY/financial_tracking.json')) as fp:
    data = json.load(fp)

capital = data['capital']
revenue = data['revenue']
burn = data['monthly_burn']

runway = capital / burn
coverage = (revenue / burn) * 100

print(f"Runway: {runway:.1f} months")
print(f"Revenue coverage: {coverage:.0f}%")
````

## Example 2 – Grant Deadline Alerts (JavaScript)

````run-js
const grants = dv.pages('"01_STRATEGY/grant_pipeline"')
  .where(g => g.deadline && g.status !== 'submitted')
  .sort(g => g.deadline);

const now = new Date();
for (const grant of grants) {
  const deadline = new Date(grant.deadline);
  const days = Math.ceil((deadline - now) / (1000*60*60*24));
  if (days <= 30) {
    console.log(`⚠️ ${grant.file.name}: ${days} days remaining`);
  }
}
````

## Example 3 – Shell Script Trigger (Bash)

````run-shell
bash AUTOMATION_SCRIPTS/obsidian_realtime_update.sh briefing
````

_Use Command Palette → “Execute Code: Run code block under cursor”._
