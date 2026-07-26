import json
from pathlib import Path
from bs4 import BeautifulSoup

RAW_RESULTS = Path("data/raw_search_results.json")
PARSED_RESULTS = Path("data/parsed_jobs.json")

def load_raw_results():
    if not RAW_RESULTS.exists():
        raise FileNotFoundError(f"Raw results file not found: {RAW_RESULTS}")
    with RAW_RESULTS.open("r", encoding="utf-8") as f:
        return json.load(f)

def parse_job_html(html_block):
    """Parse a single LinkedIn job HTML block into structured fields."""
    soup = BeautifulSoup(html_block, "html.parser")

    def safe_select(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    # Updated LinkedIn selectors (2024–2026)
    title = safe_select(".base-search-card__title")
    company = safe_select(".base-search-card__subtitle")
    location = safe_select(".job-search-card__location")
    description = safe_select(".job-search-card__snippet")

    # Fallback selectors (older DOM)
    if not title:
        title = safe_select(".job-card-list__title")
    if not company:
        company = safe_select(".job-card-container__company-name")
    if not location:
        location = safe_select(".job-card-container__metadata-item")
    if not description:
        description = safe_select(".job-card-list__description")

    # Skip malformed entries
    if not title or not company or not location:
        return None

    return {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
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

        # Deduplication key (title/company/location)
        key = (job["title"], job["company"], job["location"])
        if key in seen:
            continue
        seen.add(key)

        parsed.append(job)

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
