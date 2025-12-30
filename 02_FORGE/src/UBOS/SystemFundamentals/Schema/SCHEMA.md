# AI Knowledge Schema

This schema defines how all AI-ready knowledge assets are stored inside `UBOS/SystemFundamentals/Books/`. The goal is to keep formats predictable so agents can read and transform content without improvisation.

## Directory Layout

```
UBOS/
  SystemFundamentals/
    Schema/                # Shared schema docs & templates
    Books/
      BookXX-<Slug>/
        source/            # Raw manuscript, summaries, helper files
          chapters/
            <chapter-id>/
              chapter.md
              key-ideas.md
              exercises.md
              quotes.md
        ai-structured/
          <book-short-name>/
            book.yaml
            README.md
            ROADMAP.md
            CHAPTER_GUIDE.md
            SPECKIT_HANDOFF.md
            chapters/
              <chapter-id>-<slug>/
                chapter.yaml
                chapter.md (optional)
                ideas/
                practices/
                quotes/
                indices/
```

All IDs use zero padding (`01`, `02`, …) so lexical order matches reading order.

## `book.yaml`
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Short identifier (`build-the-system`). |
| `title` | string | Human-readable title. |
| `author` | string | Author attribution. |
| `publisher` | string | Optional publisher credit. |
| `source_files` | list | Relative paths to raw manuscript assets. |
| `chapters` | list | Minimal metadata per chapter (`id`, `slug`, `title`). |
| `topics` | list | Allowed topic tags shared across chapters. |
| `exports` | dict | Paths for generated aggregate files (e.g., `ideas_jsonl`). |

## `chapter.yaml`
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Zero-padded chapter number. |
| `slug` | string | Kebab-case shorthand. |
| `title` | string | Chapter title. |
| `summary` | string | 2–3 sentence overview. |
| `objectives` | list | Learning goals or outcomes. |
| `dependencies` | list | IDs of prerequisite chapters/ideas. |
| `topics` | list | Allowed topic tags for the chapter. |
| `source_refs` | list | Pointers back to raw text (`<path>:<line>`). |
| `assets` | dict | Links to derivative summaries (`chapter-summary.md`, etc.). |

## Idea / Practice / Quote Records
Every granular YAML file shares the same core header:

```
id: idea-01-blueprint-thinking
chapter: "01"
kind: principle        # principle | framework | metaphor | question | checklist | ritual | quote
title: Blueprint Thinking
one_liner: "Intentional architecture precedes sustainable abundance."
description: |
  Multi-paragraph explanation …
topics:
  - architecture
  - abundance
source_refs:
  - UBOS/SystemFundamentals/Books/Book01-BuildTheSystem/source/docs/chapters/01/chapter.md:5
  - UBOS/SystemFundamentals/Books/Book01-BuildTheSystem/source/BuildTheSystem/02-chapter-01-abundance-architecture/chapter-summary.md:4
actions:
  - Map one routine currently handled reactively.
  - Define the structural counterpart.
related_ids:
  - practice-02-morning-architecture
  - quote-03-system-carries-you
metadata:
  token_estimate: 120
  reading_time_seconds: 45
```

Only include fields that apply. Omit empty arrays to reduce noise. `metadata` can store helper metrics (token estimates, difficulty, etc.).

## Aggregates (`indices/`)
Automation may populate the following files:
- `ideas.jsonl` — flattened idea records.
- `practices.jsonl` — flattened practices.
- `quotes.jsonl` — flattened quotes.
- `topic_index.json` — map of topic → idea IDs.

These files are generated and should not be edited manually.

## Naming Rules
- Filenames mirror the `id` field (`ideas/idea-01-blueprint-thinking.yaml`).
- Use lowercase slugs with dashes.
- ASCII only.
- Ensure `id` inside YAML exactly equals the filename stem.

## Source Referencing
Always cite the origin material using repo-relative paths:
- Format: `<relative-path-from-repo-root>:<line>` (1-based).
- Prefer stable sources in `source/docs/` or `source/BuildTheSystem/`.
- List multiple entries instead of line ranges when necessary.

## Validation Expectations
Specs and validation scripts must enforce:
1. Filenames align with the `id` field.
2. Required fields exist (`id`, `kind`, `title`, `source_refs`).
3. Topic tags belong to `book.yaml > topics`.
4. `source_refs` resolve to existing files.

## Workflow Summary
1. **Ingest** the raw materials from `source/`.
2. **Outline** candidate ideas, practices, and quotes with source references.
3. **Author** YAML records following this schema.
4. **Generate** aggregate files in `indices/`.
5. **Validate** using the shared scripts.
6. **Automate** via SpecKit once manual checks pass.

Keep this schema updated before modifying any downstream directories.
