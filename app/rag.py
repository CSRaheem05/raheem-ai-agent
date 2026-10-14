from pypdf import PdfReader
import requests
import math


def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def split_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_embedding(text: str):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text,
        },
    )

    result = response.json()

    return result["embedding"]


def cosine_similarity(a, b):
    dot_product = sum(
        x * y
        for x, y in zip(a, b)
    )

    norm_a = math.sqrt(
        sum(x * x for x in a)
    )

    norm_b = math.sqrt(
        sum(y * y for y in b)
    )

    if norm_a == 0 or norm_b == 0:
        return 0

    return dot_product / (norm_a * norm_b)


def find_best_chunks(
    question: str,
    chunks: list[str],
    embeddings: list,
    top_k: int = 3
):
    question_embedding = create_embedding(question)

    scored_chunks = []

    for chunk, chunk_embedding in zip(
        chunks,
        embeddings
    ):
        score = cosine_similarity(
            question_embedding,
            chunk_embedding
        )

        scored_chunks.append(
            (chunk, score)
        )

    scored_chunks.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return scored_chunks[:top_k]