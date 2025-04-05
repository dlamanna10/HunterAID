import mwclient
import json
from dataclasses import dataclass
import os

# Define your Document structure
@dataclass
class Document:
    name: str
    content: str
    metadata: dict

def scrape_test_pages():
    site = mwclient.Site('monsterhunter.fandom.com', path='/')
    test_titles = [
        "Rathalos",
        "Great Sword",
        "Armor",
        "Rajang",
        "Monster Hunter World"
    ]

    documents = []

    for title in test_titles:
        try:
            page = site.pages[title]
            content = page.text()
        except Exception as e:
            print(f"✗ Failed to scrape: {title} — {e}")
            continue

        url = f"https://monsterhunter.fandom.com/wiki/{title.replace(' ', '_')}"
        doc = Document(
            name=title,
            content=content,
            metadata={"url": url, "source": "web"}
        )
        documents.append(doc)
        print(f"✓ Scraped: {title}")

    return documents

def save_documents_to_jsonl(documents, filename="data/test/test_docs.jsonl"):
    os.makedirs("data", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        for doc in documents:
            record = {
                "name": doc.name,
                "content": doc.content,
                "metadata": doc.metadata
            }
            f.write(json.dumps(record) + "\n")
    print(f"Saved {len(documents)} documents to {filename}")

if __name__ == "__main__":
    docs = scrape_test_pages()
    save_documents_to_jsonl(docs)
