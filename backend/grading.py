# -*- coding: utf-8 -*-
"""
Recall grading for the drill trainer.

Kept free of FastAPI imports so it can be unit-tested, and mirrored 1:1 by
frontend/src/lib/grade.js for the static (Netlify) build. `tests/grading_parity.py`
asserts both implementations agree.
"""
from __future__ import annotations

import re

_WS = re.compile(r"[ \t]+")


def normalise(code: str) -> str:
    """Whitespace- and quote-insensitive normal form used for recall grading.

    Recall is about *knowing the code*, not pixel-perfect indentation, so:
      * tabs become four spaces, trailing whitespace is dropped,
      * blank lines are ignored,
      * every run of spaces collapses to one,
      * single quotes are treated as double quotes,
      * trailing commas (end of line or before a closing bracket) are ignored.
    """
    lines = []
    for raw in code.replace("\t", "    ").split("\n"):
        line = raw.rstrip()
        if not line.strip():
            continue
        line = _WS.sub(" ", line.strip())
        line = line.replace("'", '"')
        line = re.sub(r",\s*$", "", line)
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


def grade_attempt(snippet: dict, typed: str, mode: str = "recall", retry_count: int = 0) -> dict:
    """Grades one attempt; mirrors gradeAttempt() in frontend/src/lib/grade.js."""
    if mode == "typing":
        passed = typed == snippet["code"]
        rows, first = line_diagnostics(snippet["code"], typed)
        return dict(
            passed=passed,
            mode="typing",
            first_mismatch=first,
            lines=rows,
            expected_normalised=normalise(snippet["code"]),
            typed_normalised=normalise(typed),
        )

    exp_n = normalise(snippet["code"])
    got_n = normalise(typed)
    passed = exp_n == got_n
    rows, first = line_diagnostics(snippet["code"], typed)

    if passed:
        feedback = "Perfect recall \u2014 first attempt." if retry_count == 0 else "Correct after retry."
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
        first_attempt=retry_count == 0,
    )
