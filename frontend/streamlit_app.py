import requests
import streamlit as st

API_KEY = st.sidebar.text_input("API Key", type="password")
headers = {"x-api-key": API_KEY}
API_URL = "http://127.0.0.1:8000"



st.sidebar.subheader("Document Management")

if st.sidebar.button("List Documents"):
    response = requests.get(f"{API_URL}/documents", headers=headers)

    if response.status_code == 200:
        st.sidebar.write(response.json()["documents"])
    else:
        st.sidebar.error(response.text)

if st.sidebar.button("Clear Knowledge Base"):
    response = requests.delete(f"{API_URL}/documents", headers=headers)

    if response.status_code == 200:
        st.sidebar.success("Knowledge base cleared")
    else:
        st.sidebar.error(response.text)

st.set_page_config(page_title="Enterprise RAG Assistant")
st.title("Enterprise RAG Assistant")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    response = requests.post(f"{API_URL}/upload-pdf", files=files, headers=headers)

    if response.status_code == 200:
        st.success("PDF uploaded and indexed successfully")
        st.json(response.json())
    else:
        st.error(response.text)

question = st.text_input("Ask a question about the uploaded document")

if st.button("Ask"):
    if question:
        response = requests.get(f"{API_URL}/ask", params={"question": question}, headers=headers)

        if response.status_code == 200:
            data = response.json()
            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Sources / Citations")
            for i, source in enumerate(data["sources"], start=1):
                with st.expander(f"Source {i} — {source['filename']} | Chunk {source['chunk_index']}"):
                    st.write(f"Similarity score: {source['score']:.4f}")
                    st.write(source["text"])

        else:
            st.error(response.text)