# -*- coding: utf-8 -*-
"""
Python Drill Trainer — FastAPI backend (optional).

The app ships as a **fully static** frontend (see frontend/, deployed to
Netlify) with the curriculum bundled as JSON and grading done in the browser.
This module is kept so the same drill engine can be hosted as a real API — it
serves the curriculum, grades attempts server-side and optionally mounts a
built SPA. Both graders share backend/grading.py; the JS twin lives in
frontend/src/lib/grade.js and tests/grading_parity.py keeps them in agreement.
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from curriculum_data import COUNT_BY_WEEK, ORDER, SNIPPETS, WEEKS, curriculum_payload, week_payload
from grading import grade_attempt

BASE_DIR = Path(__file__).resolve().parent
# A static build may be mounted here for single-process hosting.
STATIC_DIR_CANDIDATES = [BASE_DIR / "static_app", BASE_DIR.parent / "frontend" / "dist"]

app = FastAPI(
    title="PyDrill — Introduction to Data Science Drill Engine",
    version="1.1.0",
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
    retry_count: int = 0          # how many previous failures on this card


# ------------------------------------------------------------------ routes
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


def _neighbour(snippet_id: str, step: int):
    ids = sorted(SNIPPET_BY_ID, key=lambda i: ORDER[i])
    idx = ids.index(snippet_id) + step
    return ids[idx] if 0 <= idx < len(ids) else None


@app.get("/api/snippets/{snippet_id}")
def snippet(snippet_id: str):
    s = SNIPPET_BY_ID.get(snippet_id)
    if s is None:
        raise HTTPException(status_code=404, detail=f"Unknown snippet '{snippet_id}'")
    return {**s, "next_id": _neighbour(snippet_id, 1), "prev_id": _neighbour(snippet_id, -1)}


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
    return grade_attempt(s, req.typed, mode=req.mode, retry_count=req.retry_count)


# ------------------------------------------------------------------ static SPA (optional)
STATIC_DIR = next((p for p in STATIC_DIR_CANDIDATES if p.is_dir()), None)

if STATIC_DIR is not None:
    if (STATIC_DIR / "assets").is_dir():
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
