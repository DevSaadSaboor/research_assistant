import ReactMarkdown from 'react-markdown'

export function MessageBubble({ message }) {
  const isUser = message.role === 'user'
  const hasSources = !isUser && message.sources?.length > 0

  // ── File upload — right-aligned user bubble with attachment card ──────────
  if (message.role === 'system' && message.type === 'upload') {
    const isReady = message.status === 'ready'
    return (
      <div className="message-row user">
        <div className="message-avatar user">👤</div>
        <div className="message-content-wrap">
          <div className="file-attachment-card">
            <div className="file-attachment-icon">📄</div>
            <div className="file-attachment-info">
              <div className="file-attachment-name">{message.fileName}</div>
              <div className={`file-attachment-status ${isReady ? 'ready' : 'processing'}`}>
                {isReady
                  ? '✅ Ready to query'
                  : <><span className="upload-spinner" />Processing…</>}
              </div>
            </div>
          </div>
          <div className="message-time">{message.time}</div>
        </div>
      </div>
    )
  }

 
  return (
    <>
      <div className={`message-row ${isUser ? 'user' : 'ai'}`}>
        <div className={`message-avatar ${isUser ? 'user' : 'ai'}`}>
          {isUser ? '👤' : '🤖'}
        </div>
        <div className="message-content-wrap">
          <div className="message-bubble">
            {isUser
              ? message.content
              : (
                <div className="markdown-body">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
              )}
            {message.streaming && <span className="cursor" />}
          </div>
          <div className="message-time">{message.time}</div>
        </div>
      </div>

      {/* Sources — full-width section below the AI message row */}
      {hasSources && (
        <div className="sources-section">
          <div className="sources-section-header">
            <span className="sources-icon">📚</span>
            <span>Sources</span>
            <span className="sources-count">{message.sources.length}</span>
          </div>
          <div className="sources-cards">
            {message.sources.map((src, i) => (
              <div key={i} className="source-card" title={src.preview}>
                <div className="source-card-top">
                  <span className="source-card-icon">📄</span>
                  <span className="source-card-page">Page {src.page}</span>
                </div>
                <div className="source-card-name">{src.file_name}</div>
                <div className="source-card-preview">{src.preview}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  )
}
