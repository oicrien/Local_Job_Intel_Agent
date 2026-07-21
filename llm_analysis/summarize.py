import json
from pathlib import Path

PARSED = Path("data/parsed_jobs.json")
SUMMARIES = Path("data/summaries.json")

def load_parsed_jobs():
    if not PARSED.exists():
        raise FileNotFoundError(f"Parsed job file not found: {PARSED}")
    with PARSED.open("r", encoding="utf-8") as f:
        return json.load(f)

def local_summary(job):
    """
    Lightweight summarizer stub.
    Replace this with a real LLM call later.
    """
    title = job.get("title") or "Unknown role"
    company = job.get("company") or "Unknown company"
    location = job.get("location") or "Unknown location"
    description = job.get("description") or ""

    summary = (
        f"{title} at {company} in {location}. "
        f"Key details: {description[:200]}..."
    )

    return summary

def summarize_all(jobs):
    summaries = []
    for job in jobs:
        summaries.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "summary": local_summary(job)
        })
    return summaries

def save_summaries(summaries):
    SUMMARIES.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARIES.open("w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2)
    print(f"Saved summaries to {SUMMARIES}")

def main():
    print("Loading parsed jobs...")
    jobs = load_parsed_jobs()

    print(f"Generating summaries for {len(jobs)} jobs...")
    summaries = summarize_all(jobs)

    print("Saving summaries...")
    save_summaries(summaries)

    print("Summarization complete.")

if __name__ == "__main__":
    main()
