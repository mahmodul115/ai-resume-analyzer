import ScoreCard from './ScoreCard.jsx';

function PillList({ title, items, emptyText }) {
  return (
    <section className="panel">
      <h3>{title}</h3>
      {items && items.length > 0 ? (
        <div className="pill-list">
          {items.map((item) => <span className="pill" key={item}>{item}</span>)}
        </div>
      ) : <p className="muted">{emptyText}</p>}
    </section>
  );
}

export default function AnalysisResults({ result }) {
  if (!result) return null;
  const sectionLabels = {
    contact_info: 'Contact Info',
    skills_section: 'Skills Section',
    experience_section: 'Experience Section',
    education_section: 'Education Section',
    projects_section: 'Projects Section',
  };

  return (
    <div className="results">
      <div className="score-grid">
        <ScoreCard label="ATS Score" value={result.ats_score} suffix="%" helper="Overall resume strength estimate" />
        <ScoreCard label="Job Match" value={result.match_percent} suffix="%" helper="Only shown when job description is provided" />
      </div>

      <section className="panel">
        <h3>Resume Sections</h3>
        <div className="section-checks">
          {Object.entries(result.sections || {}).map(([key, value]) => (
            <div className="check-row" key={key}>
              <span>{sectionLabels[key] || key}</span>
              <strong className={value ? 'yes' : 'no'}>{value ? 'Found' : 'Missing'}</strong>
            </div>
          ))}
        </div>
      </section>

      <PillList title="Skills Found" items={result.skills_found} emptyText="No major technical skills detected yet." />
      <PillList title="Missing Job Skills" items={result.missing_skills} emptyText="No missing skills detected, or no job description was provided." />

      <section className="panel">
        <h3>Improvement Suggestions</h3>
        <ul className="suggestions">
          {(result.suggestions || []).map((item, index) => <li key={index}>{item}</li>)}
        </ul>
      </section>
    </div>
  );
}
