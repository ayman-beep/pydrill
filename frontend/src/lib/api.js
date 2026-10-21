// Thin API client. All requests are same-origin ('/api/...') so the Vite dev
// proxy (and the FastAPI static mount in production) can serve them.
const BASE = '/api'

async function req(path, init) {
  const res = await fetch(BASE + path, init)
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      detail = body.detail || detail
    } catch (_) {}
    throw new Error(detail)
  }
  return res.json()
}

export const api = {
  health: () => req('/health'),
  curriculum: () => req('/curriculum'),
  weeks: () => req('/weeks'),
  spec: () => req('/spec'),
  snippet: (id) => req(`/snippets/${encodeURIComponent(id)}`),
  grade: (payload) =>
    req('/grade', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }),
}
