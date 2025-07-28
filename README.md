# 📚 PDF Question Answering App using RAG and Chainlit

This project allows users to upload a PDF, automatically processes and chunks the document, creates vector embeddings using **SentenceTransformers**, stores them in **Pinecone**, and answers user queries with a **RAG (Retrieval-Augmented Generation)** pipeline powered by **Cohere Re-Ranker** and **Gemini 2.0** LLM from Google.

## 🔧 Tech Stack

- **LangChain**: For document loading and text splitting.
- **PyMuPDF (fitz)**: PDF loader for structured parsing.
- **SentenceTransformers (GTE-Large)**: For embedding generation.
- **Pinecone**: Vector store for efficient similarity search.
- **Cohere Re-rank**: Improves context selection for LLM.
- **Google Gemini 2.0 Flash**: Used to answer the final query.
- **Chainlit**: Interactive frontend for chatbot interface.

---

## ⚙️ Features

- 📄 Upload any PDF (up to 40MB)
- 🔎 Smart chunking and embedding generation
- 🚀 Fast vector search and retrieval using Pinecone
- 🔁 Reranking context using Cohere for accuracy
- 💬 Natural language query answering with Gemini 2.0
- ✅ Duplicate embedding checks using PDF hash
- 🧠 Streamed responses with a real-time typing effect

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/pdf-rag-chainlit.git
cd pdf-rag-chainlit
