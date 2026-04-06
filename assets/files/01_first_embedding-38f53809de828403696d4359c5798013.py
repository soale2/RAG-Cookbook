"""
Exercise 01: Your first embedding
===================================
Run this file and inspect the output.

Goal:
  - Call the Ollama embeddings API
  - Understand the shape and range of the output
  - Verify that Ollama is working correctly

Prerequisites:
  - Ollama running: `ollama serve`
  - Model pulled:   `ollama pull nomic-embed-text`
"""

import requests
import numpy as np


def get_embedding(text: str) -> np.ndarray:
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    response.raise_for_status()
    return np.array(response.json()["embedding"], dtype=np.float32)


if __name__ == "__main__":
    text = "Retrieval-Augmented Generation grounds an LLM in external documents."

    vector = get_embedding(text)

    print(f"Input text:  {text!r}")
    print(f"Vector shape: {vector.shape}")         # should be (768,)
    print(f"First 8 values: {vector[:8]}")
    print(f"Min: {vector.min():.4f}  Max: {vector.max():.4f}")
    print(f"Vector magnitude (L2 norm): {np.linalg.norm(vector):.4f}")

    # Questions to think about:
    # 1. Is the magnitude close to 1? If not, what would you need to do?
    # 2. What happens to the vector if you change one word in the input?
    # 3. Try embedding an empty string. What do you get?
