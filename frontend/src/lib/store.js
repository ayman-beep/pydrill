import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { addDays, dayKey } from './dates'

export const STORAGE_KEY = 'pydrill.progress.v1'
export const TYPING_REPS = 3
export const INTERVALS = [1, 3, 7, 14, 30] // days, in ascending stage order

// stage: 0 unseen | 1 typed (awaiting recall) | 2..6 spaced-repetition levels
export const STAGE_LABEL = {
  0: 'Not started',
  1: 'Typing drill done',
  2: 'Day 1 review',
  3: 'Day 3 review',
  4: 'Day 7 review',
  5: 'Day 14 review',
  6: 'Mastered · Day 30',
}

// 0-100 mastery percentage that powers the weekly progress bars.
export const STAGE_PCT = { 0: 0, 1: 30, 2: 45, 3: 60, 4: 75, 5: 90, 6: 100 }

export function blankCard() {
  return {
    stage: 0,
    ease: 2.5,
    due: null,
    lapses: 0,
    reps: 0,           // successful recall reps
    typeRuns: 0,       // total perfect typing runs ever
    recallAttempts: 0,
    needsTyping: false,
    lastReviewed: null,
    history: [],       // [{ day, mode, passed }]
  }
}

export function blankState() {
  return {
    version: 1,
    created: dayKey(),
    cards: {},
    xp: 0,
    streak: { current: 0, best: 0, lastDay: null },
    daily: {}, // day -> { reviews, typingRuns, keystrokes, recalls, exact }
    sessions: [],
    settings: { sound: true, strict: true, tts: false },
  }
}

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return blankState()
    const parsed = JSON.parse(raw)
    return { ...blankState(), ...parsed, streak: { ...blankState().streak, ...(parsed.streak || {}) },
      settings: { ...blankState().settings, ...(parsed.settings || {}) } }
  } catch (e) {
    console.warn('progress load failed, starting fresh', e)
    return blankState()
  }
}

export function cardOf(state, id) {
  return state.cards[id] || blankCard()
}

export function linesLabel(n) {
  return `${n} line${n === 1 ? '' : 's'}`
}

export function intervalForStage(stage) {
  if (stage < 2) return 0
  return INTERVALS[Math.min(stage - 2, INTERVALS.length - 1)]
}

export function isDue(state, id, today = dayKey()) {
  const c = state.cards[id]
  if (!c) return false
  if (!c.due) return false
  return c.due <= today
}

export function reviewDueCount(state, snippetIds) {
  const today = dayKey()
  return snippetIds.filter((id) => isDue(state, id, today)).length
}

function touchStreak(state, today) {
  const s = { ...state.streak }
  if (s.lastDay === today) return s
  const yesterday = dayKey(addDays(new Date(), -1))
  s.current = s.lastDay === yesterday ? s.current + 1 : 1
  s.best = Math.max(s.best, s.current)
  s.lastDay = today
  return s
}

function bumpDaily(state, today, patch) {
  const prev = state.daily[today] || { reviews: 0, typingRuns: 0, keystrokes: 0, recalls: 0, exact: 0 }
  return { ...state.daily, [today]: { ...prev, ...patch } }
}

function withCard(state, id, card) {
  return { ...state, cards: { ...state.cards, [id]: card } }
}

// --------------------------------------------------------------- mutators
/** Records one perfect character-for-character typing run (Step 1/2). */
export function recordTypingRun(state, id) {
  const today = dayKey()
  const card = { ...cardOf(state, id) }
  card.typeRuns += 1
  if (card.stage === 0) {
    card.stage = 1
    card.due = today
  }
  if (card.needsTyping) card.needsTyping = false
  card.history = [...card.history.slice(-49), { day: today, mode: 'typing', passed: true }]

  let next = withCard(state, id, card)
  const d = next.daily[today] || {}
  next = {
    ...next,
    xp: next.xp + 10,
    streak: touchStreak(next, today),
    daily: bumpDaily(next, today, { typingRuns: (d.typingRuns || 0) + 1, reviews: d.reviews || 0 }),
  }
  return next
}

export function recordKeystrokes(state, n) {
  const today = dayKey()
  const d = state.daily[today] || {}
  return { ...state, daily: bumpDaily(state, today, { keystrokes: (d.keystrokes || 0) + n }) }
}

/** Applies the SM-2 style scheduling after a hidden-recall attempt (Step 3/4). */
export function recordRecall(state, id, { passed, firstAttempt }) {
  const today = dayKey()
  const card = { ...cardOf(state, id) }
  card.recallAttempts += 1
  card.lastReviewed = today

  if (passed) {
    const prevStage = card.stage
    card.stage = Math.max(2, Math.min(6, prevStage + 1))
    card.ease = Math.min(2.9, card.ease + 0.1)
    card.reps += 1
    card.needsTyping = false
    const days = intervalForStage(card.stage)
    card.due = dayKey(addDays(new Date(), days))
    card.history = [...card.history.slice(-49), { day: today, mode: 'recall', passed: true }]

    let next = withCard(state, id, card)
    const d = next.daily[today] || {}
    next = {
      ...next,
      xp: next.xp + (firstAttempt ? 40 : 18),
      streak: touchStreak(next, today),
      daily: bumpDaily(next, today, {
        reviews: (d.reviews || 0) + 1,
        recalls: (d.recalls || 0) + 1,
        exact: (d.exact || 0) + (firstAttempt ? 1 : 0),
      }),
    }
    return next
  }

  // Failed recall -> lapse: drop back to Day 1 and force Step 1 again.
  card.stage = 1
  card.ease = Math.max(1.3, card.ease - 0.2)
  card.lapses += 1
  card.needsTyping = true
  card.due = today
  card.history = [...card.history.slice(-49), { day: today, mode: 'recall', passed: false }]

  let next = withCard(state, id, card)
  const d = next.daily[today] || {}
  next = {
    ...next,
    streak: touchStreak(next, today),
    daily: bumpDaily(next, today, { reviews: (d.reviews || 0) + 1, recalls: (d.recalls || 0) + 1 }),
  }
  return next
}

export function logSession(state, entry) {
  return { ...state, sessions: [...state.sessions.slice(-59), entry] }
}

export function levelFromXp(xp) {
  const level = Math.floor(Math.sqrt(xp / 60)) + 1
  const floorXp = (level - 1) ** 2 * 60
  const nextXp = level ** 2 * 60
  return { level, floorXp, nextXp, pct: Math.round(((xp - floorXp) / Math.max(1, nextXp - floorXp)) * 100) }
}

// --------------------------------------------------------------- hook
export function useProgress() {
  const [state, setState] = useState(load)
  const ref = useRef(state)
  ref.current = state

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
    } catch (e) {
      console.warn('could not persist progress', e)
    }
  }, [state])

  useEffect(() => {
    const onStorage = (ev) => {
      if (ev.key === STORAGE_KEY && ev.newValue) {
        try {
          setState(JSON.parse(ev.newValue))
        } catch (_) {}
      }
    }
    window.addEventListener('storage', onStorage)
    return () => window.removeEventListener('storage', onStorage)
  }, [])

  const update = useCallback((fn) => setState((s) => fn(s)), [])

  const reset = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY)
    setState(blankState())
  }, [])

  const toggleSetting = useCallback((key) => {
    setState((s) => ({ ...s, settings: { ...s.settings, [key]: !s.settings[key] } }))
  }, [])

  const exportJson = useCallback(() => JSON.stringify(ref.current, null, 2), [])

  const importJson = useCallback((text) => {
    const parsed = JSON.parse(text)
    if (typeof parsed !== 'object' || !parsed) throw new Error('Not a progress file')
    const merged = { ...blankState(), ...parsed }
    setState(merged)
    return merged
  }, [])

  return useMemo(
    () => ({ state, update, reset, toggleSetting, exportJson, importJson }),
    [state, update, reset, toggleSetting, exportJson, importJson],
  )
}
