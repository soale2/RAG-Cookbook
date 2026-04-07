"""
Exercise 2: Swap the Generator
================================
Introduce a Generator abstraction and run the full pipeline
with both Ollama and Gemini using a single line change.

Run:
    python exercises/02_swap_generator.py
"""

import json
import os
from abc import ABC, abstractmethod

import faiss
import numpy as np
import requests


INDEX_PATH = "../../../foundations/03-vector-stores/exercises/index.faiss"
CHUNKS_PATH = "../../../foundations/03-vector-stores/exercises/chunks.json"


# ── Generator abstraction ─────────────────────────────────────────────────────

class Generator(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...


class OllamaGenerator(Generator):
    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def generate(self, prompt: str) -> str:
        # TODO: POST to Ollama /api/generate, return response text.
        pass


class GeminiGenerator(Generator):
    def __init__(self, model: str = "gemini-2.0-flash"):
        # TODO:
        # import google.generativeai as genai
        # genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        # self._model = genai.GenerativeModel(model)
        pass

    def generate(self, prompt: str) -> str:
        # TODO: Call self._model.generate_content(prompt), return response text.
        pass


# ── Pipeline ──────────────────────────────────────────────────────────────────

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
    # TODO: Same as before.
    pass


def build_prompt(context_chunks: list[str], question: str) -> str:
    # TODO: Same strict prompt as before.
    pass


def ask(question: str, index, chunks: list[str], generator: Generator, k: int = 5) -> str:
    # TODO: Retrieve -> build prompt -> generator.generate(prompt) -> return answer.
    pass


# ── Main ──────────────────────────────────────────────────────────────────────

QUESTIONS = [
    "What is the main contribution of this paper?",
    "What hardware was used for training?",
    "What BLEU score was achieved?",
    "What are the limitations?",
    "Who invented the telephone?",   # out-of-corpus
]

if __name__ == "__main__":
    index, chunks = load_index()

    ollama = OllamaGenerator()
    gemini = GeminiGenerator()

    for question in QUESTIONS:
        print(f"\nQ: {question}")
        print(f"  Ollama : {ask(question, index, chunks, ollama)}")
        print(f"  Gemini : {ask(question, index, chunks, gemini)}")
