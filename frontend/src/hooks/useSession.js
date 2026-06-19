import { useState } from 'react'

const KEY = 'ra_session_id'

function createId() {
  const id = crypto.randomUUID()
  localStorage.setItem(KEY, id)
  return id
}

export function useSession() {
  const [sessionId, setSessionId] = useState(
    () => localStorage.getItem(KEY) || createId()
  )

  function newSession() {
    setSessionId(createId())
  }

  function copySessionId() {
    navigator.clipboard.writeText(sessionId)
  }

  return { sessionId, newSession, copySessionId }
}
