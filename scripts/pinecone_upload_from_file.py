import os
import json
import re
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Set credentials from .env
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")
region = os.getenv("PINECONE_ENV")  # e.g., "us-east-1"

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)

# Create index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=region)
    )

# Connect to the index
index = pc.Index(index_name)

# Load the local embeddings file
embedding_path = "data/processed/embeddings.jsonl"
batch = []

with open(embedding_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        record = json.loads(line)

        # Sanitize vector ID (ASCII only)
        raw_id = record["chunk_id"]
        chunk_id = re.sub(r"[^\x00-\x7F]+", "", raw_id)               # Remove non-ASCII
        chunk_id = re.sub(r"[^a-zA-Z0-9_\-]", "_", chunk_id)          # Replace special chars

        vector = record["embedding"]
        metadata = {
            "text": record["text"],
            **record.get("metadata", {})
        }

        batch.append({
            "id": chunk_id,
            "values": vector,
            "metadata": metadata
        })

        # Upload in batches of 100
        if len(batch) == 100:
            index.upsert(vectors=batch)
            print(f"📤 Uploaded {i+1} vectors...")
            batch = []

# Upload remaining vectors
if batch:
    index.upsert(vectors=batch)
    print(f"📤 Uploaded final {len(batch)} vectors.")

print("✅ All vectors successfully uploaded to Pinecone!")
