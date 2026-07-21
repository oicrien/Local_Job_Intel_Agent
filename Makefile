SHELL := /bin/bash
VENV = source venv/bin/activate

.PHONY: pipeline scrape analyze db md pdf report clean

# Full pipeline: scrape → analyze → db → md → pdf
pipeline: scrape analyze db md pdf
    @echo "Full pipeline complete."

# Scrape job listings
scrape:
    @$(VENV) && python3 linkedin_scraper/search.py
    @$(VENV) && python3 linkedin_scraper/parse.py
    @echo "Scraping complete."

# Analyze listings (summaries + fit scores)
analyze:
    @$(VENV) && python3 llm_analysis/summarize.py
    @$(VENV) && python3 llm_analysis/fit_score.py
    @echo "Analysis complete."

# Regenerate the SQLite database
db:
    @$(VENV) && python3 main.py
    @echo "Database regenerated."

# Generate Markdown report
md:
    @$(VENV) && python3 reports/weekly_report_md.py
    @echo "Markdown report generated."

# Generate PDF report
pdf:
    @$(VENV) && python3 reports/weekly_report_tex.py
    @echo "PDF report generated."

# Clean LaTeX build artifacts
clean:
    rm -f reports/output/*.aux reports/output/*.log reports/output/*.out
    @echo "Cleaned LaTeX build artifacts."

