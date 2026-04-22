# prompt.py
"""
Project Part 2a: Prompt Builder
================================
Constructs grounded prompts from retrieved chunks.
Strict instruction to prevent hallucination.
"""


def build_prompt(context_chunks: list[str], question: str) -> str:
    """
    Build a RAG prompt that instructs the model to answer
    only from the provided context.
    """
    context = "\n\n---\n\n".join(context_chunks)
    return f"""You are a helpful assistant. Answer the question using only the context below.
Do not add information that is not in the context.
If the context does not contain enough information to answer, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""


NO_ANSWER_PHRASES = [
    "i don't have enough information",
    "the context does not",
    "not mentioned in the",
    "cannot find",
    "no information",
]


def has_answer(response: str) -> bool:
    """Check whether the model produced an actual answer or declined."""
    return not any(phrase in response.lower() for phrase in NO_ANSWER_PHRASES)
