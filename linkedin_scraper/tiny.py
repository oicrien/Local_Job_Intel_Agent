from playwright.sync_api import sync_playwright
import json

JOB_ID = "4334423582"   # you can replace this with any ID from your guest API results
API_URL = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{JOB_ID}"

PROFILE_PATH = "/home/twig/.playwright-profile"

def main():
    with sync_playwright() as p:
        print("Launching browser with persistent LinkedIn profile...")
        browser = p.chromium.launch_persistent_context(
            PROFILE_PATH,
            headless=False
        )

        page = browser.new_page()

        print(f"\nRequesting jobPosting API:\n{API_URL}\n")
        response = page.request.get(API_URL, timeout=15000)

        print("Status:", response.status)

        text = response.text()
        print("\n--- Raw Response (first 500 chars) ---\n")
        print(text[:500])

        print("\n--- JSON Parse Attempt ---")
        try:
            data = response.json()
            print("JSON parsed successfully!")
            print(json.dumps(data, indent=2)[:500])
        except Exception as e:
            print("JSON parsing failed:", e)

        browser.close()

if __name__ == "__main__":
    main()
