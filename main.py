import os
import sys
import uvicorn
import shutil
import logging
import sqlite3
import json
import math
from typing import List, Optional, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- Configuration ---
print("DEBUG: Loading environment variables...", flush=True)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROFILE_PATH = "rohit_portfolio_profile_full.md"
DB_PATH = "data/portfolio.db" # Changed to standard .db file
EMBEDDING_MODEL = "models/text-embedding-004"
GENERATION_MODEL = "gemini-2.5-flash" 
VECTOR_DIM = 768

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Data Structures ---

class ChatIn(BaseModel):
    question: str

class Chunk(BaseModel):
    id: int
    text: str
    vector: List[float]

# --- Helper Logic: Math & Chunking ---

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Pure Python Cosine Similarity."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
        
    return dot_product / (norm_v1 * norm_v2)

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

# --- Core RAG Logic (SQLite + Python) ---

class RAGEngine:
    def __init__(self, api_key: str, profile_path: str, db_path: str):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing!")
        
        print(f"DEBUG: Initializing GenAI Client...", flush=True)
        self.client = genai.Client(api_key=api_key)
        self.profile_path = profile_path
        self.db_path = db_path
        
        # Initialize DB
        print(f"DEBUG: Connecting to SQLite at {db_path}...", flush=True)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY,
                text TEXT,
                vector_json TEXT
            )
        """)
        self.conn.commit()
        print("DEBUG: SQLite connected and table verified.", flush=True)
        
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
        """Checks if DB has data; if not, ingests data."""
        
        self.cursor.execute("SELECT COUNT(*) FROM chunks")
        count = self.cursor.fetchone()[0]
        
        if count > 0:
            logger.info("SQLite loaded with existing data.")
            print("DEBUG: SQLite Knowledge Base already populated.", flush=True)
            return

        # If we are here, we need to ingest
        logger.info("Initializing Knowledge Base from Markdown...")
        
        if not os.path.exists(self.profile_path):
            logger.warning(f"Profile file not found: {self.profile_path}")
            return

        with open(self.profile_path, "r", encoding="utf-8") as f:
            full_text = f.read()

        raw_chunks = split_markdown_into_chunks(full_text)
        logger.info(f"Split profile into {len(raw_chunks)} chunks. Generating embeddings...")
        print(f"DEBUG: Found {len(raw_chunks)} chunks. Starting embedding generation...", flush=True)

        for i, text in enumerate(raw_chunks):
            print(f"DEBUG: Processing chunk {i+1}/{len(raw_chunks)}...", flush=True)
            embedding = self._get_embedding(text)
            if embedding:
                # Store vector as JSON string
                vector_str = json.dumps(embedding)
                self.cursor.execute("INSERT INTO chunks (id, text, vector_json) VALUES (?, ?, ?)", (i, text, vector_str))
        
        self.conn.commit()
        logger.info(f"Ingested {len(raw_chunks)} chunks into SQLite.")
        print(f"DEBUG: Successfully ingested {len(raw_chunks)} chunks.", flush=True)

    def generate_response(self, query: str) -> str:
        # 1. Retrieve
        query_vec = self._get_embedding(query)
        if not query_vec:
            return "System is not ready or failed to understand the query."

        # Fetch all chunks (Small dataset makes this okay ~100 rows)
        self.cursor.execute("SELECT text, vector_json FROM chunks")
        rows = self.cursor.fetchall()
        
        scored_chunks: List[Tuple[float, str]] = []
        
        for text, vector_json in rows:
            chunk_vec = json.loads(vector_json)
            score = cosine_similarity(query_vec, chunk_vec)
            scored_chunks.append((score, text))
            
        # Sort by score desc
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_k = scored_chunks[:4]
        
        relevant_texts = [text for score, text in top_k]
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
    allow_origins=[
        "http://localhost:5174"
        "https://rohitsingh.online",
        "https://www.rohitsingh.online",
        "https://rohit-portfolio-front.vercel.app"
    ],
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
            rag_engine = RAGEngine(GEMINI_API_KEY, PROFILE_PATH, DB_PATH) # Updated Init
            print("DEBUG: RAGEngine initialized successfully.", flush=True)
        except Exception as e:
            logger.error(f"Failed to initialize RAG Engine: {e}")
            print(f"DEBUG: RAGEngine failed: {e}", flush=True)
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
    ready = rag_engine is not None
    return {"status": "ok", "rag_ready": ready}

if __name__ == "__main__":
    print("DEBUG: Starting server via uvicorn...", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
