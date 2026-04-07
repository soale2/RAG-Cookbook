"""
Exercise 2: First API Calls
============================
Make a real embedding call and a real generation call.

Run:
    python exercises/02_first_calls.py
"""

import time
import requests
import numpy as np

OLLAMA_URL = "http://localhost:11434"


# ── Part A: Embeddings ────────────────────────────────────────────────────────

def get_embedding(text: str) -> np.ndarray:
    # TODO: POST to /api/embeddings with model="nomic-embed-text" and prompt=text.
    # Return the embedding as a numpy float32 array.
    pass


def part_a():
    print("=== Part A: Embeddings ===")
    text = "The transformer architecture changed natural language processing forever."

    vector = get_embedding(text)

    # TODO: Print the shape, min, max, and L2 norm of the vector.
    # Expected shape: (768,)
    pass


# ── Part B: Generation ────────────────────────────────────────────────────────

def generate(prompt: str) -> str:
    # TODO: POST to /api/generate with model="llama3.2", the prompt, and stream=False.
    # Return the "response" field from the JSON.
    pass


def part_b():
    print("\n=== Part B: Generation ===")
    prompt = "In one sentence, what is retrieval-augmented generation?"

    start = time.time()
    response = generate(prompt)
    elapsed = time.time() - start

    # TODO: Print the response and the elapsed time.
    pass


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    part_a()
    part_b()

    # Part C: add your observations as comments here.
    # - Was the embedding norm close to 1.0?
    # - How long did generation take?
