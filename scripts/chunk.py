import json
import os
from typing import List

INPUT_FILE = "data/raw/docs.jsonl"
OUTPUT_FILE = "data/processed/chunks.jsonl"
CHUNK_SIZE = 500
OVERLAP = 50

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=OVERLAP) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def main():
    os.makedirs("data/processed", exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:

        for line in f_in:
            doc = json.loads(line)
            chunks = chunk_text(doc["content"])
            for i, chunk in enumerate(chunks):
                record = {
                    "chunk_id": f"{doc['name'].replace(' ', '_')}_{i}",
                    "text": chunk,
                    "metadata": doc["metadata"]
                }
                f_out.write(json.dumps(record) + "\n")

    print(f"✅ Chunked data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
