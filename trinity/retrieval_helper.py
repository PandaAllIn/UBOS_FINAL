"""Retrieval helper to build and query a semantic index of UBOS documents.

This helper uses the OpenAI resident to generate embeddings for text chunks
from specified documentation directories. The resulting index is stored as a
JSONL file and can be queried to find relevant documents.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
from openai_resident import ResidentOpenAI


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def build_index(
    root_dirs: List[str],
    index_path: str = "/srv/janus/trinity_memory/openai_embeddings/index.jsonl",
    chunk_size: int = 512,
) -> str:
    """Builds a semantic index from documents in the specified directories."""
    print("Starting index build...")
    openai_resident = ResidentOpenAI()
    index_file = Path(index_path)
    index_file.parent.mkdir(parents=True, exist_ok=True)

    documents = []
    print(f"Searching for documents in: {root_dirs}")
    for root in root_dirs:
        root_path = Path(root)
        for ext in ("*.md", "*.txt", "*.rst"):
            documents.extend(root_path.rglob(ext))
    print(f"Found {len(documents)} documents.")

    with index_file.open("w", encoding="utf-8") as f:
        total_docs = len(documents)
        for idx, doc_path in enumerate(documents):
            print(f"Processing document {idx + 1}/{total_docs}: {doc_path}")
            try:
                content = doc_path.read_text(encoding="utf-8")
                chunks = [content[i : i + chunk_size] for i in range(0, len(content), chunk_size)]
                if not chunks:
                    print(f"  Skipping empty document.")
                    continue

                embeddings = openai_resident.embed_texts(chunks)
                if not embeddings:
                    print(f"  Failed to generate embeddings. Skipping.")
                    continue

                for i, chunk in enumerate(chunks):
                    item = {
                        "path": str(doc_path),
                        "chunk": chunk,
                        "embedding": embeddings[i],
                    }
                    f.write(json.dumps(item) + "\n")
            except Exception as e:
                print(f"  Error processing document: {e}")
                continue  # Skip files that can't be read

    return f"Index built successfully at {index_path}."


def search_index(
    query: str,
    top_n: int = 5,
    index_path: str = "/srv/janus/trinity_memory/openai_embeddings/index.jsonl",
) -> List[Dict[str, Any]]:
    """Searches the index for the most relevant document chunks."""
    openai_resident = ResidentOpenAI()
    index_file = Path(index_path)

    if not index_file.exists():
        return [{"error": "Index not found. Please build it first."}]

    query_embedding = openai_resident.embed_texts([query])
    if not query_embedding:
        return [{"error": "Failed to generate query embedding."}]

    results = []
    with index_file.open("r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            similarity = cosine_similarity(query_embedding, item["embedding"])
            results.append(
                {
                    "path": item["path"],
                    "score": similarity,
                    "preview": item["chunk"][:200] + "...",
                }
            )

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


def retrieve_ubos_docs(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Convenience function to search the UBOS document index."""
    return search_index(query, top_n=top_k)


if __name__ == "__main__":
    # Example usage:
    # 1. Build the index
    roots = ["/srv/janus/00_CONSTITUTION", "/srv/janus/01_STRATEGY", "/srv/janus/BOOKS"]
    print(build_index(roots))

    # 2. Search the index
    results = retrieve_ubos_docs("Lion Sanctuary", top_k=3)
    print(f"{len(results)} results")
    print(results if results else "EMPTY")