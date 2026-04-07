---
slug: /01-embeddings/exercises/02-similarity
---

# Exercise 2 — Similarity

> **Goal:** Compute cosine similarity between embeddings and build intuition for what scores actually mean.

---

## Background

In Exercise 1 you saw that an embedding is a 768-dimensional vector. Similarity between two embeddings is the cosine of the angle between their vectors — a number between -1 and 1.

The script normalises vectors before comparing them, so similarity is just a dot product:

```python
similarity = np.dot(a, b)   # only valid when both are L2-normalised
```

---

## Assignment

Open `02_similarity.py` and run it:

```bash
python exercises/02_similarity.py
```

It embeds 5 sentences and prints a similarity matrix. Study the output, then:

1. Identify the pair with the highest similarity. Does the number match your intuition?
2. Find two sentences that share words but are semantically different. Are their scores high or low? What does this tell you about how embeddings work versus keyword matching?
3. Add two new sentences of your own — one that should be very similar to sentence [0], and one that should be very different. Run again and check the scores.
4. What is the similarity of any sentence with itself? Why is that the maximum possible value?

---

## Thinking questions

- Cosine similarity measures angle, not distance. Two vectors can point in the same direction but have very different magnitudes. Why does normalisation solve this?
- If you used a different embedding model, would the similarity scores between the same sentences be the same? Why or why not?

---

[← Exercise 1](./01-first-embedding) · [Next: Exercise 3 — Normalisation →](./03-normalisation)
