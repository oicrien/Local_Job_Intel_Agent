# Use bash for better scripting
SHELL := /bin/bash

# Virtual environment activation
VENV = source venv/bin/activate

# Default target
.PHONY: report db md pdf clean

report: db md pdf
    @echo "Full report pipeline complete."

db:
    @$(VENV) && python3 main.py
    @echo "Database regenerated."

md:
    @$(VENV) && python3 reports/weekly_report_md.py
    @echo "Markdown report generated."

pdf:
    @$(VENV) && python3 reports/weekly_report_tex.py
    @echo "PDF report generated."

clean:
    rm -f reports/output/*.aux reports/output/*.log reports/output/*.out
    @echo "Cleaned LaTeX build artifacts."
