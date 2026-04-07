---
slug: /01-embeddings
---

# 01: Embeddings

> **Goal:** Understand what embeddings are, why normalization matters, and how similarity search works. By the end you will be able to embed text with Ollama and measure how semantically close two pieces of text are.

---

## Theory

### What is an embedding?

An embedding is a list of floating point numbers that represents the meaning of a piece of text.

```python
"The cat sat on the mat"  ->  [0.023, -0.418, 0.761, ..., 0.094]  # 768 numbers
```

The model (`nomic-embed-text`) is trained so that text with similar meaning produces similar vectors. That is the entire idea. Everything else (retrieval, similarity search, RAG) flows from that one property.

A few things to internalise early:

- The individual numbers mean nothing on their own. You never inspect dimension 42 and conclude "this is about cats." The meaning is encoded collectively across all 768 dimensions.
- The same model must be used for both indexing and querying. Vectors from different models live in different spaces and cannot be compared.
- Longer text does not produce longer vectors. Whether you embed a single word or a 500-word paragraph, you always get 768 numbers back. This is why chunking (module 02) matters: you lose information when you compress too much text into one vector.

---

### Vector spaces

Picture a 2D map where every word is a point. Words with related meanings cluster together. "Dog" and "cat" are close. "Quantum" and "entanglement" are close. "Dog" and "quantum" are far apart.

Real embedding models use 768 dimensions instead of 2, but the intuition is the same. The model places semantically related text in the same neighbourhood of this high-dimensional space.

A classic illustration of what the model learns:

```
king - man + woman = queen
```

The vector arithmetic works because the model has learned that the direction from "man" to "woman" encodes gender, and the same direction applies equally to "king" -> "queen". This is geometry, not magic.

---

### Measuring similarity

Once text is in vector space, you measure similarity by measuring how close two vectors are. There are a few ways to do this.

**Euclidean distance** is the straight-line distance between two points. It works, but it is sensitive to the *magnitude* (length) of the vectors. A long vector and a short vector pointing in exactly the same direction would have non-zero distance despite being semantically identical.

**Cosine similarity** measures the *angle* between two vectors, ignoring their magnitude. Two vectors pointing in the same direction have cosine similarity of 1.0 (identical meaning). Opposite directions give -1.0. Perpendicular gives 0.

```
cosine_similarity(A, B) = (A . B) / (|A| x |B|)
```

This is what you want for semantic search. The content matters, not how "loud" the embedding is.

**Dot product** is just `A . B` with no normalisation. It is the fastest operation, but magnitude affects the result.

Here is the trick: if you **L2-normalise** all vectors to unit length before storing them, their magnitude is always 1. Then:

```
dot_product(A, B) = cosine_similarity(A, B)
```

You get cosine similarity at dot-product speed. This is exactly what the reference implementation in `reference/local-rag-faiss/` does, and it is why FAISS's `IndexFlatIP` (inner product) works correctly there.

---

### L2 normalisation

Normalising a vector means dividing it by its own length so the result has length 1.

```python
import numpy as np

def l2_normalise(v: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(v)
    return v / (norm + 1e-10)   # small epsilon avoids division by zero
```

Before normalisation:
```python
v = np.array([3.0, 4.0])
np.linalg.norm(v)   # -> 5.0
```

After normalisation:
```python
v_norm = l2_normalise(v)   # -> [0.6, 0.8]
np.linalg.norm(v_norm)     # -> 1.0
```

In practice you normalise an entire batch at once:

```python
def normalise_batch(embeddings: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / (norms + 1e-10)
```

**Always normalise before storing vectors in your index.** If you forget, similarity scores will be distorted by magnitude differences between chunks. Longer chunks tend to have larger magnitude and will score higher regardless of relevance.

---

### Getting embeddings with Ollama

`nomic-embed-text` produces 768-dimensional embeddings and runs entirely on your machine. The API call is a simple POST:

```python
import requests
import numpy as np

def embed(text: str) -> np.ndarray:
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    response.raise_for_status()
    vector = np.array(response.json()["embedding"], dtype=np.float32)
    return vector / (np.linalg.norm(vector) + 1e-10)   # normalise immediately

a = embed("The transformer architecture relies on self-attention.")
b = embed("Attention mechanisms are central to modern NLP models.")
c = embed("The stock market closed up 2% on Friday.")

print(np.dot(a, b))   # high: semantically close
print(np.dot(a, c))   # low:  unrelated topics
```

---

### Key takeaways

- Embeddings convert text into vectors that encode semantic meaning.
- Similar meaning produces similar vectors with high cosine similarity.
- L2 normalisation makes dot product equal to cosine similarity. Always do it.
- Use the same model for indexing and querying.
- The embedding dimension (768 for `nomic-embed-text`) is fixed regardless of input length.

---

## Exercises

1. [Your First Embedding](./exercises/01-first-embedding) — call the API and inspect the raw output
2. [Similarity](./exercises/02-similarity) — compare pairs of sentences and build score intuition
3. [Normalisation](./exercises/03-normalisation) — see what breaks when you skip L2 normalisation

---

## Project: Part 1

See [`project/`](./project/).

You will write a function that loads a list of text chunks and returns a normalised embedding matrix. This becomes the foundation of the retrieval pipeline you build in later modules.

---

[← 00 Setup](../00-setup/) · [02 Chunking →](../02-chunking/)
