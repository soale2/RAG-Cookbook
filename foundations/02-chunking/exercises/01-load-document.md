---
slug: /02-chunking/exercises/01-load-document
---

# Exercise 1 — Load a Document

> **Goal:** Load a real file into Python and inspect its raw text and metadata before touching any splitter.

---

## Background

Before you can chunk, you need text. Langchain loaders handle the file I/O and return a list of `Document` objects — each has `.page_content` (the text) and `.metadata` (source path, page number, etc.).

There are sample papers in `data/papers/` you can use.

---

## Assignment

Open `01_load_document.py`.

1. Use `PyPDFLoader` to load one of the PDF files from `data/papers/`.
2. Print the number of pages (documents) returned.
3. Print the metadata of the first page.
4. Print the first 500 characters of the first page's content.
5. Now load a plain text file using `TextLoader`. Print the same information.

Compare the two:
- Does the PDF loader split by page? Does the text loader split at all?
- What metadata does each loader attach?

---

## Thinking questions

- The `.metadata` dict contains a `"source"` key. Why is it important to keep this through the entire pipeline?
- A PDF page might be very short (just a figure caption) or very long (dense text). Is "one document per page" a good chunking strategy? What problems might it cause?

---

[Next: Exercise 2 — Split Text →](./02-split-text)
