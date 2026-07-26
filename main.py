import subprocess
from pathlib import Path

RAW = Path("data/raw_search_results.json")
PARSED = Path("data/parsed_jobs.json")
SUMMARIES = Path("data/summaries.json")
REPORT_MD = Path("reports/output/weekly_report.md")
REPORT_TEX = Path("reports/output/weekly_report.tex")
REPORT_PDF = Path("reports/output/weekly_report.pdf")

def run_scraper():
    print("\n=== STEP 1: Scraping LinkedIn ===")
    subprocess.run(["python", "linkedin_scraper/search.py"], check=True)
    if RAW.exists():
        print(f"Raw job data saved to {RAW}")

def run_parser():
    print("\n=== STEP 2: Parsing job HTML ===")
    subprocess.run(["python", "linkedin_scraper/parse.py"], check=True)
    if PARSED.exists():
        print(f"Parsed job data saved to {PARSED}")

def run_summarizer():
    print("\n=== STEP 3: Summarizing jobs ===")
    subprocess.run(["python", "llm_analysis/summarize.py"], check=True)
    if SUMMARIES.exists():
        print(f"Summaries saved to {SUMMARIES}")

def run_fit_score():
    print("\n=== STEP 4: Scoring job fit ===")
    subprocess.run(["python", "llm_analysis/fit_score.py"], check=True)
    print("Fit scores generated.")

def run_md_report():
    print("\n=== STEP 5: Generating Markdown report ===")
    subprocess.run(["python", "reports/weekly_report_md.py"], check=True)
    if REPORT_MD.exists():
        print(f"Markdown report saved to {REPORT_MD}")

def run_tex_report():
    print("\n=== STEP 6: Generating LaTeX report ===")
    subprocess.run(["python", "reports/weekly_report_tex.py"], check=True)
    if REPORT_TEX.exists():
        print(f"LaTeX report saved to {REPORT_TEX}")

def compile_pdf():
    print("\n=== STEP 7: Compiling PDF ===")
    subprocess.run([
        "pdflatex",
        "-output-directory", "reports/output",
        str(REPORT_TEX)
    ], check=True)

    if REPORT_PDF.exists():
        print(f"PDF report saved to {REPORT_PDF}")

def main():
    print("\n==============================")
    print(" Local Job Intel Agent Pipeline")
    print("==============================")

    # Your existing functions
    from db import init_db
    from ingest import ingest_jobs

    init_db()

    # Full pipeline
    run_scraper()
    run_parser()
    run_summarizer()
    run_fit_score()
    run_md_report()
    run_tex_report()
    compile_pdf()

    # Your existing ingestion step
    ingest_jobs()

    print("\n=== Pipeline complete! ===")
    print(f"Your weekly report is ready:\n{REPORT_PDF}\n")

if __name__ == "__main__":
    main()
