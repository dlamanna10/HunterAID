"use client";
import { useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setResponse(null);
    setSources([]);

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Server error: ${errorText}`);
      }

      const data = await res.json();
      setResponse(data.answer);
      setSources(data.sources || []);
    } catch (error: any) {
      console.error("❌ RAG API Error:", error.message);
      setResponse("⚠️ Oops! Something went wrong while fetching your answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="p-10 max-w-2xl mx-auto text-white">
      <h1 className="text-3xl font-bold mb-6">HunterAID 🐉</h1>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a Monster Hunter question..."
        className="w-full p-3 mb-4 rounded bg-zinc-800 border border-zinc-700"
      />
      <button
        onClick={ask}
        disabled={loading}
        className={`px-6 py-2 rounded font-semibold ${
          loading ? "bg-red-400" : "bg-red-600 hover:bg-red-700"
        }`}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {response && (
        <>
          <div className="mt-8 bg-zinc-900 p-4 rounded border border-zinc-700">
            <h2 className="text-xl font-semibold mb-2">💬 Answer</h2>
            <p className="whitespace-pre-line">{response}</p>
          </div>
          {sources.length > 0 && (
            <div className="mt-4">
              <h3 className="font-semibold mb-1">🔗 Sources</h3>
              <ul className="list-disc list-inside text-blue-400">
                {sources.map((src, i) => (
                  <li key={i}>
                    <a href={src} target="_blank" rel="noopener noreferrer">
                      {src}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </main>
  );
}
