import { useState } from "react";
import { useLocalStorage } from "./hooks/useLocalStorage";
import SearchForm from "./components/SearchForm";
import ResultTable from "./components/ResultTable";

function App() {
  const [results, setResults] = useState<any[]>([]);
  const [filename, setFilename] = useState("");
  const [filterMissing, setFilterMissing] = useState(false);
  const [history, setHistory] = useLocalStorage<any[]>("search_history", []);

  const handleResults = (data: any[], file: string, query: string, industry:string) => {
    const timestamp = new Date().toISOString();
    const newEntry = { query, industry, timestamp, data, file };
    setHistory([newEntry, ...history]);
    setResults(data);
    setFilename(file);
  };

  const filteredResults = filterMissing
    ? results.filter((r) => r.Website === "No website")
    : results;

  return (
    <div className="px-4 p-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Business Lead Scraper</h1>
        <SearchForm onResults={handleResults} />

        {results.length > 0 && (
          <>
            <label className="flex items-center gap-2 mb-2">
              <input
                type="checkbox"
                checked={filterMissing}
                onChange={() => setFilterMissing(!filterMissing)}
              />
              Show only businesses with no website
            </label>
          </>
        )}
      </div>
      
      {results.length > 0 && (
        <>
          <div className="flex justify-center">
            <ResultTable results={filteredResults} />
          </div>

          <div className="max-w-3xl mx-auto mt-4">
            <a
              className="block text-blue-600 underline"
              href={`http://localhost:8000/download?filename=${filename.split("/").pop()}`}
              download
            >
              Download CSV
            </a>
          </div>
        </>
      )}

      {history.length > 0 && (
        <div className="mt-10">
          <h2 className="text-lg font-semibold mb-2">Recent Searches</h2>
          <ul className="space-y-2">
            {history.map((item, idx) => (
              <li key={idx} className="border p-2 rounded">
                <div>
                  <strong>{item.query}</strong> – {item.industry}
                </div>
                <div className="text-xs text-gray-500">
                  {new Date(item.timestamp).toLocaleString()}
                </div>
                <button
                  onClick={() => {
                    setResults(item.data);
                    setFilename(item.file);
                  }}
                  className="text-blue-600 underline text-sm mt-1"
                >
                  Load Results
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
