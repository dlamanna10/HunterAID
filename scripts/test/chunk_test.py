import json
import os
from typing import List

CHUNK_SIZE = 500  # ~500 words, or change to tokens later
OVERLAP = 50
INPUT_FILE = "data//test/test_docs.jsonl"
OUTPUT_FILE = "data//test/test_chunks.jsonl"

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
    os.makedirs("data", exist_ok=True)

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

    print(f"✅ Saved chunks to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
