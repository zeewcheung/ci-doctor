# Free classifier capabilities and limitations

Included examples are FICTIONAL LOCAL DEMO material.

## Capability

`tools/classify_ci_failure.py` reads one already-sanitized local text log, extracts the first likely actionable error, and assigns one of nine heuristic categories: YAML, dependency, test, permission, cache, matrix, timeout, artifact, or environment. It reports confidence, evidence lines, matched categories, and whether manual review is required.

When evidence is missing or supports multiple categories, it returns `unknown` with `manual_review_required: true`. The free command never creates or applies a patch.

## Limitations

- Rules are regular-expression heuristics, not a YAML parser, Actions expression evaluator, dependency resolver, or hosted runner.
- Output quality depends on the completeness and correctness of the sanitized input.
- The first matching error can be downstream of an earlier event omitted from the log.
- A category is not proof of root cause, and synthetic fixture results are not a real-world accuracy measurement.
- The tool has no network, GitHub API, repository, credential, telemetry, deployment, or production capability.
- No result is a repair, security, uptime, compatibility, or hosted-runner guarantee.

Use the result as a triage aid. Confirm any change in a controlled local copy and in the repository owner's own authorized environment.
