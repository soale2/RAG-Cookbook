"""
Exercise 02: Comparing similarity
====================================
Embed a set of sentences and compare their similarity scores.

Goal:
  - Compute cosine similarity between embeddings
  - Build intuition for what "high" and "low" similarity looks like numerically
  - See that semantic similarity is not the same as word overlap
"""

import requests
import numpy as np


def embed(text: str) -> np.ndarray:
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    response.raise_for_status()
    v = np.array(response.json()["embedding"], dtype=np.float32)
    return v / (np.linalg.norm(v) + 1e-10)   # normalised, so dot product = cosine similarity


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    # Both vectors are already normalised, so this is just a dot product.
    return float(np.dot(a, b))


if __name__ == "__main__":
    sentences = [
        "The transformer architecture uses self-attention mechanisms.",
        "Attention is the key innovation behind modern language models.",
        "RAG retrieves relevant documents before generating an answer.",
        "The Eiffel Tower is located in Paris, France.",
        "Paris is the capital city of France.",
    ]

    print("Embedding sentences...")
    vectors = [embed(s) for s in sentences]

    print("\nPairwise cosine similarity:\n")
    header = f"{'':>6}" + "".join(f"  [{i}]" for i in range(len(sentences)))
    print(header)

    for i, vi in enumerate(vectors):
        row = f"  [{i}]"
        for j, vj in enumerate(vectors):
            score = cosine_similarity(vi, vj)
            row += f"  {score:.2f}"
        print(row)

    print("\nSentences:")
    for i, s in enumerate(sentences):
        print(f"  [{i}] {s}")

    # Questions to think about:
    # 1. Which pair has the highest similarity? Does that match your intuition?
    # 2. Sentences [3] and [4] share the word "Paris". Are they more similar
    #    to each other than [0] and [1]? Why or why not?
    # 3. What score do you get when comparing a sentence with itself? Why?
