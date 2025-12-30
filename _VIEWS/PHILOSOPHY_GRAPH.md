---
type: guide
category: graph_view
created: 2025-11-20
tags: [graph, philosophy, filter]
---

# 🌌 Philosophy Graph View

Use this view when you want to trace ideas from the Four Books down into missions and dashboards.

## Quick Access
1. Open Graph View (`Ctrl/Cmd + G`).
2. Enable **Filters → Search** and paste: `path:00_CONSTITUTION/principles/philosophy_books`.
3. Toggle **Groups → Tags** and color nodes tagged `#principle`, `#constitutional`, `#decision`.
4. Adjust **Depth** slider to 2 to see immediate descendants without overwhelming the graph.

## Filter Recipes
- `path:01_STRATEGY` → Strategy dossiers + grant planning.
- `path:03_OPERATIONS/MALAGA_EMBASSY` → Málaga-only operational graph.
- `tag:#grant` → Grants + partners powering revenue.
- `tag:#constitutional` → All constitutional decisions and references.
- `tag:#mission` `OR` `tag:#partner` → Mission/partner relationships.

## Usage Notes
- Combine search filters with the **Neighbors** panel to step through lineage (e.g., Decision → Principle → Book → Mission).
- Save the filter as a **Graph preset** (top-right ••• menu → Save view) for quick reuse.
- Pair with [[_DASHBOARDS/CONSTITUTIONAL_AUDIT|Constitutional Audit]] to verify Trinity locks before acting.

_This guide keeps graph exploration focused and performant even on mobile._
