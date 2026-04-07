---
slug: /01-retrieval
---

# 01 — Retrieval

> **Goal:** Build a retriever that takes a natural language query and returns the most relevant chunks from your vector store. Learn top-k search, how to interpret similarity scores, and how MMR improves result diversity.

---

## Theory

### The retrieval problem

You have embedded and indexed thousands of chunks. Given a user's question, you need to find the handful of chunks most likely to contain the answer. This is the retrieval step.

The query goes through the same embedding model as the chunks:

```
query text  →  embed  →  query vector  →  search index  →  top-k chunks
```

The model has been trained so that semantically similar text produces similar vectors. A good query vector lands near the vectors of chunks that answer the question.

---

### Top-k similarity search

The most direct retrieval strategy: return the `k` chunks with the highest similarity score.

```python
import numpy as np
import faiss

def retrieve(query_text: str, index, chunks: list[str], k: int = 5) -> list[dict]:
    query_vec = embed(query_text)                          # embed and normalise
    query_vec = query_vec.reshape(1, -1).astype(np.float32)

    scores, positions = index.search(query_vec, k)

    results = []
    for score, pos in zip(scores[0], positions[0]):
        results.append({
            "text": chunks[pos],
            "score": float(score),
        })
    return results
```

`k` is the single most important retrieval parameter. Too small and you risk missing the relevant chunk. Too large and you flood the LLM with irrelevant context, hurting generation quality. Start with `k=5` and tune from there.

---

### Interpreting similarity scores

With L2-normalised vectors and inner product, scores are cosine similarities in the range [-1, 1]:

| Score | Interpretation |
|-------|---------------|
| 0.90+ | Near-identical meaning |
| 0.75–0.90 | Strongly related |
| 0.60–0.75 | Somewhat related |
| Below 0.60 | Probably not relevant |

These thresholds are rough guides — they vary by embedding model and domain. What matters more than the absolute score is the **gap** between results. If the top result scores 0.88 and the fifth scores 0.61, the top result is clearly stronger. If all five cluster around 0.70, the query may be ambiguous.

You can filter by a minimum score threshold:

```python
MIN_SCORE = 0.65

results = [r for r in retrieve(query, index, chunks, k=10) if r["score"] >= MIN_SCORE]
```

---

### The redundancy problem

Top-k has a subtle failure mode: the top results are often near-duplicates of each other. If three chunks from the same paragraph were indexed, they will all score highly for related queries. You retrieve three chunks but get roughly one chunk worth of unique information.

---

### Maximal Marginal Relevance (MMR)

MMR balances relevance with diversity. Instead of picking the top-k most similar chunks all at once, it picks them one at a time:

1. Add the single most similar chunk to the result set.
2. For each remaining candidate, compute a score that rewards similarity to the query and penalises similarity to already-selected chunks.
3. Add the best-scoring candidate. Repeat until you have `k` results.

```python
def mmr(
    query_vec: np.ndarray,
    candidate_vecs: np.ndarray,
    candidate_texts: list[str],
    k: int = 5,
    lambda_: float = 0.5,
) -> list[str]:
    selected_indices = []
    remaining = list(range(len(candidate_vecs)))

    while len(selected_indices) < k and remaining:
        if not selected_indices:
            # First pick: most similar to query
            scores = candidate_vecs[remaining] @ query_vec
            best = remaining[int(np.argmax(scores))]
        else:
            selected_vecs = candidate_vecs[selected_indices]
            query_scores = candidate_vecs[remaining] @ query_vec
            redundancy = (candidate_vecs[remaining] @ selected_vecs.T).max(axis=1)
            mmr_scores = lambda_ * query_scores - (1 - lambda_) * redundancy
            best = remaining[int(np.argmax(mmr_scores))]

        selected_indices.append(best)
        remaining.remove(best)

    return [candidate_texts[i] for i in selected_indices]
```

`lambda_` controls the trade-off: 1.0 is pure relevance (equivalent to top-k), 0.0 is pure diversity. 0.5 is a good starting point.

Use MMR when your corpus has many similar chunks (e.g. multiple papers covering the same topic) or when users ask broad questions that deserve varied coverage.

---

### Metadata filtering

Sometimes you want to restrict retrieval to a subset of documents — for example, only search a specific paper, or only chunks from the last year. This is metadata filtering, and it is done before or during the vector search:

```python
# With ChromaDB
results = collection.query(
    query_embeddings=[query_vec.tolist()],
    n_results=5,
    where={"source": "attention_is_all_you_need.pdf"},
)
```

With FAISS, pre-filtering requires you to build a subset index or post-filter by checking metadata after retrieval. This is one of the reasons ChromaDB is preferable when filtering is a core requirement.

---

### Key takeaways

- Retrieval is a nearest-neighbour search: embed the query, find the closest chunk vectors.
- `k=5` is a reasonable starting point. Too large floods the LLM; too small risks missing the answer.
- Scores above ~0.75 are generally good matches. Pay attention to the gap between results, not just the absolute values.
- Top-k returns redundant results when chunks overlap. MMR trades some relevance for diversity.
- Use metadata filtering to scope retrieval when the question is clearly about a specific source.

---

## Exercises

1. [Top-k Retrieval](./exercises/01-top-k) — build a retriever and run it against your FAISS index
2. [Score Threshold](./exercises/02-score-threshold) — filter out irrelevant results using a minimum similarity score
3. [MMR](./exercises/03-mmr) — implement Maximal Marginal Relevance and compare diversity against top-k

---

## Project — Part 1 (Naive RAG)

See [`project/`](./project/).

---

[← Foundations](../../foundations/) · [02 Generation →](../02-generation/)
