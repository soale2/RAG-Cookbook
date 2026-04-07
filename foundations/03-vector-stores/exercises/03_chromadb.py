"""
Exercise 3: ChromaDB
=====================
Store and search vectors using ChromaDB instead of FAISS.
Persistence and metadata filtering are built in.

Run:
    python exercises/03_chromadb.py

Prerequisites:
    pip install chromadb
"""

import numpy as np
import requests
from pathlib import Path


COLLECTION_NAME = "rag-exercises"
DB_PATH = "./chroma_db"

QUERIES = [
    "What is the main contribution of this paper?",
    "How does the attention mechanism work?",
    "What datasets were used for evaluation?",
]


def embed(text: str) -> list[float]:
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype=np.float32)
    v = v / (np.linalg.norm(v) + 1e-10)
    return v.tolist()   # ChromaDB expects a plain list


def load_and_split(pdf_path: str, chunk_size: int = 500) -> list[str]:
    # TODO: Reuse your loader + splitter from the chunking exercises.
    pass


def build_collection(chunks: list[str], source_name: str):
    # TODO:
    # 1. Create chromadb.PersistentClient(path=DB_PATH).
    # 2. Get or create the collection (collection names must be unique).
    # 3. If the collection already has documents, skip adding.
    # 4. Otherwise, add all chunks with ids, embeddings, and metadata.
    #    metadata should include {"source": source_name, "chunk_index": i}
    pass


def search(query: str, k: int = 3):
    # TODO:
    # 1. Load the persistent client and get the collection.
    # 2. Embed the query.
    # 3. Call collection.query(query_embeddings=[...], n_results=k).
    # 4. Return the list of document strings from the results.
    pass


if __name__ == "__main__":
    pdfs = list(Path("data/papers").glob("*.pdf"))
    if not pdfs:
        print("No PDFs in data/papers/.")
        exit()

    chunks = load_and_split(str(pdfs[0]))
    print(f"Loaded {len(chunks)} chunks from {pdfs[0].name}")

    print("Adding to ChromaDB collection...")
    build_collection(chunks, source_name=pdfs[0].name)
    print("  Done.\n")

    for query in QUERIES:
        print(f"Query: {query!r}")
        results = search(query, k=3)
        for i, doc in enumerate(results, 1):
            print(f"  [{i}] {doc[:120]!r}")
        print()
