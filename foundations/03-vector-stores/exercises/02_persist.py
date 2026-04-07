"""
Exercise 2: Persist and Reload
================================
Save your FAISS index and chunk list to disk, then reload without re-embedding.

Run:
    python exercises/02_persist.py
"""

import json
import time
from pathlib import Path

import faiss
import numpy as np
import requests


INDEX_PATH = "index.faiss"
CHUNKS_PATH = "chunks.json"
QUERY = "What is the main contribution of this paper?"


def embed(text: str) -> np.ndarray:
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype=np.float32)
    return v / (np.linalg.norm(v) + 1e-10)


def build_and_save(pdf_path: str):
    # TODO:
    # 1. Load and split the PDF.
    # 2. Embed all chunks and build a faiss.IndexFlatIP(768).
    # 3. Save with faiss.write_index(index, INDEX_PATH).
    # 4. Save chunks list to CHUNKS_PATH as JSON.
    # 5. Print file sizes of both saved files.
    pass


def load_and_search() -> list[dict]:
    # TODO:
    # 1. Load the index with faiss.read_index(INDEX_PATH).
    # 2. Load chunks from CHUNKS_PATH.
    # 3. Embed the QUERY, search, return top-3 results.
    pass


if __name__ == "__main__":
    pdfs = list(Path("data/papers").glob("*.pdf"))
    if not pdfs:
        print("No PDFs in data/papers/.")
        exit()

    # Part A: Build and save (skip if already done)
    if not Path(INDEX_PATH).exists():
        print("Building index (first run)...")
        t0 = time.time()
        build_and_save(str(pdfs[0]))
        print(f"  Built in {time.time() - t0:.1f}s\n")
    else:
        print(f"Index already exists at {INDEX_PATH}. Skipping build.\n")

    # Part B: Load and search
    print("Loading from disk...")
    t0 = time.time()
    results = load_and_search()
    print(f"  Loaded and searched in {time.time() - t0:.3f}s\n")

    print(f"Query: {QUERY!r}")
    for i, r in enumerate(results, 1):
        print(f"  [{i}] score={r['score']:.4f}  {r['text'][:120]!r}")
