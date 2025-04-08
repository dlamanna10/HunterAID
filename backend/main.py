from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .pinecone_index import retrieve_top_k
from .rag_engine import generate_rag_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    chunks, source_meta = retrieve_top_k(request.question)
    answer = generate_rag_answer(request.question, chunks, source_meta)
    sources = list({m["url"] for m in source_meta if "url" in m})
    return {"answer": answer, "sources": sources}

@app.get("/")
def root():
    return {"message": "HunterAID backend is running!"}
