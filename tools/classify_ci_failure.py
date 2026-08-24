#!/usr/bin/env python3
"""Classify a sanitized CI log locally without creating a candidate patch."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from ci_doctor import classify


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Offline, heuristic GitHub Actions / CI failure classification"
    )
    parser.add_argument("--log", type=Path, required=True, help="path to a sanitized text log")
    parser.add_argument("--output", type=Path, help="optional JSON output path")
    args = parser.parse_args()

    diagnosis = classify(args.log.read_text(encoding="utf-8"))
    payload = {
        "notice": "FICTIONAL LOCAL DEMO when used with included fixtures; never submit secrets or private code.",
        "tool_scope": "classification_only",
        "candidate_fix_generated": False,
        **asdict(diagnosis),
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
