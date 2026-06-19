import { useState, useCallback } from 'react'
import { fetchDocuments, uploadDocument, deleteDocument } from '../api/client'

export function useDocuments() {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)

  const loadDocuments = useCallback(async () => {
    setLoading(true)
    try {
      const docs = await fetchDocuments()
      setDocuments(docs)
    } finally {
      setLoading(false)
    }
  }, [])

  const upload = useCallback(async (file) => {
    setUploading(true)
    try {
      await uploadDocument(file)
      setTimeout(loadDocuments, 3000)
    } finally {
      setUploading(false)
    }
  }, [loadDocuments])

  const remove = useCallback(async (fileName) => {
    await deleteDocument(fileName)
    setDocuments(prev => prev.filter(d => d.file_name !== fileName))
  }, [])

  return { documents, loading, uploading, loadDocuments, upload, remove }
}
