"""
Exercise 3: Chunk Size Trade-offs
===================================
Index the same document at three chunk sizes and compare retrieval precision.

Run:
    python exercises/03_chunk_size.py
"""

import numpy as np
import requests
from pathlib import Path


QUERY = "What attention mechanism does the paper propose?"   # change to match your paper


def embed(text: str) -> np.ndarray:
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype=np.float32)
    return v / (np.linalg.norm(v) + 1e-10)


def load_and_split(pdf_path: str, chunk_size: int) -> list[str]:
    # TODO:
    # 1. Load the PDF with PyPDFLoader and join all pages into one string.
    # 2. Split with RecursiveCharacterTextSplitter using the given chunk_size
    #    and overlap = chunk_size // 5.
    # 3. Return the list of chunk strings.
    pass


def build_index(chunks: list[str]) -> np.ndarray:
    # TODO: Embed each chunk and stack into a (N, 768) float32 array.
    # Print progress every 20 chunks.
    pass


def search(query: str, index: np.ndarray, chunks: list[str], k: int = 3) -> list[str]:
    # TODO: Embed the query, compute dot products against the index, return top-k chunks.
    pass


if __name__ == "__main__":
    pdfs = list(Path("data/papers").glob("*.pdf"))
    if not pdfs:
        print("No PDFs in data/papers/.")
        exit()

    pdf_path = str(pdfs[0])
    print(f"Using: {pdfs[0].name}\n")

    for size in [200, 500, 1500]:
        print(f"── chunk_size={size} ──────────────────────────────")
        chunks = load_and_split(pdf_path, chunk_size=size)
        print(f"   {len(chunks)} chunks")
        index = build_index(chunks)
        results = search(QUERY, index, chunks, k=1)
        print(f"   Top result:\n   {results[0][:300]!r}")
        print()
