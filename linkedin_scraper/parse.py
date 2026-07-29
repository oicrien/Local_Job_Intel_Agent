import json
from pathlib import Path
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from linkedin_scraper.semantic_parsers import (
    parse_job_type,
    parse_job_level,
    parse_company_industry,
    is_job_remote
)

RAW_RESULTS = Path("data/raw_search_results.json")
PARSED_RESULTS = Path("data/parsed_jobs.json")


# -------------------------
# Load raw HTML results
# -------------------------
def load_raw_results():
    if not RAW_RESULTS.exists():
        raise FileNotFoundError(f"Raw results file not found: {RAW_RESULTS}")
    with RAW_RESULTS.open("r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------
# Parse a single job PAGE (HTML)
# -------------------------
def parse_job_page(job_entry):
    """
    job_entry structure:
    {
        "job_id": "...",
        "html": "<!DOCTYPE html>..."
    }
    """

    html = job_entry.get("html")
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # -----------------------------
    # Extract basic fields
    # -----------------------------
    def safe_text(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    # Job title
    title = safe_text("h1.top-card-layout__title")
    if not title:
        title = safe_text("h1.top-card__title")  # fallback

    # Company name
    company = safe_text("a.top-card-layout__company-url")
    if not company:
        company = safe_text("span.top-card-layout__company-name")
    if not company:
        company = safe_text("a.topcard__org-name-link")  # fallback

    # Location
    location = safe_text("span.top-card-layout__location")
    if not location:
        location = safe_text("span.topcard__flavor--bullet")  # fallback

    # Description (full HTML)
    desc_el = soup.select_one("div.description__text")
    if not desc_el:
        desc_el = soup.select_one("section.description")  # fallback

    description_html = desc_el.decode_contents() if desc_el else ""
    description_text = strip_html(description_html)

    # -----------------------------
    # Skip malformed entries
    # -----------------------------
    if not title or not company or not location:
        return None

    # -----------------------------
    # Semantic fields
    # -----------------------------
    job_type = parse_job_type(description_text)
    job_level = parse_job_level(description_text)
    industry = parse_company_industry(description_text)
    remote = is_job_remote(title, description_text, location)

    # -----------------------------
    # Return structured job object
    # -----------------------------
    return {
        "job_id": job_entry.get("job_id"),
        "title": title,
        "company": company,
        "location": location,
        "description": description_text,
        "job_type": job_type,
        "job_level": job_level,
        "industry": industry,
        "remote": remote
    }


# -------------------------
# Strip HTML tags from description
# -------------------------
def strip_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ", strip=True)


# -------------------------
# Parse all jobs
# -------------------------
def parse_all_jobs(raw_data):
    parsed = []
    seen = set()

    for entry in raw_data:
        job = parse_job_page(entry)
        if not job:
            continue

        # --- Reliability filtering ---
        TITLE_KEYWORDS = [
            "reliability", "maintenance", "asset integrity",
            "failure analysis", "condition monitoring",
            "predictive", "preventive", "equipment engineer",
            "root cause", "rca", "fmea",
        ]

        DESC_KEYWORDS = [
            "reliability", "maintenance", "failure",
            "root cause", "rca", "condition monitoring",
            "predictive", "preventive", "fmea", "pf curve",
        ]

        title_lower = job["title"].lower()
        desc_lower = job["description"].lower()

        if not any(k in title_lower for k in TITLE_KEYWORDS):
            continue
        if not any(k in desc_lower for k in DESC_KEYWORDS):
            continue

        # Deduplication
        key = (job["title"], job["company"], job["location"])
        if key in seen:
            continue
        seen.add(key)

        parsed.append(job)

        if len(parsed) >= 60:
            break

    return parsed


# -------------------------
# Save parsed results
# -------------------------
def save_parsed_results(parsed):
    PARSED_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    with PARSED_RESULTS.open("w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2)


# -------------------------
# Main
# -------------------------
def main():
    print("Loading raw search results...")
    raw_data = load_raw_results()

    print(f"Parsing {len(raw_data)} job entries...")
    parsed = parse_all_jobs(raw_data)

    print(f"Saving parsed results to {PARSED_RESULTS}")
    save_parsed_results(parsed)

    print("Parsing complete.")


if __name__ == "__main__":
    main()
