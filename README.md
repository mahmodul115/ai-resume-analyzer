# AI Resume Analyzer

A full-stack portfolio project built with **FastAPI** and **React**. It analyzes resumes against job descriptions and provides ATS-style scoring, skills found, missing keywords, section checks, and improvement suggestions.

## Features

- Paste resume text or upload PDF, DOCX, or TXT files
- Paste an optional job description
- ATS-style score
- Job match percentage
- Skills extraction
- Missing skills detection
- Resume section checks
- Improvement suggestions
- FastAPI backend
- React + Vite frontend
- Docker Compose setup
- GitHub Actions CI

## Tech Stack

**Frontend**

- React
- Vite
- CSS
- Lucide React icons

**Backend**

- Python
- FastAPI
- PyPDF2
- python-docx
- Uvicorn
- Pytest

## Project Structure

```text
ai-resume-analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── tests/
│   │   └── test_api.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnalysisResults.jsx
│   │   │   └── ScoreCard.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── style.css
│   ├── Dockerfile
│   ├── index.html
│   └── package.json
├── docs/
│   └── ARCHITECTURE.md
├── .github/workflows/ci.yml
├── docker-compose.yml
├── LICENSE
├── .gitignore
└── README.md
```

## Run with Docker

Make sure Docker Desktop is installed and running.

```bash
docker compose up --build
```

Open:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Run manually in VS Code

Open the project folder in VS Code.

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

For Mac/Linux:

```bash
source .venv/bin/activate
```

Backend runs at:

```text
http://localhost:8000
```

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## Test the backend

```bash
cd backend
pytest
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| POST | `/analyze` | Analyze pasted resume text |
| POST | `/analyze-file` | Analyze uploaded PDF/DOCX/TXT resume |

## Example Use

1. Start backend and frontend.
2. Open http://localhost:5173.
3. Upload a resume or paste resume text.
4. Paste a job description.
5. Click **Analyze Resume**.
6. Review ATS score, skills found, missing skills, and suggestions.

## Portfolio Notes

This project is designed for a software engineering internship or new graduate portfolio. It demonstrates frontend development, backend API design, file upload handling, text processing, Docker, testing, and documentation.

## License

MIT
