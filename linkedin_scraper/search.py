import json
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

OUTPUT = Path("data/raw_search_results.json")

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def linkedin_login(page):
    page.goto("https://www.linkedin.com/login", timeout=60000)
    page.wait_for_timeout(2000)

    if "feed" in page.url or "jobs" in page.url:
        return

    page.fill('input[name="session_key"]', EMAIL)
    page.fill('input[name="session_password"]', PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_timeout(5000)


def extract_job_ids(page):
    """Extract job IDs from LinkedIn's JSON blobs."""
    content = page.content()
    soup = BeautifulSoup(content, "html.parser")

    job_ids = set()

    # Look for JSON blobs
    for script in soup.find_all("script"):
        if script.string and "jobPosting" in script.string:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and "jobPosting" in data:
                    job_id = data["jobPosting"].get("identifier", {}).get("value")
                    if job_id:
                        job_ids.add(job_id)
            except:
                continue

    return list(job_ids)


def scrape_linkedin_jobs(query="Reliability Engineer", location="Canada", pages=5):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        linkedin_login(page)

        for page_num in range(pages):
            start = page_num * 25

            search_url = (
                f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}"
                f"&location={location.replace(' ', '%20')}&start={start}"
            )

            print(f"\nNavigating to page {page_num+1}/{pages}: {search_url}")
            page.goto(search_url, timeout=60000)
            page.wait_for_timeout(5000)

            job_ids = extract_job_ids(page)
            print(f"Found {len(job_ids)} job IDs on page {page_num+1}")

            # Fetch each job page
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
