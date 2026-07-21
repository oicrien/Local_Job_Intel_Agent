import sqlite3
from pathlib import Path

TEMPLATE_PATH = Path("reports/templates/report_template.tex")
OUTPUT_PATH = Path("reports/output/weekly_report.tex")

def fetch_jobs():
    conn = sqlite3.connect("data/jobs.db")
    cur = conn.cursor()
    cur.execute("SELECT title, company, location, fit_score FROM jobs ORDER BY fit_score DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def generate_latex():
    jobs = fetch_jobs()

    job_entries = ""
    for title, company, location, score in jobs:
        job_entries += f"\\item {title} — {company} ({location}) (Fit Score: {score:.2f})\n"

    template = TEMPLATE_PATH.read_text()
    latex_output = template.replace("{{JOB_LIST}}", job_entries)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(latex_output)

    print("LaTeX weekly report generated:", OUTPUT_PATH)

if __name__ == "__main__":
    generate_latex()

