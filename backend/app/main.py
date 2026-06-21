from fastapi import FastAPI, UploadFile, File, HTTPException
from .pdf_loader import extract_text_from_pdf
from .chunker import split_text_into_chunks
from .vector_store import store_chunks, search_chunks, list_documents, clear_collection
from .rag_graph import answer_with_graph
from fastapi import Depends
from .security import verify_api_key
from fastapi import HTTPException
from .guardrails import is_safe_question

app = FastAPI(title="Enterprise RAG Assistant")


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Enterprise RAG Assistant is running"
    }


@app.post("/upload-pdf", dependencies=[Depends(verify_api_key)])
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    text = await extract_text_from_pdf(file)
    chunks = split_text_into_chunks(text)
    stored_chunks = store_chunks(chunks, file.filename)


    return {
    "filename": file.filename,
    "characters_extracted": len(text),
    "number_of_chunks": len(chunks),
    "stored_chunks": stored_chunks,
    "first_chunk_preview": chunks[0] if chunks else ""
}

@app.get("/search", dependencies=[Depends(verify_api_key)])
def search(query: str):
    results = search_chunks(query)

    return {
        "query": query,
        "results": results
    }
@app.get("/ask", dependencies=[Depends(verify_api_key)])
def ask(question: str):
    if not is_safe_question(question):
        raise HTTPException(
            status_code=400,
            detail="Question blocked by security guardrails."
        )

    return answer_with_graph(question)

@app.get("/documents", dependencies=[Depends(verify_api_key)])
def documents():
    return {"documents": list_documents()}


@app.delete("/documents", dependencies=[Depends(verify_api_key)])
def delete_documents():
    clear_collection()
    return {"message": "Knowledge base cleared successfully"}