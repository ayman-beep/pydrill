import { Fragment, useMemo, useState } from 'react'
import { tokenize } from '../lib/highlight'
import { Bulb, Check, Warn } from './Icons'

/** Renders `backticked` fragments inside prose as inline code chips. */
export function Rich({ text }) {
  const parts = useMemo(() => String(text || '').split(/(`[^`]+`)/g), [text])
  return (
    <>
      {parts.map((p, i) =>
        p.startsWith('`') && p.endsWith('`') && p.length > 2 ? (
          <code className="inline-code" key={i}>
            {p.slice(1, -1)}
          </code>
        ) : (
          <Fragment key={i}>{p}</Fragment>
        ),
      )}
    </>
  )
}

function CodeLine({ code }) {
  const tokens = tokenize(code)
  return (
    <>
      {tokens.length === 0 ? ' ' : tokens.map((t, i) => (
        <span key={i} className={`tok ${t.cls}`}>
          {t.text}
        </span>
      ))}
    </>
  )
}

/** Code with a plain-language note beside every line. */
export function AnnotatedCode({ snippet }) {
  const { notes = [], code } = snippet
  const blankCount = code.split('\n').length - notes.length
  return (
    <div className="annot">
      {notes.map((n) => (
        <div className="annot-row" key={n.line}>
          <span className="annot-n">{n.line}</span>
          <code className="annot-code">
            <CodeLine code={n.code} />
          </code>
          <span className="annot-note">
            <Rich text={n.note} />
          </span>
        </div>
      ))}
      {blankCount > 0 && (
        <div className="annot-row annot-more">
          <span className="annot-n">·</span>
          <span className="muted small">
            plus {blankCount} blank line{blankCount === 1 ? '' : 's'} for readability
          </span>
        </div>
      )}
    </div>
  )
}

/** Paragraph explanation + the classic mistake for this snippet. */
export function ExplainBox({ snippet, showGotcha = true }) {
  return (
    <div className="explain-box">
      <div className="explain-text">
        <Rich text={snippet.explain} />
      </div>
      {showGotcha && snippet.gotcha && (
        <div className="gotcha">
          <Warn width={14} height={14} />
          <span>
            <strong>Common mistake:</strong> <Rich text={snippet.gotcha} />
          </span>
        </div>
      )}
    </div>
  )
}

/** Tabbed reference: raw highlighted code vs. line-by-line annotated code. */
export default function SnippetExplainer({ snippet, defaultTab = 'annotated', showExplain = true, accent }) {
  const [tab, setTab] = useState(defaultTab)
  return (
    <div className="explainer">
      <div className="segmented" role="tablist">
        <button
          role="tab"
          aria-selected={tab === 'code'}
          className={tab === 'code' ? 'on' : ''}
          onClick={() => setTab('code')}
        >
          Code
        </button>
        <button
          role="tab"
          aria-selected={tab === 'annotated'}
          className={tab === 'annotated' ? 'on' : ''}
          onClick={() => setTab('annotated')}
        >
          <Bulb width={13} height={13} /> Explained line by line
        </button>
        <span className="grow" />
        <span className="muted small">
          {snippet.lines} line{snippet.lines === 1 ? '' : 's'}
        </span>
      </div>

      {tab === 'code' ? (
        <div className="codeblock plain">
          <div className="cb-gutter" aria-hidden="true">
            {snippet.code.split('\n').map((_, i) => (
              <div key={i}>{i + 1}</div>
            ))}
          </div>
          <pre className="cb-code">
            <code>
              {snippet.code.split('\n').map((line, i) => (
                <div className="cb-line" key={i}>
                  <CodeLine code={line} />
                </div>
              ))}
            </code>
          </pre>
        </div>
      ) : (
        <AnnotatedCode snippet={snippet} />
      )}

      {showExplain && (
        <>
          <div className="explain-label">
            <Check width={13} height={13} /> What this snippet does
          </div>
          <ExplainBox snippet={snippet} />
        </>
      )}
    </div>
  )
}
