import json
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

INPUT_FILE = "data/processed/chunks.jsonl"
OUTPUT_FILE = "data/processed/embeddings.jsonl"

def embed_text(text):
    try:
        response = openai.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"✗ Failed: {e}")
        return None

def main():
    os.makedirs("data/processed", exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:

        for line in f_in:
            chunk = json.loads(line)
            embedding = embed_text(chunk["text"])
            if embedding is None:
                continue
            f_out.write(json.dumps({
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "embedding": embedding,
                "metadata": chunk["metadata"]
            }) + "\n")

    print(f"✅ Embeddings saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
