import json
from pathlib import Path
from llm_analysis.ollama_client import ollama_generate

SUMMARIES = Path("data/summaries.json")

MODEL = "phi3"

def score_job(job):
    prompt = f"""
Rate how well this job fits a candidate with the following background:

- Reliability engineering
- Product integrity
- Physical chemistry
- Hands-on hardware troubleshooting
- AI/ML engineering interest

Job summary:
{job.get('summary')}

Give a score from 0 to 100 and explain briefly.
"""
    response = ollama_generate(MODEL, prompt)

    # Extract score (simple heuristic)
    import re
    match = re.search(r"(\d{1,3})", response)
    score = int(match.group(1)) if match else 50

    return score, response

def main():
    jobs = json.load(open(SUMMARIES))
    for job in jobs:
        score, explanation = score_job(job)
        job["fit_score"] = score
        job["fit_explanation"] = explanation

    json.dump(jobs, open(SUMMARIES, "w"), indent=2)

if __name__ == "__main__":
    main()
