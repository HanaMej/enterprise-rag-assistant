import os
from openai import OpenAI
from dotenv import load_dotenv
from backend.app.vector_store import search_chunks

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def answer_question(question: str):
    chunks = search_chunks(question, limit=5)

    context = "\n\n".join(
        [
            f"[Source {i+1}] File: {chunk['filename']}, Chunk: {chunk['chunk_index']}\n{chunk['text']}"
            for i, chunk in enumerate(chunks)
        ]
    )

    prompt = f"""
You are an enterprise document assistant.

Answer the user's question using only the context below.
If the answer is not in the context, say: "I don't know based on the uploaded document."

Include citations like [Source 1], [Source 2].

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You answer questions using retrieved document context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return {
        "question": question,
        "answer": response.choices[0].message.content,
        "sources": chunks
    }