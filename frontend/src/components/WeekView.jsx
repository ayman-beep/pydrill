import { useState } from 'react'
import Ring from './Ring'
import SnippetExplainer from './Explainer'
import { Book, Play } from './Icons'
import { STAGE_LABEL, STAGE_PCT, cardOf } from '../lib/store'
import { weekStats } from '../lib/selectors'
import { dayKey, prettyDate, relativeDue } from '../lib/dates'

function StageChip({ stage }) {
  const cls = stage === 0 ? 'fresh' : stage >= 6 ? 'mastered' : 'progress'
  return <span className={`chip ${cls}`}>{STAGE_LABEL[stage]}</span>
}

export default function WeekView({ week, snippets, state, onBack, onDrill, onStartWeek, onStartDue }) {
  const weekSnippets = snippets.filter((s) => s.week === week.n)
  const [openId, setOpenId] = useState(null)
  const stats = weekStats(state, week, snippets)
  const today = dayKey()

  return (
    <div className="week-view">
      <button className="btn ghost small" onClick={onBack}>← All weeks</button>
      <section className="week-header" style={{ borderColor: `${week.accent}55` }}>
        <div>
          <div className="eyebrow" style={{ color: week.accent }}>Week {week.n} of 14</div>
          <h1>{week.title}</h1>
          <p className="muted">{week.blurb}</p>
          <div className="hero-actions">
            <button className="btn primary" onClick={() => onStartWeek(week.n)}><Play width={14} height={14} /> Drill this module</button>
            <button className="btn ghost" onClick={() => onStartDue(week.n)} disabled={!stats.due}>
              Review {stats.due} due
            </button>
          </div>
        </div>
        <Ring value={stats.pct} size={140} stroke={12} accent={week.accent} label={`${stats.pct}%`} sub="mastery" />
      </section>

      <div className="week-summary-row">
        <div><span className="muted small">Snippets</span><strong>{stats.total}</strong></div>
        <div><span className="muted small">Mastered</span><strong>{stats.mastered}</strong></div>
        <div><span className="muted small">Learning</span><strong>{stats.inProgress}</strong></div>
        <div><span className="muted small">Unseen</span><strong>{stats.notStarted}</strong></div>
        <div><span className="muted small">Due now</span><strong>{stats.due}</strong></div>
      </div>

      <div className="snippet-list">
        {weekSnippets.map((s) => {
          const card = cardOf(state, s.id)
          const due = card.due
          const isDue = due && due <= today
          return (
            <div className={`snippet-item ${openId === s.id ? 'open' : ''}`} key={s.id}>
            <div className="snippet-row">
              <div className="snippet-id">{s.id.toUpperCase()}</div>
              <div className="snippet-main">
                <div className="snippet-title">
                  {s.title}
                  <span className="pill topic">{s.topic}</span>
                </div>
                <div className="snippet-prompt">{s.prompt}</div>
              </div>
              <div className="snippet-meta">
                <span className="stars">{'★'.repeat(s.difficulty)}{'☆'.repeat(3 - s.difficulty)}</span>
                <span className="muted small">{s.lines} line{s.lines === 1 ? '' : 's'}</span>
              </div>
              <div className="snippet-stage">
                <StageChip stage={card.stage} />
                <div className="mini-progress">
                  <div className="mini-fill" style={{ width: `${STAGE_PCT[card.stage]}%`, background: week.accent }} />
                </div>
                <span className="muted small">
                  {due ? `next ${relativeDue(due)} · ${prettyDate(due)}` : 'not scheduled'}
                </span>
              </div>
              <div className="snippet-actions">
                <button
                  className={`btn ghost small explain-toggle ${openId === s.id ? 'on' : ''}`}
                  onClick={() => setOpenId(openId === s.id ? null : s.id)}
                  title="Explain this code"
                >
                  <Book width={13} height={13} /> Explain
                </button>
                <button className={`btn ${isDue ? 'warn' : 'primary'} small`} onClick={() => onDrill(s.id)}>
                  {isDue ? 'Review' : card.stage === 0 ? 'Learn' : 'Drill'}
                </button>
              </div>
            </div>
            {openId === s.id && (
              <div className="snippet-explain">
                <SnippetExplainer snippet={s} accent={week.accent} />
              </div>
            )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
