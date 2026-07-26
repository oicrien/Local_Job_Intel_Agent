import json
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT = Path("data/raw_search_results.json")

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def linkedin_login(page):
    print("Logging into LinkedIn...")

    # Go to login page
    page.goto("https://www.linkedin.com/login", timeout=60000)
    page.wait_for_timeout(2000)

    # If redirected to feed or jobs, you're already logged in
    if "feed" in page.url or "jobs" in page.url:
        print("Already logged in — skipping login.")
        return

    # Otherwise perform login
    try:
        page.fill('input[name="session_key"]', EMAIL)
        page.fill('input[name="session_password"]', PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_timeout(5000)
    except Exception as e:
        print(f"Login form not found, skipping login. Reason: {e}")
        return

    if "feed" in page.url or "jobs" in page.url:
        print("Login successful.")
    else:
        print("Login may have failed — continuing anyway.")


def scrape_linkedin_jobs(query="Reliability Engineer", location="Canada", pages=5):
    results = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        linkedin_login(page)

        for page_num in range(pages):
            start = page_num * 25

            search_url = (
                "https://www.linkedin.com/jobs/search/?keywords="
                + query.replace(" ", "%20")
                + "&location="
                + location.replace(" ", "%20")
                + f"&start={start}"
            )

            print(f"\nNavigating to page {page_num+1}/{pages}: {search_url}")
            page.goto(search_url, timeout=60000)

            page.wait_for_timeout(5000)

            for _ in range(8):
                page.mouse.wheel(0, 4000)
                page.wait_for_timeout(1500)

            job_cards = page.query_selector_all(
                "div.job-search-card, li.jobs-search-results__list-item, div.base-card"
            )



            print(f"Found {len(job_cards)} job cards on page {page_num+1}")

            for card in job_cards:
                html = card.inner_html()

                if not html or len(html.strip()) < 50:
                    continue

                key = hash(html)
                if key in seen:
                    continue
                seen.add(key)

                results.append({"html": html})

        browser.close()

    print(f"\nValid job cards after filtering: {len(results)}")
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
