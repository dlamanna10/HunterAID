from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .faiss_index import load_vectors, retrieve_top_k, generate_rag_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load full data once at startup
EMBEDDING_FILE = "data/processed/embeddings.jsonl"
vectors, texts, metadata, index = load_vectors(EMBEDDING_FILE)

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    chunks, source_meta = retrieve_top_k(request.question, vectors, texts, metadata, index)
    answer = generate_rag_answer(request.question, chunks, source_meta)
    sources = list({m["url"] for m in source_meta if "url" in m})
    return {"answer": answer, "sources": sources}

@app.get("/")
def root():
    return {"message": "HunterAID backend is running"}
