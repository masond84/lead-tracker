# scraper_api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from pydantic import BaseModel
from scraper_logic import search_google_maps
import os
import uuid

app = FastAPI()
# Enable CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RELATED_QUERIES = {
    # industry: sub-industry (related)
    "salons": ["salons", "hair salons", "nail salons", "barber shops", "beauty parlors"],
    "automotive": ["auto repair", "car detailing", "mechanic", "oil change", "body shop"],
    "fitness": ["gyms", "yoga studios", "personal trainers", "fitness centers"]
}

class ScrapeRequest(BaseModel):
    query: str
    industry: str

@app.post("/scrape")
def scrape(request: ScrapeRequest):
    related_queries = RELATED_QUERIES.get(request.query.lower(), [request.query])
    all_results = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(search_google_maps, q, request.industry) for q in related_queries]
        for future in futures:
            result = future.result()
            all_results.extend(result)
    
    # Debug Logging
    print(f"\nRecieved total of {len(all_results)} raw results from {len(related_queries)}")

    if all_results:
        print("Sample result:", all_results[0])
    else:
        print("No results returned from scraper. Check logic.")

    if not isinstance(all_results[0], dict):
        print("Invalid result format:", all_results[:2])
        return {
            "message": "Scraper returned invalid format.",
            "business_count": 0,
            "file_saved": "",
            "preview": []
        }

    # Deduplicate by business name + address
    df = pd.DataFrame(all_results)
    
    required_cols = {"Name", "Address"}
    if required_cols.issubset(df.columns):
        df = df.drop_duplicates(subset=["Name", "Address"])
    else:
        print(f"⚠️ Skipping deduplication: missing expected columns {required_cols}")
    
    os.makedirs("data", exist_ok=True)
    output_file = f"data/{uuid.uuid4().hex}_combined_results.csv"
    df.to_csv(output_file, index=False)

    return {
        "message": f"Scraped {len(related_queries)} queries",
        "business_count": len(df),
        "file_saved": output_file,
        "preview": df.to_dict(orient="records")
    }

@app.get("/download")
def download_file(filename: str):
    file_path = os.path.join("data", filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='text/csv')
    return {"error": "File not found"}
