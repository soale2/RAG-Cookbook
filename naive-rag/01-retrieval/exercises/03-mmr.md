---
slug: /01-retrieval/exercises/03-mmr
---

# Exercise 3 - Maximal Marginal Relevance

> **Goal:** Implement MMR and see how it trades a small amount of relevance for meaningfully more diverse results.

---

## Background

Top-k retrieval often returns near-duplicate chunks - three slightly different versions of the same sentence. MMR fixes this by penalising candidates that are too similar to already-selected results.

The score for each remaining candidate is:

```
mmr_score = λ × sim(candidate, query) − (1 − λ) × max_sim(candidate, selected)
```

`λ = 1.0` is pure top-k. `λ = 0.0` is maximum diversity. `λ = 0.5` is the usual starting point.

---

## Assignment

Open `03_mmr.py`.

1. Implement `mmr(query_vec, candidate_vecs, candidate_texts, k, lambda_)` following the algorithm above. Select results one at a time, each time picking the candidate with the highest MMR score.
2. Write a wrapper `retrieve_mmr(query, index, chunks, k, lambda_)` that:
   - Fetches a larger candidate pool (e.g. top-50) from the FAISS index
   - Runs your MMR implementation over that pool
   - Returns the final k results
3. For each of three queries, run both `retrieve` (top-k) and `retrieve_mmr` side by side. Print the top-5 results from each.
4. Look for cases where top-k returns near-duplicates and MMR does not.

---

## Thinking questions

- MMR requires computing similarities between all pairs of candidates in the pool. How does the time complexity grow with pool size?
- If `lambda_ = 1.0`, MMR should return exactly the same results as top-k. Verify this.
- When is diversity harmful? (Think: a very specific factual question vs. a broad survey question.)

---

[← Exercise 2](./02-score-threshold) · [Next: 02 Generation →](../../02-generation/exercises/01-build-prompt)
