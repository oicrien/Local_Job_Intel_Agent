import json
import os
import time
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

OUTPUT = Path("data/raw_search_results.json")

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")


# -------------------------
# LinkedIn Login (Playwright)
# -------------------------
def linkedin_login(page):
    # Go to login page
    page.goto("https://www.linkedin.com/login", timeout=60000)
    page.wait_for_timeout(2000)

    # If LinkedIn auto-redirected you to feed or jobs, you're already logged in
    if "feed" in page.url or "jobs" in page.url:
        print("Already logged in — skipping login.")
        return

    # Check if login form exists
    try:
        page.wait_for_selector('input[name="session_key"]', timeout=5000)
    except:
        print("Login form not found — assuming already logged in.")
        return

    # Perform login
    print("Logging in with credentials...")
    page.fill('input[name="session_key"]', EMAIL)
    page.fill('input[name="session_password"]', PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_timeout(5000)

    if "feed" in page.url or "jobs" in page.url:
        print("Login successful.")
    else:
        print("Login may have failed — continuing anyway.")


# -------------------------
# Guest API Job ID Extractor
# -------------------------
def fetch_job_ids_via_guest_api(query, location, start=0):
    """
    Uses LinkedIn's internal guest API to reliably extract job IDs.
    This replaces brittle DOM scraping of job cards.
    """

    params = {
        "keywords": query,
        "location": location,
        "start": start,
        "pageNum": 0,
    }

    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"

    try:
        response = requests.get(url, params=params, timeout=10)
    except Exception as e:
        print(f"Guest API request failed: {e}")
        return []

    if response.status_code != 200:
        print(f"Guest API error: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("div", class_="base-search-card")

    job_ids = []

    for card in job_cards:
        href_tag = card.find("a", class_="base-card__full-link")
        if not href_tag:
            continue

        href = href_tag.get("href")
        if not href:
            continue

        href = href.split("?")[0]
        job_id = href.split("-")[-1]

        job_ids.append(job_id)

    return job_ids


# -------------------------
# Main Scraper
# -------------------------
def scrape_linkedin_jobs(query="Reliability Engineer", location="Canada", pages=5):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            "/home/twig/.playwright-profile",
            headless=False
        )
        page = browser.new_page()


        linkedin_login(page)

        for page_num in range(pages):
            start = page_num * 25

            print(f"\nFetching job IDs via guest API (page {page_num+1}/{pages})...")
            job_ids = fetch_job_ids_via_guest_api(query, location, start=start)
            print(f"Found {len(job_ids)} job IDs on page {page_num+1}")

            # Fetch each job page using Playwright
            for job_id in job_ids:
                job_url = f"https://www.linkedin.com/jobs/view/{job_id}"
                print(f"Fetching job page: {job_url}")

                page.goto(job_url, timeout=60000)
                page.wait_for_timeout(3000)

                html = page.content()
                results.append({"html": html, "job_id": job_id})

        browser.close()

    print(f"\nTotal job pages fetched: {len(results)}")
    return results


# -------------------------
# Save Results
# -------------------------
def save_results(results):
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved raw results to {OUTPUT}")


# -------------------------
# Main Entry
# -------------------------
def main():
    results = scrape_linkedin_jobs()
    save_results(results)


if __name__ == "__main__":
    main()
