---
slug: /03-cloud-models/exercises/02-swap-generator
---

# Exercise 2 - Swap the Generator

> **Goal:** Introduce the `Generator` abstraction from the theory and plug Gemini into the pipeline you built in 02-generation with a single line change.

---

## Background

Right now your pipeline calls Ollama directly. If you want to switch to Gemini, you have to find and edit every place the model is called. The abstraction fixes this: the pipeline accepts a `Generator` and does not know or care which model is underneath.

---

## Assignment

Open `02_swap_generator.py`.

1. Define a `Generator` base class with a single `generate(prompt: str) -> str` method.
2. Implement `OllamaGenerator` and `GeminiGenerator` subclasses.
3. Copy your `ask(question, index, chunks, generator, k)` function from the previous module - change only the signature to accept a `generator` instance instead of calling Ollama directly.
4. Run the same five questions from Generation Exercise 2 using both generators.
5. Compare the answers side by side. Are there questions where one model is noticeably better?

---

## Thinking questions

- Your `ask` function now has no `import requests` inside it - all model-specific code is in the generator classes. What are the testing benefits of this design?
- If you wanted to add a third generator (e.g. OpenAI GPT-4), how many lines of the pipeline would you need to change?
- Gemini has a 1 million token context window. Does that mean you should always pass more chunks? What is the argument against it?

---

[← Exercise 1](./01-gemini-call)
