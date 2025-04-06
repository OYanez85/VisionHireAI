# VisionHireAI

VisionHireAI is a modular, AI-powered CV screening assistant designed to streamline hiring processes using semantic similarity scoring, fast frontend-backend integration, and explainable automation.

## 🚀 Features

- 📄 Upload and parse CVs in PDF format
- 🧠 Match CVs to job descriptions using TF-IDF & cosine similarity
- 📊 View scores, shortlist candidates, and simulate HR actions
- 💾 Save results in a local SQLite database
- 📬 Simulate sending email alerts to reviewers
- 🌐 Frontend (Streamlit) + Backend (FastAPI)
- 🐳 Docker + Docker Compose setup for easy deployment

---

## 📂 Project Structure

```bash
VisionHireAI/
├── agents/             # Core logic modules (extractors, scorers, shortlister, etc.)
├── api/                # FastAPI backend
├── db/                 # Local data: job descriptions, CVs, SQLite DB
├── ui/                 # Streamlit dashboard interface
├── utils/              # Helper utilities (e.g., emailer)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/OYanez85/VisionHireAI.git
cd VisionHireAI
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Run the App
- **Streamlit UI**:
  ```bash
  streamlit run ui/dashboard.py
  ```
- **FastAPI Backend**:
  ```bash
  uvicorn api.main:app --reload
  ```

---

## 🐳 Docker Setup (Optional)

```bash
docker-compose up --build
```

This runs both frontend and backend services using Docker.

---

## 📚 Tech Stack

- **Python 3.10+**
- **Streamlit** – UI interface
- **FastAPI** – REST backend
- **PyPDF2** – CV text extraction
- **scikit-learn** – TF-IDF & cosine similarity scoring
- **SQLite** – Simple persistence layer
- **Docker / Docker Compose** – Containerization

---

## 🎯 Next Features (Roadmap)

- [ ] Upload & select multiple job descriptions
- [ ] Integrate OpenAI/Gemini LLMs for better scoring
- [ ] Add charts for score distribution
- [ ] Export results to CSV/Excel
- [ ] Deploy to Fly.io / Render

---

## 🤝 Contributors
- **Oscar Yanez** – Developer / Architect

---

## 📄 License
[MIT](LICENSE) License

---

## 📸 Demo
_Add your recorded video or link here_

# VisionHireAI

**VisionHireAI** is a generative AI solution submitted for the "Hack The Future: A Gen AI Sprint Powered By Data" hackathon.

## 🚀 Project Links

- 🔗 **GitHub Repository**  
  👉 [https://github.com/OYanez85/VisionHireAI#](https://github.com/OYanez85/VisionHireAI#)

- 📄 **Google Drive File (PDF or Report)**  
  👉 [View Report](https://drive.google.com/file/d/1s3tw3rbmDdd7-TYUS6quVyfJlhWZHqRf/view?usp=drive_link)

- 🌐 **Streamlit App (Live Demo)**  
  👉 [Launch App](https://visionhireai.streamlit.app/)

- 📽️ **Google Slides Presentation**  
  👉 [View Slides](https://docs.google.com/presentation/d/1PKLlha74MLJwgR326pWl-JbBU1zKXTGM/edit?usp=sharing&ouid=100907462623455240504&rtpof=true&sd=true)

- 🎬 **Demo / Pitch Video**  
  👉 [Watch on Google Drive](https://drive.google.com/file/d/1s3tw3rbmDdd7-TYUS6quVyfJlhWZHqRf/view?usp=drive_link)


---

For questions or suggestions, feel free to reach out or create an issue!

---
