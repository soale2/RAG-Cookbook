"""
Exercise 3: Maximal Marginal Relevance
========================================
Implement MMR to retrieve diverse, relevant results.

Run:
    python exercises/03_mmr.py
"""

import json

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
    # TODO: Same as previous exercises.
    pass


def mmr(
    query_vec: np.ndarray,
    candidate_vecs: np.ndarray,
    candidate_texts: list[str],
    k: int = 5,
    lambda_: float = 0.5,
) -> list[str]:
    """
    Select k items from candidate_vecs using Maximal Marginal Relevance.

    At each step, score each remaining candidate as:
        lambda_ * sim(candidate, query) - (1 - lambda_) * max(sim(candidate, selected))

    For the very first pick there are no selected items yet, so just pick
    the most similar to the query.
    """
    # TODO: Implement the MMR loop.
    # - Keep track of selected indices and remaining indices.
    # - At each step, compute MMR scores for all remaining candidates.
    # - Select the one with the highest score and move it to selected.
    # - Return the selected texts in order.
    pass


def retrieve_topk(query: str, index, chunks: list[str], k: int) -> list[dict]:
    q = embed(query).reshape(1, -1)
    scores, positions = index.search(q, k)
    return [{"text": chunks[p], "score": float(s)} for s, p in zip(scores[0], positions[0])]


def retrieve_mmr(query: str, index, chunks: list[str], k: int = 5, lambda_: float = 0.5, pool: int = 50) -> list[str]:
    # TODO:
    # 1. Fetch `pool` candidates using top-k search.
    # 2. Collect their vectors by re-embedding (or reconstruct from the index).
    # 3. Call mmr() and return results.
    #
    # Hint: re-embed each candidate text for simplicity.
    # In production you would use index.reconstruct(i) to avoid re-embedding.
    pass


if __name__ == "__main__":
    index, chunks = load_index()

    queries = [
        "How does attention work in this model?",
        "What are the experimental results?",
        "What are the limitations of this approach?",
    ]

    for query in queries:
        print(f"\nQuery: {query!r}")

        print("  Top-k:")
        for i, r in enumerate(retrieve_topk(query, index, chunks, k=5), 1):
            print(f"    [{i}] score={r['score']:.4f}  {r['text'][:90]!r}")

        print("  MMR (lambda=0.5):")
        for i, text in enumerate(retrieve_mmr(query, index, chunks, k=5, lambda_=0.5), 1):
            print(f"    [{i}] {text[:90]!r}")
