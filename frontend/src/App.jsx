import { useState } from 'react';
import { Upload, FileText, Sparkles } from 'lucide-react';
import AnalysisResults from './components/AnalysisResults.jsx';
import { analyzeText, analyzeFile } from './services/api.js';

export default function App() {
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleAnalyze() {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const data = file
        ? await analyzeFile(file, jobDescription)
        : await analyzeText(resumeText, jobDescription);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  }

  const canAnalyze = file || resumeText.trim().length > 20;

  return (
    <main className="app">
      <section className="hero">
        <div className="badge"><Sparkles size={16} /> AI Portfolio Project</div>
        <h1>AI Resume Analyzer</h1>
        <p>Analyze resumes against software engineering job descriptions and get ATS-style feedback, skills found, missing keywords, and improvement suggestions.</p>
      </section>

      <section className="workspace">
        <div className="form-card">
          <h2><FileText size={22} /> Resume Input</h2>
          <label className="file-box">
            <Upload size={28} />
            <span>{file ? file.name : 'Upload PDF, DOCX, or TXT resume'}</span>
            <input type="file" accept=".pdf,.docx,.txt" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          </label>
          <div className="divider"><span>or paste resume text</span></div>
          <textarea
            placeholder="Paste your resume text here..."
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            disabled={Boolean(file)}
          />
          {file && <button className="ghost" onClick={() => setFile(null)}>Remove file and paste text instead</button>}
        </div>

        <div className="form-card">
          <h2>Job Description</h2>
          <textarea
            placeholder="Paste the job description here. This is optional but improves matching results."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
          <button className="primary" onClick={handleAnalyze} disabled={!canAnalyze || loading}>
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>
          {error && <p className="error">{error}</p>}
        </div>
      </section>

      <AnalysisResults result={result} />
    </main>
  );
}
