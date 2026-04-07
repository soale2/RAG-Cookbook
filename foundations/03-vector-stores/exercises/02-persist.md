---
slug: /03-vector-stores/exercises/02-persist
---

# Exercise 2 — Persist and Reload

> **Goal:** Save your FAISS index to disk and reload it in a fresh process, without re-embedding the document.

---

## Background

In Exercise 1 you built the index every time the script ran. That means re-embedding the entire document on each run — slow and wasteful. In a real pipeline you build the index once and reload it instantly.

FAISS handles vector storage with `faiss.write_index` / `faiss.read_index`. But FAISS only stores vectors, not text. You need to save the chunk list separately.

---

## Assignment

Open `02_persist.py`.

**Part A — Save**

1. If `index.faiss` does not already exist, build the index from Exercise 1.
2. Save the index: `faiss.write_index(index, "index.faiss")`.
3. Save the chunks list to `chunks.json` using the `json` module.
4. Print the file sizes of both files.

**Part B — Load**

1. Load the index: `faiss.read_index("index.faiss")`.
2. Load the chunks list from `chunks.json`.
3. Run the same query as in Exercise 1 and confirm results are identical.
4. Time the load. Compare it to the time it took to build from scratch.

---

## Thinking questions

- You saved chunks as plain text in JSON. What metadata would you want to save alongside the text in a production system?
- `faiss.write_index` only saves vectors and index structure — not the original Document objects or their page numbers. Design a simple file format (JSON or otherwise) that would store everything you need to fully reconstruct the search results.

---

[← Exercise 1](./01-flat-index) · [Next: Exercise 3 — ChromaDB →](./03-chromadb)
