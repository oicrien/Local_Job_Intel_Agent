import json
from pathlib import Path

OUTPUT = Path("data/raw_search_results.json")

def fake_linkedin_results():
    return [
        {
            "html": f"""
                <div class="job-card">
                    <h3 class="job-card-list__title">Reliability Engineer</h3>
                    <span class="job-card-container__company-name">FusionTech Labs</span>
                    <span class="job-card-container__metadata-item">Vancouver, BC</span>
                    <p class="job-card-list__description">
                        We are seeking a reliability engineer with experience in product integrity and safety...
                    </p>
                </div>
            """
        },
        {
            "html": f"""
                <div class="job-card">
                    <h3 class="job-card-list__title">Radiation Protection Technologist</h3>
                    <span class="job-card-container__company-name">CleanCore Energy</span>
                    <span class="job-card-container__metadata-item">Burnaby, BC</span>
                    <p class="job-card-list__description">
                        NRRPT certification preferred. Experience in nuclear operations and safety...
                    </p>
                </div>
            """
        },
    ]

def save_results(results):
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved raw results to {OUTPUT}")

def main():
    results = fake_linkedin_results()
    save_results(results)

if __name__ == "__main__":
    main()
