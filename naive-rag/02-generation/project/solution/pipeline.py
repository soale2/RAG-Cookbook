# pipeline.py
"""
Project Part 2b: Naive RAG Pipeline
=====================================
Wires retrieval (Part 1) and generation into a complete Q&A loop.
Uses Ollama for both embedding and generation.

Usage:
    python pipeline.py
"""

import sys
from pathlib import Path

import requests

# Add Part 1 project to the import path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "01-retrieval" / "project"))

from retriever import load_index, retrieve_top_k, retrieve_mmr  # noqa: E402
from prompt import build_prompt, has_answer  # noqa: E402


def generate(prompt: str, model: str = "llama3.2") -> str:
    """Generate a response via Ollama."""
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["response"].strip()


def ask(
    question: str,
    index,
    chunks: list[str],
    k: int = 5,
    use_mmr: bool = False,
    verbose: bool = False,
) -> dict:
    """
    Full naive RAG pipeline: retrieve, build prompt, generate.

    Returns a dict with the answer and metadata about the retrieval.
    """
    # 1. Retrieve
    if use_mmr:
        results = retrieve_mmr(question, index, chunks, k=k)
    else:
        results = retrieve_top_k(question, index, chunks, k=k)

    context = [r["text"] for r in results]

    # 2. Build prompt
    prompt = build_prompt(context, question)

    if verbose:
        print(f"\n{'='*60}")
        print("FULL PROMPT:")
        print(f"{'='*60}")
        print(prompt)
        print(f"{'='*60}\n")

    # 3. Generate
    answer = generate(prompt)

    return {
        "question": question,
        "answer": answer,
        "has_answer": has_answer(answer),
        "sources": [
            {"score": r["score"], "preview": r["text"][:120]} for r in results
        ],
    }


if __name__ == "__main__":
    print("Loading index...")
    index, chunks = load_index()
    print(f"  {index.ntotal} vectors, {len(chunks)} chunks\n")

    questions = [
        "What is the main contribution of this paper?",
        "What hardware was used for training?",
        "What BLEU score was achieved?",
        "What are the limitations of this approach?",
        "Who won the 2024 FIFA World Cup?",  # out-of-corpus
    ]

    for question in questions:
        print(f"Q: {question}")
        result = ask(question, index, chunks, k=5)

        print(f"A: {result['answer']}")
        if not result["has_answer"]:
            print("  (model declined to answer)")
        print("  Sources:")
        for src in result["sources"]:
            print(f"    [{src['score']:.3f}] {src['preview']!r}")
        print()
