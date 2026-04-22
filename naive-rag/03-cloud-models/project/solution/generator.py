# generator.py
"""
Project Part 3a: Generator Abstraction
========================================
ABC + concrete implementations for Ollama and Gemini.
Adding a new provider means adding one class.
"""

import os
import time
from abc import ABC, abstractmethod

import requests


class Generator(ABC):
    """Base class for all LLM generators."""

    @abstractmethod
    def generate(self, prompt: str) -> str: ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class OllamaGenerator(Generator):
    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def generate(self, prompt: str) -> str:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["response"].strip()

    def __repr__(self) -> str:
        return f"OllamaGenerator(model={self.model!r})"


class GeminiGenerator(Generator):
    def __init__(self, model: str = "gemini-2.0-flash", retries: int = 3):
        import google.generativeai as genai

        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self._model = genai.GenerativeModel(model)
        self._model_name = model
        self._retries = retries

    def generate(self, prompt: str) -> str:
        for attempt in range(self._retries):
            try:
                response = self._model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                if attempt == self._retries - 1:
                    raise
                wait = 2 ** attempt
                print(f"  Gemini error: {e}. Retrying in {wait}s...")
                time.sleep(wait)

    def __repr__(self) -> str:
        return f"GeminiGenerator(model={self._model_name!r})"
