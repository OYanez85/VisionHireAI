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

st.sidebar.title("VisionHireAI Menu")
section = st.sidebar.radio("Go to", ["Home", "Upload CVs", "Job Description", "Shortlisted", "Match Scores", "About"])

base_path = Path(__file__).resolve().parents[1]
job_path = base_path / "db" / "CVs" / "job_description.csv"
job_description = load_job_description(job_path)

if "cv_texts" not in st.session_state:
    st.session_state.cv_texts = {}
    st.session_state.scores = {}
    st.session_state.top_candidates = []

if section == "Home":
    st.title("VisionHireAI Dashboard")
    st.markdown("Welcome to the **VisionHireAI** platform.")

elif section == "Upload CVs":
    uploaded_files = st.file_uploader("Upload candidate CVs (PDF):", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state.cv_texts = parse_uploaded_cvs(uploaded_files)
        st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")

elif section == "Job Description":
    st.subheader("Job Description")
    with st.expander("View Job Description"):
        st.write(job_description)

    if st.button("Match CVs"):
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

elif section == "Shortlisted":
    st.subheader("Shortlisted Candidates")
    if st.session_state.top_candidates:
        shortlisted_data = [(name, st.session_state.scores[name]) for name in st.session_state.top_candidates]
        df = pd.DataFrame(shortlisted_data, columns=["Filename", "Score"])
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Shortlisted CSV", csv, "shortlisted_candidates.csv", "text/csv")
    else:
        st.info("No candidates shortlisted yet.")

elif section == "Match Scores":
    st.subheader("Match Scores")
    if st.session_state.scores:
        df = pd.DataFrame({
            "Filename": list(st.session_state.scores.keys()),
            "Score": list(st.session_state.scores.values())
        }).sort_values(by="Score", ascending=False)

        st.dataframe(df)

        # Plot updated heatmap
        data = pd.DataFrame(df["Score"]).T  # single row heatmap
        data.columns = df["Filename"]

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(data, ax=ax, cmap="YlGnBu", annot=True, fmt=".1f", cbar=True)
        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No scores available. Go to 'Job Description' to run matching.")

elif section == "About":
    st.markdown("""
    **VisionHireAI** is a smart resume filtering tool that matches candidates to job descriptions using state-of-the-art NLP.

    **Features**:
    - Upload PDF CVs
    - Match using SentenceTransformers
    - See shortlisted candidates
    - Visualize scores

    **Developer**: Oscar Yanez
    """)

