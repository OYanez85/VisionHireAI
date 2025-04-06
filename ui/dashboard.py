# Updated: ui/dashboard.py
import streamlit as st
import sys
from pathlib import Path
import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

sys.path.append(str(Path(__file__).resolve().parents[1]))

from agents.jd_analyzer import load_job_description
from agents.cv_extractor import load_all_cvs, parse_uploaded_cvs
from agents.match_scorer import score_cvs
from agents.shortlister import shortlist
from agents.scheduler import log_review_schedule
from utils.emailer import send_email

st.set_page_config(page_title="VisionHireAI", layout="wide")

st.sidebar.title("\ud83d\udcca VisionHireAI Menu")
section = st.sidebar.radio("Go to", ["\ud83c\udfe0 Home", "\ud83d\udcc4 Upload CVs", "\ud83d\udccb Job Description", "\u2705 Shortlisted", "\ud83d\udcca Match Scores", "\u2139\ufe0f About"])

base_path = Path(__file__).resolve().parents[1]
job_path = base_path / "db" / "CVs" / "job_description.csv"
job_description = load_job_description(job_path)

if "cv_texts" not in st.session_state:
    st.session_state.cv_texts = {}
    st.session_state.scores = {}
    st.session_state.top_candidates = []

if section == "\ud83c\udfe0 Home":
    st.title("\ud83d\udcc4 VisionHireAI Dashboard")
    st.markdown("Welcome to the **VisionHireAI** platform.")

elif section == "\ud83d\udcc4 Upload CVs":
    uploaded_files = st.file_uploader("\ud83d\udcc4 Upload candidate CVs (PDF):", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state.cv_texts = parse_uploaded_cvs(uploaded_files)
        st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")

elif section == "\ud83d\udccb Job Description":
    st.subheader("\ud83d\udcc3 Job Description")
    with st.expander("\ud83d\udcc3 View Job Description"):
        st.write(job_description)

    if st.button("\ud83d\udd0d Match CVs"):
        if not st.session_state.cv_texts:
            st.warning("Please upload CVs first.")
        else:
            with st.spinner("Scoring CVs..."):
                st.session_state.scores = score_cvs(job_description, st.session_state.cv_texts)
                st.session_state.top_candidates = shortlist(st.session_state.scores)

                conn = sqlite3.connect(base_path / "db" / "candidates.db")
                cur = conn.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS candidates (
                        name TEXT PRIMARY KEY,
                        score REAL
                    )
                """)

                for name, score in st.session_state.scores.items():
                    cur.execute("REPLACE INTO candidates (name, score) VALUES (?, ?)", (name, score))
                conn.commit()
                conn.close()

                for candidate in st.session_state.top_candidates:
                    send_email(
                        os.getenv("EMAIL_RECIPIENT", "hr@example.com"),
                        f"Review CV: {candidate}",
                        f"Candidate {candidate} matched with score {st.session_state.scores[candidate]}%"
                    )

                log_review_schedule(st.session_state.top_candidates)
                st.success("Scoring and shortlisting complete.")

elif section == "\u2705 Shortlisted":
    st.subheader("\u2705 Shortlisted Candidates")
    if st.session_state.top_candidates:
        shortlisted_data = [(name, st.session_state.scores[name]) for name in st.session_state.top_candidates]
        df = pd.DataFrame(shortlisted_data, columns=["Filename", "Score"])
        st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("\ud83d\udd27 Download Shortlisted CSV", csv, "shortlisted_candidates.csv", "text/csv")
    else:
        st.info("No candidates shortlisted yet.")

elif section == "\ud83d\udcca Match Scores":
    st.subheader("\ud83d\udcca Match Scores")
    if st.session_state.scores:
        df = pd.DataFrame({"Filename": list(st.session_state.scores.keys()), "Score": list(st.session_state.scores.values())})
        df = df.sort_values(by="Score", ascending=False)
        st.dataframe(df)

        # Plot heatmap
        fig, ax = plt.subplots(figsize=(10, 1))
        sns.heatmap([df["Score"]], cmap="YlGnBu", annot=True, fmt=".1f", xticklabels=df["Filename"], yticklabels=False, ax=ax, cbar=False)
        plt.xticks(rotation=90)
        st.pyplot(fig)
    else:
        st.info("No scores available. Go to 'Job Description' to run matching.")

elif section == "\u2139\ufe0f About":
    st.markdown("""
    **VisionHireAI** is a smart resume filtering tool that matches candidates to job descriptions using state-of-the-art NLP.

    **Features**:
    - \ud83d\udcc5 Upload PDF CVs
    - \ud83e\udde0 Match using SentenceTransformers
    - \u2705 See shortlisted candidates
    - \ud83d\udcca Visualize scores

    **Developer**: Oscar Yanez
    """)


