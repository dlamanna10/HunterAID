from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .pinecone_index import retrieve_top_k
from .rag_engine import generate_rag_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend dev origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Accept both question and game
class QueryRequest(BaseModel):
    question: str
    game: str | None = None  # Optional, "All Games" by default

@app.post("/ask")
def ask_question(request: QueryRequest):
    print(f"🧾 Received question: {request.question} | Game: {request.game}")
    
    chunks, source_meta = retrieve_top_k(request.question)
    
    # Pass the selected game (or None) into the prompt generator
    answer = generate_rag_answer(
        request.question,
        chunks,
        source_meta,
        game=request.game
    )
    
    sources = list({m["url"] for m in source_meta if "url" in m})
    return {"answer": answer, "sources": sources}

@app.get("/")
def root():
    return {"message": "HunterAID backend is running!"}
