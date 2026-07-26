import json
from pathlib import Path
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
    summaries = []

    for job in jobs:
        job["summary_mistral"] = summarize_job(job)
        summaries.append(job)

    json.dump(summaries, open(SUMMARIES, "w"), indent=2)
    print("Summaries generated using Mistral.")

if __name__ == "__main__":
    main()
