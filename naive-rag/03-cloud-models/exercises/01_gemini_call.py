"""
Exercise 1: Your First Gemini Call
=====================================
Call the Gemini API and compare output to llama3.2 on the same prompts.

Run:
    python exercises/01_gemini_call.py

Prerequisites:
    pip install google-generativeai
    export GEMINI_API_KEY="your-key"
"""

import os
import time
import requests


def generate_ollama(prompt: str, model: str = "llama3.2") -> tuple[str, float]:
    """Returns (response_text, elapsed_seconds)."""
    # TODO: POST to Ollama /api/generate with stream=False. Return text and timing.
    pass


def generate_gemini(prompt: str, model: str = "gemini-2.0-flash") -> tuple[str, float]:
    """Returns (response_text, elapsed_seconds)."""
    # TODO:
    # 1. import google.generativeai as genai
    # 2. genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    # 3. Create a GenerativeModel and call generate_content(prompt).
    # 4. Return response.text and timing.
    pass


PROMPTS = [
    "In one sentence, what is self-attention in transformer models?",
    (
        "Summarise this in one sentence: "
        "'Retrieval-Augmented Generation combines a retrieval system with a language model. "
        "The retrieval system finds relevant documents, which are passed to the model as context. "
        "This grounds the model's output in real source material and reduces hallucination.'"
    ),
    "What was the score in last night's football match?",
]


if __name__ == "__main__":
    for prompt in PROMPTS:
        display = prompt if len(prompt) < 80 else prompt[:77] + "..."
        print(f"\nPrompt: {display!r}")
        print("-" * 60)

        ollama_text, ollama_time = generate_ollama(prompt)
        print(f"llama3.2  ({ollama_time:.2f}s):\n  {ollama_text}")

        gemini_text, gemini_time = generate_gemini(prompt)
        print(f"Gemini    ({gemini_time:.2f}s):\n  {gemini_text}")
