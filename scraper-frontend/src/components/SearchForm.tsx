import { useState } from "react";
import axios from "axios";

interface Props {
  onResults: (data: any[], filename: string, query: string, industry: string) => void;
}

export default function SearchForm({ onResults }: Props) {
  const [query, setQuery] = useState("");
  const [industry, setIndustry] = useState("");
  const [loading, setLoading] = useState(false);

  const handleScrape = async () => {
    if (!query || !industry) return alert("Fill out both fields");
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/scrape", {
        query,
        industry,
      });
      onResults(res.data.preview, res.data.file_saved, query, industry);
    } catch (err) {
      alert("Failed to scrape. Check server logs.");
    }
    setLoading(false);
  };

  return (
    <div className="space-y-4 mb-6">
      <input
        type="text"
        className="border p-2 w-full"
        placeholder="Search query"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <input
        type="text"
        className="border p-2 w-full"
        placeholder="Industry"
        value={industry}
        onChange={(e) => setIndustry(e.target.value)}
      />
      <button
        onClick={handleScrape}
        className="bg-blue-600 text-white px-4 py-2"
        disabled={loading}
      >
        {loading ? "Scraping..." : "Run Scraper"}
      </button>
    </div>
  );
}
