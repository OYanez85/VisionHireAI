# agents/match_scorer.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def score_cvs(job_description: str, cvs: dict) -> dict:
    scores = {}
    for filename, content in cvs.items():
        try:
            vectorizer = TfidfVectorizer().fit([job_description, content])
            vectors = vectorizer.transform([job_description, content])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            scores[filename] = round(similarity * 100, 2)
        except Exception as e:
            print(f"❌ Error scoring {filename}: {e}")
    return scores