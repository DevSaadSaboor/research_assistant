import { useState, useEffect, useCallback } from 'react'
import { Sidebar } from './components/Sidebar'
import { ChatArea } from './components/ChatArea'
import { SummaryModal } from './components/SummaryModal'
import { Toast } from './components/Toast'
import { useSession } from './hooks/useSession'
import { useDocuments } from './hooks/useDocuments'
import { useChat } from './hooks/useChat'

export default function App() {
  const { sessionId, newSession, copySessionId } = useSession()
  const { documents, loading, uploading, loadDocuments, upload, remove } = useDocuments()
  const { messages, streaming, sendMessage, addUploadMessage, markUploadReady } = useChat(sessionId)
  const [summaryFile, setSummaryFile] = useState(null)
  const [toasts, setToasts] = useState([])
  const [pendingAttachment, setPendingAttachment] = useState(null)

  useEffect(() => { loadDocuments() }, [loadDocuments])

  const addToast = useCallback((message, type = 'info') => {
    const id = Date.now()
    setToasts(prev => [...prev, { id, message, type }])
  }, [])

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  async function handleUpload(file) {
    const msgId = addUploadMessage(file.name)
    try {
      await upload(file)
      setPendingAttachment(file.name)
      setTimeout(() => markUploadReady(msgId), 4000)
    } catch (err) {
      addToast(err.message || 'Upload failed', 'error')
      markUploadReady(msgId)
    }
  }

  function handleSend(text) {
    sendMessage(text)
    setPendingAttachment(null)
  }

  async function handleDelete(fileName) {
    try {
      await remove(fileName)
      addToast(`"${fileName}" deleted`, 'success')
    } catch {
      addToast('Delete failed', 'error')
    }
  }

  function handleNewSession() {
    newSession()
    setPendingAttachment(null)
  }

  function handleCopySession() {
    copySessionId()
    addToast('Session ID copied to clipboard', 'info')
  }

  return (
    <div className="app-layout">
      <Sidebar
        documents={documents}
        loading={loading}
        uploading={uploading}
        onUpload={handleUpload}
        onDelete={handleDelete}
        onSummarize={setSummaryFile}
        onNewChat={handleNewSession}
      />
      <ChatArea
        messages={messages}
        streaming={streaming}
        onSend={handleSend}
        sessionId={sessionId}
        onCopySession={handleCopySession}
        attachment={pendingAttachment}
        onClearAttachment={() => setPendingAttachment(null)}
      />
      {summaryFile && (
        <SummaryModal
          fileName={summaryFile}
          onClose={() => setSummaryFile(null)}
        />
      )}
      <Toast toasts={toasts} remove={removeToast} />
    </div>
  )
}
