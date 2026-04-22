---
slug: /03-vector-stores/project
---

# Project: Vector Store Builder

> Embed your chunks and persist them in a FAISS index that the Naive RAG track will use for retrieval.

---

## Brief

You have a document processor that produces chunks. Now embed those chunks and store the vectors so you can search them later.

Your script should:

1. Load chunks - either from the Document Processor (Project Part 2) or from a JSON file of pre-chunked texts
2. Embed each chunk using `nomic-embed-text` via Ollama
3. L2-normalise every vector
4. Build a FAISS `IndexFlatIP` index and add all vectors
5. Save `index.faiss` and `chunks.json` to disk

The output files (`index.faiss` and `chunks.json`) are the inputs to the Naive RAG retrieval module. Chunk texts and FAISS positions must stay aligned by index.

---

## Example output

```
Loading and chunking documents from ./papers...
Found 3 file(s)
Split into 147 chunks

Embedding 147 chunks...
  50/147
  100/147
  147/147

Index built: 147 vectors, 768 dimensions
Saved: ./index.faiss (147 vectors)
Saved: ./chunks.json (147 chunks)
```

---

## Requirements

- [ ] Embed all chunks via Ollama and L2-normalise
- [ ] Build a `faiss.IndexFlatIP` index
- [ ] Save `index.faiss` and `chunks.json` to disk
- [ ] Print progress during embedding (every N chunks)
- [ ] Positions in `chunks.json` match positions in the FAISS index

## Stretch goals

- Accept either a folder of documents or a pre-chunked `chunks.json` as input
- Add CLI arguments for input path and output directory
- Compare query speed between `IndexFlatIP` and `IndexIVFFlat` on a large corpus
