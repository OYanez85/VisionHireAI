# ui/dashboard.py
import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path so "agents" and other top-level modules can be found
sys.path.append(str(Path(__file__).resolve().parents[1]))

from agents.jd_analyzer import load_job_description
from agents.cv_extractor import load_all_cvs, parse_uploaded_cvs
from agents.match_scorer import score_cvs
from agents.shortlister import shortlist
from agents.scheduler import log_review_schedule
from utils.emailer import send_email
import sqlite3
import os

st.set_page_config(page_title="VisionHireAI", layout="wide")
st.title("📄 VisionHireAI Dashboard")

base_path = Path(__file__).resolve().parents[1]
job_path = base_path / "db" / "CVs" / "job_description.csv"

job_description = load_job_description(job_path)

with st.expander("📋 View Job Description"):
    st.write(job_description)

uploaded_files = st.file_uploader("📤 Upload candidate CVs (PDF):", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")
    cvs = parse_uploaded_cvs(uploaded_files)
    scores = score_cvs(job_description, cvs)
    top_candidates = shortlist(scores)

    # Save to SQLite DB
    conn = sqlite3.connect(base_path / "db" / "candidates.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            name TEXT PRIMARY KEY,
            score REAL
        )
    """)

    for name, score in scores.items():
        cur.execute("REPLACE INTO candidates (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()

    st.subheader("✅ Shortlisted Candidates")
    for candidate in top_candidates:
        st.markdown(f"- **{candidate}** — {scores[candidate]}% match")
        send_email(os.getenv("EMAIL_RECIPIENT", "hr@example.com"),
                   f"Review CV: {candidate}",
                   f"Candidate {candidate} matched with score {scores[candidate]}%")

    log_review_schedule(top_candidates)

    st.subheader("📊 Match Scores")
    st.dataframe({name: [score] for name, score in scores.items()})


