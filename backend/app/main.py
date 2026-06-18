from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import re

try:
    import PyPDF2
except Exception:
    PyPDF2 = None

try:
    import docx
except Exception:
    docx = None

app = FastAPI(
    title="AI Resume Analyzer API",
    description="A simple FastAPI backend for analyzing resumes against job descriptions.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TECH_SKILLS = [
    "python", "java", "javascript", "typescript", "react", "node", "fastapi",
    "django", "flask", "sql", "postgresql", "mysql", "mongodb", "docker",
    "kubernetes", "aws", "azure", "gcp", "git", "github", "linux", "api",
    "rest", "graphql", "machine learning", "ai", "data analysis", "pandas",
    "numpy", "tensorflow", "pytorch", "html", "css", "tailwind", "vite",
    "testing", "pytest", "ci/cd", "agile", "scrum"
]

ACTION_WORDS = [
    "built", "created", "developed", "implemented", "designed", "deployed",
    "improved", "optimized", "automated", "integrated", "managed", "led"
]

class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str = ""


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_skills(text: str) -> List[str]:
    lower = normalize(text)
    found = []
    for skill in TECH_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, lower):
            found.append(skill.title())
    return sorted(set(found))


def extract_keywords(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z+#.\-]{2,}", normalize(text))
    stopwords = {
        "the", "and", "for", "with", "you", "are", "this", "that", "from", "will",
        "your", "our", "have", "has", "job", "role", "work", "team", "using", "into"
    }
    keywords = [w for w in words if w not in stopwords]
    counts: Dict[str, int] = {}
    for word in keywords:
        counts[word] = counts.get(word, 0) + 1
    return [w for w, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:25]]


def section_score(text: str) -> Dict[str, bool]:
    lower = normalize(text)
    return {
        "contact_info": bool(re.search(r"[\w\.-]+@[\w\.-]+\.\w+|\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)),
        "skills_section": "skills" in lower or "technical skills" in lower,
        "experience_section": "experience" in lower or "employment" in lower or "work history" in lower,
        "education_section": "education" in lower or "degree" in lower or "university" in lower,
        "projects_section": "projects" in lower or "portfolio" in lower or "github" in lower,
    }


def analyze_resume(resume_text: str, job_description: str = "") -> Dict[str, Any]:
    resume = normalize(resume_text)
    jd = normalize(job_description)
    skills_found = extract_skills(resume_text)
    job_skills = extract_skills(job_description) if job_description else []
    missing_skills = sorted(set(job_skills) - set(skills_found))
    sections = section_score(resume_text)

    score = 35
    score += min(len(skills_found) * 3, 25)
    score += sum(8 for ok in sections.values() if ok)
    score += 10 if any(word in resume for word in ACTION_WORDS) else 0
    score += 10 if re.search(r"\d+%|\$\d+|\d+\+", resume_text) else 0

    match_percent = None
    if job_description:
        jd_keywords = set(extract_keywords(job_description))
        resume_keywords = set(extract_keywords(resume_text))
        if jd_keywords:
            overlap = jd_keywords.intersection(resume_keywords)
            match_percent = round((len(overlap) / len(jd_keywords)) * 100)
            score = round((score * 0.65) + (match_percent * 0.35))

    score = max(0, min(score, 100))

    suggestions = []
    if not sections["contact_info"]:
        suggestions.append("Add clear contact information such as email, phone, LinkedIn, and GitHub.")
    if not sections["skills_section"]:
        suggestions.append("Add a dedicated Technical Skills section near the top of your resume.")
    if not sections["projects_section"]:
        suggestions.append("Add 2–4 software projects with GitHub links, tech stack, and impact bullets.")
    if len(skills_found) < 6:
        suggestions.append("Include more relevant technical keywords such as Python, React, FastAPI, SQL, Docker, and Git.")
    if not re.search(r"\d+%|\$\d+|\d+\+", resume_text):
        suggestions.append("Add measurable impact, such as percentages, time saved, users supported, or performance gains.")
    if missing_skills:
        suggestions.append("Add relevant missing job-description skills if you genuinely have experience with them: " + ", ".join(missing_skills[:8]) + ".")
    if not suggestions:
        suggestions.append("Strong resume. Continue tailoring keywords and achievements for each job application.")

    return {
        "ats_score": score,
        "match_percent": match_percent,
        "skills_found": skills_found,
        "job_skills": job_skills,
        "missing_skills": missing_skills,
        "sections": sections,
        "suggestions": suggestions,
        "top_resume_keywords": extract_keywords(resume_text),
        "top_job_keywords": extract_keywords(job_description) if job_description else [],
    }


def read_upload_file(file: UploadFile) -> str:
    filename = file.filename.lower()
    content = file.file.read()

    if filename.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        if PyPDF2 is None:
            raise HTTPException(status_code=500, detail="PDF support is not installed.")
        import io
        reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text

    if filename.endswith(".docx"):
        if docx is None:
            raise HTTPException(status_code=500, detail="DOCX support is not installed.")
        import io
        document = docx.Document(io.BytesIO(content))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF, DOCX, or TXT.")


@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required.")
    return analyze_resume(request.resume_text, request.job_description)


@app.post("/analyze-file")
def analyze_file(file: UploadFile = File(...), job_description: str = Form("")):
    text = read_upload_file(file)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file.")
    result = analyze_resume(text, job_description)
    result["filename"] = file.filename
    result["characters_extracted"] = len(text)
    return result
