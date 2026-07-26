import json
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from llm_analysis.ollama_client import ollama_generate

SUMMARIES = Path("data/summaries_qwen2.json")
MODEL = "qwen2.5:3b"

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
{job.get('summary_qwen2')}

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
        job["fit_score_qwen2"] = score
        job["fit_explanation_qwen2"] = explanation

    json.dump(jobs, open(SUMMARIES, "w"), indent=2)
    print("Fit scores generated using Qwen2 (parallel).")

if __name__ == "__main__":
    main()
