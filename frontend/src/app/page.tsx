"use client";
import { useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [game, setGame] = useState("All Games");
  const [response, setResponse] = useState<string | null>(null);
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const games = [
    { value: "Monster Hunter World", label: "World (Iceborn)" },
    { value: "Monster Hunter World: Iceborne", label: "World" },
    { value: "Monster Hunter Rise", label: "Rise" },
    { value: "Monster Hunter Rise: Sunbreak", label: "Rise (Sunbreak)" },
    { value: "Monster Hunter Wilds", label: "Wilds" },
    { value: "Monster Hunter Generations", label: "Generations" },
    { value: "Monster Hunter Generations Ultimate", label: "Gen. Ultimate" },
    { value: "Monster Hunter", label: "MH1" },
    { value: "Monster Hunter Freedom", label: "Freedom" },
    { value: "Monster Hunter Freedom Unite", label: "Freedom Unite" },
    { value: "Monster Hunter 2", label: "MH2" },
    { value: "Monster Hunter Portable 3rd", label: "Portable 3rd" },
    { value: "Monster Hunter 3 Ultimate", label: "MH3U" },
    { value: "Monster Hunter 4", label: "MH4" },
    { value: "Monster Hunter 4 Ultimate", label: "MH4U" },
    { value: "Monster Hunter Stories", label: "Stories" },
    { value: "Monster Hunter Stories 2: Wings of Ruin", label: "Stories 2" },
    { value: "Monster Hunter Frontier", label: "Frontier" },
    { value: "Monster Hunter Explore", label: "Explore" },
    { value: "Monster Hunter Online", label: "Online" },
    { value: "All", label: "All Games" }
  ];

  const ask = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setResponse(null);
    setSources([]);

    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        question,
        game: game === "All Games" ? null : game // send null if not filtered
      })
    });

    const data = await res.json();
    setResponse(data.answer);
    setSources(data.sources);
    setLoading(false);
  };

  return (
    <main className="p-10 max-w-2xl mx-auto text-white">
      <img
        src="/HunterAIDLogo.svg"
        alt="HunterAID Logo"
        className="w-70 h-auto mb-6"
      />
      {/* Question input */}
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a Monster Hunter question..."
        className="w-full p-3 mb-4 rounded bg-zinc-800 border border-zinc-700"
      />

      {/* Game selector */}
      <select
        value={game}
        onChange={(e) => setGame(e.target.value)}
        className="w-full p-3 mb-4 rounded bg-zinc-800 border border-zinc-700"
      >
        {games.map((g, idx) => (
          <option key={idx} value={g.value}>
            {g.label}
          </option>
        ))}
      </select>

      {/* Ask button */}
      <button
        onClick={ask}
        className="bg-red-600 hover:bg-red-700 px-6 py-2 rounded font-semibold"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {/* Response */}
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
