#!/usr/bin/env python3
"""Offline GitHub Actions failure triage for the fictional local demo.

Uses only the Python standard library. It never connects to GitHub and never
reads credentials. Reports are hypotheses based solely on supplied files.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


RULES = (
    ("yaml", re.compile(r"(invalid workflow|yaml syntax|mapping values are not allowed|could not find expected|unexpected value)", re.I)),
    ("permission", re.compile(r"(resource not accessible by integration|permission (?:to .* )?denied|permission denied|\b403\b|github_token.*permission)", re.I)),
    ("dependency", re.compile(r"(npm err!|eresolve|could not resolve dependency|no matching distribution|module not found|cannot find module|lock file.*out of date)", re.I)),
    ("test", re.compile(r"(assertionerror|assert\.strictEqual|tests? failed|expected:.*actual:|not ok \d+)", re.I)),
    ("cache", re.compile(r"(cache.*(not found|failed|corrupt|key.*512)|unable to reserve cache|failed to restore cache)", re.I)),
    ("matrix", re.compile(r"(matrix.*(invalid|undefined|not found)|unrecognized named-value: ['\"]?matrix|fail-fast.*cancel)", re.I)),
    ("timeout", re.compile(r"(timed out|timeout-minutes|operation was canceled|job.*exceeded.*time)", re.I)),
    ("artifact", re.compile(r"(no files were found with the provided path|unable to find any files for the provided path|artifact path .*does not exist|no files matched.*artifact)", re.I)),
    ("environment", re.compile(r"(command not found|not recognized as an internal|no such file or directory|unsupported platform|environment variable|env mismatch|unsupported (?:node|python)(?:\.js)? version|requires (?:node|python)(?:\.js)?|current (?:node|python)(?:\.js)? version|bad substitution|syntax error near unexpected token)", re.I)),
)

NOISE = re.compile(
    r"(##\[(group|endgroup|command|debug)\]|process completed with exit code|error: process completed|finishing:|post job cleanup|fictional synthetic benchmark)",
    re.I,
)
SIGNAL = re.compile(
    r"(assertionerror|assert\.strictEqual|npm err!|eresolve|invalid workflow|yaml|permission denied|resource not accessible|403 forbidden|cache|matrix|timed out|timeout|no files were found with the provided path|artifact path|unsupported (?:node|python)|requires (?:node|python)|command not found|not recognized as an internal|bad substitution|syntax error near unexpected token|no such file|error:|fatal:|not ok)",
    re.I,
)
EVIDENCE_SIGNAL = re.compile(
    r"(not ok|assertionerror|expected values|\bexpected:|\bactual:|npm err!|invalid workflow|permission|\b403\b|cache|matrix|timed out|no files were found with the provided path|artifact path|unsupported (?:node|python)|requires (?:node|python)|command not found|not recognized as an internal|bad substitution|syntax error near unexpected token|no such file|error:|fatal:)",
    re.I,
)

EXPLANATIONS = {
    "yaml": "Workflow parsing or schema validation failed before normal step execution.",
    "dependency": "Dependency installation or module resolution failed.",
    "test": "The test command ran and reported a product-code assertion failure.",
    "permission": "A workflow operation was rejected because the token or runner lacks required access.",
    "cache": "Cache restore/save configuration or cache contents caused the failure.",
    "matrix": "A matrix expression, combination, or failure policy caused the job failure/cancellation.",
    "timeout": "The step or job exceeded an enforced time limit or was canceled on timeout.",
    "artifact": "The artifact upload path did not match a file produced in the local workspace.",
    "environment": "The runner environment differs from what the command expects.",
    "unknown": "The supplied evidence does not match a supported category; manual review is required.",
}


@dataclass
class Diagnosis:
    category: str
    first_error: str
    line_number: int
    root_cause: str
    confidence: str
    evidence: list[str]
    limitations: list[str]
    disposition: str
    manual_review_required: bool
    matched_categories: list[str]


def clean_line(raw: str) -> str:
    line = re.sub(r"^\d{4}-\d{2}-\d{2}T[^ ]+\s+", "", raw.rstrip())
    # Downloaded job archives may prefix fields with tabs; preserve ordinary
    # spaces because they are often part of the error itself.
    if "\t" in line:
        line = line.rsplit("\t", 1)[-1]
    return line.strip()


def classify(log_text: str) -> Diagnosis:
    lines = [(idx, clean_line(raw)) for idx, raw in enumerate(log_text.splitlines(), 1)]
    meaningful = [(idx, line) for idx, line in lines if line and not NOISE.search(line)]
    candidates = [(idx, line) for idx, line in meaningful if SIGNAL.search(line)]
    first_idx, first_error = candidates[0] if candidates else (meaningful[0] if meaningful else (0, "No diagnostic line found"))

    # Classification uses a bounded window from the first signal so stack traces
    # and an immediately-following assertion can strengthen the diagnosis.
    window = "\n".join(line for idx, line in meaningful if first_idx <= idx <= first_idx + 30)
    matched = [name for name, pattern in RULES if pattern.search(window)]
    category = matched[0] if len(matched) == 1 else "unknown"
    confidence = "high" if len(matched) == 1 else "low"
    evidence = [line for idx, line in meaningful if first_idx <= idx <= first_idx + 30 and EVIDENCE_SIGNAL.search(line)][:8]
    root_cause = EXPLANATIONS[category]
    if category == "test" and "expected: 'hello'" in window and "actual: 'hello world'" in window:
        root_cause = "The workflow configures EXPECTED_GREETING as 'hello', but the application returns 'hello world'."
    return Diagnosis(
        category=category,
        first_error=first_error,
        line_number=first_idx,
        root_cause=root_cause,
        confidence=confidence,
        evidence=evidence,
        limitations=[
            "Offline heuristic analysis only; no GitHub API or private repository access was used.",
            "Validate the proposed change in an isolated branch or local copy before production use.",
        ],
        disposition="diagnose" if len(matched) == 1 else "manual_review",
        manual_review_required=len(matched) != 1,
        matched_categories=matched,
    )


def demo_patch(workflow: Path, diagnosis: Diagnosis) -> str:
    original = workflow.read_text(encoding="utf-8")
    updated = original
    rationale = "No safe deterministic patch is available for this evidence."
    if diagnosis.category == "test" and "EXPECTED_GREETING: hello" in original:
        updated = original.replace("EXPECTED_GREETING: hello", "EXPECTED_GREETING: hello world", 1)
        rationale = "Align the workflow's test expectation with the intentional application output."
    if updated == original:
        return f"# {rationale}\n"
    relative = ".github/workflows/ci.yml"
    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        updated.splitlines(keepends=True),
        fromfile=f"a/{relative}",
        tofile=f"b/{relative}",
    )
    return "".join(diff)


def render_report(d: Diagnosis, log: Path, workflow: Path, patch: Path) -> str:
    evidence = "\n".join(f"- `{item}`" for item in d.evidence) or "- No evidence line found."
    limits = "\n".join(f"- {item}" for item in d.limitations)
    return f"""# CI Doctor Root Cause Report

> FICTIONAL LOCAL DEMO — not a real customer, repository, incident, testimonial, or result.

## Executive summary

- Category: **{d.category}**
- Confidence: **{d.confidence}**
- First real error: log line {d.line_number}: `{d.first_error}`
- Root-cause hypothesis: {d.root_cause}

## Evidence

{evidence}

## Local reproduction guidance

Use a sanitized local copy with the same runtime and command shown in the supplied workflow. Do not request credentials or trigger hosted CI.

## Candidate fix

Patch: `{patch.name}`. The patch is intentionally limited to the workflow expectation used by this demo.

## Local verification

1. Reproduce the failure in an isolated local copy.
2. Apply the patch to that copy.
3. Run `./scripts/local_ci.sh` from the demo repository.
4. Record command, exit code, and test output; do not claim GitHub-hosted validation from a local run.

## Inputs reviewed

- Log: `{log.name}`
- Workflow: `{workflow.name}` (supplied sanitized copy)

## Limitations and safety

{limits}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline CI failure triage")
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--workflow", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--patch", type=Path, required=True)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    diagnosis = classify(args.log.read_text(encoding="utf-8"))
    patch_text = demo_patch(args.workflow, diagnosis)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.patch.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render_report(diagnosis, args.log, args.workflow, args.patch), encoding="utf-8")
    args.patch.write_text(patch_text, encoding="utf-8")
    if args.json:
        args.json.write_text(json.dumps(asdict(diagnosis), indent=2) + "\n", encoding="utf-8")
    print(f"category={diagnosis.category}")
    print(f"first_error_line={diagnosis.line_number}")
    print(f"report={args.report}")
    print(f"patch={args.patch}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
