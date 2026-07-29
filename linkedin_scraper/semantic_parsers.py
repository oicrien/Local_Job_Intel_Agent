from bs4 import BeautifulSoup

# -----------------------------
# JobSpy semantic parsing utils
# -----------------------------

def parse_job_type(soup: BeautifulSoup):
    """
    Extracts job type (Full-time, Part-time, Contract, etc.)
    """
    h3_tag = soup.find(
        "h3",
        class_="description__job-criteria-subheader",
        string=lambda text: "Employment type" in text if text else False,
    )
    if not h3_tag:
        return None

    span = h3_tag.find_next_sibling(
        "span",
        class_="description__job-criteria-text description__job-criteria-text--criteria",
    )
    if not span:
        return None

    employment_type = span.get_text(strip=True).lower().replace("-", "")
    return employment_type


def parse_job_level(soup: BeautifulSoup):
    """
    Extracts seniority level (Entry, Mid, Senior, etc.)
    """
    h3_tag = soup.find(
        "h3",
        class_="description__job-criteria-subheader",
        string=lambda text: "Seniority level" in text if text else False,
    )
    if not h3_tag:
        return None

    span = h3_tag.find_next_sibling(
        "span",
        class_="description__job-criteria-text description__job-criteria-text--criteria",
    )
    return span.get_text(strip=True) if span else None


def parse_company_industry(soup: BeautifulSoup):
    """
    Extracts company industry (Manufacturing, Software, etc.)
    """
    h3_tag = soup.find(
        "h3",
        class_="description__job-criteria-subheader",
        string=lambda text: "Industries" in text if text else False,
    )
    if not h3_tag:
        return None

    span = h3_tag.find_next_sibling(
        "span",
        class_="description__job-criteria-text description__job-criteria-text--criteria",
    )
    return span.get_text(strip=True) if span else None


def is_job_remote(title: str, description: str, location: str):
    """
    Determines if a job is remote based on title, description, and location.
    """
    remote_keywords = ["remote", "work from home", "wfh"]

    combined = f"{title} {description} {location}".lower()
    return any(keyword in combined for keyword in remote_keywords)
