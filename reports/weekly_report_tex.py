import sqlite3
from pathlib import Path
import subprocess

TEMPLATE_PATH = Path("reports/templates/report_template.tex")
OUTPUT_DIR = Path("reports/output")
OUTPUT_TEX = OUTPUT_DIR / "weekly_report.tex"
OUTPUT_PDF = OUTPUT_DIR / "weekly_report.pdf"

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

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_TEX.write_text(latex_output)

    print("LaTeX file generated:", OUTPUT_TEX)

    # Compile PDF directly into reports/output/
    try:
        subprocess.run(
            [
                "pdflatex",
                f"-output-directory={OUTPUT_DIR}",
                str(OUTPUT_TEX)
            ],
            check=True
        )
        print("PDF generated:", OUTPUT_PDF)
    except Exception as e:
        print("Error during PDF compilation:", e)

if __name__ == "__main__":
    generate_latex()

