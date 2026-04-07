---
slug: /02-chunking/exercises/02-split-text
---

# Exercise 2 — Split Text

> **Goal:** Use `RecursiveCharacterTextSplitter` to chunk a document, inspect the output, and understand how overlap works.

---

## Background

`RecursiveCharacterTextSplitter` tries to split on paragraph breaks first (`\n\n`), then line breaks, then sentences, then words — falling back to smaller boundaries only when a piece is still over the `chunk_size` limit.

Overlap repeats the tail of each chunk at the start of the next so that sentences cut at a boundary are not lost.

---

## Assignment

Open `02_split_text.py`.

1. Load a PDF from `data/papers/` (reuse your loader from Exercise 1).
2. Split the full document text using `RecursiveCharacterTextSplitter` with `chunk_size=500` and `chunk_overlap=100`.
3. Print the total number of chunks produced.
4. Print the length (in characters) of each chunk.
5. Print the first and last 100 characters of chunk[0] and chunk[1]. Confirm that chunk[1] starts with text that also appeared near the end of chunk[0] — that is the overlap.

Now change `chunk_overlap` to `0` and re-run. Does chunk[1] now start where chunk[0] ended, with no repetition?

---

## Thinking questions

- If a single paragraph is longer than `chunk_size`, what does the splitter do?
- You set `chunk_size=500` but some chunks might be shorter. Why?
- Overlap increases index size (more chunks, some redundant content). When is it worth the cost?

---

[← Exercise 1](./01-load-document) · [Next: Exercise 3 — Chunk Size →](./03-chunk-size)
