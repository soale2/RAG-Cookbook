---
slug: /01-embeddings/exercises/01-first-embedding
---

# Exercise 1 - Your First Embedding

> **Goal:** Call the embedding API, inspect the raw output, and understand what the numbers represent.

---

## Assignment

Open `01_first_embedding.py` and run it:

```bash
python exercises/01_first_embedding.py
```

The script embeds one sentence and prints the vector's shape, range, and magnitude. Read the output carefully.

Now make these changes:

1. Try changing one word in the sentence. Re-run. Do the values shift noticeably?
2. Try embedding a completely unrelated sentence (e.g. `"The price of eggs went up this quarter."`). Compare the first 8 values side by side. Are they different?
3. Try embedding an empty string `""`. What happens?

---

## Thinking questions

- The vector has 768 dimensions. Each number is meaningless on its own. Where is the meaning?
- The magnitude (L2 norm) is probably not 1.0. What would you need to do to fix that, and why does it matter?
- If you embed the same sentence twice, do you get identical vectors? Why?

---

[Next: Exercise 2 - Similarity →](./02-similarity)
