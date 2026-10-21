# -*- coding: utf-8 -*-
"""
Python Drill Trainer — FastAPI backend.

Serves the 14-week curriculum database, performs server-side grading for the
recall drills, and serves the built React single-page app.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from curriculum_data import COUNT_BY_WEEK, ORDER, SNIPPETS, WEEKS, curriculum_payload, week_payload

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static_app"

app = FastAPI(
    title="PyDrill — Introduction to Data Science Drill Engine",
    version="1.0.0",
    description="Chessable-style spaced repetition move trainer for Python data-science code.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

SNIPPET_BY_ID = {s["id"]: s for s in SNIPPETS}


# ------------------------------------------------------------------ models
class GradeRequest(BaseModel):
    snippet_id: str
    typed: str
    mode: str = "recall"          # "recall" | "typing"
    retry_count: int = 0           # how many previous failures on this card


# ------------------------------------------------------------------ grading
_WS = re.compile(r"[ \t]+")


def normalise(code: str) -> str:
    """Whitespace- and quote-insensitive normal form used for recall grading.

    Recall is about *knowing the code*, not pixel-perfect indentation, so:
      * tabs become four spaces, trailing whitespace is dropped,
      * blank lines are ignored,
      * every run of spaces collapses to one,
      * single quotes are treated as double quotes,
      * a trailing statement comma is ignored.
    """
    lines = []
    for raw in code.replace("\t", "    ").split("\n"):
        line = raw.rstrip()
        if not line.strip():
            continue
        line = _WS.sub(" ", line.strip())
        line = line.replace("'", '"')
        line = re.sub(r",(\s*[)\]])", r"\1", line)
        lines.append(line)
    return "\n".join(lines)


def line_diagnostics(expected: str, typed: str):
    """Per-line comparison used to drive the inline feedback panel."""
    exp = normalise(expected).split("\n") if expected.strip() else []
    got = normalise(typed).split("\n") if typed.strip() else []
    rows = []
    for i in range(max(len(exp), len(got))):
        e = exp[i] if i < len(exp) else None
        t = got[i] if i < len(got) else None
        rows.append(
            dict(
                line=i + 1,
                expected=e,
                typed=t,
                status="match" if e == t else ("missing" if t is None else ("extra" if e is None else "mismatch")),
            )
        )
    first = next((r for r in rows if r["status"] != "match"), None)
    return rows, first


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "weeks": len(WEEKS),
        "snippets": len(SNIPPETS),
        "total_chars": sum(s["chars"] for s in SNIPPETS),
    }


@app.get("/api/curriculum")
def curriculum():
    return curriculum_payload()


@app.get("/api/weeks")
def weeks():
    return [
        {
            **week_payload(w["n"]),
            "difficulty_avg": round(
                sum(s["difficulty"] for s in SNIPPETS if s["week"] == w["n"]) / COUNT_BY_WEEK[w["n"]], 2
            ),
            "lines_total": sum(s["lines"] for s in SNIPPETS if s["week"] == w["n"]),
        }
        for w in WEEKS
    ]


@app.get("/api/snippets/{snippet_id}")
def snippet(snippet_id: str):
    s = SNIPPET_BY_ID.get(snippet_id)
    if s is None:
        raise HTTPException(status_code=404, detail=f"Unknown snippet '{snippet_id}'")
    return {**s, "next_id": _neighbour(snippet_id, 1), "prev_id": _neighbour(snippet_id, -1)}


def _neighbour(snippet_id: str, step: int):
    ids = sorted(SNIPPET_BY_ID, key=lambda i: ORDER[i])
    idx = ids.index(snippet_id) + step
    return ids[idx] if 0 <= idx < len(ids) else None


@app.get("/api/spec")
def spec():
    """Machine-readable description of the drill pipeline (used by the UI)."""
    return {
        "steps": [
            {"step": 1, "name": "Visual Demonstration", "detail": "Target snippet shown with syntax highlighting."},
            {"step": 2, "name": "Muscle Memory", "detail": "Type the snippet character-for-character 3 consecutive times."},
            {"step": 3, "name": "Error Correction", "detail": "Any wrong keystroke resets the run counter to 0."},
            {"step": 4, "name": "Hidden Recall", "detail": "Snippet hidden; natural-language prompt only."},
            {"step": 5, "name": "Spaced Repetition", "detail": "SM-2 style intervals: 1, 3, 7, 14, 30 days."},
        ],
        "intervals_days": [1, 3, 7, 14, 30],
        "typing_reps_required": 3,
    }


@app.post("/api/grade")
def grade(req: GradeRequest):
    s = SNIPPET_BY_ID.get(req.snippet_id)
    if s is None:
        raise HTTPException(status_code=404, detail=f"Unknown snippet '{req.snippet_id}'")

    if req.mode == "typing":
        passed = req.typed == s["code"]
        rows, first = line_diagnostics(s["code"], req.typed)
        return dict(
            passed=passed,
            mode="typing",
            first_mismatch=first,
            lines=rows,
            expected_normalised=normalise(s["code"]),
            typed_normalised=normalise(req.typed),
        )

    # ---- hidden recall -------------------------------------------------
    exp_n = normalise(s["code"])
    got_n = normalise(req.typed)
    passed = exp_n == got_n
    rows, first = line_diagnostics(s["code"], req.typed)

    if passed:
        feedback = "Perfect recall — first attempt." if req.retry_count == 0 else "Correct after retry."
    elif not got_n:
        feedback = "Nothing submitted."
    elif first and first["status"] == "missing":
        feedback = f"Your answer is missing line {first['line']}."
    elif first and first["status"] == "extra":
        feedback = f"Line {first['line']} should not be there."
    else:
        feedback = f"First difference on line {first['line'] if first else '?'}."

    return dict(
        passed=passed,
        mode="recall",
        feedback=feedback,
        first_mismatch=first,
        lines=rows,
        expected_normalised=exp_n,
        typed_normalised=got_n,
        expected_lines=len(exp_n.split("\n")) if exp_n else 0,
        typed_lines=len(got_n.split("\n")) if got_n else 0,
        first_attempt=req.retry_count == 0,
    )


# ------------------------------------------------------------------ SPA
if STATIC_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/")
    def index():
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/{path:path}")
    def spa(path: str):
        if path.startswith("api/"):
            return JSONResponse({"detail": "Not found"}, status_code=404)
        candidate = STATIC_DIR / path
        if candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
