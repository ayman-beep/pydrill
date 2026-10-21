import Ring from './Ring'
import { Bolt, Check, Flame, Play, Target } from './Icons'
import { levelFromXp } from '../lib/store'
import { activityDays, nextUp, overallStats, upcomingLoad, weekStats } from '../lib/selectors'
import { dayKey, prettyDate } from '../lib/dates'

const METHOD = [
  { n: 1, title: 'Demonstrate', body: 'Read the highlighted snippet and drill it into muscle memory.' },
  { n: 2, title: 'Muscle memory', body: 'Type it character-for-character — 3 consecutive error-free runs.' },
  { n: 3, title: 'Hidden recall', body: 'The code disappears. Write it from the prompt alone.' },
  { n: 4, title: 'Spaced review', body: 'SM-2 scheduling: 1 → 3 → 7 → 14 → 30 days. A miss sends you back to Step 1.' },
]

export default function Dashboard({ curriculum, state, onStartReview, onOpenWeek, onDrill, onOpenStats }) {
  const { weeks, snippets, total_snippets } = curriculum
  const stats = overallStats(state, snippets)
  const next = nextUp(state, snippets)
  const lvl = levelFromXp(state.xp)
  const today = dayKey()
  const todayStats = state.daily[today] || { reviews: 0, typingRuns: 0, keystrokes: 0 }
  const activity = activityDays(state, 35)
  const load = upcomingLoad(state)
  const maxLoad = Math.max(1, ...load.map((l) => l.n))

  return (
    <div className="dashboard">
      <section className="hero">
        <div className="hero-copy">
          <div className="eyebrow">Introduction to Data Science · Weeks 1–14</div>
          <h1>
            Drill Python until it is <em>automatic</em>.
          </h1>
          <p className="lede">
            A Chessable-style move trainer for data science code. Every snippet passes through four gates:
            watch it, type it three times perfectly, recall it blind, then revisit it on a spaced schedule.
            {` ${total_snippets} curated snippets across 14 weekly modules.`}
          </p>
          <div className="hero-actions">
            <button className="btn primary lg" onClick={onStartReview} disabled={!stats.dueCount}>
              <>{stats.dueCount ? <><Play width={14} height={14} /> Review {stats.dueCount} due snippet{stats.dueCount === 1 ? '' : 's'}</> : 'Nothing due — learn something new'}</>
            </button>
            {next && (
              <button className="btn ghost lg" onClick={() => onDrill(next.snippet.id)}>
                Next: {next.snippet.id.toUpperCase()} — {next.snippet.title}
              </button>
            )}
            <button className="btn ghost lg" onClick={onOpenStats}>
              Stats
            </button>
          </div>
          <div className="hero-meta">
            <span className="meta-item"><Flame width={14} height={14} /> {state.streak.current}-day streak</span>
            <span className="meta-item"><Bolt width={14} height={14} /> Level {lvl.level}</span>
            <span className="meta-item"><Check width={14} height={14} /> {stats.mastered} mastered</span>
            <span className="meta-item"><Target width={14} height={14} /> {stats.dueCount} due today</span>
          </div>
        </div>
        <div className="hero-ring">
          <Ring value={stats.pct} size={190} stroke={14} label={`${stats.pct}%`} sub="course mastery" />
          <div className="hero-ring-legend">
            <span><i className="dot mastered" /> {stats.mastered} mastered</span>
            <span><i className="dot progress" /> {stats.inProgress} learning</span>
            <span><i className="dot fresh" /> {stats.notStarted} unseen</span>
          </div>
        </div>
      </section>

      <section className="stat-row">
        <div className="stat-card">
          <span className="stat-label">Daily streak</span>
          <strong className="stat-value">{state.streak.current}<small> days</small></strong>
          <span className="stat-foot">best {state.streak.best}</span>
        </div>
        <div className="stat-card accent-mint">
          <span className="stat-label">Due today</span>
          <strong className="stat-value">{stats.dueCount}<small> cards</small></strong>
          <span className="stat-foot">{stats.learning} learned total</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Reviews today</span>
          <strong className="stat-value">{todayStats.reviews + (todayStats.typingRuns || 0)}<small> drills</small></strong>
          <span className="stat-foot">{todayStats.keystrokes || 0} keystrokes</span>
        </div>
        <div className="stat-card accent-amber">
          <span className="stat-label">Experience</span>
          <strong className="stat-value">{state.xp}<small> XP</small></strong>
          <div className="xp-bar">
            <div className="xp-fill" style={{ width: `${lvl.pct}%` }} />
          </div>
          <span className="stat-foot">{lvl.nextXp - state.xp} XP to level {lvl.level + 1}</span>
        </div>
      </section>

      <section className="method-strip">
        {METHOD.map((m) => (
          <div className="method-card" key={m.n}>
            <span className="method-n">{m.n}</span>
            <div>
              <h4>{m.title}</h4>
              <p>{m.body}</p>
            </div>
          </div>
        ))}
      </section>

      <section className="weeks-section">
        <header className="section-head">
          <h2>Curriculum · 14 weekly modules</h2>
          <span className="muted small">Click a module to drill its snippets</span>
        </header>
        <div className="week-grid">
          {weeks.map((w) => {
            const s = weekStats(state, w, snippets)
            return (
              <button className="week-card" key={w.n} onClick={() => onOpenWeek(w.n)}>
                <div className="week-bar" style={{ background: w.accent }} />
                <div className="week-card-top">
                  <span className="week-n" style={{ color: w.accent }}>Week {w.n}</span>
                  <span className="week-pct">{s.pct}%</span>
                </div>
                <h3>{w.title}</h3>
                <p className="week-blurb">{w.blurb}</p>
                <div className="progress">
                  <div className="progress-fill" style={{ width: `${s.pct}%`, background: w.accent }} />
                </div>
                <div className="week-foot">
                  <span>{s.mastered}/{s.total} mastered</span>
                  {s.due > 0 ? <span className="pill due">{s.due} due</span> : <span className="muted">{s.notStarted} new</span>}
                </div>
              </button>
            )
          })}
        </div>
      </section>

      <section className="lower-grid">
        <div className="panel">
          <header className="panel-head">
            <h2>Review load · next 7 days</h2>
            <span className="muted small">SM-2 schedule</span>
          </header>
          <div className="load-chart">
            {load.map((l, i) => (
              <div className="load-col" key={l.key}>
                <div className="load-bar-wrap">
                  <div
                    className={`load-bar ${i === 0 ? 'today' : ''}`}
                    style={{ height: `${Math.max(4, (l.n / maxLoad) * 100)}%` }}
                    title={`${l.n} cards`}
                  />
                </div>
                <span className="load-n">{l.n}</span>
                <span className="load-label">{i === 0 ? 'today' : prettyDate(l.key).split(' ')[1]}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <header className="panel-head">
            <h2>Activity · last 5 weeks</h2>
            <span className="muted small">drills per day</span>
          </header>
          <div className="heatmap">
            {activity.map((a) => {
              const lvlH = a.load === 0 ? 0 : a.load < 4 ? 1 : a.load < 9 ? 2 : a.load < 15 ? 3 : 4
              return (
                <div
                  key={a.key}
                  className={`heat-cell h${lvlH}`}
                  title={`${a.key}: ${a.load} drills`}
                />
              )
            })}
          </div>
          <div className="heat-legend muted small">
            <span>less</span>
            {[0, 1, 2, 3, 4].map((h) => <i key={h} className={`heat-cell h${h}`} />)}
            <span>more</span>
          </div>
        </div>
      </section>
    </div>
  )
}
