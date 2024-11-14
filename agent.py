import os 
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_ollama import ChatOllama
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()
class Agent:
    def __init__(self):
        self.index_name = 'google-employee-handbook'
        self.pinecone_database = self.initialize_pinecone()
        self.index = self.pinecone_database.Index(self.index_name)
        self.number_retrieved_chunks = 3

        self.llm_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.embedding_model = OpenAIEmbeddings()

        self.prompt_template = PromptTemplate(
            input_variables=["context", "query"],
            template=(
                "The following context comes from the company's employee handbook. "
                "Please respond to the question based strictly on the provided context. "
                "If the information is not found in the context, respond with 'The handbook does not specify.'\n\n"
                "Context:\n{context}\n\n"
                "Question: {query}\n\n"
                "Answer:"
            )
        )

    def initialize_pinecone(self):
        """Initializes Pinecone with the API key and returns a Pinecone instance."""
        load_dotenv()
        api_key = os.getenv("PINECONE_API_KEY")
        return Pinecone(api_key=api_key)
    
    def search_similar_chunks(self, query):
        """Embeds the query and retrieves the top K most similar chunks from Pinecone."""

        # Generate embedding for the query
        query_embedding = self.embedding_model.embed_query(query)

        # Search for the top K most similar chunks
        results = self.index.query(
            vector=query_embedding,
            top_k=self.number_retrieved_chunks,
            include_metadata=True  # Include metadata to retrieve chunk text
        )
        
        return results['matches']
    
    def generate_response_from_chunks(self, query, chunks):
        """Uses ChatOllama to generate a response based on the query and related chunks."""
        
        # Combine the last interaction and current context
        context = "\n\n".join(chunk['metadata']['text'] for chunk in chunks)
        
        # Prompt with memory of last interaction and current context
        prompt = (
            f"The following context comes from the company's employee handbook. "
            f"Consider the previous interaction if relevant and respond to the question based on the provided context. "
            f"If the information is not found, respond with 'The handbook does not specify.'\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            f"Answer:"
        )
        
        messages = [SystemMessage(content=prompt)]

        # Get the model's response
        response = self.llm_model.invoke(messages)
        print(response)
        
        return response.content
    
    def answer_user(self, query):
        chunks = self.search_similar_chunks(query)
        response = self.generate_response_from_chunks(query=query, chunks=chunks)
        
        return response
