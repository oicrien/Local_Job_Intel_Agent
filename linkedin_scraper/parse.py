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

    return {
        "title": safe_select(".job-card-list__title"),
        "company": safe_select(".job-card-container__company-name"),
        "location": safe_select(".job-card-container__metadata-item"),
        "listed": safe_select(".job-card-list__footer-wrapper"),
        "description": safe_select(".job-card-list__description"),
        "source": safe_select(".job-card-list_source"),
    }

def parse_all_jobs(raw_data):
    parsed = []

    for entry in raw_data:
        html_block = entry.get("html")
        if not html_block:
            continue
        parsed.append(parse_job_html(html_block))

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
