---
slug: /03-cloud-models
---

# 03 - Cloud Models

> **Goal:** Make the pipeline model-agnostic. Swap Ollama for the Gemini API with minimal code changes. Understand the trade-offs between local and cloud inference so you can choose deliberately.

---

## Theory

### Local vs cloud inference

Throughout Foundations and the first two Naive RAG modules, everything ran locally via Ollama. That was intentional: local inference is transparent, free, and offline. But local models have real limitations.

| | Local (Ollama) | Cloud (Gemini, OpenAI, etc.) |
|---|---|---|
| Cost | Free | Pay per token |
| Latency | Depends on hardware | Fast, consistent |
| Privacy | Data stays on machine | Data leaves machine |
| Model quality | Good for small models | State-of-the-art |
| Setup | Requires Ollama + GPU/CPU | Just an API key |
| Rate limits | None | Yes |

Neither is universally better. The right choice depends on your data sensitivity, budget, and quality requirements. The wrong choice is coupling your code so tightly to one provider that switching is painful.

---

### Model-agnostic design

The fix is a thin abstraction over the generation step. Keep the embedding and retrieval code unchanged - only the generation function needs to know which model it is using.

```python
from abc import ABC, abstractmethod

class Generator(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...

class OllamaGenerator(Generator):
    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def generate(self, prompt: str) -> str:
        import requests
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["response"].strip()

class GeminiGenerator(Generator):
    def __init__(self, model: str = "gemini-2.0-flash"):
        import google.generativeai as genai
        import os
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel(model)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()
```

Your pipeline function then accepts a `Generator` instance:

```python
def ask(question: str, index, chunks: list[str], generator: Generator, k: int = 5) -> str:
    top_chunks = retrieve(question, index, chunks, k=k)
    context = [c["text"] for c in top_chunks]
    prompt = build_prompt(context, question)
    return generator.generate(prompt)
```

Switching models is now one line:

```python
# Local
answer = ask(question, index, chunks, generator=OllamaGenerator())

# Cloud
answer = ask(question, index, chunks, generator=GeminiGenerator())
```

---

### The Gemini API

Google Gemini is accessible via the `google-generativeai` Python package. The free tier is generous enough for development and experimentation.

Install:

```bash
pip install google-generativeai
```

Get an API key from [Google AI Studio](https://aistudio.google.com/) and store it as an environment variable - never hardcode it:

```bash
export GEMINI_API_KEY="your-key-here"
```

Basic call:

```python
import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("What is retrieval-augmented generation?")
print(response.text)
```

`gemini-2.0-flash` is fast and cheap. Use `gemini-1.5-pro` when you need higher quality or a larger context window (1 million tokens).

---

### API key management

Never put API keys in source files. Use environment variables or a `.env` file (never committed to git):

```bash
# .env  (add this to .gitignore)
GEMINI_API_KEY=your-key-here
```

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ["GEMINI_API_KEY"]
```

Install `python-dotenv` to load `.env` files automatically. This pattern works identically for any API key - OpenAI, Anthropic, Cohere - so get into the habit now.

---

### Embeddings in the cloud

This module keeps Ollama for embeddings and only swaps the generator. That is intentional: you already have a working embedding pipeline, and mixing embedding providers mid-project breaks your index (vectors from different models live in different spaces and cannot be compared).

If you want to move embeddings to the cloud too - for example to use Google's `text-embedding-004` model - you need to rebuild the index from scratch with the new embedding model.

```python
import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def embed_cloud(text: str) -> list[float]:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
    )
    return result["embedding"]
```

The dimension for `text-embedding-004` is 768 - same as `nomic-embed-text` - so the index shape stays the same, but the vector space is different. Rebuild, do not reuse.

---

### Rate limits and error handling

Cloud APIs enforce rate limits. Production code needs retries:

```python
import time

def generate_with_retry(model, prompt: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            return model.generate_content(prompt).text.strip()
        except Exception as e:
            if attempt == retries - 1:
                raise
            wait = 2 ** attempt
            print(f"Error: {e}. Retrying in {wait}s...")
            time.sleep(wait)
```

Exponential backoff (1s, 2s, 4s) handles transient rate limit errors without hammering the API.

---

### Key takeaways

- Local models are free and private. Cloud models are faster and more capable. Choose based on your requirements, not convenience.
- Abstract the generator behind an interface. Switching providers should be one line, not a refactor.
- Store API keys in environment variables. Never hardcode them or commit them to git.
- Keep your embedding model consistent within an index. Switching embedding providers requires rebuilding the index.
- Add retry logic with exponential backoff for cloud API calls.

---

## Exercises

1. [Your First Gemini Call](./exercises/01-gemini-call) - call the Gemini API and compare output to llama3.2
2. [Swap the Generator](./exercises/02-swap-generator) - introduce the Generator abstraction and switch models with one line

---

## Project - Part 3 (Naive RAG)

See [`project/`](./project/).

---

[← 02 Generation](../02-generation/)
