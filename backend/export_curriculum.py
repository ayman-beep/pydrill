# -*- coding: utf-8 -*-
"""
Exports the curriculum database to JSON for the static frontend build.

The Python modules stay the single source of truth; the generated file is
committed so Netlify (and `npm run build`) never needs a Python toolchain.

    python3 backend/export_curriculum.py
    # or, from frontend/:  npm run sync:data
"""
from __future__ import annotations

import json
from pathlib import Path

from curriculum_data import curriculum_payload

OUT = Path(__file__).resolve().parent.parent / "frontend" / "src" / "data" / "curriculum.json"


def main() -> None:
    payload = curriculum_payload()
    payload["generated_by"] = "backend/export_curriculum.py"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    snippets = payload["snippets"]
    notes = sum(len(s["notes"]) for s in snippets)
    print(f"wrote {OUT.relative_to(OUT.parents[3])}")
    print(f"  weeks={len(payload['weeks'])} snippets={len(snippets)} notes={notes}")
    print(f"  bytes={OUT.stat().st_size:,}")


if __name__ == "__main__":
    main()
