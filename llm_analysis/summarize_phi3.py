import json
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from concurrent.futures import ThreadPoolExecutor
from llm_analysis.ollama_client import ollama_generate
from tqdm import tqdm


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

    with ThreadPoolExecutor(max_workers=8) as executor:
        summaries = list(tqdm(
            executor.map(summarize_job, jobs),
            total=len(jobs),
            desc="Summarizing jobs"
        ))


    for job, summary in zip(jobs, summaries):
        job["summary_phi3"] = summary

    json.dump(jobs, open(SUMMARIES, "w"), indent=2)
    print("Summaries generated using Phi‑3 (parallel).")

if __name__ == "__main__":
    main()
