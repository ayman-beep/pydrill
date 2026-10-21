import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import Dashboard from './components/Dashboard'
import WeekView from './components/WeekView'
import DrillSession from './components/DrillSession'
import StatsView from './components/StatsView'
import { api } from './lib/api'
import {
  cardOf,
  levelFromXp,
  recordKeystrokes,
  recordRecall,
  recordTypingRun,
  useProgress,
} from './lib/store'
import { overallStats, snippetMap } from './lib/selectors'
import { sfx } from './lib/sfx'
import { Flame, Speaker } from './components/Icons'

function parseHash() {
  const h = window.location.hash.replace(/^#\/?/, '')
  if (!h) return { name: 'home' }
  const parts = h.split('/')
  if (parts[0] === 'week' && parts[1]) return { name: 'week', n: Number(parts[1]) }
  if (parts[0] === 'drill' && parts[1]) return { name: 'drill', id: decodeURIComponent(parts[1]) }
  if (parts[0] === 'stats') return { name: 'stats' }
  return { name: 'home' }
}

function hashFor(route) {
  if (route.name === 'week') return `#/week/${route.n}`
  if (route.name === 'drill') return `#/drill/${encodeURIComponent(route.id)}`
  if (route.name === 'stats') return '#/stats'
  return '#/'
}

export default function App() {
  const [curriculum, setCurriculum] = useState(null)
  const [loadError, setLoadError] = useState(null)
  const [route, setRoute] = useState(parseHash)
  const [queue, setQueue] = useState({ ids: [], index: 0, label: '' })
  const [toasts, setToasts] = useState([])
  const progress = useProgress()
  const { state, update } = progress
  const pendingKeys = useRef(0)
  const prevLevel = useRef(null)

  useEffect(() => {
    api
      .curriculum()
      .then(setCurriculum)
      .catch((e) => setLoadError(e.message || 'The bundled curriculum could not be read'))
  }, [])

  useEffect(() => {
    const onHash = () => setRoute(parseHash())
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])

  // keep a valid queue whenever we are on a drill route
  useEffect(() => {
    if (route.name !== 'drill') return
    setQueue((q) => (q.ids[q.index] === route.id ? q : { ids: [route.id], index: 0, label: 'Single drill' }))
  }, [route])

  const snippets = curriculum?.snippets || []
  const byId = useMemo(() => snippetMap(snippets), [snippets])
  const stats = useMemo(() => overallStats(state, snippets), [state, snippets])

  const pushToast = useCallback((t) => {
    const id = Math.random().toString(36).slice(2)
    setToasts((list) => [...list, { ...t, id }])
    setTimeout(() => setToasts((list) => list.filter((x) => x.id !== id)), 3200)
  }, [])

  // keystrokes are batched so localStorage is not written on every keypress
  const flushKeys = useCallback(() => {
    if (pendingKeys.current > 0) {
      const n = pendingKeys.current
      pendingKeys.current = 0
      update((s) => recordKeystrokes(s, n))
    }
  }, [update])

  useEffect(() => {
    const t = setInterval(flushKeys, 4000)
    return () => clearInterval(t)
  }, [flushKeys])

  // level-up celebration
  useEffect(() => {
    const lvl = levelFromXp(state.xp).level
    if (prevLevel.current && lvl > prevLevel.current) {
      sfx.levelUp()
      pushToast({ kind: 'great', text: `Level ${lvl} reached!` })
    }
    prevLevel.current = lvl
  }, [state.xp, pushToast])

  const navigate = useCallback((r) => {
    window.location.hash = hashFor(r)
    setRoute(r)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [])

  const go = useCallback(
    (r, q) => {
      flushKeys()
      if (q) setQueue(q)
      navigate(r)
    },
    [navigate, flushKeys],
  )

  const startQueue = useCallback(
    (ids, label) => {
      if (!ids.length) return
      go({ name: 'drill', id: ids[0] }, { ids, index: 0, label })
    },
    [go],
  )

  const onStartReview = useCallback(() => {
    startQueue(stats.dueIds, 'Spaced review queue')
  }, [startQueue, stats.dueIds])

  const onStartWeek = useCallback(
    (n) => {
      const ids = snippets
        .filter((s) => s.week === n)
        .sort((a, b) => cardOf(state, a.id).stage - cardOf(state, b.id).stage)
        .map((s) => s.id)
      startQueue(ids, `Week ${n}`)
    },
    [snippets, state, startQueue],
  )

  const onStartDue = useCallback(
    (n) => {
      const today = new Date().toISOString().slice(0, 10)
      const ids = snippets
        .filter((s) => s.week === n && state.cards[s.id]?.due && state.cards[s.id].due <= today)
        .map((s) => s.id)
      startQueue(ids, `Week ${n} · due`)
    },
    [snippets, state, startQueue],
  )

  const drillSnippet = useCallback((id) => go({ name: 'drill', id }, { ids: [id], index: 0, label: 'Single drill' }), [go])

  const currentSnippet = route.name === 'drill' ? byId[route.id] : null
  const currentWeek = curriculum?.weeks.find((w) => w.n === currentSnippet?.week)

  const handleNext = useCallback(() => {
    flushKeys()
    const nextIndex = queue.index + 1
    if (nextIndex < queue.ids.length) {
      setQueue({ ...queue, index: nextIndex })
      navigate({ name: 'drill', id: queue.ids[nextIndex] })
    } else {
      pushToast({ kind: 'great', text: 'Queue finished — nice work.' })
      navigate(currentSnippet ? { name: 'week', n: currentSnippet.week } : { name: 'home' })
    }
  }, [queue, navigate, pushToast, currentSnippet, flushKeys])

  const handlePrev = useCallback(() => {
    if (queue.index === 0) return
    const prevIndex = queue.index - 1
    setQueue({ ...queue, index: prevIndex })
    navigate({ name: 'drill', id: queue.ids[prevIndex] })
  }, [queue, navigate])

  const handleExit = useCallback(() => {
    flushKeys()
    if (queue.label === 'Spaced review queue' || queue.ids.length > 1) {
      navigate(currentSnippet ? { name: 'week', n: currentSnippet.week } : { name: 'home' })
    } else {
      navigate({ name: 'home' })
    }
  }, [navigate, currentSnippet, queue, flushKeys])

  if (loadError) {
    return (
      <div className="center-screen">
        <div className="panel error-panel">
          <h2>Could not load the curriculum</h2>
          <p className="muted">{loadError}</p>
          <p className="muted small">
            This build is fully static: the snippet database ships inside the bundle. If this persists,
            the deployed assets may be stale — hard-reload the page.
          </p>
          <button className="btn primary" onClick={() => window.location.reload()}>Reload</button>
        </div>
      </div>
    )
  }

  if (!curriculum) {
    return (
      <div className="center-screen">
        <div className="loader">
          <span className="loader-dot" />
          <span className="loader-dot" />
          <span className="loader-dot" />
          <p className="muted small">Loading 14 weeks of drills…</p>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="topbar">
        <button className="brand" onClick={() => navigate({ name: 'home' })}>
          <span className="brand-mark">&gt;_</span>
          <span className="brand-text">
            PyDrill
            <small>Introduction to Data Science</small>
          </span>
        </button>
        <nav className="topnav">
          <button className={route.name === 'home' ? 'on' : ''} onClick={() => navigate({ name: 'home' })}>
            Dashboard
          </button>
          <button className={route.name === 'stats' ? 'on' : ''} onClick={() => navigate({ name: 'stats' })}>
            Progress
          </button>
        </nav>
        <div className="topbar-right">
          <button className="chip-btn streak" onClick={() => navigate({ name: 'stats' })} title="Daily streak">
            <Flame width={14} height={14} /> {state.streak.current}
          </button>
          <button
            className={`chip-btn due ${stats.dueCount ? 'hot' : ''}`}
            onClick={onStartReview}
            disabled={!stats.dueCount}
            title="Snippets due for spaced review"
          >
            {stats.dueCount} due today
          </button>
          <button
            className="icon-btn"
            title="Toggle sound"
            onClick={() => progress.toggleSetting('sound')}
          >
            <Speaker muted={!state.settings.sound} width={16} height={16} />
          </button>
        </div>
      </header>

      <main className="main">
        {route.name === 'home' && (
          <Dashboard
            curriculum={curriculum}
            state={state}
            onStartReview={onStartReview}
            onOpenWeek={(n) => navigate({ name: 'week', n })}
            onDrill={drillSnippet}
            onOpenStats={() => navigate({ name: 'stats' })}
          />
        )}

        {route.name === 'week' && (
          <WeekView
            week={curriculum.weeks.find((w) => w.n === route.n) || curriculum.weeks[0]}
            snippets={snippets}
            state={state}
            onBack={() => navigate({ name: 'home' })}
            onDrill={drillSnippet}
            onStartWeek={onStartWeek}
            onStartDue={onStartDue}
          />
        )}

        {route.name === 'stats' && (
          <StatsView
            curriculum={curriculum}
            state={state}
            onDrill={drillSnippet}
            onBack={() => navigate({ name: 'home' })}
            settings={state.settings}
            onToggleSetting={progress.toggleSetting}
            onExport={progress.exportJson}
            onImport={progress.importJson}
            onReset={progress.reset}
          />
        )}

        {route.name === 'drill' && currentSnippet && (
          <DrillSession
            key={currentSnippet.id}
            snippet={currentSnippet}
            week={currentWeek}
            card={cardOf(state, currentSnippet.id)}
            settings={state.settings}
            queueInfo={{ index: queue.index, total: queue.ids.length, label: queue.label }}
            hasNext={queue.index + 1 < queue.ids.length}
            hasPrev={queue.index > 0}
            onNext={handleNext}
            onPrev={handlePrev}
            onExit={handleExit}
            onTypingRun={() => update((s) => recordTypingRun(s, currentSnippet.id))}
            onRecall={(r) => update((s) => recordRecall(s, currentSnippet.id, r))}
            onKeystroke={(n) => {
              pendingKeys.current += n
            }}
            pushToast={pushToast}
          />
        )}

        {route.name === 'drill' && !currentSnippet && (
          <div className="panel">
            <h2>Unknown snippet</h2>
            <p className="muted">No snippet with id “{route.id}”.</p>
            <button className="btn primary" onClick={() => navigate({ name: 'home' })}>Back to dashboard</button>
          </div>
        )}
      </main>

      <footer className="footer">
        <span>PyDrill · Chessable-style spaced repetition for the Introduction to Data Science Python curriculum</span>
        <span className="muted">
          SM-2 intervals 1 → 3 → 7 → 14 → 30 days · {snippets.length} snippets · runs entirely in your browser
          (no server, no account) · progress saved locally
        </span>
      </footer>

      <div className="toasts">
        {toasts.map((t) => (
          <div key={t.id} className={`toast ${t.kind || 'ok'}`}>{t.text}</div>
        ))}
      </div>
    </div>
  )
}
