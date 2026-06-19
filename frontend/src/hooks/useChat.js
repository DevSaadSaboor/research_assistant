import { useState, useCallback, useEffect } from 'react'
import { askStream } from '../api/client'

const SOURCES_MARKER = '\n\n__SOURCES__:'

export function useChat(sessionId) {
  const [messages, setMessages] = useState([])
  const [streaming, setStreaming] = useState(false)

  useEffect(() => {
    setMessages([])
    setStreaming(false)
  }, [sessionId])

  const sendMessage = useCallback(async (question) => {
    if (!question.trim() || streaming) return

  
    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: question,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }
    setMessages(prev => [...prev, userMsg])

   
    const aiId = Date.now() + 1
    const aiMsg = {
      id: aiId,
      role: 'ai',
      content: '',
      sources: [],
      streaming: true,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }
    setMessages(prev => [...prev, aiMsg])

    setStreaming(true)
    let fullText = ''   

    try {
      await askStream(sessionId, question, (chunk) => {
        fullText += chunk
        setMessages(prev =>
          prev.map(m =>
            m.id === aiId ? { ...m, content: m.content + chunk } : m
          )
        )
      })

   
      const markerIdx = fullText.indexOf(SOURCES_MARKER)
      const cleanText = markerIdx !== -1
        ? fullText.slice(0, markerIdx)
        : fullText

      let sources = []
      if (markerIdx !== -1) {
        try {
          sources = JSON.parse(fullText.slice(markerIdx + SOURCES_MARKER.length))
        } catch { /* sources are non-critical */ }
      }


      setMessages(prev =>
        prev.map(m =>
          m.id === aiId
            ? { ...m, content: cleanText, sources, streaming: false }
            : m
        )
      )
    } catch (err) {
      setMessages(prev =>
        prev.map(m =>
          m.id === aiId
            ? { ...m, content: '⚠️ Something went wrong. Please try again.', streaming: false }
            : m
        )
      )
    } finally {
      setStreaming(false)
    }
  }, [sessionId, streaming])


  const addUploadMessage = useCallback((fileName) => {
    const id = Date.now()
    setMessages(prev => [...prev, {
      id,
      role: 'system',
      type: 'upload',
      fileName,
      status: 'processing',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }])
    return id
  }, [])

  const markUploadReady = useCallback((id) => {
    setMessages(prev => prev.map(m => m.id === id ? { ...m, status: 'ready' } : m))
  }, [])

  return { messages, streaming, sendMessage, addUploadMessage, markUploadReady }
}
