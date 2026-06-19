import { useRef, useEffect } from 'react'

export function InputBar({ onSend, streaming, attachment, onClearAttachment }) {
  const ref = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 180) + 'px'
  })


  useEffect(() => {
    if (attachment) ref.current?.focus()
  }, [attachment])

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  function submit() {
    const value = ref.current?.value.trim()
    if (!value || streaming) return
    onSend(value)
    ref.current.value = ''
    ref.current.style.height = 'auto'
    onClearAttachment?.()
  }

  return (
    <div className="input-bar-wrap">
      <div className="input-bar">
        <div className="input-inner">
          {/* File attachment chip — shown when a file was just uploaded */}
          {attachment && (
            <div className="input-attachment-chip">
              <span className="input-attachment-icon">📄</span>
              <span className="input-attachment-name">{attachment}</span>
              <button
                className="input-attachment-remove"
                onClick={onClearAttachment}
                title="Remove attachment"
              >
                ✕
              </button>
            </div>
          )}

          <div className="input-row">
            <textarea
              ref={ref}
              className="input-textarea"
              placeholder={attachment
                ? `Ask something about ${attachment}…`
                : 'Ask a question about your documents…'
              }
              rows={2}
              onKeyDown={handleKeyDown}
              disabled={streaming}
            />
            <button
              className="send-btn"
              onClick={submit}
              disabled={streaming}
              title="Send (Enter)"
            >
              {streaming ? <span className="spinner" /> : '↑'}
            </button>
          </div>
        </div>
      </div>
      <div className="input-hint">
        Press <strong>Enter</strong> to send · <strong>Shift+Enter</strong> for newline
      </div>
    </div>
  )
}
