---
slug: /00-setup
---

# 00 — Setup

> **Goal:** Get your local environment ready. By the end you will have Ollama running, the right models pulled, and have made your first embedding call from Python.

---

## Theory

### Why local-first?

Most RAG tutorials send every chunk and every query to a cloud API. That costs money, leaks data, and hides what is actually happening. This curriculum runs entirely on your machine during the foundations and naive RAG stages. You will see real latency, real memory usage, and real trade-offs — then move to cloud models deliberately in module 03 of Naive RAG, not by default.

The two tools you need are **Ollama** (runs LLMs and embedding models locally) and a **Python virtual environment** (isolates project dependencies).

---

### Ollama

Ollama is a server that runs open-weight models locally via a simple REST API. Once it is running, you interact with it exactly like a cloud API — just pointed at `localhost` instead.

Start the server:

```bash
ollama serve
```

Ollama listens on `http://localhost:11434` by default. It manages model downloads, GPU/CPU scheduling, and keeps models warm in memory between calls.

#### Models used in this curriculum

| Model | Purpose | Size |
|-------|---------|------|
| `nomic-embed-text` | Embeddings (768 dims) | ~270 MB |
| `llama3.2` | Text generation | ~2 GB |

Pull them before starting:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

Verify they are available:

```bash
ollama list
```

---

### Embedding API

The embedding endpoint takes a string and returns a vector:

```python
import requests
import numpy as np

response = requests.post(
    "http://localhost:11434/api/embeddings",
    json={"model": "nomic-embed-text", "prompt": "Hello, world."},
    timeout=30,
)
vector = np.array(response.json()["embedding"], dtype=np.float32)
print(vector.shape)   # (768,)
```

This is the call you will make thousands of times throughout the curriculum. Keep it in muscle memory.

---

### Generation API

The generation endpoint streams tokens by default. Pass `"stream": false` to get the full response at once:

```python
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2",
        "prompt": "What is retrieval-augmented generation?",
        "stream": False,
    },
    timeout=60,
)
print(response.json()["response"])
```

---

### Python environment

Always work inside a virtual environment. It prevents dependency conflicts and makes the project reproducible.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Confirm the key packages installed:

```python
import numpy as np
import requests
import faiss
print("All good.")
```

---

### Verifying the full setup

Run this end-to-end smoke test before moving on:

```python
import requests
import numpy as np

def embed(text: str) -> np.ndarray:
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype=np.float32)
    return v / np.linalg.norm(v)

a = embed("Retrieval-augmented generation grounds LLMs in facts.")
b = embed("RAG reduces hallucination by providing source documents.")
c = embed("The price of eggs went up this quarter.")

print(f"a·b = {np.dot(a, b):.4f}")   # should be high (~0.85+)
print(f"a·c = {np.dot(a, c):.4f}")   # should be low  (~0.5 or less)
```

If both similarity scores look plausible, your environment is ready.

---

### Key takeaways

- Ollama runs LLMs and embedding models locally via a REST API on `localhost:11434`.
- Always normalise embedding vectors immediately after receiving them.
- Use a virtual environment — never install project packages globally.
- The embedding and generation APIs are simple HTTP POST calls. No SDK required.

---

## Exercises

1. [Verify Ollama](./exercises/01-verify-ollama) — confirm models are installed and the server is running
2. [First API Calls](./exercises/02-first-calls) — make a real embedding call and a real generation call

---

## Next

[01 - Embeddings →](../01-embeddings/)
