import json
from pathlib import Path
from llm_analysis.ollama_client import ollama_generate

PARSED = Path("data/parsed_jobs.json")
SUMMARIES = Path("data/summaries_phi3.json")

MODEL = "phi3"

def summarize_job(job):
    prompt = f"""
Summarize this job posting in 5 short bullet points:

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
        job["summary_phi3"] = summarize_job(job)
        summaries.append(job)

    json.dump(summaries, open(SUMMARIES, "w"), indent=2)
    print("Summaries generated using Phi‑3.")

if __name__ == "__main__":
    main()
