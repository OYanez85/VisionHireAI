# agents/scheduler.py
from datetime import datetime

def log_review_schedule(candidate_list: list):
    """Logs the review schedule of shortlisted candidates."""
    now = datetime.now().isoformat()
    for candidate in candidate_list:
        print(f"[{now}] Review scheduled for: {candidate}")