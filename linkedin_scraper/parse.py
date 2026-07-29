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

def load_raw_results():
    if not RAW_RESULTS.exists():
        raise FileNotFoundError(f"Raw results file not found: {RAW_RESULTS}")
    with RAW_RESULTS.open("r", encoding="utf-8") as f:
        return json.load(f)

def parse_job_html(html_block):
    """Parse a single LinkedIn job HTML block into structured fields."""

    # Skip malformed or empty HTML
    if not html_block or "<html" not in html_block.lower():
        return None

    soup = BeautifulSoup(html_block, "html.parser")

    def safe_select(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    # -----------------------------
    # Extract basic fields FIRST
    # -----------------------------
    title = safe_select(".base-search-card__title")
    company = safe_select(".base-search-card__subtitle")
    location = safe_select(".job-search-card__location")
    description = safe_select(".job-search-card__snippet")

    # Fallback selectors
    if not title:
        title = safe_select(".job-card-list__title")
    if not company:
        company = safe_select(".job-card-container__company-name")
    if not location:
        location = safe_select(".job-card-container__metadata-item")
    if not description:
        description = safe_select(".job-card-list__description")

    # Additional description fallbacks
    if not description:
        description = safe_select(".job-search-card__description")
    if not description:
        description = safe_select(".job-card-container__description")
    if not description:
        description = safe_select(".job-details__content")
    if not description:
        description = safe_select(".job-details__section")
    if not description:
        description = safe_select(".description__text")
    if not description:
        description = safe_select(".job-details__body")
    if not description:
        description = safe_select(".job-details__text")
    if not description:
        description = safe_select(".job-details__main-content")

    # -----------------------------
    # Safe defaults for missing fields
    # -----------------------------
    if not title:
        title = "N/A"
    if not company:
        company = "N/A"
    if not location:
        location = ""
    if not description:
        description = ""

    # -----------------------------
    # Extract semantic fields AFTER basics exist
    # -----------------------------
    job_type = parse_job_type(soup)
    job_level = parse_job_level(soup)
    industry = parse_company_industry(soup)
    remote = is_job_remote(title, description, location)

    # -----------------------------
    # Description cleanup
    # -----------------------------
    if description:
        lowered = description.lower()

        section_headers = [
            "requirements",
            "qualifications",
            "job responsibilities",
            "responsibilities",
            "about the role",
            "about",
            "skills",
            "duties",
            "what you'll do",
            "what you will do",
            "role"
        ]

        extracted = None
        for header in section_headers:
            idx = lowered.find(header)
            if idx != -1:
                extracted = description[idx + len(header):].strip()
                break

        if extracted:
            description = extracted

        MAX_DESC_LEN = 1000
        if len(description) > MAX_DESC_LEN:
            description = description[:MAX_DESC_LEN] + "..."

    # -----------------------------
    # Skip malformed entries
    # -----------------------------
    if title == "N/A" or company == "N/A" or location == "":
        return None

    # -----------------------------
    # Return structured job object
    # -----------------------------
    return {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
        "job_type": job_type,
        "job_level": job_level,
        "industry": industry,
        "remote": remote
    }


def parse_all_jobs(raw_data):
    parsed = []
    seen = set()  # Deduplication across ALL pages

    for entry in raw_data:
        html_block = entry.get("html")
        if not html_block:
            continue

        job = parse_job_html(html_block)
        if not job:
            continue

        # --- Reliability filtering (title + description) ---
        TITLE_KEYWORDS = [
            "reliability",
            "maintenance",
            "asset integrity",
            "failure analysis",
            "condition monitoring",
            "predictive",
            "preventive",
            "equipment engineer",
            "root cause",
            "rca",
            "fmea",
        ]

        DESC_KEYWORDS = [
            "reliability",
            "maintenance",
            "failure",
            "root cause",
            "rca",
            "condition monitoring",
            "predictive",
            "preventive",
            "fmea",
            "pf curve",
        ]

        title_lower = job["title"].lower()
        desc_lower = job["description"].lower() if job["description"] else ""

        # Title must match at least one keyword
        if not any(k in title_lower for k in TITLE_KEYWORDS):
            continue

        # Description must match at least one keyword
        if not any(k in desc_lower for k in DESC_KEYWORDS):
            continue

        # Deduplication key (title/company/location)
        key = (job["title"], job["company"], job["location"])
        if key in seen:
            continue
        seen.add(key)

        parsed.append(job)

        # Hard cap on number of jobs (easy to adjust)
        if len(parsed) >= 60:
            break
            
    return parsed

def save_parsed_results(parsed):
    PARSED_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    with PARSED_RESULTS.open("w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2)

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
