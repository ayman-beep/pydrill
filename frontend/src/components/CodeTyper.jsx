import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { progressSpans } from '../lib/highlight'
import { sfx } from '../lib/sfx'

/**
 * Step 1/2 editor: the target snippet is visible (ghost text) and the user must
 * retype it character-for-character. Any deviation is flagged instantly and, in
 * strict mode (default), clears the whole run so the counter drops back to 0.
 *
 * The textarea is intentionally *uncontrolled*: fast typing must never race
 * React's value reconciliation, so the DOM owns the text and we mirror the
 * length into state for the ghost overlay.
 */
export default function CodeTyper({
  code,
  strict = true,
  sound = true,
  disabled = false,
  onPerfectRun,
  onError,
  onKeystroke,
  resetSignal = 0,
}) {
  const [typedCount, setTypedCount] = useState(0)
  const [errorAt, setErrorAt] = useState(null)
  const [flash, setFlash] = useState(false)
  const [perfect, setPerfect] = useState(false)
  const [errors, setErrors] = useState(0)
  const taRef = useRef(null)
  const startedAt = useRef(null)
  const timers = useRef([])

  const lines = useMemo(() => code.split('\n'), [code])
  const spans = useMemo(() => progressSpans(code, typedCount, errorAt), [code, typedCount, errorAt])
  const currentLine = useMemo(() => code.slice(0, typedCount).split('\n').length, [code, typedCount])

  const clearTimers = () => {
    timers.current.forEach(clearTimeout)
    timers.current = []
  }

  const focus = useCallback(() => {
    if (!disabled && taRef.current) taRef.current.focus()
  }, [disabled])

  const hardReset = useCallback(() => {
    if (taRef.current) taRef.current.value = ''
    setTypedCount(0)
    setErrorAt(null)
    setPerfect(false)
    setErrors(0)
    startedAt.current = null
  }, [])

  useEffect(() => {
    hardReset()
    focus()
    return clearTimers
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [code, resetSignal])

  const longestPrefix = (typed) => {
    let i = 0
    while (i < typed.length && i < code.length && typed[i] === code[i]) i += 1
    return i
  }

  const registerError = (el, typed, badIndex) => {
    setErrors((e) => e + 1)
    setErrorAt(badIndex)
    setFlash(true)
    if (sound) sfx.error()
    onError && onError({ index: badIndex, expected: code[badIndex] ?? '', got: typed[badIndex] ?? '' })
    timers.current.push(setTimeout(() => setFlash(false), 380))
    timers.current.push(setTimeout(() => setErrorAt(null), 1000))
    // Strict mode: the whole run is invalidated -> the sequence starts over.
    if (strict) {
      el.value = ''
      setTypedCount(0)
    } else {
      const keep = longestPrefix(typed)
      el.value = typed.slice(0, keep)
      setTypedCount(keep)
      el.setSelectionRange(keep, keep)
    }
  }

  const handleInput = (e) => {
    if (disabled) return
    const el = e.target
    const next = el.value
    if (!startedAt.current) startedAt.current = Date.now()

    if (!code.startsWith(next)) {
      registerError(el, next, longestPrefix(next))
      return
    }

    const added = next.length - typedCount
    if (added > 0) {
      onKeystroke && onKeystroke(added)
      if (sound) sfx.key()
    }
    setTypedCount(next.length)
    setErrorAt(null)

    if (next === code) {
      setPerfect(true)
      if (sound) sfx.runComplete()
      onPerfectRun && onPerfectRun({ durationMs: startedAt.current ? Date.now() - startedAt.current : null })
      el.value = ''
      setTypedCount(0)
      startedAt.current = null
      timers.current.push(setTimeout(() => setPerfect(false), 700))
    }
  }

  const handleKeyDown = (e) => {
    if (disabled) return
    if (e.key === 'Tab') {
      e.preventDefault()
      const el = e.target
      const pos = el.selectionStart
      const candidate = el.value.slice(0, pos) + '    ' + el.value.slice(el.selectionEnd)
      if (code.startsWith(candidate)) {
        el.setRangeText('    ', pos, el.selectionEnd, 'end')
        setTypedCount(el.value.length)
        onKeystroke && onKeystroke(4)
        if (sound) sfx.key()
      } else {
        registerError(el, candidate, longestPrefix(candidate))
      }
    }
  }

  const handlePaste = (e) => {
    e.preventDefault()
    setFlash(true)
    timers.current.push(setTimeout(() => setFlash(false), 380))
  }

  const pct = Math.round((typedCount / Math.max(1, code.length)) * 100)

  return (
    <div
      className={`typer ${flash ? 'typer-error' : ''} ${perfect ? 'typer-perfect' : ''} ${disabled ? 'is-disabled' : ''}`}
      onClick={focus}
    >
      <div className="typer-top">
        <span className="typer-dot" />
        <span className="typer-file">snippet.py</span>
        <span className="typer-spacer" />
        <span className="typer-stat">
          {typedCount}/{code.length} chars
        </span>
        <span className="typer-stat err">✕ {errors}</span>
        <div className="typer-mini">
          <div className="typer-mini-fill" style={{ width: `${pct}%` }} />
        </div>
      </div>

      <div className="typer-body">
        <div className="typer-gutter" aria-hidden="true">
          {lines.map((_, i) => (
            <div key={i} className={i + 1 === currentLine ? 'gutter-active' : ''}>
              {i + 1}
            </div>
          ))}
        </div>
        <div className="typer-stage">
          <pre className="typer-ghost" aria-hidden="true">
            <code>
              {spans.map((s, i) => (
                <span key={i} className={s.cls}>
                  {s.text}
                </span>
              ))}
            </code>
          </pre>
          <textarea
            ref={taRef}
            className="typer-input"
            defaultValue=""
            onInput={handleInput}
            onKeyDown={handleKeyDown}
            onPaste={handlePaste}
            spellCheck={false}
            autoCapitalize="off"
            autoCorrect="off"
            autoComplete="off"
            disabled={disabled}
            aria-label="Type the target Python snippet"
          />
        </div>
      </div>
      <div className="typer-hintbar">
        <span className="mono-keys">Tab</span> inserts 4 spaces · <span className="mono-keys">Enter</span> newline · pasting is disabled
        <span className="grow" />
        <span className={flash ? 'warn-strong' : 'muted'}>{flash ? 'Mismatch — run reset to 0' : 'Live validation on'}</span>
      </div>
    </div>
  )
}
