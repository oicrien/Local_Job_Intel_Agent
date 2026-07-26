import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from llm_analysis.ollama_client import ollama_generate

PARSED = Path("data/parsed_jobs.json")
SUMMARIES = Path("data/summaries_mistral.json")

MODEL = "mistral:7b-instruct-q4_K_M"

def summarize_job(job):
    prompt = f"""
Summarize the following job posting in 5 bullet points:

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
        job["summary_mistral"] = summary

    json.dump(jobs, open(SUMMARIES, "w"), indent=2)
    print("Summaries generated using Mistral (parallel).")

if __name__ == "__main__":
    main()
