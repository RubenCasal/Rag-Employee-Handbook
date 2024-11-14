import fitz  # PyMuPDF for PDF text extraction
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os


def initialize_pinecone():
    """Initializes Pinecone with the API key and returns a Pinecone instance."""
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    return Pinecone(api_key=api_key)


def create_pinecone_index(pc, index_name="employee", dimension=1536, metric="cosine"):
    """Creates a Pinecone index if it doesn't exist and returns the index."""
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    return pc.Index(index_name)


def extract_text_from_pdf(pdf_path):
    """Extracts text from all pages of a PDF."""
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):  # Loop through all pages
            print(page_num)
            if page_num > 5:
                page = pdf[page_num]
                text += page.get_text()
    return text


def split_text_into_chunks(text):
    """Splits text into semantically meaningful chunks."""
    text_splitter = SemanticChunker(
        OpenAIEmbeddings(), breakpoint_threshold_type="percentile"
    )
    return text_splitter.create_documents([text])


def generate_and_upload_embeddings(documents, index):
    """Generates embeddings for each document chunk and uploads them to Pinecone."""
    embedding_model = OpenAIEmbeddings()
    for i, doc in enumerate(documents):
        # Generate the embedding for each chunk's text
        embedding = embedding_model.embed_query(doc.page_content)

        # Create a unique ID and prepare metadata
        vector_data = {
            "id": f"chunk_{i}",
            "values": embedding,
            "metadata": {"text": doc.page_content}  # Store the chunk text as metadata
        }

        # Upload to Pinecone
        index.upsert([vector_data])

    print(f"Uploaded {len(documents)} chunks to Pinecone index.")


def main():
    # Initialize Pinecone
    pc = initialize_pinecone()

    # Create or connect to the Pinecone index
    index = create_pinecone_index(pc, index_name="google-employee-handbook", dimension=1536)

    # Extract text from the entire PDF
    pdf_path = "google_handbook.pdf"
    text = extract_text_from_pdf(pdf_path)

    # Split text into semantically meaningful chunks
    documents = split_text_into_chunks(text)

    # Generate embeddings and upload each chunk to Pinecone
    generate_and_upload_embeddings(documents, index)


if __name__ == "__main__":
    main()
