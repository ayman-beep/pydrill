// Day helpers — everything is stored as a local YYYY-MM-DD key.
export const DAY_MS = 86400000

export function dayKey(d = new Date()) {
  const dt = d instanceof Date ? d : new Date(d)
  const y = dt.getFullYear()
  const m = String(dt.getMonth() + 1).padStart(2, '0')
  const dd = String(dt.getDate()).padStart(2, '0')
  return `${y}-${m}-${dd}`
}

export function addDays(date, n) {
  const d = new Date(date)
  d.setDate(d.getDate() + n)
  return d
}

export function daysBetween(aKey, bKey) {
  const a = new Date(aKey + 'T00:00:00')
  const b = new Date(bKey + 'T00:00:00')
  return Math.round((b - a) / DAY_MS)
}

export function prettyDate(key) {
  if (!key) return '—'
  const d = new Date(key + 'T00:00:00')
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}

export function relativeDue(key) {
  const diff = daysBetween(dayKey(), key)
  if (diff < 0) return `${Math.abs(diff)}d overdue`
  if (diff === 0) return 'due today'
  if (diff === 1) return 'tomorrow'
  return `in ${diff}d`
}
