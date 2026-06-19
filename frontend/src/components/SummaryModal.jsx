import { useState, useEffect } from 'react'
import { summarizeDocument } from '../api/client'

export function SummaryModal({ fileName, onClose }) {
  const [summary, setSummary] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    summarizeDocument(fileName)
      .then(data => setSummary(data.summary))
      .catch(() => setError('Failed to generate summary. Please try again.'))
      .finally(() => setLoading(false))
  }, [fileName])

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal-header">
          <div>
            <div className="modal-title">📋 Document Summary</div>
            <div className="modal-filename">{fileName}</div>
          </div>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {loading ? (
            <>
              {[90, 75, 85, 60, 80].map((w, i) => (
                <div key={i} className="skeleton skeleton-line" style={{ width: `${w}%` }} />
              ))}
            </>
          ) : error ? (
            <p style={{ color: 'var(--danger)' }}>{error}</p>
          ) : (
            <p>{summary}</p>
          )}
        </div>
      </div>
    </div>
  )
}
