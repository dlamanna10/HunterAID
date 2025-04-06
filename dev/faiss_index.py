import json
import faiss
import numpy as np
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_CHUNK_CHARS = 500
TOP_K = 4

def load_vectors(file_path):
    texts = []
    metadata = []
    vectors = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            vectors.append(record["embedding"])
            texts.append(record["text"])
            metadata.append(record["metadata"])

    vectors_np = np.array(vectors).astype("float32")
    index = faiss.IndexFlatL2(vectors_np.shape[1])
    index.add(vectors_np)

    return vectors_np, texts, metadata, index

def embed_query(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding).astype("float32").reshape(1, -1)

def retrieve_top_k(query, texts, metadata, index, k=TOP_K):
    query_vec = embed_query(query)
    D, I = index.search(query_vec, k)

    top_chunks = []
    sources = []

    for idx in I[0]:
        chunk_text = texts[idx][:MAX_CHUNK_CHARS]
        top_chunks.append(chunk_text)
        sources.append(metadata[idx])

    return top_chunks, sources

def generate_rag_answer(query, chunks, source_meta):
    context = "\n\n".join(
    [
        f"Source: {meta.get('title', 'Unknown')} — {meta.get('url', '')}\n{chunk}"
        for chunk, meta in zip(chunks, source_meta)
    ]
)

    prompt = f"""You are an incredibly knowledgeable and detailed individual specialized in Monster Hunter knowledge. Use only the context provided below to answer the user's question. If the answer is not clearly stated in the context, respond honestly and say that you don't have enough information.
---
{context}
---
Question: {query}
Answer:"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
