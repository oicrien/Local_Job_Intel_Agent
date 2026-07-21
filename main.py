from storage.db import init_db, get_connection
from llm_analysis.fit_score import simple_fit_score
import json
from pathlib import Path

SUMMARIES = Path("data/summaries.json")

def load_summaries():
    if not SUMMARIES.exists():
        raise FileNotFoundError(f"Summaries file not found: {SUMMARIES}")
    with SUMMARIES.open("r", encoding="utf-8") as f:
        return json.load(f)

def ingest_jobs():
    jobs = load_summaries()
    conn = get_connection()
    cur = conn.cursor()

    for job in jobs:
        # Safe field extraction
        source = job.get("source", "linkedin")
        title = job.get("title", "Unknown Title")
        company = job.get("company", "Unknown Company")
        location = job.get("location", "Unknown Location")
        summary_text = job.get("summary", "")

        # Fit score based on summary text
        fit = simple_fit_score({"raw_text": summary_text})

        # Insert into DB (fields not present are stored as NULL)
        cur.execute(
            """
            INSERT INTO jobs (source, title, company, location, url, posted_date, raw_text, fit_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source,
                title,
                company,
                location,
                None,          # url not available in summaries.json
                None,          # posted_date not available
                summary_text,  # store summary as raw_text
                fit,
            ),
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    ingest_jobs()
    print("Jobs ingested with basic fit scores.")
