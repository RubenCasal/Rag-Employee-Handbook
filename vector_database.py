import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from pinecone import Pinecone, ServerlessSpec

# Load environment variables (Pinecone API key)
load_dotenv()

# Initialize Pinecone with API key
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

# Set index name and check if it exists, create if not
index_name = "employee"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=4096,  # Ensure this matches your embedding model's output dimension
        metric="cosine",
        spec = ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
index = pc.Index(index_name)

# Initialize the embedding model with the required model name
embedding_model = OllamaEmbeddings(model="llama3.1")  # Specify model explicitly

# Read chunks from split_documents.txt
chunks = []
with open("split_documents.txt", "r", encoding="utf-8") as file:
    chunk = ""
    for line in file:
        if line.strip() == "" and chunk:  # Empty line signals end of a chunk
            chunks.append(chunk.strip())
            chunk = ""
        else:
            chunk += line
    # Append the last chunk if there's no trailing empty line
    if chunk:
        chunks.append(chunk.strip())

# Process each chunk and upload to Pinecone
for i, chunk in enumerate(chunks):
    # Generate the embedding for each chunk
    embedding = embedding_model.embed_query(chunk)  # Use embed_query instead of embed_text
    
    # Create an entry for Pinecone
    vector_data = {
        "id": f"chunk_{i}",  # Unique ID for each chunk
        "values": embedding,
        "metadata": {"text": chunk}  # Optional metadata to store the chunk text
    }
    
    # Upload to Pinecone
    index.upsert([vector_data])

print(f"Uploaded {len(chunks)} chunks to Pinecone index '{index_name}'.")
