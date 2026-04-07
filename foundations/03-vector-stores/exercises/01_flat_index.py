"""
Exercise 1: Build a FAISS Flat Index
======================================
Embed a document, store vectors in a FAISS IndexFlatIP, and search it.

Run:
    python exercises/01_flat_index.py

Prerequisites:
    pip install faiss-cpu
"""

import numpy as np
import requests
import faiss
from pathlib import Path


def embed(text: str) -> np.ndarray:
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype=np.float32)
    return v / (np.linalg.norm(v) + 1e-10)


def load_and_split(pdf_path: str, chunk_size: int = 500) -> list[str]:
    # TODO: Load the PDF and split into chunks. Return list of strings.
    pass


def build_index(chunks: list[str]) -> tuple[faiss.IndexFlatIP, np.ndarray]:
    """
    Returns the FAISS index and the embedding matrix.
    Keep the matrix so you can map index positions back to chunks.
    """
    # TODO:
    # 1. Embed each chunk (print progress every 20 chunks).
    # 2. Stack into a (N, 768) float32 array.
    # 3. Create faiss.IndexFlatIP(768) and add the vectors.
    # 4. Return (index, vectors).
    pass


def search(query_text: str, index: faiss.IndexFlatIP, chunks: list[str], k: int = 3):
    # TODO:
    # 1. Embed and normalise the query.
    # 2. Reshape to (1, 768).
    # 3. Call index.search(query, k) — returns (scores, positions).
    # 4. Return list of {"text": ..., "score": ...} dicts.
    pass


if __name__ == "__main__":
    pdfs = list(Path("data/papers").glob("*.pdf"))
    if not pdfs:
        print("No PDFs in data/papers/.")
        exit()

    print(f"Loading {pdfs[0].name}...")
    chunks = load_and_split(str(pdfs[0]))
    print(f"  {len(chunks)} chunks")

    print("Building index...")
    index, _ = build_index(chunks)
    print(f"  Index size: {index.ntotal} vectors\n")

    queries = [
        "What is the main contribution of this paper?",
        "How does the attention mechanism work?",
        "What datasets were used for evaluation?",
    ]

    for query in queries:
        print(f"Query: {query!r}")
        results = search(query, index, chunks, k=3)
        for i, r in enumerate(results, 1):
            print(f"  [{i}] score={r['score']:.4f}  {r['text'][:120]!r}")
        print()
