"""
Exercise 2: Split Text
=======================
Chunk a loaded document and inspect sizes and overlap.

Run:
    python exercises/02_split_text.py
"""

from pathlib import Path


def load_text_from_pdf(path: str) -> str:
    # TODO: Load the PDF with PyPDFLoader and join all page_content into one string.
    pass


def split(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    # TODO: Use RecursiveCharacterTextSplitter to split the text.
    # Return a list of chunk strings.
    pass


def print_chunk_stats(chunks: list[str], label: str):
    print(f"\n=== {label} ===")
    # TODO:
    # 1. Print total number of chunks.
    # 2. Print min, max, and average chunk length.
    # 3. Print the first and last 100 chars of chunks[0] and chunks[1].
    pass


if __name__ == "__main__":
    papers_dir = Path("data/papers")
    pdfs = list(papers_dir.glob("*.pdf"))
    if not pdfs:
        print("No PDFs found in data/papers/.")
    else:
        text = load_text_from_pdf(str(pdfs[0]))
        print(f"Loaded {len(text):,} characters from {pdfs[0].name}")

        # With overlap
        chunks_with = split(text, chunk_size=500, chunk_overlap=100)
        print_chunk_stats(chunks_with, "chunk_size=500, overlap=100")

        # Without overlap
        chunks_without = split(text, chunk_size=500, chunk_overlap=0)
        print_chunk_stats(chunks_without, "chunk_size=500, overlap=0")
