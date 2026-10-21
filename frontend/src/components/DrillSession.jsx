import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import SnippetExplainer from './Explainer'
import CodeTyper from './CodeTyper'
import FreeEditor from './FreeEditor'
import { api } from '../lib/api'
import { INTERVALS, STAGE_LABEL, intervalForStage } from '../lib/store'
import { addDays, dayKey, prettyDate } from '../lib/dates'
import { haptic, sfx, speak } from '../lib/sfx'
import { Bulb, Check, Clock, Speaker } from './Icons'

const STEPS = [
  { n: 1, label: 'Demonstrate' },
  { n: 2, label: 'Muscle memory' },
  { n: 3, label: 'Hidden recall' },
  { n: 4, label: 'Schedule' },
]

function Stepper({ phase, runs }) {
  const active = phase === 'typing' ? (runs > 0 ? 2 : 1) : phase === 'recall' ? 3 : 4
  return (
    <div className="stepper">
      {STEPS.map((s) => (
        <div key={s.n} className={`step ${active === s.n ? 'on' : ''} ${active > s.n ? 'done' : ''}`}>
          <span className="step-n">{active > s.n ? '✓' : s.n}</span>
          <span className="step-label">{s.label}</span>
        </div>
      ))}
      <div className="stepper-line" style={{ width: `${((active - 1) / 3) * 100}%` }} />
    </div>
  )
}

export default function DrillSession({
  snippet,
  week,
  card,
  settings,
  queueInfo,
  onTypingRun,
  onRecall,
  onKeystroke,
  onExit,
  onNext,
  hasNext,
  onPrev,
  hasPrev,
  pushToast,
}) {
  const needsTyping = card.stage === 0 || card.needsTyping
  const [phase, setPhase] = useState(needsTyping ? 'typing' : 'recall')
  const [runs, setRuns] = useState(0)
  const [resetSignal, setResetSignal] = useState(0)
  const [recallText, setRecallText] = useState('')
  const [attempts, setAttempts] = useState(0)
  const [result, setResult] = useState(null)
  const [grading, setGrading] = useState(false)
  const [showHint, setShowHint] = useState(false)
  const [revealed, setRevealed] = useState(false)
  const [errors, setErrors] = useState(0)
  const [runTimes, setRunTimes] = useState([])
  const [banner, setBanner] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const startedAt = useRef(Date.now())
  const [elapsed, setElapsed] = useState(0)
  const timers = useRef([])

  useEffect(() => {
    const t = setInterval(() => setElapsed(Math.round((Date.now() - startedAt.current) / 1000)), 1000)
    return () => clearInterval(t)
  }, [])

  useEffect(() => () => timers.current.forEach(clearTimeout), [])

  // reset everything when the snippet changes
  useEffect(() => {
    const c = card
    setPhase(c.stage === 0 || c.needsTyping ? 'typing' : 'recall')
    setRuns(0)
    setResetSignal((s) => s + 1)
    setRecallText('')
    setAttempts(0)
    setResult(null)
    setShowHint(false)
    setRevealed(false)
    setErrors(0)
    setRunTimes([])
    setBanner(null)
    startedAt.current = Date.now()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [snippet.id])

  useEffect(() => {
    if (settings.tts) speak(snippet.prompt, true)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [snippet.id, settings.tts])

  const flashBanner = useCallback(
    (text, kind = 'ok') => {
      setBanner({ text, kind, key: Date.now() })
      timers.current.push(setTimeout(() => setBanner(null), 2200))
    },
    [],
  )

  const handlePerfectRun = ({ durationMs }) => {
    const nextRuns = runs + 1
    setRuns(nextRuns)
    setRunTimes((t) => [...t, durationMs])
    onTypingRun()
    haptic(14)
    if (nextRuns < 3) {
      flashBanner(`Run ${nextRuns}/3 perfect — ${3 - nextRuns} to go`, 'ok')
    } else {
      if (settings.sound) sfx.typingMastered()
      flashBanner('Step 1 & 2 complete · 3 error-free runs. Recall unlocked.', 'great')
      timers.current.push(
        setTimeout(() => {
          setPhase('recall')
          setResetSignal((s) => s + 1)
        }, 650),
      )
    }
  }

  const handleError = () => {
    setErrors((e) => e + 1)
    setRuns(0)
    haptic(30)
  }

  const handleSubmit = async () => {
    if (!recallText.trim() || submitting) return
    setSubmitting(true)
    setResult(null)
    try {
      const res = await api.grade({
        snippet_id: snippet.id,
        typed: recallText,
        mode: 'recall',
        retry_count: attempts,
      })
      setResult(res)
      if (res.passed) {
        if (settings.sound) sfx.recallPass()
        haptic(20)
        onRecall({ passed: true, firstAttempt: attempts === 0 })
        pushToast?.({ kind: 'great', text: `Recall passed · +${attempts === 0 ? 40 : 18} XP` })
      } else {
        if (settings.sound) sfx.recallFail()
        haptic(40)
        setAttempts((a) => a + 1)
        onRecall({ passed: false, firstAttempt: attempts === 0 })
        pushToast?.({ kind: 'bad', text: 'Recall failed — card dropped to Day 1' })
      }
    } catch (e) {
      flashBanner(e.message || 'Grading failed', 'bad')
    } finally {
      setSubmitting(false)
    }
  }

  const restartTyping = () => {
    setPhase('typing')
    setRuns(0)
    setResetSignal((s) => s + 1)
    setResult(null)
    setRecallText('')
  }

  const nextDue = useMemo(() => {
    const stage = Math.max(2, Math.min(6, card.stage + 1))
    const days = intervalForStage(stage)
    return { stage, days, date: prettyDate(dayKey(addDays(new Date(), days))) }
  }, [card.stage])

  const accuracy = useMemo(() => {
    const typed = runs * snippet.chars
    if (!typed) return 100
    return Math.max(0, Math.round((typed / (typed + errors)) * 100))
  }, [runs, errors, snippet.chars])

  return (
    <div className="drill">
      <div className="drill-head">
        <div className="drill-head-left">
          <button className="btn ghost small" onClick={onExit}>
            ← Exit drill
          </button>
          <div className="drill-title">
            <div className="crumb" style={{ color: week.accent }}>
              Week {week.n} · {week.title}
            </div>
            <h1>
              {snippet.title} <span className="pill topic">{snippet.topic}</span>
            </h1>
          </div>
        </div>
        <div className="drill-head-right">
          {queueInfo && (
            <span className="pill">
              {queueInfo.index + 1} / {queueInfo.total} in queue
            </span>
          )}
          <span className="pill"><Clock width={12} height={12} /> {Math.floor(elapsed / 60)}:{String(elapsed % 60).padStart(2, '0')}</span>
          <span className="pill">{'★'.repeat(snippet.difficulty)}{'☆'.repeat(3 - snippet.difficulty)}</span>
          <button className="btn ghost small" onClick={onPrev} disabled={!hasPrev}>←</button>
          <button className="btn ghost small" onClick={onNext} disabled={!hasNext}>→</button>
        </div>
      </div>

      <Stepper phase={phase} runs={runs} />

      {banner && (
        <div key={banner.key} className={`banner ${banner.kind}`}>
          {banner.text}
        </div>
      )}

      {phase === 'typing' && (
        <div className="typing-grid">
          <section className="panel reference">
            <header className="panel-head">
              <h2>Step 1 · Read and understand</h2>
              <span className="muted small">{snippet.chars} chars</span>
            </header>
            <SnippetExplainer snippet={snippet} />
            <div className="panel-foot">
              <div className="run-dots">
                {[0, 1, 2].map((i) => (
                  <span key={i} className={`run-dot ${i < runs ? 'filled' : ''}`}>
                    {i < runs ? '✓' : i + 1}
                  </span>
                ))}
              </div>
              <span className="muted small">
                {runs}/3 consecutive error-free runs · accuracy {accuracy}% · {errors} mistake{errors === 1 ? '' : 's'}
              </span>
            </div>
          </section>

          <section className="panel">
            <header className="panel-head">
              <h2>
                Step 2 · Type it exactly <span className="badge-live">live validation</span>
              </h2>
              <span className="muted small">3 consecutive perfect runs to pass</span>
            </header>
            <CodeTyper
              code={snippet.code}
              strict={settings.strict}
              sound={settings.sound}
              resetSignal={resetSignal}
              onPerfectRun={handlePerfectRun}
              onError={handleError}
              onKeystroke={onKeystroke}
            />
            <div className="panel-foot wrap">
              <span className="muted small">
                {settings.strict
                  ? 'Strict mode: a single wrong keystroke resets the run counter to 0.'
                  : 'Lenient mode: wrong keystrokes are highlighted but your progress is kept.'}
              </span>
              <span className="grow" />
              <button
                className="btn ghost small"
                onClick={() => {
                  setRuns(0)
                  setErrors(0)
                  setResetSignal((s) => s + 1)
                  flashBanner('Attempt sequence reset', 'warn')
                }}
              >
                Reset sequence
              </button>
            </div>
          </section>
        </div>
      )}

      {phase === 'recall' && (
        <div className="recall-grid">
          <section className="panel prompt-panel">
            <header className="panel-head">
              <h2>Step 3 · Hidden recall</h2>
              <span className="pill">{STAGE_LABEL[card.stage] || 'Review'}</span>
            </header>
            <p className="prompt-text">{snippet.prompt}</p>
            <div className="prompt-actions">
              <button className="btn ghost small" onClick={() => speak(snippet.prompt, true)}>
                <Speaker width={14} height={14} /> Read prompt
              </button>
              <button className="btn ghost small" onClick={() => setShowHint((h) => !h)}>
                {showHint ? 'Hide hint' : 'Show hint'}
              </button>
              {attempts > 0 && !revealed && (
                <button className="btn ghost small danger" onClick={() => setRevealed(true)}>
                  Reveal solution
                </button>
              )}
            </div>
            {showHint && <div className="hint-box"><Bulb width={14} height={14} /> {snippet.hint}</div>}
            {revealed && (
              <div className="reveal-box">
                <div className="muted small">Solution, explained</div>
                <SnippetExplainer snippet={snippet} />
              </div>
            )}
            <div className="meta-grid">
              <div><span className="muted small">Lines</span><strong>{snippet.lines}</strong></div>
              <div><span className="muted small">Difficulty</span><strong>{'★'.repeat(snippet.difficulty)}</strong></div>
              <div><span className="muted small">Attempts</span><strong>{attempts + (result?.passed ? 1 : 0)}</strong></div>
              <div><span className="muted small">Lapses</span><strong>{card.lapses}</strong></div>
            </div>
            <div className="interval-ladder">
              <div className="muted small">Spaced repetition ladder</div>
              <div className="ladder">
                {INTERVALS.map((d, i) => (
                  <span
                    key={d}
                    className={`ladder-step ${card.stage - 2 >= i ? 'reached' : ''} ${card.stage - 2 === i ? 'current' : ''}`}
                  >
                    {d}d
                  </span>
                ))}
              </div>
            </div>
          </section>

          <section className="panel">
            <header className="panel-head">
              <h2>Write the code from memory</h2>
              <span className="muted small">no hints · no ghost text</span>
            </header>
            <FreeEditor
              value={recallText}
              onChange={setRecallText}
              onSubmit={handleSubmit}
              disabled={submitting || result?.passed}
              sound={settings.sound}
              onKeystroke={onKeystroke}
              autoFocus
            />
            <div className="panel-foot wrap">
              <button
                className="btn primary"
                onClick={handleSubmit}
                disabled={submitting || !recallText.trim() || result?.passed}
              >
                {submitting ? 'Grading…' : result?.passed ? 'Passed ✓' : 'Submit recall'}
              </button>
              <button className="btn ghost" onClick={() => setRecallText('')} disabled={!recallText}>
                Clear
              </button>
              <span className="grow" />
              {attempts > 0 && !result?.passed && (
                <button className="btn warn" onClick={restartTyping}>
                  Restart Step 1 (3× typing)
                </button>
              )}
            </div>
          </section>
        </div>
      )}

      {result && (
        <div className={`result ${result.passed ? 'pass' : 'fail'}`}>
          <div className="result-head">
            <span className="result-icon">{result.passed ? '✓' : '✕'}</span>
            <div>
              <h3>{result.passed ? 'Recall passed' : 'Recall failed'}</h3>
              <p className="muted">
                {result.passed
                  ? `Advanced to ${STAGE_LABEL[nextDue.stage]} — next review in ${nextDue.days} day${nextDue.days === 1 ? '' : 's'} (${nextDue.date}).`
                  : `${result.feedback || 'Differences found.'} The card is back at Day 1 and Step 1 must be repeated.`}
              </p>
            </div>
            <span className="grow" />
            {result.passed ? (
              <button className="btn primary" onClick={hasNext ? onNext : onExit}>
                {hasNext ? 'Next snippet →' : 'Finish session'}
              </button>
            ) : (
              <button className="btn warn" onClick={restartTyping}>
                Repeat 3× typing drill
              </button>
            )}
          </div>
          {result.passed && (
            <div className="result-explain">
              <div className="explain-label">
                <Check width={13} height={13} /> You wrote it — now here is what it does
              </div>
              <SnippetExplainer snippet={snippet} defaultTab="annotated" />
            </div>
          )}
          {!result.passed && result.lines && (
            <div className="diff">
              {result.lines.map((l) => (
                <div key={l.line} className={`diff-row ${l.status}`}>
                  <span className="diff-n">{l.line}</span>
                  <span className="diff-expected">{l.expected ?? '·'}</span>
                  <span className="diff-typed">{l.typed ?? '·'}</span>
                  <span className="diff-status">
                    {l.status === 'match' ? 'match' : l.status === 'missing' ? 'missing' : l.status === 'extra' ? 'extra' : 'mismatch'}
                  </span>
                </div>
              ))}
              <div className="diff-legend muted small">
                <span>#</span> line · <span>expected</span> · <span>yours</span>
              </div>
            </div>
          )}
        </div>
      )}

      <div className="drill-foot muted small">
        Step 1 visual demonstration → Step 2 3× error-free typing → Step 3 hidden recall → Step 4 SM-2 scheduling.
        {errors > 0 && ` This snippet cost you ${errors} reset${errors === 1 ? '' : 's'}.`}
      </div>
    </div>
  )
}
