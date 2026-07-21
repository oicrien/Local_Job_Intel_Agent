import json
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT = Path("data/raw_search_results.json")

def scrape_linkedin_jobs(query="Reliability Engineer", location="Canada"):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # LinkedIn job search URL
        search_url = (
            "https://www.linkedin.com/jobs/search/?keywords="
            + query.replace(" ", "%20")
            + "&location="
            + location.replace(" ", "%20")
        )

        print(f"Navigating to {search_url}")
        page.goto(search_url)

        # Scroll to load more jobs
        for _ in range(5):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(1500)

        # Select job cards
        job_cards = page.query_selector_all("div.job-card-container")

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
