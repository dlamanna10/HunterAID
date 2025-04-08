print("🧩 rag_engine.py loaded")

import openai
import os
import textwrap
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_rag_answer(query, chunks, source_meta):
    context = "\n\n".join(
        [
            f"Source: {meta.get('title', 'Unknown')} — {meta.get('url', '')}\n{chunk}"
            for chunk, meta in zip(chunks, source_meta)
        ]
    )

    prompt = f"""You are HunterAID — an expert assistant specialized only in the Monster Hunter franchise. You have access to detailed context pulled from official Monster Hunter sources including items, monsters, maps, quests, weapons, armor, and in-game mechanics.

Do not answer questions that are unrelated to the Monster Hunter franchise. If a question is outside this domain (such as general gaming, other Capcom titles, or unrelated trivia), respond with: "I'm here to help with Monster Hunter-related questions only."

Only use the information provided in the context below to answer the user's question. Do not guess or fabricate information that is not clearly stated in the context.

Format things in an easy-to-read manner; materials in lists, steps that are numbered, etc

---
{context}
---
Question: {query}
Answer:"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

