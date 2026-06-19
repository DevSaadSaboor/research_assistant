import { useEffect } from 'react'

export function Toast({ toasts, remove }) {
  useEffect(() => {
    if (toasts.length === 0) return
    const last = toasts[toasts.length - 1]
    const timer = setTimeout(() => remove(last.id), 3500)
    return () => clearTimeout(timer)
  }, [toasts, remove])

  const icon = { success: '✅', error: '❌', info: 'ℹ️' }

  return (
    <div className="toast-container">
      {toasts.map(t => (
        <div key={t.id} className={`toast ${t.type}`}>
          <span className="toast-icon">{icon[t.type] ?? 'ℹ️'}</span>
          <span className="toast-msg">{t.message}</span>
        </div>
      ))}
    </div>
  )
}
