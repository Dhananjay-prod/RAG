from langchain_community.document_loaders import PyMuPDFLoader
from pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import hashlib
import chainlit as cl
import asyncio
import requests
import cohere
from google import genai
COHERE_API_KEY = "your_api_key"  # replace with your actual key
co = cohere.Client(COHERE_API_KEY)
client = genai.Client(api_key="your_api_key")
PINECONE_API_KEY = "your_api_key"
INDEX_NAME = "your_index_name"

# Initialize connections
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)
embedder = SentenceTransformer("thenlper/gte-large")

def get_pdf_hash(file_path):
    """Get MD5 hash of PDF file"""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:12]  # Use first 12 chars

def check_embeddings_exist(pdf_hash):
    try:
        dummy_vector = [0.0] * 1024  # gte-large dimension
        results = index.query(
            vector=dummy_vector,
            filter={"pdf_hash": pdf_hash},
            top_k=1
        )
        return len(results.matches) > 0
    except:
        return False

def create_chunks(file_path):
    """Load PDF and create chunks"""
    print(f"📄 Loading PDF: {file_path}")
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    
    print(f"Created {len(chunks)} chunks from {len(docs)} pages")
    return chunks

def create_and_store_embeddings(chunks, pdf_hash):
    """Create embeddings and store in Pinecone"""
    print("🔄 Creating embeddings...")
    
    vectors = []
    for i, chunk in enumerate(tqdm(chunks, desc="Processing chunks")):
        # Create embedding
        embedding = embedder.encode(chunk.page_content)
        
        # Prepare vector for Pinecone
        vectors.append({
            "id": f"{pdf_hash}_{i}",
            "values": embedding.tolist(),
            "metadata": {
                "text": chunk.page_content,
                "pdf_hash": pdf_hash,
                "chunk_id": i,
                "page": chunk.metadata.get('page', 0)
            }
        })
    
    # Upload to Pinecone in batches
    print("⬆️ Uploading to Pinecone...")
    BATCH_SIZE = 100
    for i in range(0, len(vectors), BATCH_SIZE):
        batch = vectors[i:i+BATCH_SIZE]
        index.upsert(vectors=batch)
        print(f"Uploaded batch {i//BATCH_SIZE + 1}/{(len(vectors)-1)//BATCH_SIZE + 1}")
    
    print(f"✅ Stored {len(vectors)} embeddings")

@cl.on_chat_start
async def start():
    files = None

    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a text file to begin!", accept=["pdf"],
            max_size_mb=40
        ).send()
    PDF_FILE = files[0]

    # Let the user know that the system is ready
    await cl.Message(
        content=f"`{PDF_FILE.name}` successfully uploaded!"
    ).send()

    pdf_path = PDF_FILE.path
    pdf_hash = get_pdf_hash(pdf_path)
    if not check_embeddings_exist(pdf_hash):
        chunks = create_chunks(pdf_path)
        create_and_store_embeddings(chunks, pdf_hash)
    await cl.Message(
        content=f"`{PDF_FILE.name}` is processed. Enter your query"
    ).send()     

@cl.on_message
async def main(message: cl.Message):
    try:
        message_embedding = embedder.encode(message.content)
        results = index.query(
            vector=message_embedding.tolist(),
            top_k=5,
            include_metadata=True
        )
        
        if not results.matches:
            await cl.Message(content="No record found").send()
            return

        candidates = [match.metadata["text"] for match in results.matches]    

        rerank_response = co.rerank(
            query=message.content,
            documents=candidates,
            top_n=3,
            model="rerank-english-v2.0"
        )

        top_chunks = [results.matches[result.index].metadata["text"] for result in rerank_response.results]

        context = "\n\n".join(top_chunks)
        prompt = f"""Based on the following context, answer the question. If the answer is not in the context, say so.
    
        Context:
        {context}

        Question: {message.content}"""
    
        loop = asyncio.get_running_loop()
        
        try:
            response = await loop.run_in_executor(None, lambda: client.models.generate_content(model="gemini-2.0-flash",contents=[f"{prompt}"]))
            answer = response.candidates[0].content.parts[0].text
            msg = cl.Message(content="")
            await msg.send()

            for char in answer:
                await msg.stream_token(char)
                await asyncio.sleep(0.0001)  # adjust speed as needed

            await msg.update()    
        except requests.exceptions.ConnectionError:
            await cl.Message(content="❌ Gemini API is not working").send()
            return

    except Exception as e:
        await cl.Message(
            content=f"Sorry, an error occurred: {str(e)}"
        ).send()
