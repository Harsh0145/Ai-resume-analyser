import os

import streamlit as st

from src.ai_analyser import ai_review, is_ai_configured
from src.resume_analyser import analyse_resume
from src.resume_parser import extract_text

st.set_page_config(
    page_title="AI Resume Analyser",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI Resume Analyser")
st.caption("ATS-style resume analytics + job-description matching + optional LLM feedback")

with st.sidebar:
    st.header("How it works")
    st.write("1. Upload a PDF resume")
    st.write("2. Paste a job description")
    st.write("3. Run the analysis")
    st.write("4. Review ATS metrics and recommendations")
    st.divider()
    st.info(
        "Your resume is processed during the current app session and is not intentionally saved to a database or permanent file by this application."
    )

resume_file = st.file_uploader(
    "Upload resume",
    type=["pdf"],
    help="PDF files only. Text-based PDFs work best.",
)
job_description = st.text_area(
    "Job description (optional)",
    height=220,
    placeholder="Paste the job description here to calculate keyword and skill alignment.",
)

if resume_file:
    try:
        text = extract_text(resume_file)

        with st.expander("Preview extracted text"):
            st.text(text[:10000])

        if st.button("🔍 Analyse Resume", type="primary", use_container_width=True):
            report = analyse_resume(text, job_description)
            st.session_state.report = report
            st.session_state.resume_text = text
            st.session_state.jd = job_description

    except Exception as exc:
        st.error(f"Could not read the PDF: {exc}")

if "report" in st.session_state:
    r = st.session_state.report
    keyword_display = (
        "N/A" if r["keyword_match"] is None else f'{r["keyword_match"]}%'
    )

    st.divider()
    st.subheader("Resume Analytics")

    a, b, c, d, e = st.columns(5)
    a.metric("ATS Score", f'{r["ats_score"]}/100')
    b.metric("Keyword Match", keyword_display)
    c.metric("Skills Found", r["skill_count"])
    d.metric("Words", r["word_count"])
    e.metric("Sections", r["sections_found"])
    st.progress(r["ats_score"] / 100)

    left, right = st.columns(2)
    with left:
        st.markdown("### ✅ Strengths")
        for item in r["strengths"]:
            st.write("• " + item)

        st.markdown("### ⚠️ Issues")
        for item in r["issues"]:
            st.write("• " + item)

    with right:
        st.markdown("### 🧰 Detected Skills")
        st.write(
            ", ".join(r["skills"])
            if r["skills"]
            else "No known technical skills detected."
        )

        st.markdown("### 🔑 Keyword Analysis")
        if r["keyword_match"] is None:
            st.write("Paste a job description to calculate keyword overlap.")
        else:
            st.write(
                "**Matched:** "
                + (", ".join(r["matched_keywords"]) if r["matched_keywords"] else "None")
            )
            st.write(
                "**Missing:** "
                + (", ".join(r["missing_keywords"]) if r["missing_keywords"] else "None")
            )

    st.markdown("### 📊 Section & Content Analysis")
    st.json(
        {
            "sections": r["sections"],
            "score_components": r["score_components"],
            "bullet_points": r["bullet_points"],
            "quantified_achievements": r["quantified_achievements"],
            "email_detected": r["email_detected"],
            "phone_detected": r["phone_detected"],
            "action_verbs_detected": r["action_verbs_detected"],
        }
    )

    st.markdown("### 🎯 Recommended Actions")
    for i, item in enumerate(r["recommendations"], 1):
        st.write(f"{i}. {item}")

    st.divider()
    st.subheader("🤖 AI Career Review")

    if is_ai_configured():
        if st.button("Generate AI Feedback"):
            with st.spinner("Generating AI feedback..."):
                result = ai_review(
                    st.session_state.resume_text,
                    st.session_state.jd,
                    r,
                )
            if result.get("error"):
                st.error(result["error"])
            else:
                st.markdown(result["feedback"])
    else:
        st.info(
            "AI feedback is optional. Set OPENAI_API_KEY and OPENAI_MODEL to enable the LLM layer. "
            "The resume analytics engine works without them."
        )
