export async function uploadDocument(file) {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch('/upload', { method: 'POST', body: form })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Upload failed')
  }
  return res.json()
}

export async function fetchDocuments() {
  const res = await fetch('/documents')
  if (!res.ok) throw new Error('Failed to load documents')
  return res.json()
}

export async function deleteDocument(fileName) {
  const res = await fetch(`/documents/${encodeURIComponent(fileName)}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error('Delete failed')
  return res.json()
}

export async function summarizeDocument(fileName) {
  const res = await fetch('/summarize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ file_name: fileName }),
  })
  if (!res.ok) throw new Error('Summarization failed')
  return res.json()
}


export async function askStream(sessionId, question, onToken) {
  const res = await fetch('/ask_stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, question }),
  })

  if (!res.ok) throw new Error('Request failed')

  const reader = res.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    onToken(decoder.decode(value, { stream: true }))
  }
}
