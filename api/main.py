# api/main.py
from fastapi import FastAPI
from pathlib import Path
from agents.jd_analyzer import load_job_description
from agents.cv_extractor import load_all_cvs
from agents.match_scorer import score_cvs
from agents.shortlister import shortlist

app = FastAPI()

@app.get("/match")
def match_candidates():
    base_path = Path(__file__).resolve().parents[1]
    job_path = base_path / "db" / "CVs" / "job_description.csv"
    cv_path = base_path / "db" / "CVs"

    jd = load_job_description(job_path)
    cvs = load_all_cvs(cv_path)
    scores = score_cvs(jd, cvs)
    top_candidates = shortlist(scores)

    return {"scores": scores, "shortlisted": top_candidates}
