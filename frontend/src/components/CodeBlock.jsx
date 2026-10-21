import { useMemo } from 'react'
import { tokenize } from '../lib/highlight'

export default function CodeBlock({ code, showLineNumbers = true, className = '' }) {
  const lines = useMemo(() => code.split('\n').map((l) => tokenize(l)), [code])
  return (
    <div className={`codeblock ${className}`}>
      {showLineNumbers && (
        <div className="cb-gutter" aria-hidden="true">
          {lines.map((_, i) => (
            <div key={i}>{i + 1}</div>
          ))}
        </div>
      )}
      <pre className="cb-code">
        <code>
          {lines.map((tokens, i) => (
            <div className="cb-line" key={i}>
              {tokens.length === 0 ? ' ' : tokens.map((t, j) => (
                <span key={j} className={`tok ${t.cls}`}>
                  {t.text}
                </span>
              ))}
            </div>
          ))}
        </code>
      </pre>
    </div>
  )
}
