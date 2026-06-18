export default function ScoreCard({ label, value, suffix = '', helper }) {
  const numeric = typeof value === 'number' ? value : 0;
  return (
    <div className="score-card">
      <div className="score-header">
        <span>{label}</span>
        <strong>{value ?? 'N/A'}{value !== null && value !== undefined ? suffix : ''}</strong>
      </div>
      <div className="progress"><div style={{ width: `${Math.min(numeric, 100)}%` }} /></div>
      {helper && <p>{helper}</p>}
    </div>
  );
}
