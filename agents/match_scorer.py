# Updated: agents/match_scorer.py
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def score_cvs(job_description: str, cvs: dict) -> dict:
    scores = {}
    try:
        job_embedding = model.encode(job_description, convert_to_tensor=True)
        for filename, content in cvs.items():
            resume_embedding = model.encode(content, convert_to_tensor=True)
            similarity = util.cos_sim(job_embedding, resume_embedding).item()
            scores[filename] = round(similarity * 100, 2)
    except Exception as e:
        print(f"\u274c Error scoring CVs: {e}")
    return scores