"""
Exercise 1: Top-k Retrieval
=============================
Load your FAISS index from Foundations and retrieve the top-k chunks for a query.

Run:
    python exercises/01_top_k.py
"""

import json
from pathlib import Path

import faiss
import numpy as np
import requests


# Adjust these paths to where you saved files in Foundations 03
INDEX_PATH = "../../../foundations/03-vector-stores/exercises/index.faiss"
CHUNKS_PATH = "../../../foundations/03-vector-stores/exercises/chunks.json"


def embed(text: str) -> np.ndarray:
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype=np.float32)
    return v / (np.linalg.norm(v) + 1e-10)


def load_index() -> tuple[faiss.IndexFlatIP, list[str]]:
    # TODO: Load the FAISS index from INDEX_PATH and chunks from CHUNKS_PATH.
    # Return (index, chunks).
    pass


def retrieve(query: str, index: faiss.IndexFlatIP, chunks: list[str], k: int = 5) -> list[dict]:
    # TODO:
    # 1. Embed the query and reshape to (1, 768).
    # 2. Call index.search(query_vec, k).
    # 3. Return [{"text": chunks[pos], "score": float(score)}, ...].
    pass


if __name__ == "__main__":
    print("Loading index...")
    index, chunks = load_index()
    print(f"  {index.ntotal} vectors, {len(chunks)} chunks\n")

    queries = [
        "What problem does this paper solve?",
        "What is the model architecture?",
        "What are the main results?",
        "How is training done?",
        "What are the limitations?",
    ]

    for query in queries:
        print(f"Query: {query!r}")
        results = retrieve(query, index, chunks, k=3)
        for i, r in enumerate(results, 1):
            print(f"  [{i}] score={r['score']:.4f}  {r['text'][:100]!r}")
        print()
