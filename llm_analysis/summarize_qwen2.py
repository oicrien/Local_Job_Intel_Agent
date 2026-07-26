import json
from pathlib import Path
from llm_analysis.ollama_client import ollama_generate

PARSED = Path("data/parsed_jobs.json")
SUMMARIES = Path("data/summaries_qwen2.json")

MODEL = "qwen2.5:3b"

def summarize_job(job):
    prompt = f"""
Provide a concise 5‑bullet summary of this job posting:

Title: {job.get('title')}
Company: {job.get('company')}
Location: {job.get('location')}
Description:
{job.get('description')}
"""
    return ollama_generate(MODEL, prompt)

def main():
    jobs = json.load(open(PARSED))
    summaries = []

    for job in jobs:
        job["summary_qwen2"] = summarize_job(job)
        summaries.append(job)

    json.dump(summaries, open(SUMMARIES, "w"), indent=2)
    print("Summaries generated using Qwen2.")

if __name__ == "__main__":
    main()
