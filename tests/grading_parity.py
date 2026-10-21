# -*- coding: utf-8 -*-
"""
Asserts the browser grader (frontend/src/lib/grade.js) agrees with the Python
grader (backend/grading.py) on a battery of tricky inputs.

    python3 tests/grading_parity.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from curriculum_data import SNIPPETS  # noqa: E402
from grading import grade_attempt  # noqa: E402

CASES = [
    ("w01-01", 'name = "Ada"\nage = 28\nprint(name, age)', 0),
    ("w01-01", "name = 'Ada'\nage = 28\nprint(name, age)", 0),          # quote style
    ("w01-01", '   name = "Ada"  \n\n   age = 28\nprint(name, age)   ', 0),  # indentation/blanks
    ("w01-01", 'name = "Ada"\tage = 28\nprint(name, age)', 0),           # tab instead of newline -> still differs
    ("w01-01", 'name = "Ada"\nage = 18\nprint(name, age)', 2),          # wrong value
    ("w01-01", 'name = "Ada"', 1),                                       # truncated
    ("w01-01", 'name = "Ada"\nage = 28\nprint(name, age)\nextra()', 0),  # extra line
    ("w01-01", "", 0),                                                   # empty
    ("w01-06", 'score = 82\nif score >= 90:\n    grade = "A"\nelif score >= 80:\n    grade = "B"\nelse:\n    grade = "C"\nprint(grade)', 0),
    ("w01-06", 'score = 82\nif score >= 90:\n  grade = "A"\nelif score >= 80:\n  grade = "B"\nelse:\n  grade = "C"\nprint(grade)', 0),  # 2-space indent
    ("w06-06", 'df = pd.read_csv(\n    "data.csv",\n    usecols=["city", "temp"],\n    dtype={"temp": float}\n)', 0),  # trailing comma dropped
    ("w05-06", 'hot = df[(df["temp"] > 30) & (df["city"] == "KL")]', 0),
    ("w10-05", "from sklearn.metrics import mean_squared_error, r2_score\n\nprint(r2_score(y_test, predictions))", 0),
]

NODE = r"""
const { gradeAttempt } = require('./frontend/src/lib/grade.js');
const fs = require('fs');
const payload = JSON.parse(fs.readFileSync('frontend/src/data/curriculum.json', 'utf8'));
const byId = Object.fromEntries(payload.snippets.map(s => [s.id, s]));
const cases = JSON.parse(fs.readFileSync('/tmp/parity_cases.json', 'utf8'));
const out = cases.map(c => gradeAttempt(byId[c.id], c.typed, { mode: 'recall', retryCount: c.retryCount }));
process.stdout.write(JSON.stringify(out));
"""


def run_js(cases):
    payload = [{"id": i, "typed": t, "retryCount": r} for i, t, r in cases]
    Path("/tmp/parity_cases.json").write_text(json.dumps(payload))
    # transpile the ESM module for node's CommonJS require
    src = (ROOT / "frontend/src/lib/grade.js").read_text()
    src = src.replace("export function ", "function ").replace("const WS =", "const WS =")
    src += "\nmodule.exports = { normalise, lineDiagnostics, gradeAttempt };\n"
    tmp = ROOT / "frontend/src/lib/__grade_cjs.cjs"
    tmp.write_text(src)
    try:
        out = subprocess.run(
            ["node", "-e", NODE.replace("grade.js", "__grade_cjs.cjs")],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
    finally:
        tmp.unlink(missing_ok=True)
    return json.loads(out.stdout)


def main():
    by_id = {s["id"]: s for s in SNIPPETS}
    py = [grade_attempt(by_id[i], t, readonly := "recall", retry_count=r) for i, t, r in CASES]
    js = run_js(CASES)

    failures = 0
    for (sid, typed, retry), p, j in zip(CASES, py, js):
        keys = ["passed", "feedback", "first_mismatch"]
        diffs = [k for k in keys if p.get(k) != j.get(k)]
        if diffs:
            failures += 1
            print(f"MISMATCH {sid} retry={retry} keys={diffs}")
            for k in diffs:
                print(f"   python: {p.get(k)!r}")
                print(f"   js    : {j.get(k)!r}")
        else:
            print(f"ok  {sid:8s} passed={p['passed']!s:5s} retry={retry}  {str(p['feedback'])[:52]}")

    print()
    print(f"{len(CASES) - failures}/{len(CASES)} cases agree between Python and JS graders")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
