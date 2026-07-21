# Local_Job_Intel_Agent
A fully local, privacy-safe Ai agent that scrapes, summarizes, scores, and tracks job listings using local LLMs - with ZERO cloud dependencies

All intelligence runs locally on the user’s machine.

🚀 Project Overview
Local_Job_Intel_Agent is a modular, CPU‑friendly job‑analysis system designed to help job seekers efficiently navigate technical roles without relying on external APIs or automated submissions.

The agent performs four core tasks:

Scrape job listings (read‑only, human‑in‑the‑loop)

Summarize and analyze each posting using a local LLM

Score job relevance based on user‑defined skills

Track results and generate weekly GitHub‑ready reports

## LaTeX Reports (Overleaf Integration)

This project generates weekly LaTeX reports as well in `reports/weekly_report.tex`.
These can be uploaded directly into an Overleaf project for professional formatting, and
PDF export.

This project is ideal for showcasing:

Python automation

Local LLM integration

Data engineering

Privacy‑aware system design

Recruiter‑friendly reporting

Real‑world workflow optimization

LaTex Report generation

🧠 Why Local‑Only?
Most AI job‑search tools rely on cloud APIs, auto‑apply pipelines, or third‑party services. This project intentionally avoids all of that.

Benefits of local‑only architecture:

Zero cost

Zero external data exposure

Zero risk of violating LinkedIn automation rules

Zero immigration‑related digital footprint concerns

Full control over the entire pipeline

🏗️ Architecture
The system is built as a clean, modular pipeline:

📁 Project Structure (Readable Format)
linkedin_scraper/
Playwright/Selenium‑based job scraping

search.py

parse.py

llm_analysis/
Local LLM summarization and scoring

summarize.py

fit_score.py

storage/
SQLite database and data models

db.py

models.py

reports/
Weekly report generators

weekly_report_md.py — Markdown report generator

weekly_report_tex.py — LaTeX report generator

templates/

report_template.tex — Base LaTeX template

github_automation/
Automated weekly GitHub commits

commit_and_push.py

config/
User‑defined settings

settings.yaml

data/
Raw and processed job listings

(SQLite DB + JSON dumps live here)

main.py
Pipeline entry point

🔍 Core Features
1. Local LinkedIn Scraping (Read‑Only)
Uses Playwright/Selenium to extract job listings without automating applications or messaging.

2. Local LLM Summaries
Runs small, CPU‑friendly models such as:

Phi‑3 Mini

Mistral 7B (quantized)

Qwen 2.5 3B

Tasks include:

Job summarization

Skill extraction

Fit scoring

3. SQLite Job Tracking
Stores:

Title

Company

Location

Posting date

Raw text

Fit score

Timestamps

4. Weekly GitHub Reports
Generates Markdown summaries of:

Jobs found

Fit scores

Skill gaps

Learning progress

Agent improvements

Then commits them automatically.

📦 Installation
Clone the repository:

bash
git clone https://github.com/<your-username>/Local_Job_Intel_Agent.git
cd Local_Job_Intel_Agent
Install dependencies:

bash
pip install -r requirements.txt
Initialize the database:

bash
python3 main.py
🛠️ Roadmap
Phase 1 — MVP (Complete)
Project structure

Basic scraping stub

SQLite storage

Simple keyword‑based scoring

Phase 2 — Local LLM Integration
Add Ollama or GPT4All

Replace keyword scoring with LLM scoring

Add job summarization

Phase 3 — Reporting
Weekly Markdown report generator

GitHub auto‑commit script

Phase 4 — Advanced Intelligence
Skill‑gap analysis

Resume‑to‑job matching

Recruiter‑note generation

Fusion/Nuclear/NRRPT‑specific job filters

🔒 Privacy & Compliance
This project is intentionally designed to be:

Local‑only

Human‑in‑the‑loop

Read‑only

Non‑automated for submissions

Safe for immigration review

Safe for LinkedIn account integrity

No cloud APIs.
No auto‑apply.
No automated messaging.
No external data sharing.

📄 License
MIT License — simple, permissive

🤝 Contributing
Pull requests are welcome.
This project is intentionally modular to encourage extension and experimentation.

🧩 Maintainer
oicrien — Chemist, reliability engineer, and AI systems builder.
