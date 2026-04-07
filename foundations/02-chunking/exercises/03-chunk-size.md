---
slug: /02-chunking/exercises/03-chunk-size
---

# Exercise 3 - Chunk Size Trade-offs

> **Goal:** See how chunk size affects how precisely a retriever can match a specific query. Small chunks find the exact sentence; large chunks dilute it.

---

## Background

You have been working with fixed parameters so far. This exercise makes the trade-off concrete: embed a document at three different chunk sizes and run the same query against each index. Compare which chunk actually surfaces the answer.

---

## Assignment

Open `03_chunk_size.py`.

1. Load a PDF from `data/papers/` and split it at three chunk sizes: `200`, `500`, and `1500` characters (use `overlap = chunk_size // 5` each time).
2. Embed all chunks at each size using `nomic-embed-text` and store them in three separate numpy arrays.
3. Write a `search(query, embeddings, chunks, k=3)` function that returns the top-3 chunks for a query.
4. Run the same query against all three indexes and print the top result from each.

Use a query that asks about a **specific detail** in the paper - a number, a name, or a single-sentence claim. Something where the answer lives in one sentence, not spread across a paragraph.

Compare the results:
- Which chunk size surfaces the exact sentence containing the answer?
- Which chunk size buries the answer inside a large block of text?
- Which chunk size returns something too fragmented to be useful?

---

## Thinking questions

- If you were building a Q&A system over a legal contract, would you choose small or large chunks? What about a chatbot over a novel?
- Chunk size is usually set once at index time. If you need to change it later, what do you have to do?

---

[← Exercise 2](./02-split-text) · [Next: 03 Vector Stores →](../../03-vector-stores/exercises/01-flat-index)
