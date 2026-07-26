import json
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from llm_analysis.ollama_client import ollama_generate
from tqdm import tqdm

SUMMARIES = Path("data/summaries_phi3.json")
MODEL = "phi3"

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
{job.get('summary_phi3')}

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
        results = list(tqdm(
            executor.map(score_job, jobs),
            total=len(jobs),
            desc="Scoring job fit"
        ))


    for job, (score, explanation) in zip(jobs, results):
        job["fit_score_phi3"] = score
        job["fit_explanation_phi3"] = explanation

    json.dump(jobs, open(SUMMARIES, "w"), indent=2)
    print("Fit scores generated using Phi‑3 (parallel).")

if __name__ == "__main__":
    main()
