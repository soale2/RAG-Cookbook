# pipeline.py
"""
Project Part 3b: Model-Agnostic Pipeline
==========================================
Final version of the naive RAG pipeline. The generator is
injected, so switching between Ollama and Gemini (or any
future provider) is a single-line change.

Usage:
    python pipeline.py                  # Ollama only
    python pipeline.py --gemini         # compare Ollama vs Gemini
    python pipeline.py --gemini-only    # Gemini only
"""

import argparse
import sys
from pathlib import Path

# Add earlier project modules to the import path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "01-retrieval" / "project"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "02-generation" / "project"))

from retriever import load_index, retrieve_top_k, retrieve_mmr  # noqa: E402
from prompt import build_prompt, has_answer  # noqa: E402
from generator import Generator, OllamaGenerator, GeminiGenerator  # noqa: E402


def ask(
    question: str,
    index,
    chunks: list[str],
    generator: Generator,
    k: int = 5,
    use_mmr: bool = False,
) -> dict:
    """
    Full naive RAG pipeline with pluggable generator.
    """
    if use_mmr:
        results = retrieve_mmr(question, index, chunks, k=k)
    else:
        results = retrieve_top_k(question, index, chunks, k=k)

    context = [r["text"] for r in results]
    prompt = build_prompt(context, question)
    answer = generator.generate(prompt)

    return {
        "question": question,
        "answer": answer,
        "generator": repr(generator),
        "has_answer": has_answer(answer),
        "sources": [
            {"score": r["score"], "preview": r["text"][:120]} for r in results
        ],
    }


QUESTIONS = [
    "What is the main contribution of this paper?",
    "What hardware was used for training?",
    "What BLEU score was achieved?",
    "What are the limitations of this approach?",
    "Who won the 2024 FIFA World Cup?",  # out-of-corpus
]


def run(generators: list[Generator], questions: list[str] = QUESTIONS):
    print("Loading index...")
    index, chunks = load_index()
    print(f"  {index.ntotal} vectors, {len(chunks)} chunks\n")

    for question in questions:
        print(f"Q: {question}")
        for gen in generators:
            result = ask(question, index, chunks, generator=gen)
            label = repr(gen)
            declined = "" if result["has_answer"] else " [declined]"
            print(f"  {label}: {result['answer']}{declined}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Naive RAG pipeline")
    parser.add_argument("--gemini", action="store_true", help="Compare Ollama and Gemini side by side")
    parser.add_argument("--gemini-only", action="store_true", help="Use Gemini only")
    args = parser.parse_args()

    if args.gemini_only:
        generators = [GeminiGenerator()]
    elif args.gemini:
        generators = [OllamaGenerator(), GeminiGenerator()]
    else:
        generators = [OllamaGenerator()]

    run(generators)
