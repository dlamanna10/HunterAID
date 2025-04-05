import faiss
import json
import os
import numpy as np

EMBEDDING_FILE = "data/test/test_embeddings.jsonl"
TOP_K = 3  # Number of results to return

# Load all embeddings
def load_embeddings(path):
    texts = []
    metadata = []
    vectors = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            vectors.append(record["embedding"])
            texts.append(record["text"])
            metadata.append(record["metadata"])

    return np.array(vectors).astype("float32"), texts, metadata

# Build FAISS index and perform a search
def run_search(query, vectors, texts, metadata, query_embedding_fn, top_k=TOP_K):
    # Embed the query
    query_vector = np.array(query_embedding_fn(query)).astype("float32").reshape(1, -1)

    # Build the FAISS index
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    # Perform search
    distances, indices = index.search(query_vector, top_k)

    print(f"\n🔎 Top {top_k} results for: \"{query}\"")
    for i, idx in enumerate(indices[0]):
        print(f"\nResult {i+1}:")
        print(f"URL: {metadata[idx]['url']}")
        print(f"Content Preview: {texts[idx][:300]}...")

# --- Replace with your OpenAI embedding function ---
from openai import OpenAI
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_query_with_openai(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# Main
if __name__ == "__main__":
    vectors, texts, metadata = load_embeddings(EMBEDDING_FILE)

    while True:
        query = input("\n🗨️  Enter a query (or 'exit' to quit): ")
        if query.lower() in {"exit", "quit"}:
            break
        run_search(query, vectors, texts, metadata, embed_query_with_openai)
