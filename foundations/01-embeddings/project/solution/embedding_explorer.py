# embedding_explorer.py
"""
Solution: Embedding Explorer
==============================
Embed arbitrary text pairs and display cosine similarity with interpretation.

Usage:
    python embedding_explorer.py "sentence one" "sentence two"
    python embedding_explorer.py --interactive
    python embedding_explorer.py --file pairs.txt
"""

import argparse
import sys

import numpy as np
import requests


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


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two L2-normalised vectors (dot product)."""
    return float(np.dot(a, b))


def interpret_score(score: float) -> str:
    """Human-readable interpretation of a cosine similarity score."""
    if score >= 0.90:
        return "near-identical meaning"
    elif score >= 0.75:
        return "strongly related"
    elif score >= 0.60:
        return "somewhat related"
    else:
        return "probably not relevant"


def compare(text_a: str, text_b: str, model: str = "nomic-embed-text") -> dict:
    """Embed two texts and return similarity info."""
    vec_a = embed(text_a, model=model)
    vec_b = embed(text_b, model=model)
    score = cosine_similarity(vec_a, vec_b)
    return {
        "text_a": text_a,
        "text_b": text_b,
        "score": score,
        "interpretation": interpret_score(score),
        "dimensions": len(vec_a),
    }


def print_result(result: dict):
    print(f"\n  A: {result['text_a']!r}")
    print(f"  B: {result['text_b']!r}")
    print(f"  Similarity: {result['score']:.4f} ({result['interpretation']})")
    print(f"  Dimensions: {result['dimensions']}")


def run_interactive():
    """Interactive mode: keep asking for pairs until user quits."""
    print("Embedding Explorer (type 'quit' to exit)\n")
    while True:
        text_a = input("Text A: ").strip()
        if text_a.lower() == "quit":
            break
        text_b = input("Text B: ").strip()
        if text_b.lower() == "quit":
            break
        result = compare(text_a, text_b)
        print_result(result)
        print()


def run_file(path: str):
    """Read pairs from a file (one pair per two lines, blank line between pairs)."""
    with open(path) as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) % 2 != 0:
        print(f"Error: file must have an even number of non-empty lines, got {len(lines)}")
        sys.exit(1)

    for i in range(0, len(lines), 2):
        result = compare(lines[i], lines[i + 1])
        print_result(result)
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare text similarity via embeddings")
    parser.add_argument("texts", nargs="*", help="Two texts to compare")
    parser.add_argument("--interactive", action="store_true", help="Interactive pair mode")
    parser.add_argument("--file", type=str, help="File with text pairs (two lines per pair)")
    args = parser.parse_args()

    if args.interactive:
        run_interactive()
    elif args.file:
        run_file(args.file)
    elif len(args.texts) == 2:
        result = compare(args.texts[0], args.texts[1])
        print_result(result)
    else:
        print("Usage: provide two texts, --interactive, or --file")
        print('  python embedding_explorer.py "text one" "text two"')
        sys.exit(1)
