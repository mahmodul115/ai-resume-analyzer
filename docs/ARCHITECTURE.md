# Architecture

The AI Resume Analyzer is a two-service full-stack web application.

## Frontend

- React with Vite
- Runs on port 5173
- Sends resume text or uploaded files to the backend
- Displays ATS score, job match score, detected skills, missing skills, and suggestions

## Backend

- FastAPI
- Runs on port 8000
- Accepts pasted resume text or PDF/DOCX/TXT uploads
- Extracts resume text
- Performs keyword and section analysis
- Returns JSON results to the frontend

## Data Flow

1. User pastes resume text or uploads a file.
2. User optionally pastes a job description.
3. Frontend sends request to FastAPI.
4. Backend extracts text and analyzes resume quality.
5. Frontend displays scoring and suggestions.

## Future Improvements

- Add user accounts
- Store resume history in PostgreSQL
- Add OpenAI-powered feedback
- Add PDF report export
- Deploy frontend to Vercel and backend to Render
