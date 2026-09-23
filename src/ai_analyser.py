import json
import os


def _get_setting(name):
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st

        value = st.secrets.get(name)
        if value:
            return value
    except Exception:
        pass

    return None


def is_ai_configured():
    return bool(_get_setting("OPENAI_API_KEY") and _get_setting("OPENAI_MODEL"))


def ai_review(resume, jd, report):
    api_key = _get_setting("OPENAI_API_KEY")
    model = _get_setting("OPENAI_MODEL")

    if not api_key:
        return {"error": "OPENAI_API_KEY is not configured."}
    if not model:
        return {
            "error": "OPENAI_MODEL is not configured. Set it to a model available to your OpenAI API account."
        }

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        prompt = f"""You are an expert resume reviewer helping a BCA/MCA fresher.

Analyse this resume against the job description. Never invent experience, skills, certifications, employers or metrics.

Return concise Markdown with: Overall assessment; Strengths; Problems to fix; Missing keywords; Improved professional summary; 5 improved bullet examples based only on facts already present; Fresher-specific next steps.

Resume:\n{resume[:18000]}\n\nJob description:\n{jd[:12000]}\n\nAutomated analytics:\n{json.dumps(report, indent=2)}"""

        response = client.responses.create(model=model, input=prompt)
        return {"feedback": response.output_text}

    except Exception as exc:
        return {"error": f"AI request failed: {exc}"}
