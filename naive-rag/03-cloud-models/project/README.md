---
slug: /03-cloud-models/project
---

# Project Part 3: Model-Agnostic Pipeline

> Make the pipeline provider-agnostic. Swap between Ollama and Gemini with a single line change.

---

## Brief

Your pipeline from Part 2 is hardcoded to Ollama. Now introduce an abstraction so you can plug in any LLM provider without touching the retrieval or prompt logic.

You need:

1. **Generator abstraction** - an ABC with a single `generate(prompt) -> str` method.

2. **OllamaGenerator** - wraps the existing Ollama call.

3. **GeminiGenerator** - calls the Gemini API via `google-generativeai`. Include retry with exponential backoff for rate limit errors.

4. **Updated pipeline** - `ask()` now takes a `generator` parameter instead of calling Ollama directly.

Run the same questions through both generators and compare the answers.

---

## Example output

```
Q: What is the main contribution of this paper?
  OllamaGenerator(model='llama3.2'): The paper introduces the Transformer...
  GeminiGenerator(model='gemini-2.0-flash'): The main contribution is a new...

Q: Who invented the telephone?
  OllamaGenerator(model='llama3.2'): I don't have enough information...
  GeminiGenerator(model='gemini-2.0-flash'): I don't have enough information...
```

---

## Requirements

- [ ] `Generator` ABC with `generate(prompt) -> str`
- [ ] `OllamaGenerator(model)` implementation
- [ ] `GeminiGenerator(model, retries)` with exponential backoff
- [ ] `ask(question, index, chunks, generator, k)` accepts any Generator
- [ ] Switching providers is a one-line change (swap the generator instance)
- [ ] API key loaded from environment variable, never hardcoded

## Stretch goals

- Add CLI flags to select provider (`--gemini`, `--gemini-only`)
- Add a `__repr__` to each generator so output shows which model answered
- Add a third generator (OpenAI, Anthropic, or Cohere)
