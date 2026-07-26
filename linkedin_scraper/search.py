import json
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT = Path("data/raw_search_results.json")

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def scrape_linkedin_jobs(query="Reliability Engineer", location="Canada"):
    if not EMAIL or not PASSWORD:
        raise RuntimeError("Missing LINKEDIN_EMAIL or LINKEDIN_PASSWORD environment variables.")

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # --- Automatic Login ---
        print("Opening LinkedIn login page...")
        page.goto("https://www.linkedin.com/login", timeout=60000)
        
        # Wait for the login form to appear
        page.wait_for_selector('input[name="session_key"]', timeout=20000)
        
        print("Filling login form...")
        page.fill('input[name="session_key"]', EMAIL)
        page.fill('input[name="session_password"]', PASSWORD)
        
        # Click the sign-in button
        page.click('button[type="submit"]')
        
        # Wait for login to complete
        page.wait_for_timeout(5000)


        # --- Navigate to job search ---
        search_url = (
            "https://www.linkedin.com/jobs/search/?keywords="
            + query.replace(" ", "%20")
            + "&location="
            + location.replace(" ", "%20")
        )

        print(f"Navigating to {search_url}")
        page.goto(search_url, timeout=60000)

        # --- Scroll to load dynamic job cards ---
        for _ in range(6):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(1500)

        # --- Correct LinkedIn job card selector ---
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
