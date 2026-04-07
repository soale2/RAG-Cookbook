---
slug: /01-embeddings/exercises/03-normalisation
---

# Exercise 3 - Normalisation

> **Goal:** See exactly what breaks when you skip L2 normalisation, and confirm why it is non-negotiable.

---

## Background

Raw embeddings from Ollama are not normalised - their L2 norm varies based on the input. If you store them un-normalised and use dot product for search, longer or "louder" texts will score higher regardless of actual relevance.

---

## Assignment

Open `03_normalisation.py` and run it:

```bash
python exercises/03_normalisation.py
```

The script compares raw dot products against normalised cosine similarities for a short text, a long text, and an unrelated text.

Study the output, then:

1. Do the raw dot products rank the semantically related pair above the unrelated pair? Or does the longer text win just because of its magnitude?
2. After normalisation, are the rankings stable? Does the related pair now consistently outscore the unrelated pair?
3. Modify the script to create a case where the raw dot product gives the **wrong** ranking - i.e. an unrelated long text scores higher than a related short text. You may need to make the long text very long.

---

## Thinking questions

- Some vector stores (like FAISS `IndexFlatIP`) do inner product search. Others do L2 distance. If your vectors are already normalised, does it matter which you use? Why?
- The normalisation formula divides by `norm + 1e-10`. Why is the small epsilon there?

---

[← Exercise 2](./02-similarity) · [Next: 02 Chunking →](../../02-chunking/exercises/01-load-document)
