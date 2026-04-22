# build_index.py
"""
Solution: Vector Store Builder
================================
Embed chunks and persist them in a FAISS index + chunks.json.

Usage:
    python build_index.py                          # default: ../../../data/papers/
    python build_index.py --input chunks.json      # from pre-chunked JSON
    python build_index.py --output ./my_index      # custom output directory
"""

import argparse
import json
import sys
from pathlib import Path

import faiss
import numpy as np
import requests

# Add the chunking project so we can reuse the document processor
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "02-chunking" / "project" / "solution"))


def embed(text: str, model: str = "nomic-embed-text") -> np.ndarray:
    """Embed text via Ollama and L2-normalise."""
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype=np.float32)
    return v / (np.linalg.norm(v) + 1e-10)


def load_chunks_from_json(path: str) -> list[str]:
    """Load pre-chunked texts from a JSON file."""
    with open(path) as f:
        return json.load(f)


def chunk_documents(folder: str) -> list[str]:
    """Load and chunk documents using the Foundations 02 pipeline."""
    from document_loader import load_documents_from_folder
    from text_splitter import split_documents

    docs = load_documents_from_folder(folder)
    chunks = split_documents(docs)
    return [c.page_content for c in chunks]


def build_faiss_index(texts: list[str], model: str = "nomic-embed-text") -> tuple[faiss.IndexFlatIP, list[str]]:
    """Embed all texts and build a FAISS inner-product index."""
    print(f"Embedding {len(texts)} chunks...")
    vectors = []
    for i, text in enumerate(texts):
        vec = embed(text, model=model)
        vectors.append(vec)
        if (i + 1) % 50 == 0 or i == len(texts) - 1:
            print(f"  {i + 1}/{len(texts)}")

    matrix = np.array(vectors, dtype=np.float32)
    dim = matrix.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(matrix)

    print(f"Index built: {index.ntotal} vectors, {dim} dimensions")
    return index, texts


def save_index(index: faiss.IndexFlatIP, chunks: list[str], output_dir: str):
    """Save FAISS index and chunk texts to disk."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    index_path = out / "index.faiss"
    chunks_path = out / "chunks.json"

    faiss.write_index(index, str(index_path))
    with open(chunks_path, "w") as f:
        json.dump(chunks, f)

    print(f"Saved: {index_path} ({index.ntotal} vectors)")
    print(f"Saved: {chunks_path} ({len(chunks)} chunks)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a FAISS index from documents or chunks")
    parser.add_argument("--input", type=str, help="Path to a chunks.json file or a folder of documents")
    parser.add_argument("--output", type=str, default=".", help="Output directory for index.faiss and chunks.json")
    args = parser.parse_args()

    input_path = args.input or str(Path(__file__).resolve().parents[4] / "data" / "papers")

    if input_path.endswith(".json"):
        print(f"Loading chunks from {input_path}...")
        texts = load_chunks_from_json(input_path)
    else:
        print(f"Loading and chunking documents from {input_path}...")
        texts = chunk_documents(input_path)

    if not texts:
        print("No chunks to index.")
        sys.exit(1)

    index, chunks = build_faiss_index(texts)
    save_index(index, chunks, args.output)
