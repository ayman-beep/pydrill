// Data + grading layer. This build is **fully static**: the curriculum ships as
// JSON inside the bundle and grading runs in the browser, so there is no API
// call and no server to host (Netlify serves the built files only).
//
// The async signatures are kept so components can call this exactly as they
// called the old HTTP client — swapping back to a server later is a one-file job.
import data from '../data/curriculum.json'
import { gradeAttempt } from './grade'

const snippetsById = new Map(data.snippets.map((s) => [s.id, s]))
const order = data.snippets.map((s) => s.id)

function neighbour(id, step) {
  const idx = order.indexOf(id)
  if (idx === -1) return null
  const next = idx + step
  return next >= 0 && next < order.length ? order[next] : null
}

export const api = {
  health: async () => ({
    status: 'static',
    weeks: data.weeks.length,
    snippets: data.snippets.length,
    total_chars: data.snippets.reduce((a, s) => a + s.code.length, 0),
  }),

  curriculum: async () => data,

  weeks: async () =>
    data.weeks.map((w) => {
      const items = data.snippets.filter((s) => s.week === w.n)
      return {
        ...w,
        difficulty_avg:
          Math.round((items.reduce((a, s) => a + s.difficulty, 0) / Math.max(1, items.length)) * 100) / 100,
        lines_total: items.reduce((a, s) => a + s.lines, 0),
      }
    }),

  snippet: async (id) => {
    const s = snippetsById.get(id)
    if (!s) throw new Error(`Unknown snippet '${id}'`)
    return { ...s, next_id: neighbour(id, 1), prev_id: neighbour(id, -1) }
  },

  /** Grade in the browser — same shape the FastAPI endpoint returned. */
  grade: async ({ snippet_id: snippetId, typed, mode = 'recall', retry_count: retryCount = 0 }) => {
    const snippet = snippetsById.get(snippetId)
    if (!snippet) throw new Error(`Unknown snippet '${snippetId}'`)
    // Yield a tick so the "Grading…" state paints before the (synchronous) work.
    await Promise.resolve()
    return gradeAttempt(snippet, typed, { mode, retryCount })
  },

  spec: async () => ({
    steps: [
      { step: 1, name: 'Visual Demonstration', detail: 'Target snippet shown with syntax highlighting.' },
      { step: 2, name: 'Muscle Memory', detail: 'Type the snippet character-for-character 3 consecutive times.' },
      { step: 3, name: 'Error Correction', detail: 'Any wrong keystroke resets the run counter to 0.' },
      { step: 4, name: 'Hidden Recall', detail: 'Snippet hidden; natural-language prompt only.' },
      { step: 5, name: 'Spaced Repetition', detail: 'SM-2 style intervals: 1, 3, 7, 14, 30 days.' },
    ],
    intervals_days: [1, 3, 7, 14, 30],
    typing_reps_required: 3,
  }),
}
