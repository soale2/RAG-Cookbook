"""
Exercise 2: Full Pipeline
==========================
Wire retrieval and generation into a single ask() function.
This is a complete naive RAG system.

Run:
    python exercises/02_full_pipeline.py
"""

import json

import faiss
import numpy as np
import requests


INDEX_PATH = "../../../foundations/03-vector-stores/exercises/index.faiss"
CHUNKS_PATH = "../../../foundations/03-vector-stores/exercises/chunks.json"


def embed(text: str) -> np.ndarray:
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype=np.float32)
    return v / (np.linalg.norm(v) + 1e-10)


def load_index() -> tuple[faiss.IndexFlatIP, list[str]]:
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH) as f:
        chunks = json.load(f)
    return index, chunks


def retrieve(question: str, index, chunks: list[str], k: int) -> list[dict]:
    # TODO: Same as Retrieval Exercise 1.
    pass


def build_prompt(context_chunks: list[str], question: str) -> str:
    # TODO: Use the strict prompt from Generation Exercise 1.
    pass


def generate(prompt: str) -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["response"].strip()


def ask(question: str, index, chunks: list[str], k: int = 5, verbose: bool = False) -> str:
    # TODO:
    # 1. Retrieve top-k chunks.
    # 2. Build the prompt.
    # 3. If verbose=True, print the full prompt.
    # 4. Generate and return the answer.
    pass


if __name__ == "__main__":
    index, chunks = load_index()

    questions = [
        "What is the main contribution of this paper?",
        "What hardware was used for training?",
        "What BLEU score was achieved?",
        "What are the limitations of this approach?",
        "Who won the 2024 FIFA World Cup?",   # out-of-corpus
    ]

    for question in questions:
        print(f"\nQ: {question}")

        results = retrieve(question, index, chunks, k=5)
        print("  Retrieved:")
        for r in results:
            print(f"    [{r['score']:.3f}] {r['text'][:80]!r}")

        answer = ask(question, index, chunks, k=5)
        print(f"  A: {answer}")
