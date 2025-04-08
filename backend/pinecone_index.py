import os
import openai
import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

TOP_K = 3
MAX_CHUNK_CHARS = 500

def embed_query(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def retrieve_top_k(query, k=TOP_K):
    query_vec = embed_query(query)

    # Perform similarity search in Pinecone
    result = index.query(
        vector=query_vec,
        top_k=20,  # Search wider, filter later
        include_metadata=True
    )

    top_chunks = []
    sources = []

    # Filter and trim long texts
    for match in result["matches"]:
        metadata = match["metadata"]
        text = metadata.get("text", "")[:MAX_CHUNK_CHARS]
        if text:
            top_chunks.append(text)
            sources.append(metadata)

        if len(top_chunks) >= k:
            break

    return top_chunks, sources
