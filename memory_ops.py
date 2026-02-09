import os
import uuid
import chromadb
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Load the key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class MemoryRag:
    def __init__(self):
        print("   [⚙️ Loading Local Embeddings... This happens once]")
        # 1. Setup Embeddings (FREE & LOCAL)
        # We use a free model from HuggingFace so you don't pay OpenAI
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 2. Setup Vector DB
        self.db_client = chromadb.PersistentClient(path="./chromadb_store")
        self.collection = self.db_client.get_or_create_collection(name="user_memories")
        
        # 3. Setup LLM (FREE & FAST)
        # We use Groq's Llama-3 model which is incredibly fast
        self.llm = ChatGroq(
           model_name="llama-3.3-70b-versatile", # <--- This is the new, powerful free model
           api_key=GROQ_API_KEY
        )

    def ingestion_pipeline(self, text, turn):
        # Embed and Save
        vector = self.embeddings.embed_query(text)
        self.collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[vector],
            documents=[text],
            metadatas=[{"turn": turn}]
        )
        print(f"   [💾 Memory Saved]")

    def retrieval_pipeline(self, query):
        # 1. Search
        query_vector = self.embeddings.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=2
        )
        
        context_text = ""
        if results['documents']:
            context_text = "\n".join(results['documents'][0])
            
        # 2. Generate
        if context_text:
            system_prompt = (
                f"You are a helpful assistant with memory.\n"
                f"RELEVANT MEMORIES:\n{context_text}\n\n"
                f"Answer the user's question using these memories."
            )
        else:
            system_prompt = "You are a helpful assistant."

        # Groq uses the standard invoke method
        response = self.llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ])
        
        return response.content, context_text