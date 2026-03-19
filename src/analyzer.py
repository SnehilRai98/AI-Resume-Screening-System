import re

# Expanded skill list covering most common JD requirements
SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "r",

    # Web / Frontend
    "html", "css", "react", "angular", "vue", "next.js", "tailwind",
    "jquery", "webpack", "sass",

    # Backend / Frameworks
    "django", "flask", "fastapi", "spring boot", "node.js", "express",
    "rest api", "graphql", "microservices",

    # Data & Analytics
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "excel",
    "pandas", "numpy", "scipy", "data analysis", "statistics",
    "etl", "data pipeline", "data warehousing",

    # Data Visualization
    "tableau", "power bi", "matplotlib", "seaborn", "plotly", "looker",

    # Machine Learning / AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "hugging face",
    "llm", "openai", "langchain", "rag",

    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "ci/cd", "jenkins", "github actions", "linux", "bash",

    # Tools & Platforms
    "git", "github", "jira", "confluence", "postman", "figma",
    "notion", "slack",

    # Soft / Domain
    "agile", "scrum", "product management", "communication",
    "problem solving", "team player", "leadership",
]


def normalize(text: str) -> str:
    """Lowercase and collapse whitespace."""
    return re.sub(r"\s+", " ", text.lower().strip())


def extract_skills(text: str) -> set:
    """Extract skills from text using word-boundary matching to avoid false positives."""
    text = normalize(text)
    found = set()
    for skill in SKILLS:
        # Use word-boundary regex so 'r' doesn't match inside 'user'
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found.add(skill)
    return found


def analyze_resume(resume_text: str, jd_text: str):
    """
    Returns:
        strengths (list): skills present in both resume and JD (max 5)
        gaps     (list): skills in JD missing from resume (max 5)
    """
    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    matched = sorted(jd_skills.intersection(resume_skills))
    missing = sorted(jd_skills.difference(resume_skills))

    return matched[:5], missing[:5]


def skill_match_score(resume_text: str, jd_text: str) -> float:
    """Returns skill match as a 0-100 percentage."""
    jd_skills = extract_skills(jd_text)
    if not jd_skills:
        return 0.0

    resume_skills = extract_skills(resume_text)
    matched = jd_skills.intersection(resume_skills)
    return round((len(matched) / len(jd_skills)) * 100, 2)


def get_recommendation(final_score: float) -> str:
    """Labels aligned with the assessment spec."""
    if final_score >= 65:
        return "Strong Fit"
    elif final_score >= 40:
        return "Moderate Fit"
    else:
        return "Not Fit"
