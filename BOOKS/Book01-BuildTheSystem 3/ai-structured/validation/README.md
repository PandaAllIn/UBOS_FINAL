# Validation Utilities

Scripts to enforce schema and source integrity before automation runs:

- `validate_yaml.py` — checks required fields, topic tags, kinds, and filename/id alignment.
- `check_sources.py` — ensures every `source_refs` entry resolves to a real file within `source/` and that line numbers exist.

Usage:
```
python3 validate_yaml.py [chapter-id]
python3 check_sources.py [chapter-id]
```
Run them from this directory or provide the full path. Both exit non-zero on errors.
