---
slug: /01-retrieval/project
---

# Project Part 1: Retriever Module

> Build a reusable retriever with top-k search, score filtering, and MMR.

---

## Brief

The exercises had you writing retrieval functions inline. Now build a proper module that the generation pipeline will import in Part 2.

Your retriever should expose three capabilities:

1. **Top-k retrieval** - return the `k` most similar chunks for a query
2. **Score-filtered retrieval** - same as top-k, but drop results below a minimum similarity threshold
3. **MMR retrieval** - fetch a larger candidate set, then re-rank using Maximal Marginal Relevance to balance relevance with diversity

All three should return a list of dicts with `text`, `score`, and `index` (the FAISS position).

---

## Example output

```
Loading index...
  147 vectors, 147 chunks

Query: 'What is the main contribution of this paper?'

--- Top-k (k=5) ---
  [0.8821] 'We propose a new simple network architecture, the Transfor...'
  [0.8654] 'The dominant sequence transduction models are based on com...'
  ...

--- Top-k with min_score=0.70 ---
  [0.8821] 'We propose a new simple network architecture, the Transfor...'
  [0.8654] 'The dominant sequence transduction models are based on com...'
  (3 results above threshold)

--- MMR (k=5, lambda=0.5) ---
  [0.8821] 'We propose a new simple network architecture, the Transfor...'
  [0.7912] 'In this work we propose the Transformer, a model architec...'
  (results are more diverse)
```

---

## Requirements

- [ ] `load_index()` - loads FAISS index and chunk texts from Foundations output
- [ ] `retrieve_top_k(query, index, chunks, k, min_score)` - top-k with optional threshold
- [ ] `retrieve_mmr(query, index, chunks, k, candidates, lambda_)` - MMR re-ranking
- [ ] Each result includes `text`, `score`, and `index`
- [ ] Module is importable (Part 2 will `from retriever import ...`)

## Stretch goals

- Add metadata filtering (e.g., restrict to a specific source document)
- Log the score gap between the top result and the k-th result
- Compare top-k vs MMR results side by side for the same query
