---
slug: /03-vector-stores
---

# 03 — Vector Stores

> **Goal:** Understand how vector databases work under the hood. Compare FAISS and ChromaDB, learn about indexing algorithms, and extend the project to persist your vectors in a real store.

---

## Theory

### What a vector store does

A vector store is a data structure optimised for one operation: given a query vector, find the stored vectors most similar to it. This is called **nearest neighbour search**.

At its simplest, you could implement this with a loop:

```python
def search(query: np.ndarray, index: np.ndarray, k: int) -> list[int]:
    scores = index @ query          # dot product with every stored vector
    top_k = np.argsort(scores)[-k:][::-1]
    return top_k.tolist()
```

This is called **flat search** or **brute-force search**. It is exact — it always finds the true nearest neighbours — but it scales as O(n). With 10 million vectors, every query scans 10 million dot products.

Vector stores exist to solve this scaling problem while keeping results accurate enough to be useful.

---

### FAISS

**FAISS** (Facebook AI Similarity Search) is a library for fast vector search. It runs in-process (no server needed) and is the right choice for datasets that fit in memory.

#### IndexFlatIP

The simplest FAISS index. "Flat" means no compression, "IP" means inner product (dot product). It is exact — no approximation.

```python
import faiss
import numpy as np

dim = 768
index = faiss.IndexFlatIP(dim)

# Add vectors (must be float32, L2-normalised for cosine similarity)
vectors = np.random.randn(1000, dim).astype(np.float32)
vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
index.add(vectors)

# Search
query = np.random.randn(1, dim).astype(np.float32)
query /= np.linalg.norm(query)
scores, indices = index.search(query, k=5)
print(indices)   # top-5 most similar vector positions
```

Because vectors are L2-normalised, inner product equals cosine similarity. Always normalise before adding to a flat IP index.

#### IndexIVFFlat

For larger datasets, use an **inverted file index**. It clusters vectors into `nlist` Voronoi cells at build time. At query time it only searches the `nprobe` nearest cells instead of all vectors.

```python
quantizer = faiss.IndexFlatIP(dim)
index = faiss.IndexIVFFlat(quantizer, dim, nlist=100, metric=faiss.METRIC_INNER_PRODUCT)

index.train(vectors)   # must train before adding
index.add(vectors)

index.nprobe = 10      # search 10 of the 100 cells
scores, indices = index.search(query, k=5)
```

Higher `nprobe` is more accurate but slower. This is the core trade-off of approximate nearest neighbour (ANN) search.

#### Persistence

FAISS indexes are in-memory. Save and load them explicitly:

```python
faiss.write_index(index, "index.faiss")
index = faiss.read_index("index.faiss")
```

FAISS does not store the original text — only vectors. You need to keep a parallel list that maps vector position to chunk text and metadata.

---

### ChromaDB

**ChromaDB** is an embedded vector database that handles persistence, metadata, and filtering out of the box. It is a better fit when you need to:
- Filter results by metadata (e.g. only search documents from a specific source)
- Persist the store without managing files manually
- Store text alongside vectors

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("chunks")

# Add documents
collection.add(
    ids=["chunk_0", "chunk_1", "chunk_2"],
    documents=["chunk text 0", "chunk text 1", "chunk text 2"],
    embeddings=vectors.tolist(),
    metadatas=[{"source": "paper.pdf", "page": 1}] * 3,
)

# Query
results = collection.query(
    query_embeddings=[query.tolist()],
    n_results=5,
    where={"source": "paper.pdf"},   # metadata filter
)
print(results["documents"])
```

ChromaDB can also generate embeddings for you (via a built-in embedding function), but in this curriculum you always embed yourself for full control.

---

### FAISS vs ChromaDB

| | FAISS | ChromaDB |
|---|---|---|
| Setup | In-process library | Embedded database |
| Persistence | Manual (`write_index`) | Automatic |
| Metadata filtering | No | Yes |
| Speed (large scale) | Very fast | Good |
| Text storage | No | Yes |
| Best for | Speed-critical, large-scale | General use, filtering |

For the projects in this curriculum, either works. FAISS is used in the reference implementation because it is explicit — you control every step. Use ChromaDB when you want persistence and filtering without extra bookkeeping.

---

### How approximate nearest neighbour works

Most production vector stores use ANN rather than exact search. The idea: trading a small amount of accuracy for a large gain in speed.

**IVF (Inverted File Index)** clusters vectors at index time. At query time, only the nearest clusters are searched.

**HNSW (Hierarchical Navigable Small World)** builds a layered graph. Search starts at the top (sparse) layer and narrows down through denser layers. It is the default in most production systems because it is fast and accurate with no training step required.

You do not need to implement these — FAISS and ChromaDB provide them. But understanding the trade-off (more cells/layers searched = more accurate, slower) lets you tune them correctly.

---

### Key takeaways

- Vector stores find nearest neighbours efficiently. The simplest version is just a dot product over all stored vectors.
- FAISS `IndexFlatIP` is exact and fast enough for up to ~100k vectors. Use `IndexIVFFlat` or HNSW beyond that.
- L2-normalise all vectors before storing. Inner product then equals cosine similarity.
- FAISS only stores vectors — keep a parallel list to map indices back to text.
- ChromaDB adds persistence, text storage, and metadata filtering. Use it when you need those features.

---

## Exercises

1. [Build a FAISS Flat Index](./exercises/01-flat-index) — embed a document, build an index, run your first vector search
2. [Persist and Reload](./exercises/02-persist) — save the index to disk and load it without re-embedding
3. [ChromaDB](./exercises/03-chromadb) — replicate the search using ChromaDB's built-in persistence and metadata filtering

---

## Project — Part 3

See [`project/`](./project/).

---

[← 02 Chunking](../02-chunking/) · [Naive RAG →](../../naive-rag/)
