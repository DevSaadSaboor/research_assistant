import { useRef } from 'react'

export function Sidebar({ documents, loading, uploading, onUpload, onDelete, onSummarize, onNewChat }) {
  const fileInput = useRef(null)

  function handleFileChange(e) {
    const file = e.target.files?.[0]
    if (file) {
      onUpload(file)
      e.target.value = ''
    }
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <div className="sidebar-brand-icon">🔬</div>
          <span className="sidebar-brand-name">Research Assistant</span>
        </div>

        <button className="new-chat-btn" onClick={onNewChat}>
          ✏️ New Chat
        </button>

        <input
          ref={fileInput}
          type="file"
          accept=".pdf"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
        <button
          className="upload-btn"
          onClick={() => fileInput.current?.click()}
          disabled={uploading}
        >
          {uploading
            ? <><span className="spinner" /> Processing…</>
            : <><span>＋</span> Upload PDF</>
          }
        </button>
      </div>

      <div className="sidebar-docs-title">Documents</div>

      <div className="sidebar-docs">
        {loading && (
          <div style={{ padding: '12px 10px' }}>
            {[1, 2, 3].map(i => (
              <div key={i} className="skeleton skeleton-line" style={{ width: '80%', marginBottom: 12 }} />
            ))}
          </div>
        )}

        {!loading && documents.length === 0 && (
          <div className="sidebar-empty">
            📂
            <br />
            No documents yet.
            <br />
            Upload a PDF to get started.
          </div>
        )}

        {documents.map(doc => (
          <div key={doc.file_name} className="doc-item">
            <span className="doc-icon">📄</span>
            <span className="doc-name" title={doc.file_name}>
              {doc.file_name}
            </span>
            <div className="doc-actions">
              <button
                className="doc-action-btn"
                title="Summarize"
                onClick={() => onSummarize(doc.file_name)}
              >
                📋
              </button>
              <button
                className="doc-action-btn danger"
                title="Delete"
                onClick={() => onDelete(doc.file_name)}
              >
                🗑
              </button>
            </div>
          </div>
        ))}
      </div>
    </aside>
  )
}
