def simple_fit_score(job, skills_keywords=None):
    if skills_keywords is None:
        skills_keywords = [
            "reliability",
            "product integrity",
            "nuclear",
            "fusion",
            "NRRPT",
            "safety",
        ]

    text = (job.get("raw_text") or "").lower()
    score = 0

    for kw in skills_keywords:
        if kw.lower() in text:
            score += 1

    max_score = len(skills_keywords)
    return score / max_score if max_score > 0 else 0.0

