import json
import os
from dotenv import load_dotenv
import openai

# Load your API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

INPUT_FILE = "data/test/test_chunks.jsonl"
OUTPUT_FILE = "data/test/test_embeddings.jsonl"

def embed_text(text):
    try:
        response = openai.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"✗ Embedding failed: {e}")
        return None

def main():
    os.makedirs("data/test", exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:

        for line in f_in:
            chunk = json.loads(line)
            embedding = embed_text(chunk["text"])
            if embedding is None:
                continue

            record = {
                "chunk_id": chunk["chunk_id"],
                "embedding": embedding,
                "metadata": chunk["metadata"],
                "text": chunk["text"]
            }
            f_out.write(json.dumps(record) + "\n")

    print(f"✅ Saved embeddings to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
