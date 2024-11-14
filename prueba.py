from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
from pinecone import Pinecone
from dotenv import load_dotenv
import os

def initialize_pinecone():
    """Initializes Pinecone with the API key and returns a Pinecone instance."""
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    return Pinecone(api_key=api_key)

def search_similar_chunks(query, index, top_k=3):
    """Embeds the query and retrieves the top K most similar chunks from Pinecone."""
    # Initialize embedding model
    embedding_model = OpenAIEmbeddings()

    # Generate embedding for the query
    query_embedding = embedding_model.embed_query(query)

    # Search for the top K most similar chunks
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True  # Include metadata to retrieve chunk text
    )
    
    return results['matches']

def generate_response_from_chunks(query, chunks):
    """Uses ChatOllama to generate a response based on the query and related chunks."""
    # Combine the chunks' text as context
    context = "\n\n".join(chunk['metadata']['text'] for chunk in chunks)

    # Initialize ChatOllama
    chat_model = ChatOllama(model="llama3.1")

    # Generate the prompt as a message for the model
    prompt = (
        f"The following context comes from the company's employee handbook. "
        f"Please answer the question based strictly on the provided context. "
        f"If the information is not found in the context, respond with 'The handbook does not specify.'\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer:"
    )
    messages = [HumanMessage(content=prompt)]

    # Get the model's response
    response = chat_model.invoke(messages)
    
    return response.content

def main():
    # Initialize Pinecone
    pc = initialize_pinecone()

    # Connect to the Pinecone index
    index_name = "google-employee-handbook"
    index = pc.Index(index_name)

    # Define the query prompt
    query = "What it is the intention of this handbook?"

    # Search for the top 3 most relevant chunks
    top_chunks = search_similar_chunks(query, index)

    # Generate a response from the retrieved chunks
    response = generate_response_from_chunks(query, top_chunks)

    # Display the response
    print("\nModel Response:\n")
    print(response)

if __name__ == "__main__":
    main()
