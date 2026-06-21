from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from backend.app.vector_store import search_chunks
from backend.app.rag_pipeline import client


class RAGState(TypedDict):
    question: str
    chunks: List[Dict]
    answer: str


def retrieve_documents(state: RAGState):
    chunks = search_chunks(state["question"], limit=5)
    return {"chunks": chunks}


def generate_answer(state: RAGState):
    context = "\n\n".join(
        [
            f"[Source {i+1}] File: {chunk['filename']}, Chunk: {chunk['chunk_index']}\n{chunk['text']}"
            for i, chunk in enumerate(state["chunks"])
        ]
    )

    prompt = f"""
Answer the question using only the context below.
Include citations like [Source 1], [Source 2].
If the answer is not in the context, say:
"I don't know based on the uploaded document."

Context:
{context}

Question:
{state["question"]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a secure enterprise RAG assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return {"answer": response.choices[0].message.content}


graph = StateGraph(RAGState)

graph.add_node("retrieve_documents", retrieve_documents)
graph.add_node("generate_answer", generate_answer)

graph.set_entry_point("retrieve_documents")
graph.add_edge("retrieve_documents", "generate_answer")
graph.add_edge("generate_answer", END)

rag_app = graph.compile()


def answer_with_graph(question: str):
    result = rag_app.invoke({
        "question": question,
        "chunks": [],
        "answer": ""
    })

    return {
        "question": question,
        "answer": result["answer"],
        "sources": result["chunks"]
    }