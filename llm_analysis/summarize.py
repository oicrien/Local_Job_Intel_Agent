import json
from pathlib import Path
from llm_analysis.ollama_client import ollama_generate

PARSED = Path("data/parsed_jobs.json")
SUMMARIES = Path("data/summaries.json")

MODEL = "phi3"   # or qwen2.5:3b or mistral:7b-instruct-q4_K_M

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
        summary = summarize_job(job)
        job["summary"] = summary
        summaries.append(job)

    json.dump(summaries, open(SUMMARIES, "w"), indent=2)

if __name__ == "__main__":
    main()
