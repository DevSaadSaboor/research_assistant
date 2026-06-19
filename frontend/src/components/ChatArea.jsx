import { useEffect, useRef } from 'react'
import { MessageBubble } from './MessageBubble'
import { InputBar } from './InputBar'

const EXAMPLE_QUESTIONS = [
  'What is the main topic of this document?',
  'Summarize the key findings',
  'What methodology was used?',
  'List the main conclusions',
]

export function ChatArea({ messages, streaming, onSend, sessionId, onCopySession, attachment, onClearAttachment }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const isEmpty = messages.length === 0

  return (
    <main className="chat-area">
      <div className="chat-header">
        <div className="chat-header-title">
          {streaming ? '🤖 Thinking…' : '💬 Chat'}
        </div>
        <button
          className="session-badge"
          onClick={onCopySession}
          title="Click to copy session ID"
        >
          Session: {sessionId.slice(0, 8)}…
        </button>
      </div>

      <div className="messages-list">
        {isEmpty ? (
          <div className="empty-state">
            <div className="empty-icon">🔬</div>
            <div className="empty-title">Ask Anything</div>
            <p className="empty-sub">
              Upload a PDF document from the sidebar, then ask questions about its content.
            </p>
            <div className="empty-chips">
              {EXAMPLE_QUESTIONS.map(q => (
                <button
                  key={q}
                  className="empty-chip"
                  onClick={() => onSend(q)}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map(msg => <MessageBubble key={msg.id} message={msg} />)
        )}
        <div ref={bottomRef} />
      </div>

      <InputBar
        onSend={onSend}
        streaming={streaming}
        attachment={attachment}
        onClearAttachment={onClearAttachment}
      />
    </main>
  )
}
