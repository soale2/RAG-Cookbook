---
slug: /03-vector-stores/exercises/03-chromadb
---

# Exercise 3 — ChromaDB

> **Goal:** Replicate the FAISS search from Exercise 1 using ChromaDB. Experience the difference: persistence and metadata filtering come for free.

---

## Background

FAISS is explicit — you manage vectors, you manage persistence, you manage metadata. ChromaDB wraps all of that into a collection. The trade-off: less control, more convenience.

---

## Assignment

Open `03_chromadb.py`.

1. Create a `chromadb.PersistentClient` pointed at `./chroma_db`.
2. Get or create a collection called `"rag-exercises"`.
3. Load and split the same PDF from previous exercises.
4. Add all chunks to the collection. Each chunk needs:
   - A unique `id` (e.g. `"chunk_0"`, `"chunk_1"`, ...)
   - The `document` text
   - The `embedding` (you still generate this with Ollama)
   - `metadata` with at least `{"source": filename, "chunk_index": i}`
5. Query the collection with the same queries from Exercise 1. Print the top-3 results.

**Bonus:** Add a metadata filter to your query. For example, only return results where `chunk_index > 10`. Does the result set change?

---

## Thinking questions

- In Exercise 2, you had to manually manage two files (`index.faiss` and `chunks.json`). What does ChromaDB give you in exchange for that bookkeeping?
- ChromaDB can also generate embeddings for you if you pass an `embedding_function`. Why does this curriculum generate embeddings explicitly instead?
- When would you choose FAISS over ChromaDB for a production system?

---

[← Exercise 2](./02-persist) · [Next: Naive RAG →](../../../naive-rag/01-retrieval/exercises/01-top-k)
