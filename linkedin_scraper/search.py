import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

OUTPUT = Path("data/raw_search_results.json")

def scrape_linkedin_jobs(query="Reliability Engineer", location="Canada"):
    results = []

    with sync_playwright() as p:
        # IMPORTANT: LinkedIn blocks headless scrapers
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        search_url = (
            "https://www.linkedin.com/jobs/search/?keywords="
            + query.replace(" ", "%20")
            + "&location="
            + location.replace(" ", "%20")
        )

        print(f"Navigating to {search_url}")
        page.goto(search_url, timeout=60000)

        print("If LinkedIn asks you to log in, do it manually.")
        time.sleep(20)  # allow login + JS load

        # Scroll to load dynamic job cards
        for _ in range(6):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(1500)

        # Updated selector — LinkedIn changed their DOM
        job_cards = page.query_selector_all("div.base-card")

        print(f"Found {len(job_cards)} job cards")

        for card in job_cards:
            html = card.inner_html()
            results.append({"html": html})

        browser.close()

    return results

def save_results(results):
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved raw results to {OUTPUT}")

def main():
    results = scrape_linkedin_jobs()
    save_results(results)

if __name__ == "__main__":
    main()
