// Extremely small Python tokenizer used for syntax highlighting. It is not a
// parser — it only needs to colour the curated snippets consistently.
const KEYWORDS = new Set([
  'import', 'from', 'as', 'def', 'return', 'if', 'elif', 'else', 'for', 'in', 'while',
  'break', 'continue', 'and', 'or', 'not', 'None', 'True', 'False', 'lambda', 'class',
  'try', 'except', 'finally', 'with', 'pass', 'raise', 'global', 'nonlocal', 'is', 'del',
  'yield', 'assert', 'async', 'await',
])

const BUILTINS = new Set([
  'print', 'len', 'sum', 'range', 'type', 'list', 'dict', 'set', 'tuple', 'float', 'int',
  'str', 'open', 'max', 'min', 'abs', 'round', 'sorted', 'enumerate', 'zip', 'len', 'bool',
  'map', 'filter', 'any', 'all', 'isinstance', 'getattr', 'setattr', 'input', 'super',
])

const RE = new RegExp(
  [
    '(#[^\\n]*)',                                  // 1 comment
    '("""[\\s\\S]*?"""|\'\'\'[\\s\\S]*?\'\'\')',   // 2 triple string
    '("(?:\\\\.|[^"\\\\])*"|\'(?:\\\\.|[^\'\\\\])*\')', // 3 string
    '\\b(\\d+\\.?\\d*)\\b',                        // 4 number
    '([A-Za-z_][A-Za-z0-9_]*)',                    // 5 identifier
    '([+\\-*/%<>=!&|^~]+)',                        // 6 operator
    '([()\\[\\]{},.:;])',                          // 7 punctuation
  ].join('|'),
  'g',
)

const CLS = { 1: 'cm', 2: 'st', 3: 'st', 4: 'nu', 6: 'op', 7: 'pu' }

/** Returns [{text, cls, start}] covering the whole string. */
export function tokenize(code) {
  const out = []
  let last = 0
  let m
  RE.lastIndex = 0
  while ((m = RE.exec(code)) !== null) {
    if (m.index > last) out.push({ text: code.slice(last, m.index), cls: 'pl', start: last })
    const group = [1, 2, 3, 4, 5, 6, 7].find((g) => m[g] !== undefined)
    const text = m[0]
    let cls
    if (group === 5) {
      if (KEYWORDS.has(text)) cls = 'kw'
      else if (BUILTINS.has(text)) cls = 'bi'
      else {
        const after = code.slice(m.index + text.length, m.index + text.length + 1)
        cls = after === '(' ? 'fn' : 'id'
      }
    } else if (group === 1 && text.startsWith('!')) {
      cls = 'sh'
    } else {
      cls = CLS[group] || 'pl'
    }
    out.push({ text, cls, start: m.index })
    last = m.index + text.length
  }
  if (last < code.length) out.push({ text: code.slice(last), cls: 'pl', start: last })
  return out
}

/** Flattens token spans against a "typed" character count. */
export function progressSpans(code, typedCount, errorAt = null) {
  const tokens = tokenize(code)
  const spans = []
  let offset = 0
  for (const tok of tokens) {
    const start = offset
    const end = start + tok.text.length
    offset = end
    if (end <= typedCount) {
      spans.push({ text: tok.text, cls: `tok ${tok.cls} done` })
    } else if (start >= typedCount) {
      spans.push({ text: tok.text, cls: `tok ${tok.cls}` })
    } else {
      const cut = typedCount - start
      spans.push({ text: tok.text.slice(0, cut), cls: `tok ${tok.cls} done` })
      spans.push({ text: tok.text.slice(cut), cls: `tok ${tok.cls}` })
    }
  }
  // split out a single caret / error character
  const idx = errorAt === null ? typedCount : errorAt
  if (idx >= 0 && idx < code.length) {
    const rebuilt = []
    let pos = 0
    for (const s of spans) {
      const sEnd = pos + s.text.length
      if (idx >= pos && idx < sEnd) {
        const cut = idx - pos
        if (cut > 0) rebuilt.push({ text: s.text.slice(0, cut), cls: s.cls })
        rebuilt.push({
          text: code[idx],
          cls: `${s.cls} ${errorAt === null ? 'caret' : 'bad'}`,
        })
        if (cut + 1 < s.text.length) rebuilt.push({ text: s.text.slice(cut + 1), cls: s.cls })
      } else {
        rebuilt.push(s)
      }
      pos = sEnd
    }
    return rebuilt
  }
  return spans
}
