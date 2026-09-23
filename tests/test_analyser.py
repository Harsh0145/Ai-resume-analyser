from src.resume_analyser import analyse_resume, detect_sections, skills_in


def sample_resume():
    return """Harish Singh
harish@example.com
+919999999999
Summary
Python developer
Skills
Python SQL Pandas
Projects
- Built a data analysis project improving speed by 20%
- Developed a Flask application for 100 users
Education
MCA
"""


def test_analysis_basic():
    report = analyse_resume(sample_resume(), "Python SQL data analysis")
    assert 0 <= report["ats_score"] <= 100
    assert report["skill_count"] >= 2
    assert report["email_detected"]
    assert report["phone_detected"]


def test_section_detection():
    sections = detect_sections(sample_resume())
    assert sections["summary"]
    assert sections["skills"]
    assert sections["projects"]
    assert sections["education"]


def test_skill_extraction():
    skills = skills_in("Python, SQL, Pandas and Flask")
    assert "python" in skills
    assert "sql" in skills
    assert "pandas" in skills
    assert "flask" in skills


def test_job_description_matching_and_missing_keywords():
    report = analyse_resume(sample_resume(), "Python SQL Pandas Tableau")
    assert report["keyword_match"] is not None
    assert "python" in report["matched_keywords"]
    assert "tableau" in report["missing_keywords"]


def test_no_job_description():
    report = analyse_resume(sample_resume())
    assert report["keyword_match"] is None
    assert report["matched_keywords"] == []
    assert report["missing_keywords"] == []


def test_quantified_achievements_and_action_verbs():
    report = analyse_resume(sample_resume())
    assert report["quantified_achievements"] >= 1
    assert report["action_verbs_detected"] >= 2


def test_empty_text_is_safe():
    report = analyse_resume("")
    assert 0 <= report["ats_score"] <= 100
    assert report["word_count"] == 0
    assert report["skill_count"] == 0
