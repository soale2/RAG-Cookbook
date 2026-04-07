---
slug: /03-vector-stores/exercises/01-flat-index
---

# Exercise 1 - Build a FAISS Flat Index

> **Goal:** Build a FAISS `IndexFlatIP` from scratch, add vectors to it, and run your first real vector search.

---

## Background

`IndexFlatIP` is the simplest FAISS index. It stores every vector in full and does exact inner product search - no approximation. It is correct by definition and fast enough for up to ~100k vectors.

Because it does inner product, you must L2-normalise all vectors before adding them. Inner product on unit vectors equals cosine similarity.

---

## Assignment

Open `01_flat_index.py`.

1. Load a PDF from `data/papers/`, split it into 500-char chunks, and embed them all.
2. Stack the embeddings into a `(N, 768)` float32 numpy array. Make sure every vector is L2-normalised.
3. Create a `faiss.IndexFlatIP(768)` and add all vectors with `index.add(vectors)`.
4. Write a `search(query_text, index, chunks, k)` function. It should embed the query, reshape to `(1, 768)`, call `index.search(query, k)`, and return the top-k chunks with their scores.
5. Run three different queries and print the top-3 results with scores for each.

---

## Thinking questions

- FAISS does not store the original text, only vectors. What data structure do you need alongside the index to map a result position back to the chunk text?
- `index.search()` returns two arrays: `scores` and `indices`. What are their shapes when you search for k=3 with a single query?
- What would happen if you added un-normalised vectors to a `IndexFlatIP` index and searched with a normalised query?

---

[Next: Exercise 2 - Persist and Reload →](./02-persist)
