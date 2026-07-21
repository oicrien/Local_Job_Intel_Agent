from storage.db import init_db, get_connection
from linkedin_scraper.search import fake_linkedin_results
from llm_analysis.fit_score import simple_fit_score

def ingest_jobs():
    jobs = fake_linkedin_results()
    conn = get_connection()
    cur = conn.cursor()

    for job in jobs:
        fit = simple_fit_score(job)
        cur.execute(
            """
            INSERT INTO jobs (source, title, company, location, url, posted_date, raw_text, fit_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job["source"],
                job["title"],
                job["company"],
                job["location"],
                job["url"],
                job["posted_date"],
                job["raw_text"],
                fit,
            ),
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    ingest_jobs()
    print("Jobs ingested with basic fit scores.")

