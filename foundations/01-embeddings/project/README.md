---
slug: /01-embeddings/project
---

# Project: Embedding Explorer

> Build a CLI tool that embeds two pieces of text and tells you how similar they are.

---

## Brief

You have learned how embeddings work, how to normalise vectors, and how cosine similarity measures semantic closeness. Now put it together into a tool you can actually use.

Your tool should:

1. Accept two text inputs (as CLI arguments, interactive prompts, or from a file)
2. Embed both using `nomic-embed-text` via Ollama
3. L2-normalise the vectors
4. Compute cosine similarity (dot product of normalised vectors)
5. Print the score and a human-readable interpretation

Use the score thresholds from the theory section:

| Score | Interpretation |
|-------|---------------|
| 0.90+ | Near-identical meaning |
| 0.75 - 0.90 | Strongly related |
| 0.60 - 0.75 | Somewhat related |
| Below 0.60 | Probably not relevant |

---

## Example output

```
  A: 'transformers use self-attention mechanisms'
  B: 'attention mechanisms in neural networks'
  Similarity: 0.8734 (strongly related)
  Dimensions: 768
```

---

## Requirements

- [ ] Embed text via Ollama (`nomic-embed-text`)
- [ ] L2-normalise before computing similarity
- [ ] Print score + interpretation for any two inputs
- [ ] Handle the case where Ollama is not running (clear error message)

## Stretch goals

- Accept a file of sentence pairs and output results for each
- Add `--interactive` mode for continuous pair comparisons
- Compare scores from two different embedding models side by side
