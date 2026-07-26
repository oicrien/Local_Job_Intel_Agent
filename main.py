import subprocess
from pathlib import Path

# --- DB imports (these are correct for your repo) ---
from storage.db import init_db, get_connection

# --- MODEL SELECTION ---
def select_model():
    print("\n=== MODEL SELECTION ===")
    print("Choose which LLM model to use:")
    print("1. Mistral")
    print("2. Qwen2")
    print("3. Phi3")
    print("4. Default (summarize.py + fit_score.py)")

    choice = input("Enter 1, 2, 3, or 4: ").strip()

    return {
        "1": "mistral",
        "2": "qwen2",
        "3": "phi3",
        "4": "default"
    }.get(choice, "default")

MODEL = select_model()
print(f"Using model: {MODEL}")


# --- Paths for pipeline outputs ---
RAW = Path("data/raw_search_results.json")
PARSED = Path("data/parsed_jobs.json")
SUMMARIES = Path("data/summaries.json")
REPORT_MD = Path("reports/output/weekly_report.md")
REPORT_TEX = Path("reports/output/weekly_report.tex")
REPORT_PDF = Path("reports/output/weekly_report.pdf")

# --- STEP 1: Scraper ---
def run_scraper():
    print("\n=== STEP 1: Scraping LinkedIn ===")
    subprocess.run(["python", "linkedin_scraper/search.py"], check=True)
    if RAW.exists():
        print(f"Raw job data saved to {RAW}")

# --- STEP 2: Parser ---
def run_parser():
    print("\n=== STEP 2: Parsing job HTML ===")
    subprocess.run(["python", "linkedin_scraper/parse.py"], check=True)
    if PARSED.exists():
        print(f"Parsed job data saved to {PARSED}")

# --- STEP 3: Summaries (model‑aware) ---
def run_summarizer():
    print("\n=== STEP 3: Summarizing jobs ===")

    script = {
        "default": "llm_analysis/summarize.py",
        "mistral": "llm_analysis/summarize_mistral.py",
        "qwen2":   "llm_analysis/summarize_qwen2.py",
        "phi3":    "llm_analysis/summarize_phi3.py"
    }.get(MODEL, "llm_analysis/summarize.py")

    subprocess.run(["python", "-m", script.replace("/", ".").replace(".py", "")], check=True)


    if SUMMARIES.exists():
        print(f"Summaries saved to {SUMMARIES}")

# --- STEP 4: Fit scoring (model‑aware) ---
def run_fit_score():
    print("\n=== STEP 4: Scoring job fit ===")

    script = {
        "default": "llm_analysis/fit_score.py",
        "mistral": "llm_analysis/fit_score_mistral.py",
        "qwen2":   "llm_analysis/fit_score_qwen2.py",
        "phi3":    "llm_analysis/fit_score_phi3.py"
    }.get(MODEL, "llm_analysis/fit_score.py")

    subprocess.run(["python", script], check=True)
    print("Fit scores generated.")

# --- STEP 5: Markdown report ---
def run_md_report():
    print("\n=== STEP 5: Generating Markdown report ===")
    subprocess.run(["python", "reports/weekly_report_md.py"], check=True)
    if REPORT_MD.exists():
        print(f"Markdown report saved to {REPORT_MD}")

# --- STEP 6: LaTeX report ---
def run_tex_report():
    print("\n=== STEP 6: Generating LaTeX report ===")
    subprocess.run(["python", "reports/weekly_report_tex.py"], check=True)
    if REPORT_TEX.exists():
        print(f"LaTeX report saved to {REPORT_TEX}")

# --- STEP 7: Compile PDF ---
def compile_pdf():
    print("\n=== STEP 7: Compiling PDF ===")
    subprocess.run([
        "pdflatex",
        "-output-directory", "reports/output",
        str(REPORT_TEX)
    ], check=True)

    if REPORT_PDF.exists():
        print(f"PDF report saved to {REPORT_PDF}")

# --- STEP 8: Ingest into SQLite ---
def ingest_jobs():
    print("\n=== STEP 8: Ingesting jobs into SQLite ===")

    conn = get_connection()
    cur = conn.cursor()

    import json
    parsed = json.load(open(PARSED))

    for job in parsed:
        cur.execute(
            """
            INSERT INTO jobs (source, title, company, location, url, posted_date, raw_text, fit_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.get("source"),
                job.get("title"),
                job.get("company"),
                job.get("location"),
                job.get("url"),
                job.get("listed"),
                job.get("description"),
                job.get("fit_score"),
            ),
        )

    conn.commit()
    conn.close()
    print("Jobs ingested into database.")

# --- MAIN PIPELINE ---
def main():
    print("\n==============================")
    print(" Local Job Intel Agent Pipeline")
    print("==============================")

    # Initialize DB
    init_db()

    # Full pipeline
    run_scraper()
    run_parser()
    run_summarizer()
    run_fit_score()
    run_md_report()
    run_tex_report()
    compile_pdf()
    ingest_jobs()

    print("\n=== Pipeline complete! ===")
    print(f"Your weekly report is ready:\n{REPORT_PDF}\n")

if __name__ == "__main__":
    main()
