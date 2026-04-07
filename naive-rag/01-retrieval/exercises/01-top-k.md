---
slug: /01-retrieval/exercises/01-top-k
---

# Exercise 1 — Top-k Retrieval

> **Goal:** Build a retriever on top of the FAISS index from Foundations. Given a query, return the k most relevant chunks with their scores.

---

## Background

This is where Foundations pays off. You have a vector index. Now you write the retrieval layer that the rest of the pipeline depends on.

---

## Assignment

Open `01_top_k.py`.

1. Load the FAISS index and chunks you persisted in Foundations `03-vector-stores/exercises/02`. (If you did not do that exercise, build the index here.)
2. Write a `retrieve(query, index, chunks, k)` function that returns a list of `{"text": str, "score": float}` dicts, sorted by score descending.
3. Run it against five different queries. For each query print the top-3 results with scores.
4. Vary `k`: try `k=1`, `k=5`, `k=10`. What changes in the result quality? What stays the same?

---

## Thinking questions

- Your retriever returns `k` results regardless of whether they are relevant. What problem does this create for the generation step?
- If you search with `k=10` and look at the scores, at what point do results start feeling irrelevant? Is there a natural cut-off, or does relevance decay gradually?
- If someone asks a question that is completely off-topic (e.g. "Who won the World Cup?"), what scores do you get? What should the pipeline do in that case?

---

[Next: Exercise 2 — Score Threshold →](./02-score-threshold)
