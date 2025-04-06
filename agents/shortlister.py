# agents/shortlister.py
def shortlist(scores: dict, threshold: float = 50.0) -> list:
    """Return a list of candidate filenames with score above the threshold."""
    return [cv for cv, score in scores.items() if score >= threshold]