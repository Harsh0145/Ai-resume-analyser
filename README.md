# 🤖 AI Resume Analyser

A portfolio-ready resume analysis web application built with **Python, Streamlit, PDF text extraction, NLP-style text processing, data analysis, and an optional OpenAI LLM layer**.

## ✨ What it does

- Upload a **PDF resume**
- Extract readable resume text
- Detect common resume sections
- Extract technical skills from a configurable skill list
- Analyse word count, bullet points, action verbs, contact details, and quantified achievements
- Calculate a transparent **ATS-style heuristic score**
- Paste a job description and calculate keyword overlap
- Identify missing job-description keywords
- Generate actionable resume improvement recommendations
- Optionally generate deeper AI feedback through an LLM
- Includes automated pytest tests
- Does not use a database or intentionally save resumes to permanent storage

## 🏗️ Architecture

```text
PDF Resume Upload
        ↓
PDF Text Extraction
        ↓
Text Normalisation
        ↓
Feature Extraction
 ┌──────────┬───────────┬──────────────┐
 │ Sections │ Skills    │ Content      │
 │          │           │ Metrics      │
 └──────────┴───────────┴──────────────┘
        ↓
ATS Heuristic Scoring + Job Keyword Matching
        ↓
Streamlit Analytics Dashboard
        ↓
Optional LLM Review
```

## 🛠️ Tech stack

- Python
- Streamlit
- PyPDF2
- Regular expressions and NLP-style text preprocessing
- Python data analysis and feature engineering
- OpenAI Responses API (optional)
- pytest

## 📁 Project structure

```text
AI-Resume-Analyser/
├── .streamlit/
│   └── config.toml
├── src/
│   ├── __init__.py
│   ├── ai_analyser.py
│   ├── resume_analyser.py
│   └── resume_parser.py
├── tests/
│   └── test_analyser.py
├── .env.example
├── .gitignore
├── app.py
├── pytest.ini
├── README.md
├── requirements-dev.txt
└── requirements.txt
```

## 🚀 Run locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-analyser.git
cd ai-resume-analyser
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the app

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## 🧪 Run tests

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the test suite:

```bash
pytest -q
```

## 🤖 Optional AI feedback

The deterministic analytics engine works without an API key.

To enable the optional LLM review, configure both:

```text
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=your_available_model
```

The model name must be one available to your OpenAI API account. Never commit an API key to GitHub.

For local development, you can use environment variables. For Streamlit deployment, use the app's Secrets settings instead of committing a secrets file.

## 📊 How the ATS-style score works

The score is intentionally transparent and heuristic. It combines:

- Resume section coverage
- Content quality signals such as bullets, action verbs and quantified achievements
- Contact information detection
- Basic readability signals
- Job-description keyword alignment when a job description is provided

This is **not a real employer ATS score** and should not be interpreted as an employer's actual screening result.

Keyword matching is primarily lexical, so the analyser can miss semantic equivalents. For example, two phrases can have similar meanings without sharing the same exact words.

## 🔒 Privacy

The application processes the uploaded resume during the current Streamlit session. The application does not intentionally save resumes to a database or permanent file.

If optional AI feedback is enabled, the resume text and job description are sent to the configured OpenAI API provider for the requested review. Do not enable the AI layer for sensitive documents unless you are comfortable with that data flow.

## ⚠️ Current limitations

- PDF only; text-based PDFs work best
- Skill detection uses a predefined skill list
- Job-description keywords are extracted using rule-based text processing
- ATS scoring is a portfolio heuristic, not a validated hiring model
- No semantic embeddings or trained ML model are currently used
- Scanned/image-only PDFs may require OCR, which is not included in this version

## 🔮 Future improvements

- Semantic similarity using embeddings
- OCR for scanned resumes
- Resume section classification
- Larger skill taxonomy with proficiency levels
- Job-role classification
- Downloadable analysis reports
- Resume version history
- Docker deployment
- Evaluation dataset and model-quality metrics
- Retrieval-augmented job-market guidance

## 💼 CV project description

**AI Resume Analyser | Python, NLP, Streamlit, OpenAI API**

Built a resume analytics application that extracts structured features from PDF resumes, evaluates ATS-style criteria, performs job-description keyword matching, identifies missing keywords and generates actionable recommendations, with an optional LLM-powered review layer.
