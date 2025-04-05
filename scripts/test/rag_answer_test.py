import faiss
import json
import os
import numpy as np
import openai
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDING_FILE = "data/test/test_embeddings.jsonl"
TOP_K = 3

def embed_query(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def generate_rag_answer(query, context_chunks):
    context = "\n---\n".join(context_chunks)
    prompt = f"""Use the following context to answer the user's question.
---
{context}
---
Question: {query}
Answer:"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

def load_vectors(file_path):
    texts, metadata, vectors = [], [], []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            vectors.append(record["embedding"])
            texts.append(record["text"])
            metadata.append(record["metadata"])

    return np.array(vectors).astype("float32"), texts, metadata

def retrieve_top_k(query, vectors, texts, metadata, k=TOP_K):
    query_vec = np.array(embed_query(query)).astype("float32").reshape(1, -1)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    distances, indices = index.search(query_vec, k)

    return [texts[i] for i in indices[0]], [metadata[i] for i in indices[0]]

if __name__ == "__main__":
    vectors, texts, metadata = load_vectors(EMBEDDING_FILE)

    while True:
        user_query = input("\n🧠 Ask your Monster Hunter question: ")
        if user_query.lower() in {"exit", "quit"}:
            break

        context_chunks, sources = retrieve_top_k(user_query, vectors, texts, metadata)
        answer = generate_rag_answer(user_query, context_chunks)

        print("\n💬 Answer:")
        print(answer)

        print("\n🔗 Sources:")
        seen = set()
        for meta in sources:
            url = meta["url"]
            if url not in seen:
                print("-", url)
                seen.add(url)

