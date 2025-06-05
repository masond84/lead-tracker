# 🧭 Lead Tracker – Business Lead Scraper

Lead Tracker is a modern web application that allows users to scrape business leads from Google Maps queries, identify missing websites, and export the results for outreach and sales purposes. 
Built with React, Tailwind CSS, TanStack Table, and a FastAPI backend.

---
## Features
- Search businesses by keyword + location + industry
- Displays scraped results in a responsive, sortable data table
- Filters for businesses with no website
- Download results as CSV
- Saves recent searches using local storage

---
## Local Setup

#### 1. Setup Frontend
```bash
cd scraper-frontend
npm install
npm run dev
```

#### 2. Setup Backend
```bash
cd scraper-backend
uvicorn scraper_api:app --reload
```
