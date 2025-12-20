import os
import sys
import uvicorn
import shutil
import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import lancedb
from lancedb.pydantic import Vector, LanceModel
from google import genai
from google.genai import types

# --- Configuration ---
print("DEBUG: Loading environment variables...", flush=True)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROFILE_PATH = "rohit_portfolio_profile_full.md"
LANCEDB_PATH = "data/rag_store"
EMBEDDING_MODEL = "models/text-embedding-004"
GENERATION_MODEL = "gemini-2.5-flash-lite" 
VECTOR_DIM = 768

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Data Structures (Pydantic + LanceDB) ---

class Chunk(LanceModel):
    id: int
    text: str
    vector: Vector(VECTOR_DIM) # 768-dim vector for text-embedding-004

class ChatIn(BaseModel):
    question: str

# --- Helper Logic: Chunking ---

def split_markdown_into_chunks(text: str) -> List[str]:
    """Splits markdown into logical chunks based on headers."""
    chunks = []
    current_chunk = []
    lines = text.split('\n')
    
    for line in lines:
        if line.strip().startswith('## ') or line.strip().startswith('### '):
            if current_chunk:
                chunks.append("\n".join(current_chunk).strip())
                current_chunk = []
            current_chunk.append(line)
        else:
            current_chunk.append(line)
            
    if current_chunk:
        chunks.append("\n".join(current_chunk).strip())
        
    return [c for c in chunks if c]

# --- Core RAG Logic ---

class RAGEngine:
    def __init__(self, api_key: str, profile_path: str, db_path: str):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing!")
        
        print(f"DEBUG: Initializing GenAI Client...", flush=True)
        self.client = genai.Client(api_key=api_key)
        self.profile_path = profile_path
        
        # Initialize LanceDB
        print(f"DEBUG: Connecting to LanceDB at {db_path}...", flush=True)
        self.db = lancedb.connect(db_path)
        print("DEBUG: LanceDB connected.", flush=True)

        self.table_name = "profile_chunks"
        self.table = None
        
        print("DEBUG: Initializing Knowledge Base...", flush=True)
        self._initialize_knowledge_base()

    def _get_embedding(self, text: str) -> List[float]:
        try:
            response = self.client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text
            )
            # Handle newer SDK response structure safely
            if hasattr(response, 'embeddings') and len(response.embeddings) > 0:
                return response.embeddings[0].values
            return []
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            return []

    def _initialize_knowledge_base(self):
        """Checks if DB exists; if not, ingests data."""
        
        # Check if table exists
        if self.table_name in self.db.table_names():
            self.table = self.db.open_table(self.table_name)
            if len(self.table) > 0:
                logger.info("LanceDB loaded with existing data.")
                return

        # If we are here, we need to ingest
        logger.info("Initializing LanceDB Knowledge Base from Markdown...")
        
        if not os.path.exists(self.profile_path):
            logger.warning(f"Profile file not found: {self.profile_path}")
            return

        with open(self.profile_path, "r", encoding="utf-8") as f:
            full_text = f.read()

        raw_chunks = split_markdown_into_chunks(full_text)
        logger.info(f"Split profile into {len(raw_chunks)} chunks. Generating embeddings...")
        print(f"DEBUG: Found {len(raw_chunks)} chunks. Starting embedding generation...", flush=True)

        data = []
        for i, text in enumerate(raw_chunks):
            print(f"DEBUG: Processing chunk {i+1}/{len(raw_chunks)}...", flush=True)
            embedding = self._get_embedding(text)
            if embedding:
                data.append(Chunk(id=i, text=text, vector=embedding))
        
        if data:
            # Create or overwrite table
            self.table = self.db.create_table(self.table_name, schema=Chunk, mode="overwrite")
            self.table.add(data)
            logger.info(f"Ingested {len(data)} chunks into LanceDB.")
            print(f"DEBUG: Successfully ingested {len(data)} chunks.", flush=True)
        else:
            logger.error("No data could be ingested.")

    def generate_response(self, query: str) -> str:
        # 1. Retrieve
        query_vec = self._get_embedding(query)
        if not query_vec or not self.table:
            return "System is not ready or failed to understand the query."

        results = self.table.search(query_vec).limit(4).to_pydantic(Chunk)
        relevant_texts = [r.text for r in results]
        context_str = "\n\n---\n\n".join(relevant_texts)

        if not context_str:
            return "I don't have enough information in my profile to answer that."

        # 2. System Prompt (Elite Agent Persona)
        system_instruction = (
            "You are an elite AI Portfolio Agent (Rohit Singh's AI).\n"
            "**Role:** Represent Rohit Singh, a Senior Software Engineer (EXL Service, VS Code, Python, Backend), to recruiters.\n"
            "**Goal:** Impress the user with high-impact, business-oriented answers grounded strictly in the provided context.\n"
            "**Tone:** Professional, confident, technically precise, and concise.\n"
            "**Process:**\n"
            "1. ANALYZE the retrieved context chunks.\n"
            "2. PLAN the answer (identify key achievements, metrics, ownership/roles).\n"
            "3. GENERATE a structured response (use BOLD for impact, Lists for readability).\n"
            "4. NEVER mention 'retrieved context' or 'chunks' in the output. Just answer naturally.\n"
            "**Constraints:**\n"
            "- STRICTLY GROUNDED: Do not invent facts outside the context.\n"
            "- If the info is missing, say: 'I don't have specific details on that in my current knowledge base.'\n"
        )

        user_prompt = (
            f"### RETRIEVED CONTEXT:\n{context_str}\n\n"
            f"### QUESTION:\n{query}\n\n"
            f"### AGENT RESPONSE:"
        )

        # 3. Generation
        try:
            response = self.client.models.generate_content(
                model=GENERATION_MODEL,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3, 
                )
            )
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"


# --- FastAPI App ---

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = None

@app.on_event("startup")
async def startup_event():
    global rag_engine
    if GEMINI_API_KEY:
        try:
            print("DEBUG: Starting up RAGEngine...", flush=True)
            rag_engine = RAGEngine(GEMINI_API_KEY, PROFILE_PATH, LANCEDB_PATH)
            print("DEBUG: RAGEngine initialized successfully.", flush=True)
        except Exception as e:
            logger.error(f"Failed to initialize RAG Engine: {e}")
    else:
        logger.warning("No API Key found. RAG disabled.")

@app.post("/chat")
def chat(payload: ChatIn):
    if not rag_engine:
        # Try to re-init if it failed before (e.g. intermittent)
        return {"answer": "System is initializing or missing API Key. Please try again in a moment."}
    
    response = rag_engine.generate_response(payload.question)
    return {"answer": response}

@app.get("/health")
def health():
    ready = rag_engine is not None and rag_engine.table is not None
    return {"status": "ok", "rag_ready": ready}

if __name__ == "__main__":
    print("DEBUG: Starting server via uvicorn...", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
