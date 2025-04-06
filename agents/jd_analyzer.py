# agents/jd_analyzer.py
from pathlib import Path
import pandas as pd

def load_job_description(path: Path) -> str:
    df = pd.read_csv(path, encoding="windows-1252")
    return df.iloc[0, 0]  # Assume job description is in the first row
