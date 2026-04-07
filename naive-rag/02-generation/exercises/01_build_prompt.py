"""
Exercise 1: Build a RAG Prompt
================================
Write prompt variants and test how instruction wording affects faithfulness.

Run:
    python exercises/01_build_prompt.py
"""

import requests


def generate(prompt: str, model: str = "llama3.2") -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["response"].strip()


def build_prompt_loose(context_chunks: list[str], question: str) -> str:
    # TODO: Join chunks with a clear separator, then write a loose instruction.
    pass


def build_prompt_strict(context_chunks: list[str], question: str) -> str:
    # TODO: Same structure, but instruct the model to use ONLY the context
    # and say "I don't have enough information" if the answer isn't there.
    pass


def build_prompt_explicit(context_chunks: list[str], question: str) -> str:
    # TODO: Same as strict, but add an explicit "do not use outside knowledge" clause.
    pass


# ── Sample context ────────────────────────────────────────────────────────────
# Replace these with real chunks from your document.

CONTEXT = [
    "The transformer model introduced in 'Attention Is All You Need' (2017) relies entirely on self-attention mechanisms, dispensing with recurrence and convolutions entirely.",
    "The model achieves state-of-the-art results on WMT 2014 English-to-German translation with a BLEU score of 28.4.",
    "Training was performed on 8 NVIDIA P100 GPUs for 12 hours for the base model.",
]

IN_CONTEXT_QUESTION = "What BLEU score did the model achieve on English-to-German translation?"
OUT_OF_CONTEXT_QUESTION = "What year was PyTorch first released?"


if __name__ == "__main__":
    for label, build_fn in [
        ("Loose",    build_prompt_loose),
        ("Strict",   build_prompt_strict),
        ("Explicit", build_prompt_explicit),
    ]:
        print(f"\n{'='*50}")
        print(f"Instruction variant: {label}")
        print(f"{'='*50}")

        print(f"\nIn-context question: {IN_CONTEXT_QUESTION!r}")
        prompt = build_fn(CONTEXT, IN_CONTEXT_QUESTION)
        print(f"Answer: {generate(prompt)}\n")

        print(f"Out-of-context question: {OUT_OF_CONTEXT_QUESTION!r}")
        prompt = build_fn(CONTEXT, OUT_OF_CONTEXT_QUESTION)
        print(f"Answer: {generate(prompt)}")
