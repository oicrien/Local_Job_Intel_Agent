import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
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

    with ThreadPoolExecutor(max_workers=8) as executor:
        summaries = list(executor.map(summarize_job, jobs))

    for job, summary in zip(jobs, summaries):
        job["summary_qwen2"] = summary

    json.dump(jobs, open(SUMMARIES, "w"), indent=2)
    print("Summaries generated using Qwen2 (parallel).")

if __name__ == "__main__":
    main()
