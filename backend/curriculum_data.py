# -*- coding: utf-8 -*-
"""Assembles and validates the 14-week curriculum database."""
from cur_a import SNIPPETS_A
from cur_b import SNIPPETS_B
from explanations import EXPLANATIONS

WEEKS = [
    dict(
        n=1,
        title="Foundations of Data Science & Python Setup",
        blurb="Variables, data types, collections, control flow and your first functions.",
        accent="#7c9cf5",
    ),
    dict(
        n=2,
        title="Version Control & Development Ecosystem",
        blurb="Git terminal commands and the Google Colab execution environment.",
        accent="#f0a05a",
    ),
    dict(
        n=3,
        title="Data Formats, Web Scraping & REST APIs",
        blurb="requests, JSON serialisation, BeautifulSoup parsing and caching results.",
        accent="#5fd0b0",
    ),
    dict(
        n=4,
        title="Tidy Data & Schema Structuring",
        blurb="Lists of dicts, columnar stores, sets, comprehensions and sorting rows.",
        accent="#c58cf0",
    ),
    dict(
        n=5,
        title="Data Processing 1 — Pandas Foundations",
        blurb="read_csv, inspection, filtering, missing values and index access.",
        accent="#e5708f",
    ),
    dict(
        n=6,
        title="Mid-Term Review Drills",
        blurb="Aggregated drills mixing Weeks 1-5 into short multi-step pipelines.",
        accent="#e8c65a",
    ),
    dict(
        n=7,
        title="Data Processing 2 — Grouping, Joining, Reshaping",
        blurb="groupby, merge, concat, derived columns and pivot tables.",
        accent="#6fb6e8",
    ),
    dict(
        n=8,
        title="Exploratory Data Analysis 1 — NumPy & Statistics",
        blurb="Arrays, vectorised maths, boolean masks and descriptive statistics.",
        accent="#8ee06f",
    ),
    dict(
        n=9,
        title="Exploratory Data Analysis 2 — Visualisation",
        blurb="Matplotlib and Seaborn charts, correlation matrices and saved figures.",
        accent="#f28fb7",
    ),
    dict(
        n=10,
        title="Machine Learning & Linear Regression",
        blurb="Train/test splits, fitting, predicting, scaling and R-squared.",
        accent="#9d8cf5",
    ),
    dict(
        n=11,
        title="Decision Trees",
        blurb="Classification and regression trees, tree plots, importance, CV.",
        accent="#5fd6a0",
    ),
    dict(
        n=12,
        title="Neural Networks",
        blurb="Keras Sequential architecture, compilation, training and evaluation.",
        accent="#f5a35f",
    ),
    dict(
        n=13,
        title="Capstone Review",
        blurb="End-to-end data pipelines from raw source to evaluated model.",
        accent="#e06f6f",
    ),
    dict(
        n=14,
        title="Final Drills",
        blurb="Comprehensive synthesis of the whole course, ready for the exam.",
        accent="#7fd9e8",
    ),
]

SNIPPETS = SNIPPETS_A + SNIPPETS_B

# ---------------------------------------------------------------- validation
_ids = set()
for _s in SNIPPETS:
    assert _s["id"] not in _ids, f"duplicate snippet id {_s['id']}"
    _ids.add(_s["id"])
    assert _s["code"].strip(), f"{_s['id']} has empty code"
    assert _s["prompt"].strip(), f"{_s['id']} has empty prompt"
    assert 1 <= _s["week"] <= 14, f"{_s['id']} bad week"
    _s.setdefault("hint", "")
    _s["lines"] = len(_s["code"].split("\n"))
    _s["chars"] = len(_s["code"])

    # ---- explanation content is mandatory: every card must teach, not just drill
    _ex = EXPLANATIONS.get(_s["id"])
    assert _ex is not None, f"{_s['id']} has no explanation entry"
    _explain, _notes = _ex["explain"].strip(), list(_ex["notes"])
    assert _explain, f"{_s['id']} has an empty explanation"
    assert len(_notes) == _s["lines"], (
        f"{_s['id']}: {len(_notes)} notes for {_s['lines']} code lines"
    )
    _s["explain"] = _explain
    _s["gotcha"] = _ex.get("gotcha", "").strip()
    _s["notes"] = [
        dict(line=i, code=line, note=note.strip())
        for i, (line, note) in enumerate(zip(_s["code"].split("\n"), _notes), start=1)
        if line.strip()  # blank lines carry no note in the UI
    ]
    assert len(_s["notes"]) == len([l for l in _s["code"].split("\n") if l.strip()]), _s["id"]

WEEK_BY_N = {w["n"]: w for w in WEEKS}
for _s in SNIPPETS:
    assert _s["week"] in WEEK_BY_N, f"{_s['id']} references unknown week"

COUNT_BY_WEEK = {w["n"]: len([s for s in SNIPPETS if s["week"] == w["n"]]) for w in WEEKS}
ORDER = {s["id"]: i for i, s in enumerate(SNIPPETS)}


def week_payload(n):
    w = WEEK_BY_N[n]
    return dict(
        n=w["n"],
        title=w["title"],
        blurb=w["blurb"],
        accent=w["accent"],
        count=COUNT_BY_WEEK[n],
        snippet_ids=[s["id"] for s in SNIPPETS if s["week"] == n],
    )


def curriculum_payload():
    return dict(
        course="Introduction to Data Science",
        weeks=[week_payload(w["n"]) for w in WEEKS],
        snippets=SNIPPETS,
        total_snippets=len(SNIPPETS),
    )
