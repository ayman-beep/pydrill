import { STAGE_PCT, cardOf, intervalForStage } from './store'
import { dayKey, daysBetween } from './dates'

export function snippetMap(snippets) {
  return Object.fromEntries(snippets.map((s) => [s.id, s]))
}

export function weekStats(state, week, snippets) {
  const ids = snippets.filter((s) => s.week === week.n).map((s) => s.id)
  const stages = ids.map((id) => cardOf(state, id).stage)
  const pct = ids.length ? Math.round(stages.reduce((a, s) => a + STAGE_PCT[s], 0) / ids.length) : 0
  return {
    pct,
    total: ids.length,
    mastered: stages.filter((s) => s >= 6).length,
    inProgress: stages.filter((s) => s >= 1 && s < 6).length,
    notStarted: stages.filter((s) => s === 0).length,
    due: ids.filter((id) => {
      const c = state.cards[id]
      return c && c.due && c.due <= dayKey()
    }).length,
  }
}

export function overallStats(state, snippets) {
  const stages = snippets.map((s) => cardOf(state, s.id).stage)
  const pct = snippets.length
    ? Math.round(stages.reduce((a, s) => a + STAGE_PCT[s], 0) / snippets.length)
    : 0
  const due = snippets.filter((s) => {
    const c = state.cards[s.id]
    return c && c.due && c.due <= dayKey()
  })
  return {
    pct,
    mastered: stages.filter((s) => s >= 6).length,
    inProgress: stages.filter((s) => s >= 1 && s < 6).length,
    notStarted: stages.filter((s) => s === 0).length,
    learning: stages.filter((s) => s >= 1).length,
    dueCount: due.length,
    dueIds: due
      .slice()
      .sort((a, b) => (state.cards[a.id].due || '').localeCompare(state.cards[b.id].due || ''))
      .map((s) => s.id),
    total: snippets.length,
  }
}

export function nextUp(state, snippets) {
  const unseen = snippets.find((s) => cardOf(state, s.id).stage === 0)
  if (unseen) return { snippet: unseen, reason: 'Next in the curriculum' }
  const due = snippets
    .filter((s) => {
      const c = state.cards[s.id]
      return c && c.due && c.due <= dayKey()
    })
    .sort((a, b) => (state.cards[a.id].due || '').localeCompare(state.cards[b.id].due || ''))
  if (due.length) return { snippet: due[0], reason: 'Due for spaced review' }
  const weakest = snippets
    .slice()
    .sort((a, b) => cardOf(state, a.id).stage - cardOf(state, b.id).stage)
    .find((s) => cardOf(state, s.id).stage < 6)
  return weakest ? { snippet: weakest, reason: 'Strengthen a weak card' } : null
}

export function upcomingLoad(state) {
  // next 7 days: how many cards fall due
  const out = []
  for (let i = 0; i < 7; i += 1) {
    const d = new Date()
    d.setDate(d.getDate() + i)
    const key = dayKey(d)
    const n = Object.values(state.cards).filter((c) => c.due === key).length
    out.push({ key, n })
  }
  return out
}

export function activityDays(state, count = 35) {
  const out = []
  for (let i = count - 1; i >= 0; i -= 1) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    const key = dayKey(d)
    const day = state.daily[key]
    const load = day ? (day.reviews || 0) + (day.typingRuns || 0) : 0
    out.push({ key, load, day })
  }
  return out
}

export function cardDetail(state, id) {
  const c = cardOf(state, id)
  return {
    ...c,
    interval: intervalForStage(c.stage),
    overdue: c.due ? Math.max(0, daysBetween(c.due, dayKey())) : 0,
  }
}
