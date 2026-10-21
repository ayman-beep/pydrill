import { useEffect, useMemo, useRef, useState } from 'react'
import { tokenize } from '../lib/highlight'

/**
 * Step 3 editor: no target text, no ghost, no autocomplete. Just a numbered
 * code box for writing the snippet from memory.
 */
export default function FreeEditor({ value, onChange, onSubmit, disabled, sound, onKeystroke, autoFocus = true }) {
  const taRef = useRef(null)
  const [caret, setCaret] = useState({ line: 1, col: 1 })
  const lines = useMemo(() => value.split('\n').length, [value])

  const trackCaret = (el) => {
    if (!el) return
    const upto = el.value.slice(0, el.selectionStart)
    const parts = upto.split('\n')
    setCaret({ line: parts.length, col: parts[parts.length - 1].length + 1 })
  }
  const tokens = useMemo(() => tokenize(value), [value])

  useEffect(() => {
    if (autoFocus && taRef.current) taRef.current.focus()
  }, [autoFocus])

  const prevLen = useRef(value.length)
  useEffect(() => {
    if (value.length > prevLen.current) onKeystroke && onKeystroke(value.length - prevLen.current)
    prevLen.current = value.length
  }, [value, onKeystroke])

  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault()
      const el = e.target
      const pos = el.selectionStart
      const next = value.slice(0, pos) + '    ' + value.slice(el.selectionEnd)
      onChange(next)
      requestAnimationFrame(() => {
        el.selectionStart = el.selectionEnd = pos + 4
      })
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault()
      onSubmit && onSubmit()
    }
  }

  return (
    <div className="typer free" onClick={() => taRef.current && taRef.current.focus()}>
      <div className="typer-top">
        <span className="typer-dot recall" />
        <span className="typer-file">recall.py</span>
        <span className="typer-spacer" />
        <span className="typer-stat">{lines} lines</span>
        <span className="typer-stat drill-line">Ln {caret.line}, Col {caret.col}</span>
        <span className="typer-stat muted2">solution hidden</span>
      </div>
      <div className="typer-body">
        <div className="typer-gutter" aria-hidden="true">
          {Array.from({ length: Math.max(lines, 3) }).map((_, i) => (
            <div key={i}>{i + 1}</div>
          ))}
        </div>
        <div className="typer-stage">
          <pre className="typer-ghost free-ghost" aria-hidden="true">
            <code>
              {tokens.map((t, i) => (
                <span key={i} className={`tok ${t.cls}`}>
                  {t.text}
                </span>
              ))}
              {value.length === 0 ? <span className="tok cm"># type the snippet from memory…</span> : null}
            </code>
          </pre>
          <textarea
            ref={taRef}
            className="typer-input"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            onKeyUp={(e) => trackCaret(e.target)}
            onClick={(e) => trackCaret(e.target)}
            onSelect={(e) => trackCaret(e.target)}
            spellCheck={false}
            autoCapitalize="off"
            autoCorrect="off"
            autoComplete="off"
            disabled={disabled}
            placeholder=""
            aria-label="Write the Python snippet from memory"
          />
        </div>
      </div>
      <div className="typer-hintbar">
        <span className="mono-keys">Ctrl</span>+<span className="mono-keys">Enter</span> to submit · <span className="mono-keys">Tab</span> inserts 4 spaces
        <span className="grow" />
        <span className="muted">Whitespace, blank lines and quote style are graded leniently</span>
      </div>
    </div>
  )
}
