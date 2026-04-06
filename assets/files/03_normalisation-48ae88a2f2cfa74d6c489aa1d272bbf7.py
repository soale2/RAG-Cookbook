"""
Exercise 03: The effect of normalisation
==========================================
See what happens to similarity scores when you skip normalisation.

Goal:
  - Understand why L2 normalisation is not optional
  - See that magnitude differences distort raw dot product scores
  - Confirm that normalised dot product equals cosine similarity
"""

import requests
import numpy as np


def embed_raw(text: str) -> np.ndarray:
    """Return the raw embedding, unnormalised."""
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    response.raise_for_status()
    return np.array(response.json()["embedding"], dtype=np.float32)


def l2_normalise(v: np.ndarray) -> np.ndarray:
    return v / (np.linalg.norm(v) + 1e-10)


if __name__ == "__main__":
    # A short and a long version of roughly the same idea
    short = "RAG retrieves documents."
    long  = (
        "Retrieval-Augmented Generation is a technique where a language model is given "
        "access to an external knowledge base. Before generating a response, the system "
        "retrieves the most relevant documents from that knowledge base and includes them "
        "in the context window. This grounds the model's output in real, verifiable sources "
        "and significantly reduces hallucination."
    )
    unrelated = "The boiling point of water is 100 degrees Celsius."

    print("Embedding texts...")
    raw_short     = embed_raw(short)
    raw_long      = embed_raw(long)
    raw_unrelated = embed_raw(unrelated)

    norm_short     = l2_normalise(raw_short)
    norm_long      = l2_normalise(raw_long)
    norm_unrelated = l2_normalise(raw_unrelated)

    print(f"\nMagnitudes (L2 norm):")
    print(f"  short:     {np.linalg.norm(raw_short):.4f}")
    print(f"  long:      {np.linalg.norm(raw_long):.4f}")
    print(f"  unrelated: {np.linalg.norm(raw_unrelated):.4f}")

    print(f"\nRaw dot products (not normalised):")
    print(f"  short . long:      {np.dot(raw_short, raw_long):.4f}")
    print(f"  short . unrelated: {np.dot(raw_short, raw_unrelated):.4f}")

    print(f"\nCosine similarity (normalised dot products):")
    print(f"  short . long:      {np.dot(norm_short, norm_long):.4f}")
    print(f"  short . unrelated: {np.dot(norm_short, norm_unrelated):.4f}")

    # Questions to think about:
    # 1. Do the raw dot products correctly rank short.long above short.unrelated?
    # 2. What if the magnitudes were very different? Could a raw dot product
    #    rank an unrelated long text above a related short text?
    # 3. After normalisation, are the rankings stable regardless of text length?
