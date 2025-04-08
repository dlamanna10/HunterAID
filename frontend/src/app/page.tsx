"use client";
import { useState, useEffect, useRef } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [sources, setSources] = useState<string[]>([]);
  const [chatHistory, setChatHistory] = useState<
    { question: string; answer: string; sources: string[]; time: string }[]
  >([]);
  const [loading, setLoading] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

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
      body: JSON.stringify({ question })
    });

    const data = await res.json();

    const timestamp = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit"
    });

    setChatHistory((prev) => [
      ...prev,
      {
        question,
        answer: data.answer,
        sources: data.sources,
        time: timestamp
      }
    ]);

    setQuestion("");
    setLoading(false);
  };

  const clearChat = () => {
    setChatHistory([]);
    setResponse(null);
    setSources([]);
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return (
    <div className="flex flex-col h-screen bg-black text-white font-sans">
      {/* Header */}
      <header className="flex justify-between items-center p-4 border-b border-zinc-800">
        <img
          src="/HunterAIDLogo.svg"
          alt="HunterAID Logo"
          className="w-44 h-auto"
        />
        {chatHistory.length > 0 && (
          <button
            onClick={clearChat}
            className="bg-zinc-700 text-sm hover:bg-red-700 px-3 py-1 rounded border border-red-500"
          >
            Clear Chat
          </button>
        )}
      </header>

      {/* Chat area */}
      <div
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto px-4 py-6 space-y-6 max-w-2xl mx-auto w-full"
      >
        {chatHistory.map((entry, idx) => (
          <div key={idx} className="flex flex-col gap-2">
            <div className="text-xs text-zinc-500">{entry.time}</div>

            <div className="self-start bg-zinc-800 px-4 py-2 rounded-xl border border-zinc-600 max-w-fit shadow-md">
              <span className="text-red-400 font-semibold">You:</span>{" "}
              {entry.question}
            </div>

            <div className="self-end bg-zinc-900 px-4 py-3 rounded-xl border border-zinc-700 shadow-md w-fit max-w-full">
              <p className="whitespace-pre-line">{entry.answer}</p>
              {entry.sources.length > 0 && (
                <ul className="mt-2 list-disc pl-4 text-blue-400 text-sm">
                  {entry.sources.map((src, i) => (
                    <li key={i}>
                      <a
                        href={src}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="underline"
                      >
                        {src}
                      </a>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Input box fixed at bottom */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          ask();
        }}
        className="border-t border-zinc-800 p-4 bg-black"
      >
        <div className="max-w-2xl mx-auto flex gap-2">
          <input
            type="text"
            ref={inputRef}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a Monster Hunter question..."
            className="flex-1 p-3 rounded bg-zinc-800 border border-zinc-700 focus:outline-none"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-red-600 hover:bg-red-700 px-6 py-2 rounded font-semibold disabled:opacity-50"
          >
            {loading ? (
              <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
            ) : (
              "Ask"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
