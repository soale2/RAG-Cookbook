# retriever.py
"""
Project Part 1: Retriever
==========================
A complete retriever with top-k, score filtering, and MMR.
Loads the FAISS index built in Foundations 03 and exposes
a clean interface the generation module will use in Part 2.

Usage:
    python retriever.py
"""

import json
from pathlib import Path

import faiss
import numpy as np
import requests

INDEX_PATH = Path(__file__).resolve().parents[3] / "foundations" / "03-vector-stores" / "exercises" / "index.faiss"
CHUNKS_PATH = Path(__file__).resolve().parents[3] / "foundations" / "03-vector-stores" / "exercises" / "chunks.json"


def embed(text: str, model: str = "nomic-embed-text") -> np.ndarray:
    """Embed text via Ollama and L2-normalise the vector."""
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype=np.float32)
    return v / (np.linalg.norm(v) + 1e-10)


def load_index(
    index_path: str | Path = INDEX_PATH,
    chunks_path: str | Path = CHUNKS_PATH,
) -> tuple[faiss.IndexFlatIP, list[str]]:
    """Load a FAISS index and its corresponding chunk texts."""
    index = faiss.read_index(str(index_path))
    with open(chunks_path) as f:
        chunks = json.load(f)
    return index, chunks


def retrieve_top_k(
    query: str,
    index: faiss.IndexFlatIP,
    chunks: list[str],
    k: int = 5,
    min_score: float | None = None,
) -> list[dict]:
    """
    Retrieve the top-k chunks by cosine similarity.
    Optionally filter by a minimum score threshold.
    """
    query_vec = embed(query).reshape(1, -1)
    scores, positions = index.search(query_vec, k)

    results = []
    for score, pos in zip(scores[0], positions[0]):
        if pos == -1:
            continue
        if min_score is not None and float(score) < min_score:
            continue
        results.append({"text": chunks[pos], "score": float(score), "index": int(pos)})

    return results


def retrieve_mmr(
    query: str,
    index: faiss.IndexFlatIP,
    chunks: list[str],
    k: int = 5,
    candidates: int = 20,
    lambda_: float = 0.5,
) -> list[dict]:
    """
    Retrieve using Maximal Marginal Relevance.
    Fetches `candidates` results first, then re-ranks for diversity.
    """
    query_vec = embed(query).reshape(1, -1)
    scores, positions = index.search(query_vec, candidates)

    # Build candidate arrays (skip invalid positions)
    cand_scores = []
    cand_positions = []
    cand_vecs = []

    for score, pos in zip(scores[0], positions[0]):
        if pos == -1:
            continue
        cand_scores.append(float(score))
        cand_positions.append(int(pos))
        # Reconstruct the stored vector for redundancy comparison
        vec = index.reconstruct(int(pos))
        cand_vecs.append(vec)

    if not cand_vecs:
        return []

    cand_vecs = np.array(cand_vecs)
    query_flat = query_vec.flatten()

    selected = []
    remaining = list(range(len(cand_vecs)))

    while len(selected) < k and remaining:
        if not selected:
            best_idx = max(remaining, key=lambda i: cand_scores[i])
        else:
            selected_vecs = cand_vecs[[s for s in selected]]
            best_idx = None
            best_mmr = -float("inf")
            for i in remaining:
                relevance = float(cand_vecs[i] @ query_flat)
                redundancy = float(np.max(cand_vecs[i] @ selected_vecs.T))
                mmr_score = lambda_ * relevance - (1 - lambda_) * redundancy
                if mmr_score > best_mmr:
                    best_mmr = mmr_score
                    best_idx = i

            if best_idx is None:
                break

        selected.append(best_idx)
        remaining.remove(best_idx)

    return [
        {
            "text": chunks[cand_positions[i]],
            "score": cand_scores[i],
            "index": cand_positions[i],
        }
        for i in selected
    ]


if __name__ == "__main__":
    print("Loading index...")
    index, chunks = load_index()
    print(f"  {index.ntotal} vectors, {len(chunks)} chunks\n")

    query = "What is the main contribution of this paper?"

    print(f"Query: {query!r}\n")

    print("--- Top-k (k=5) ---")
    for r in retrieve_top_k(query, index, chunks, k=5):
        print(f"  [{r['score']:.4f}] {r['text'][:100]!r}")

    print("\n--- Top-k with min_score=0.70 ---")
    for r in retrieve_top_k(query, index, chunks, k=10, min_score=0.70):
        print(f"  [{r['score']:.4f}] {r['text'][:100]!r}")

    print("\n--- MMR (k=5, lambda=0.5) ---")
    for r in retrieve_mmr(query, index, chunks, k=5, lambda_=0.5):
        print(f"  [{r['score']:.4f}] {r['text'][:100]!r}")
