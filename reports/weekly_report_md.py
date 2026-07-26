from pathlib import Path
import sqlite3

OUTPUT_PATH = Path("reports/output/weekly_report.md")

def fetch_jobs():
    conn = sqlite3.connect("data/jobs.db")
    cur = conn.cursor()
    cur.execute("SELECT title, company, location, fit_score FROM jobs ORDER BY fit_score DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def generate_markdown():
    jobs = fetch_jobs()

    lines = ["# Weekly Job Intelligence Report\n"]

    for title, company, location, score in jobs:
        safe_score = score if isinstance(score, (int, float)) else 0
        lines.append(f"- **{title}** — {company} ({location}) — Fit Score: {safe_score:.2f}")


    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines))

    print("Markdown weekly report generated:", OUTPUT_PATH)

if __name__ == "__main__":
    generate_markdown()

