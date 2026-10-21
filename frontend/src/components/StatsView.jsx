import { useMemo, useState } from 'react'
import { STAGE_LABEL, STAGE_PCT, cardOf, levelFromXp } from '../lib/store'
import { overallStats, weekStats } from '../lib/selectors'
import { prettyDate, relativeDue } from '../lib/dates'

export default function StatsView({ curriculum, state, onDrill, onBack, settings, onToggleSetting, onExport, onImport, onReset }) {
  const { weeks, snippets } = curriculum
  const stats = overallStats(state, snippets)
  const lvl = levelFromXp(state.xp)
  const [q, setQ] = useState('')
  const [filter, setFilter] = useState('all')
  const [importText, setImportText] = useState('')
  const [msg, setMsg] = useState(null)

  const rows = useMemo(() => {
    return snippets
      .filter((s) => (filter === 'due' ? state.cards[s.id]?.due && state.cards[s.id].due <= new Date().toISOString().slice(0, 10) : true))
      .filter((s) => (filter === 'mastered' ? cardOf(state, s.id).stage >= 6 : true))
      .filter((s) => (filter === 'learning' ? cardOf(state, s.id).stage >= 1 && cardOf(state, s.id).stage < 6 : true))
      .filter((s) => (filter === 'new' ? cardOf(state, s.id).stage === 0 : true))
      .filter((s) => {
        if (!q.trim()) return true
        const t = q.toLowerCase()
        return s.id.includes(t) || s.title.toLowerCase().includes(t) || s.topic.toLowerCase().includes(t) || s.code.toLowerCase().includes(t)
      })
  }, [snippets, q, filter, state])

  return (
    <div className="stats-view">
      <button className="btn ghost small" onClick={onBack}>← Dashboard</button>
      <h1>Progress & settings</h1>

      <div className="stat-row">
        <div className="stat-card accent-mint">
          <span className="stat-label">Course mastery</span>
          <strong className="stat-value">{stats.pct}<small>%</small></strong>
          <span className="stat-foot">{stats.mastered} of {stats.total} at day-30</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Learning</span>
          <strong className="stat-value">{stats.learning}<small> cards</small></strong>
          <span className="stat-foot">{stats.dueCount} due now</span>
        </div>
        <div className="stat-card accent-amber">
          <span className="stat-label">Level</span>
          <strong className="stat-value">{lvl.level}</strong>
          <span className="stat-foot">{state.xp} XP total</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Streak</span>
          <strong className="stat-value">{state.streak.current}<small> days</small></strong>
          <span className="stat-foot">best {state.streak.best}</span>
        </div>
      </div>

      <section className="panel">
        <header className="panel-head">
          <h2>Per-week mastery</h2>
          <span className="muted small">average stage across snippets</span>
        </header>
        <div className="week-table">
          {weeks.map((w) => {
            const s = weekStats(state, w, snippets)
            return (
              <div className="week-table-row" key={w.n}>
                <span className="week-table-n" style={{ color: w.accent }}>W{w.n}</span>
                <span className="week-table-title">{w.title}</span>
                <div className="progress thin">
                  <div className="progress-fill" style={{ width: `${s.pct}%`, background: w.accent }} />
                </div>
                <span className="week-table-pct">{s.pct}%</span>
                <span className="muted small">{s.mastered}/{s.total}</span>
              </div>
            )
          })}
        </div>
      </section>

      <section className="panel">
        <header className="panel-head">
          <h2>Card browser</h2>
          <span className="muted small">{rows.length} shown</span>
        </header>
        <div className="browser-controls">
          <input
            className="input"
            placeholder="Search id, title, topic or code…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
          {['all', 'due', 'learning', 'mastered', 'new'].map((f) => (
            <button key={f} className={`chip-btn ${filter === f ? 'on' : ''}`} onClick={() => setFilter(f)}>
              {f}
            </button>
          ))}
        </div>
        <div className="card-table">
          {rows.slice(0, 200).map((s) => {
            const c = cardOf(state, s.id)
            return (
              <button className="card-row" key={s.id} onClick={() => onDrill(s.id)}>
                <span className="card-id">{s.id.toUpperCase()}</span>
                <span className="card-title">{s.title}</span>
                <span className="muted small">W{s.week}</span>
                <span className="chip small">{STAGE_LABEL[c.stage]}</span>
                <div className="mini-progress"><div className="mini-fill" style={{ width: `${STAGE_PCT[c.stage]}%` }} /></div>
                <span className="muted small">{c.reps} reps</span>
                <span className="muted small">{c.due ? `${relativeDue(c.due)} (${prettyDate(c.due)})` : '—'}</span>
                <span className="muted small">{c.lapses} lapses</span>
              </button>
            )
          })}
        </div>
      </section>

      <section className="panel settings-panel">
        <header className="panel-head"><h2>Drill settings</h2></header>
        <label className="toggle-row">
          <span>Sound effects <small className="muted">— key clicks, error buzz, success chimes</small></span>
          <input type="checkbox" checked={settings.sound} onChange={() => onToggleSetting('sound')} />
        </label>
        <label className="toggle-row">
          <span>Strict mode <small className="muted">— a single wrong keystroke resets the run counter to 0</small></span>
          <input type="checkbox" checked={settings.strict} onChange={() => onToggleSetting('strict')} />
        </label>
        <label className="toggle-row">
          <span>Read prompts aloud <small className="muted">— uses the browser speech synthesiser</small></span>
          <input type="checkbox" checked={settings.tts} onChange={() => onToggleSetting('tts')} />
        </label>
        <div className="danger-zone">
          <button
            className="btn ghost small"
            onClick={() => {
              const blob = new Blob([onExport()], { type: 'application/json' })
              const url = URL.createObjectURL(blob)
              const a = document.createElement('a')
              a.href = url
              a.download = 'pydrill-progress.json'
              a.click()
              URL.revokeObjectURL(url)
            }}
          >
            Export progress
          </button>
          <input className="input" placeholder="Paste exported JSON to import…" value={importText} onChange={(e) => setImportText(e.target.value)} />
          <button
            className="btn ghost small"
            onClick={() => {
              try {
                onImport(importText)
                setMsg('Progress imported.')
                setImportText('')
              } catch (e) {
                setMsg(`Import failed: ${e.message}`)
              }
            }}
          >
            Import
          </button>
          <button
            className="btn danger small"
            onClick={() => {
              if (window.confirm('Reset all progress? This cannot be undone.')) {
                onReset()
                setMsg('Progress reset.')
              }
            }}
          >
            Reset all
          </button>
        </div>
        {msg && <p className="muted small">{msg}</p>}
        <p className="muted small">
          Progress is stored in this browser (localStorage). Streak days, per-card SM-2 state and session history
          are all included in the export.
        </p>
      </section>
    </div>
  )
}
