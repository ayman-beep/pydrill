// Browser-side grading engine — a faithful port of the FastAPI `/api/grade`
// logic, so the app runs with no server at all (Netlify static hosting).
//
// Recall grading is deliberately lenient about formatting and strict about
// content: tabs -> 4 spaces, trailing whitespace and blank lines ignored,
// space runs collapsed, single quotes treated as double quotes, and a trailing
// commas at end of line or before a closing bracket ignored. Everything else must match.

const WS = /[ \t]+/g

/** Whitespace- and quote-insensitive normal form used for recall grading. */
export function normalise(code) {
  const lines = []
  for (const raw of String(code ?? '').replace(/\t/g, '    ').split('\n')) {
    let line = raw.replace(/\s+$/, '')
    if (!line.trim()) continue
    line = line.trim().replace(WS, ' ')
    line = line.replace(/'/g, '"')
    line = line.replace(/,\s*$/, '')
    line = line.replace(/,(\s*[)\]])/g, '$1')
    lines.push(line)
  }
  return lines.join('\n')
}

/** Per-line comparison used to drive the inline feedback panel. */
export function lineDiagnostics(expected, typed) {
  const expN = normalise(expected)
  const gotN = normalise(typed)
  const exp = expN ? expN.split('\n') : []
  const got = gotN ? gotN.split('\n') : []
  const rows = []
  for (let i = 0; i < Math.max(exp.length, got.length); i += 1) {
    const e = i < exp.length ? exp[i] : null
    const t = i < got.length ? got[i] : null
    rows.push({
      line: i + 1,
      expected: e,
      typed: t,
      status: e === t ? 'match' : t === null ? 'missing' : e === null ? 'extra' : 'mismatch',
    })
  }
  const first = rows.find((r) => r.status !== 'match') || null
  return { rows, first }
}

/** Grades one attempt. Mirrors POST /api/grade (mode: "recall" | "typing"). */
export function gradeAttempt(snippet, typed, { mode = 'recall', retryCount = 0 } = {}) {
  if (!snippet) throw new Error('Unknown snippet')

  if (mode === 'typing') {
    const passed = typed === snippet.code
    const { rows, first } = lineDiagnostics(snippet.code, typed)
    return {
      passed,
      mode: 'typing',
      first_mismatch: first,
      lines: rows,
      expected_normalised: normalise(snippet.code),
      typed_normalised: normalise(typed),
    }
  }

  const expN = normalise(snippet.code)
  const gotN = normalise(typed)
  const passed = expN === gotN
  const { rows, first } = lineDiagnostics(snippet.code, typed)

  let feedback
  if (passed) {
    feedback = retryCount === 0 ? 'Perfect recall — first attempt.' : 'Correct after retry.'
  } else if (!gotN) {
    feedback = 'Nothing submitted.'
  } else if (first && first.status === 'missing') {
    feedback = `Your answer is missing line ${first.line}.`
  } else if (first && first.status === 'extra') {
    feedback = `Line ${first.line} should not be there.`
  } else {
    feedback = `First difference on line ${first ? first.line : '?'}.`
  }

  return {
    passed,
    mode: 'recall',
    feedback,
    first_mismatch: first,
    lines: rows,
    expected_normalised: expN,
    typed_normalised: gotN,
    expected_lines: expN ? expN.split('\n').length : 0,
    typed_lines: gotN ? gotN.split('\n').length : 0,
    first_attempt: retryCount === 0,
  }
}
