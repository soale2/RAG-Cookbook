---
slug: /02-generation/project
---

# Project Part 2: Generation Pipeline

> Wire retrieval and generation into a complete naive RAG Q&A loop.

---

## Brief

You have a working retriever from Part 1. Now add generation to complete the pipeline. You need two pieces:

1. **Prompt builder** - takes retrieved chunks and a question, returns a grounded prompt. The instruction must tell the model to answer only from the provided context and decline when the answer is not there.

2. **Pipeline function** - an `ask()` function that retrieves, builds the prompt, generates via Ollama, and returns the answer along with metadata (sources, scores, whether the model declined).

Also write a simple `has_answer()` check that detects common decline phrases ("I don't have enough information", "not mentioned in the context", etc.).

---

## Example output

```
Q: What BLEU score was achieved?
A: The model achieved a BLEU score of 28.4 on English-to-German translation.
  Sources:
    [0.891] 'The model achieves state-of-the-art results on WMT 2014...'
    [0.823] 'On the WMT 2014 English-to-French translation task, our...'

Q: Who won the 2024 FIFA World Cup?
A: I don't have enough information to answer that.
  (model declined)
```

---

## Requirements

- [ ] `build_prompt(context_chunks, question)` - strict grounded prompt
- [ ] `has_answer(response)` - detect decline phrases
- [ ] `ask(question, index, chunks, k)` - full retrieve + generate pipeline
- [ ] `ask()` returns a dict with `answer`, `has_answer`, and `sources`
- [ ] Test with at least one in-corpus and one out-of-corpus question
- [ ] Import the retriever from Part 1 (do not duplicate retrieval code)

## Stretch goals

- Add a `verbose` flag that prints the full prompt before generating
- Support both top-k and MMR retrieval via a parameter
- Track token count of the prompt and warn if it exceeds 4,000 tokens
