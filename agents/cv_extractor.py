from pathlib import Path
from PyPDF2 import PdfReader

def load_all_cvs(cv_folder: Path) -> dict:
    cv_data = {}
    for cv_file in cv_folder.glob("*.pdf"):
        try:
            reader = PdfReader(cv_file)
            text = " ".join(page.extract_text() or "" for page in reader.pages)
            cv_data[cv_file.name] = text
        except Exception as e:
            print(f"❌ Error reading {cv_file.name}: {e}")
    return cv_data

def parse_uploaded_cvs(uploaded_files) -> dict:
    cvs = {}
    for file in uploaded_files:
        try:
            reader = PdfReader(file)
            text = " ".join(page.extract_text() or "" for page in reader.pages)
            cvs[file.name] = text
        except Exception as e:
            print(f"❌ Error reading uploaded file {file.name}: {e}")
    return cvs
