

## Local search and indexes

- Use the search CLI:
  - `python3 scripts/search_docs.py <query terms> --k 10`
  - Example: `python3 scripts/search_docs.py architecture rhythm alignment --k 5`
- Index files:
  - `docs/meta/search_index.json`: word/bigram/trigram inverted index over chapters and key ideas
  - `docs/meta/key_ideas_matrix.md`: human-readable keyword presence matrix
  - `docs/meta/key_ideas_index.json`: machine-readable key ideas per chapter
  - `docs/meta/topics_index.json`: list of generated topic pages
- Manifest pointers:
  - `indexes.search_index_json`
  - `indexes.key_ideas_matrix_md`
  - `indexes.key_ideas_index_json`
  - `topics`
