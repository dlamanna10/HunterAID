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

def scrape_monster_hunter_wiki():
    site = mwclient.Site('monsterhunter.fandom.com', path='/')
    documents = []

    for page in site.allpages():
        title = page.name
        try:
            content = page.text()
        except:
            print(f"Failed to scrape: {title}")
            continue

        url = f"https://monsterhunter.fandom.com/wiki/{title.replace(' ', '_')}"
        doc = Document(
            name=title,
            content=content,
            metadata={"url": url, "source": "web"}
        )
        documents.append(doc)
        print(f"Scraped: {title}")

    return documents

def save_documents_to_jsonl(documents, filename="data/docs.jsonl"):
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
    docs = scrape_monster_hunter_wiki()
    save_documents_to_jsonl(docs)
