# 🎯 ATS Resume Scorer

An AI-powered resume analysis platform that evaluates how well a resume matches a job description and provides actionable feedback to improve ATS (Applicant Tracking System) performance.

Built with **FastAPI + Streamlit**, this application combines NLP techniques, semantic similarity models, and LLM-powered suggestions to analyze resumes, identify improvement areas, and help candidates optimize their resumes for better job matching.

---

# 🚀 Live Deployment

- **Frontend:** Streamlit Cloud
- **Backend API:** Railway (FastAPI)

## Application Architecture

```
User
 |
 v
Streamlit Frontend
 |
 v
FastAPI Backend (Railway)
 |
 +--> Resume Processing
 +--> NLP Analysis
 +--> Sentence Transformers
 +--> Groq LLM Suggestions
 +--> Supabase Authentication & Database
```

---

# ✨ Features

## 📄 Resume Analysis

- Upload resumes in PDF, DOC, and DOCX formats
- Extract resume content automatically
- Analyze resume structure and formatting
- Compare resume content with job descriptions
- Generate ATS compatibility scores

---

## 🤖 AI-Powered Feedback

The system provides:

- Overall ATS score
- Category-wise scoring:
  - Formatting
  - Keywords & Skills
  - Content Quality
  - Skill Validation
  - ATS Compatibility

- Detailed resume feedback
- Critical issue detection
- Actionable improvement recommendations
- AI-generated suggestions for optimization

---

## 🎯 Job Description Matching

- Semantic similarity comparison between resume and job description
- Matched keyword detection
- Missing keyword identification
- Skills gap analysis
- Resume-to-job alignment insights

---

## 🔐 User Authentication & History

- Email/password authentication
- Google OAuth login
- Secure user sessions
- Save previous resume analyses
- View analysis history
- Delete saved reports

---

## 📑 Report Generation

- Generate ATS analysis reports
- Export results as PDF
- Download detailed resume feedback

---

# 🛠 Tech Stack

## Frontend

- Streamlit

## Backend

- FastAPI
- Python

## NLP & Machine Learning

- spaCy (`en_core_web_md`)
- Sentence Transformers (`all-MiniLM-L6-v2`)

## Large Language Model

- Groq API
- Llama models

## Authentication & Database

- Supabase
  - Authentication
  - PostgreSQL Database

## PDF Generation

- WeasyPrint
- Jinja2

---

# 📂 Project Structure

```
ATS_SCORER/

├── backend/
│   ├── API routes
│   ├── NLP services
│   ├── Resume processing
│   └── Scoring logic
│
├── frontend/
│   ├── Streamlit application
│   ├── Views
│   ├── Components
│   └── API client
│
├── jupyter notebooks/
│   └── Research and experimentation
│
├── ml model/
│   └── ML artifacts
│
├── requirements.txt
└── .env.example
```

---

# ⚙️ Local Setup

## 1. Clone Repository

```bash
git clone <repo-url>

cd ATS_SCORER
```

Create a virtual environment:

```bash
python3 -m venv venvats

source venvats/bin/activate
```

For Windows:

```bash
venvats\Scripts\activate
```

---

## 2. Install Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Download spaCy language model:

```bash
python -m spacy download en_core_web_md
```

---

# 🔑 Environment Configuration

Create your environment file:

```
.env
```

using:

```
.env.example
```

Required services:

## Supabase

Required variables:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`

Supabase is used for:

- User authentication
- Database storage
- Saved analysis history

---

## Groq API

Required variable:

- `GROQ_API_KEY`

Used for generating AI-powered resume improvement suggestions.

---

## Google OAuth (Optional)

Google login can be enabled through the Supabase authentication dashboard.

---

# ▶️ Running the Application Locally

## Start Backend

From the project root:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at:

```
http://localhost:8000
```

FastAPI documentation:

```
http://localhost:8000/docs
```

---

## Start Frontend

Open another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Frontend will run at:

```
http://localhost:8501
```

---

# 🌐 Production Deployment

## Frontend

Deployed using:

**Streamlit Cloud**

The frontend communicates with the backend through REST API calls.

---

## Backend

Deployed using:

**Railway**

The FastAPI backend handles:

- Resume processing
- NLP analysis
- ATS scoring
- AI suggestions
- Database communication

---

# 🔒 Security Notes

- Never commit `.env` files
- Never commit `secrets.toml`
- Keep API keys inside deployment environment variables
- Never expose Supabase service role keys publicly
- Use Supabase anonymous keys only on frontend applications

---

# 📌 Additional Notes

- The Sentence Transformer model downloads automatically on the first run and is cached afterwards.
- ATS scoring works without Groq, but AI-generated suggestions require a Groq API key.
- Jupyter notebooks contain research experiments and are not required for running the application.
- ML artifacts are included for experimentation and future improvements.

---

# 👨‍💻 Project Overview

ATS Resume Scorer is an AI/NLP-based career assistance platform designed to help job seekers improve their resumes by combining traditional ATS scoring methods with modern semantic search and large language models.

The goal is to provide candidates with clear insights into resume quality, job-description alignment, missing skills, and practical improvements that increase their chances of passing automated resume screening systems.