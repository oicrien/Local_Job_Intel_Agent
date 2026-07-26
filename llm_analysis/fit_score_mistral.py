import json
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from llm_analysis.ollama_client import ollama_generate

SUMMARIES = Path("data/summaries_mistral.json")
MODEL = "mistral:7b-instruct-q4_K_M"

def score_job(job):
    prompt = f"""
Evaluate job fit for a candidate with this background:

- Reliability engineering
- Product integrity
- Physical chemistry
- Hardware troubleshooting
- AI/ML engineering interest
- Nuclear safety & fusion operations interest

Job summary:
{job.get('summary_mistral')}

Provide:
Score: <0-100>
Explanation: <3–6 sentences>
"""
    response = ollama_generate(MODEL, prompt)

    match = re.search(r"Score:\s*(\d{1,3})", response)
    score = int(match.group(1)) if match else None

    return score, response

def main():
    jobs = json.load(open(SUMMARIES))

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(score_job, jobs))

    for job, (score, explanation) in zip(jobs, results):
        job["fit_score_mistral"] = score
        job["fit_explanation_mistral"] = explanation

    json.dump(jobs, open(SUMMARIES, "w"), indent=2)
    print("Fit scores generated using Mistral (parallel).")

if __name__ == "__main__":
    main()
