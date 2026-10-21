# PyDrill — Introduction to Data Science Code Trainer

A full-stack, Chessable-style **spaced-repetition move trainer** for the Python side of an *Introduction to Data Science* course. Instead of multiple-choice quizzes, every card is a real Python snippet that you must be able to **type perfectly** and then **write blind from a natural-language prompt** — exactly like drilling chess moves.

- **96 curated snippets** across **14 weekly modules** (Weeks 1–14 of the syllabus)
- **Every snippet is explained**: a plain-English paragraph, a line-by-line annotation (297 notes), and the classic mistake to avoid — visible before you type, when you reveal, and again after you pass
- **4-gate drill pipeline** per snippet: demonstrate → 3× perfect typing → hidden recall → SM-2 scheduling
- **Live character validation** with instant error reset (strict mode)
- **Progress dashboard**: per-week mastery bars, daily streak, review queue, SM-2 review-load forecast, 5-week heatmap, XP/levels
- **Audio-visual feedback**: WebAudio key clicks, error buzz, success chimes, level-up fanfare, screen shake on error, run dots
- **Responsive** down to phone width; works with mouse or keyboard only

---

## Run it

```bash
./run.sh            # API + prebuilt UI  → http://localhost:8000
./run.sh dev        # FastAPI :8000 + Vite dev server :5173 (hot reload, /api proxied)
```

Manual equivalent:

```bash
# 1. backend (serves the REST API and, if present, the built React app)
cd backend && pip install fastapi uvicorn && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

# 2. frontend, either use the prebuilt bundle in backend/static_app, or:
cd frontend && npm install && npm run dev     # http://localhost:5173
cd frontend && npm run build                  # rebuilds backend/static_app
```

No database, no accounts. Progress lives in the browser (`localStorage`, key `pydrill.progress.v1`) with export/import/reset in **Progress → Drill settings**.

---

## The drill pipeline (exactly as specified)

| Gate | What the app does | Where |
| --- | --- | --- |
| **1. Visual demonstration** | Target snippet rendered with a custom Python tokenizer (keywords, strings, numbers, builtins, comments, shell magics), plus a tab that explains it line by line and a plain-language "what this does" box. Reference panel stays pinned next to the editor. | `components/Explainer.jsx`, `lib/highlight.js` |
| **2. Muscle memory (3×)** | Ghost-text editor: the snippet is visible, your typed characters progressively dim the target. `Tab` = 4 spaces, `Enter` = newline, paste blocked. **3 consecutive error-free runs** required; run dots ①②③ light up. | `components/CodeTyper.jsx` |
| **3. Immediate error correction** | Every keystroke is compared to the expected character. A mismatch → red flash + shake + buzz, the offending character waved-underlined, the run counter **reset to 0**, and (strict mode) the buffer cleared so the sequence restarts. Error count and per-snippet accuracy are tracked. | `CodeTyper.registerError` |
| **4. Hidden recall** | Snippet disappears completely. Only the natural-language prompt (optional hint / reveal after a failed attempt) remains. Graded server-side with a whitespace- and quote-insensitive normal form, and a line-by-line diff when wrong. | `components/FreeEditor.jsx`, `POST /api/grade` |
| **5. Spaced repetition** | SM-2 style ladder **1 → 3 → 7 → 14 → 30 days**. First-attempt success advances a stage; a failed recall is a lapse: card drops to Day 1 and **forces Step 1 (3× typing)** again before the next recall. | `lib/store.js` (`recordRecall`) |

Stage → mastery weighting: unseen 0%, typing passed 30%, Day 1 45%, Day 3 60%, Day 7 75%, Day 14 90%, Day 30 100%. Weekly and course-wide progress bars are the average across their snippets.

---

## Explanations (added for every card)

Each snippet carries three layers of teaching content, authored by hand and validated at import time
(`curriculum_data.py` asserts every card has an explanation and that the note count matches the code line
count exactly, so nothing can drift out of alignment):

| Field | What it is | Where you see it |
| --- | --- | --- |
| `explain` | One paragraph: what the snippet does and why it matters in the data-science workflow | Step 1 panel, week list, and again after a passed recall |
| `notes[]` | One note per non-blank source line, paired with that exact line of code | "Explained line by line" tab (annotated code), week list |
| `gotcha` | The mistake students actually make here | "Common mistake" strip under the explanation |

Surfaced in four places:

1. **Step 1 · Read and understand** — the drill opens with the annotated snippet + explanation, so you understand
   the code *before* drilling it into muscle memory.
2. **Week list → `Explain` button** — expand any row to read its code, notes and explanation without starting a drill.
3. **Recall → `Reveal solution`** — after a failed attempt the revealed solution is annotated, not bare.
4. **After a pass** — "You wrote it — now here is what it does" re-shows the line-by-line notes to close the loop.

Inline `` `code` `` fragments inside the prose are rendered as highlighted chips by `Rich` in `Explainer.jsx`.

## Curriculum (96 snippets)

| Week | Module | Snippets |
| --- | --- | --- |
| 1 | Foundations of Data Science & Python Setup | 9 |
| 2 | Version Control & Development Ecosystem (git, Colab) | 6 |
| 3 | Data Formats, Web Scraping & REST APIs (requests, JSON, BeautifulSoup) | 8 |
| 4 | Tidy Data & Schema Structuring | 7 |
| 5 | Data Processing 1 — Pandas Foundations | 9 |
| 6 | Mid-Term Review Drills (multi-step, Weeks 1–5) | 6 |
| 7 | Data Processing 2 — GroupBy, joins, reshaping | 8 |
| 8 | EDA 1 — NumPy & descriptive statistics | 7 |
| 9 | EDA 2 — Matplotlib & Seaborn | 7 |
| 10 | Machine Learning & Linear Regression | 7 |
| 11 | Decision Trees | 6 |
| 12 | Neural Networks (Keras) | 6 |
| 13 | Capstone Review — end-to-end pipelines | 5 |
| 14 | Final Drills — comprehensive synthesis | 5 |

Each card carries `id, week, title, topic, difficulty (1–3), prompt, hint, code, explain, notes, gotcha`. Snippets are 1–10 lines so a drill stays under a minute. Content is validated at import time (unique ids, non-empty code/prompt, valid week).

---

## API

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | liveness + counts |
| `GET` | `/api/curriculum` | weeks + all 96 snippets (single payload the SPA caches) |
| `GET` | `/api/weeks` | week metadata with average difficulty and line counts |
| `GET` | `/api/snippets/{id}` | one snippet (code, prompt, hint, `explain`, `notes`, `gotcha`) + `prev_id` / `next_id` |
| `GET` | `/api/spec` | machine-readable description of the drill pipeline |
| `POST` | `/api/grade` | grades a recall (or typing) attempt, returns `passed`, `feedback`, `first_mismatch`, full line diff |

`POST /api/grade` body:

```json
{ "snippet_id": "w05-01", "typed": "import pandas as pd\n...", "mode": "recall", "retry_count": 0 }
```

Recall grading is deliberately **lenient about formatting and strict about content**: tabs→4 spaces, trailing whitespace and blank lines ignored, internal space runs collapsed, `'` vs `"` treated the same, trailing commas before `)`/`]` ignored. Everything else (names, operators, argument order, quotes' contents) must match.

---

## Project layout

```
backend/
  main.py              FastAPI app: API + grading + static SPA mount
  curriculum_data.py   14 week definitions, validation, payload assembly
  cur_a.py             Weeks 1–7 snippets
  cur_b.py             Weeks 8–14 snippets
  ex_a.py              explanations + per-line notes, weeks 1–7
  ex_b.py              explanations + per-line notes, weeks 8–14
  explanations.py      merges both into one lookup
  static_app/          prebuilt React bundle (npm run build output)
frontend/
  src/App.jsx          hash router, queue management, XP/level-up, toasts
  src/components/      Dashboard, WeekView, DrillSession, CodeTyper,
                       FreeEditor, Explainer (annotated code + prose),
                       CodeBlock, StatsView, Ring, Icons
  src/lib/store.js     localStorage persistence, SM-2 scheduler, streaks, XP
  src/lib/selectors.js per-week / overall stats, review queue, heatmap data
  src/lib/highlight.js tiny Python tokenizer + ghost-progress spans
  src/lib/sfx.js       WebAudio SFX, speech synthesis, haptics
tests/smoke.py         Playwright end-to-end walkthrough (needs a running app)
tests/screenshots.py   Seeds sample progress and captures the shots in shots/
```

## Notes on the interactive editor

The typing textarea is intentionally **uncontrolled**: at ~10 keystrokes/second a controlled React input can reconcile against a stale value and reject legitimate characters. The DOM owns the text, React mirrors only the length (drives the ghost overlay, progress bar and line indicator), and strict-mode resets write straight to `textarea.value`. That keeps validation correct while typing as fast as you can.

`tests/smoke.py` drives the whole flow with Playwright: inline explanations → 3 perfect typing runs → failing recall (diff shown) → forced typing restart → passing recall → post-pass explanation → SM-2 scheduling → dashboard/stat updates. Latest run: all assertions pass, zero console errors.
