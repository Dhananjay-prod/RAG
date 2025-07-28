# 📚 PDF Question Answering App using RAG and Chainlit

A seamless PDF Question Answering application using Retrieval-Augmented Generation (RAG) with an interactive Chainlit frontend. Upload a PDF, get it processed and chunked, generate vector embeddings, store in **Pinecone**, and get instant answers to your queries—powered by cutting-edge NLP tools.

---

## 🔧 Tech Stack

- **LangChain** – Document loading, smart text splitting, and chaining.
- **PyMuPDF (`fitz`)** – Robust PDF parsing and extraction.
- **SentenceTransformers (GTE-Large)** – High-quality embedding generation.
- **Pinecone** – Fast and scalable vector database for similarity search.
- **Cohere Re-rank** – Enhanced context selection for better accuracy.
- **Google Gemini 2.0 Flash** – Advanced LLM for answering queries.
- **Chainlit** – Interactive, real-time chat frontend.

---

## ⚙️ Features

- 📄 Upload PDFs up to 40MB
- 🔎 Intelligent text chunking and vector embedding
- 🚀 Lightning-fast vector search and retrieval (Pinecone)
- 🔁 Context reranking with Cohere for precise answers
- 💬 Natural language Q&A using Gemini 2.0 Flash
- ✅ Duplicate embedding avoidance with PDF hashing
- 🧠 Streamed, real-time answer typing for great UX

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Dhananjay-prod/RAG.git
cd RAG
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Or, if using Conda:
# conda create -n pdf-rag-chainlit python=3.10
# conda activate pdf-rag-chainlit
```

### 3. Install Dependencies

Make sure you have a `requirements.txt` file listing all dependencies. Example content:

```
langchain-community
pymupdf
pinecone-client
sentence-transformers
tqdm
chainlit
cohere
google-generativeai
requests
```

Install all dependencies at once:

```bash
pip install -r requirements.txt
```

> **Tip:** It's best to keep your requirements.txt up-to-date as you add/remove libraries!

### 4. Set Your API Keys

Be sure to set your API keys securely (e.g., using environment variables or a `.env` file). **Never hardcode secrets in your code!**

Example in your Python code (using environment variables):

```python
import os
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
import google.generativeai as genai
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
```

Or, if using a `.env` file, consider [python-dotenv](https://pypi.org/project/python-dotenv/) for automatic loading.

### 5. Run the App

```bash
chainlit run app.py
```

---

## 📂 File Structure

```
📁 RAG/
├── app.py               # Main Chainlit app
├── requirements.txt     # Required dependencies
├── README.md            # Project documentation
```

---

## 📝 Notes & Best Practices

- **API Keys**: Store keys securely! Use environment variables or a `.env` file, not plain text in code.
- **requirements.txt**: Keep this in sync with your imports for reproducibility.
- **PDF size**: The app currently accepts PDFs up to 40MB (adjust as needed).
- **Extensibility**: The codebase is modular, so feel free to swap out the LLM or vector DB as needed.

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [SentenceTransformers](https://www.sbert.net/)
- [Pinecone](https://www.pinecone.io/)
- [Cohere](https://cohere.com/)
- [Google Generative AI](https://ai.google.dev/)
- [Chainlit](https://www.chainlit.io/)

---

## 📬 License

MIT License

---

Feel free to open issues or pull requests to contribute or ask questions!
