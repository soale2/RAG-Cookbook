"""
Exercise 2: Score Threshold
=============================
Filter retrieval results by minimum similarity score.
Stop returning irrelevant chunks.

Run:
    python exercises/02_score_threshold.py
"""

import json
from pathlib import Path

import faiss
import numpy as np
import requests


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
    # TODO: Load index and chunks (same as Exercise 1).
    pass


def retrieve(query: str, index, chunks: list[str], k: int) -> list[dict]:
    # TODO: Copy from Exercise 1.
    pass


def retrieve_with_threshold(
    query: str,
    index,
    chunks: list[str],
    k: int = 5,
    min_score: float = 0.70,
) -> list[dict]:
    # TODO:
    # 1. Call retrieve() with a large k (e.g. 20) to get many candidates.
    # 2. Filter out results where score < min_score.
    # 3. Return the top k of what remains (or fewer if not enough pass the threshold).
    pass


if __name__ == "__main__":
    index, chunks = load_index()

    in_corpus = [
        "What is the main contribution of this paper?",
        "What architecture does the model use?",
        "What datasets were used?",
    ]

    out_of_corpus = [
        "Who won the 2024 Olympics?",
        "What is the best recipe for banana bread?",
        "How do I fix a flat tyre?",
    ]

    for min_score in [0.60, 0.70, 0.80]:
        print(f"\n{'='*50}")
        print(f"min_score = {min_score}")
        print(f"{'='*50}")

        print("\n-- In-corpus queries --")
        for q in in_corpus:
            results = retrieve_with_threshold(q, index, chunks, k=3, min_score=min_score)
            print(f"  [{len(results)} results]  {q!r}")
            for r in results:
                print(f"    score={r['score']:.4f}  {r['text'][:80]!r}")

        print("\n-- Out-of-corpus queries --")
        for q in out_of_corpus:
            results = retrieve_with_threshold(q, index, chunks, k=3, min_score=min_score)
            print(f"  [{len(results)} results]  {q!r}")
