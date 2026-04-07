---
slug: /01-retrieval/exercises/02-score-threshold
---

# Exercise 2 - Score Threshold

> **Goal:** Stop returning irrelevant chunks by filtering results below a minimum similarity score.

---

## Background

Top-k always returns exactly k results - even when none of them are relevant. A score threshold lets you say "only return results above 0.70" and return fewer (or zero) results when the query does not match the corpus.

---

## Assignment

Open `02_score_threshold.py`.

1. Reuse the `retrieve` function from Exercise 1.
2. Write a `retrieve_with_threshold(query, index, chunks, k, min_score)` function that calls `retrieve` with a large `k` (e.g. 20) then filters out results below `min_score`.
3. Run it against two sets of queries:
   - **In-corpus queries** - questions that the document can answer.
   - **Out-of-corpus queries** - questions the document cannot answer (try "Who won the 2024 Olympics?" or something completely off-topic).
4. Print the results and how many were returned for each query.
5. Experiment with `min_score` values: `0.60`, `0.70`, `0.80`. Find a threshold that passes in-corpus queries and blocks out-of-corpus ones.

---

## Thinking questions

- Is there a single "correct" threshold that works for all corpora and all models? What factors affect where you set it?
- If you set `min_score` too high, you might return zero results for a valid question. How would your pipeline handle that gracefully?
- Threshold filtering and top-k are not mutually exclusive. When would you use both together?

---

[← Exercise 1](./01-top-k) · [Next: Exercise 3 - MMR →](./03-mmr)
