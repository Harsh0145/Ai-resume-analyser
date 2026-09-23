import re
from collections import Counter

SKILLS = [
    "python", "java", "c++", "c#", ".net", "sql", "mysql", "postgresql",
    "mongodb", "javascript", "typescript", "react", "node.js", "flask",
    "django", "fastapi", "pandas", "numpy", "matplotlib", "seaborn",
    "scikit-learn", "tensorflow", "pytorch", "machine learning",
    "deep learning", "data analysis", "data science", "statistics",
    "power bi", "tableau", "excel", "git", "github", "docker", "aws",
    "azure", "rest api", "nlp", "spark", "hadoop",
]

SECTIONS = {
    "summary": ["summary", "profile", "objective", "professional summary"],
    "skills": ["skills", "technical skills", "core skills", "technologies"],
    "experience": ["experience", "work experience", "employment", "internship"],
    "education": ["education", "academic background", "qualifications"],
    "projects": ["projects", "academic projects", "personal projects"],
    "certifications": ["certifications", "certificates", "courses"],
}

STOP = {
    "the", "and", "for", "with", "from", "this", "that", "are", "you", "your",
    "our", "will", "have", "has", "not", "but", "all", "can", "job", "role",
    "work", "using", "use", "their", "they", "what", "who", "looking", "required",
    "preferred", "strong", "good", "candidate", "ability", "years", "year", "a",
    "an", "to", "in", "of", "on", "as", "or", "be", "is", "we", "team",
    "responsibilities", "requirements", "skills", "experience", "including",
}

ACTION = {
    "built", "developed", "created", "designed", "implemented", "analysed",
    "analyzed", "automated", "optimized", "improved", "deployed", "integrated",
    "engineered", "managed", "tested", "reduced", "increased", "led", "configured",
    "trained",
}


def norm(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def contains_term(text, term):
    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return bool(re.search(pattern, text))


def detect_sections(text):
    low = norm(text)
    return {name: any(alias in low for alias in aliases) for name, aliases in SECTIONS.items()}


def skills_in(text):
    low = norm(text)
    return sorted(skill for skill in SKILLS if contains_term(low, skill))


def jd_keywords(jd):
    low = norm(jd)
    found = set(skills_in(jd))
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", low)
    counts = Counter(word for word in words if word not in STOP)

    for word, count in counts.most_common(40):
        if count >= 2:
            found.add(word)

    return sorted(found)


def analyse_resume(resume, jd=""):
    low = norm(resume)
    sections = detect_sections(resume)
    skills = skills_in(resume)
    words = re.findall(r"\b[\w+#.-]+\b", resume)
    word_count = len(words)
    bullets = len(re.findall(r"(?m)^\s*[-•*]\s+", resume))
    quantified = len(
        re.findall(
            r"\b\d+(?:\.\d+)?\s*(?:%|percent|x|users|projects|years|months|hours|days|₹|\$)\b",
            low,
        )
    )
    email = bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume))
    phone = bool(re.search(r"(?:\+91[\s-]?)?[6-9]\d{9}\b", resume))
    action = sum(
        1
        for verb in ACTION
        if re.search(r"(?<!\w)" + re.escape(verb) + r"(?!\w)", low)
    )

    jdks = jd_keywords(jd) if jd.strip() else []
    matched = [keyword for keyword in jdks if contains_term(low, keyword)]
    missing = [keyword for keyword in jdks if keyword not in matched]
    keyword_pct = round(len(matched) / len(jdks) * 100) if jdks else None

    section_score = round(sum(sections.values()) / 6 * 25)
    content_score = min(25, 8 + min(8, bullets) + min(5, quantified) + min(4, action // 2))
    contact_score = 10 if email and phone else 5 if email or phone else 0

    readability_score = 20
    if word_count < 250:
        readability_score -= 8
    if word_count > 1000:
        readability_score -= 6
    if bullets < 3:
        readability_score -= 5

    keyword_score = round(keyword_pct * 0.20) if keyword_pct is not None else 15

    score_components = {
        "sections": section_score,
        "content": content_score,
        "contact": contact_score,
        "readability": readability_score,
        "job_keyword_alignment": keyword_score,
    }
    ats = max(0, min(100, sum(score_components.values())))

    strengths = []
    issues = []
    recommendations = []

    if email and phone:
        strengths.append("Email and phone number detected.")
    else:
        issues.append("Add a professional email address and phone number.")

    if len(skills) >= 5:
        strengths.append(f"{len(skills)} technical skills detected.")
    else:
        issues.append("Expand the technical skills section with relevant tools you genuinely know.")

    if bullets >= 5:
        strengths.append("Good use of bullet points for scanability.")
    else:
        issues.append("Use concise bullet points for projects and experience.")

    if quantified:
        strengths.append("Quantified achievements were detected.")
    else:
        issues.append("Add measurable results to projects where possible.")

    missing_sections = [name.title() for name, present in sections.items() if not present]
    if missing_sections:
        recommendations.append("Add relevant missing sections: " + ", ".join(missing_sections) + ".")

    if jdks:
        recommendations.append(
            f"Current job-description keyword overlap is {keyword_pct}%. "
            "Add only relevant missing terms you genuinely know."
        )
        if missing:
            recommendations.append("Review missing keywords: " + ", ".join(missing[:12]) + ".")

    if word_count < 350:
        recommendations.append(
            "As a fresher, use the available space for 2–3 strong projects, skills, education and relevant certifications."
        )
    if word_count > 850:
        recommendations.append(
            "Remove repetitive or low-value content to improve one-page readability."
        )

    recommendations.extend(
        [
            "Start bullets with action verbs and include technology + task + measurable result when possible.",
            "Keep ATS formatting simple: standard headings, consistent dates, readable fonts and no important text inside images.",
        ]
    )

    if not strengths:
        strengths = ["The resume contains enough text for automated analysis."]
    if not issues:
        issues = ["No major structural issue was detected by the automated checks."]

    return {
        "ats_score": ats,
        "keyword_match": keyword_pct,
        "skill_count": len(skills),
        "skills": skills,
        "word_count": word_count,
        "sections_found": sum(sections.values()),
        "sections": sections,
        "score_components": score_components,
        "bullet_points": bullets,
        "quantified_achievements": quantified,
        "action_verbs_detected": action,
        "email_detected": email,
        "phone_detected": phone,
        "matched_keywords": matched,
        "missing_keywords": missing[:30],
        "strengths": strengths,
        "issues": issues,
        "recommendations": recommendations,
    }
