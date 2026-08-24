# CI Doctor

> **FICTIONAL LOCAL DEMO — no customer case or hosted-runner validation**

CI Doctor is a local, heuristic GitHub Actions / CI failure classifier. The free tool extracts the first actionable error and classifies common failures without connecting to GitHub or generating a patch. A separate paid human service is proposed for deeper diagnosis and bounded candidate fixes.

Every repository, incident, log, patch, report, benchmark, and result included here is a **FICTIONAL LOCAL DEMO**. There is no customer case, testimonial, production incident, validated price, revenue result, or private repository in this candidate.

## Free classifier

Supported categories are YAML, dependency/lockfile, test, permission, cache, matrix, timeout, artifact-path, and environment/runtime failures. When evidence is insufficient or contradictory, the tool returns `unknown`, requires manual review, and does not invent a cause.

Requirements: Python 3.10 or later. No package installation, account, token, or network connection is required.

```sh
python3 tools/classify_ci_failure.py \
  --log tests/fixtures/permission.log \
  --output classification.json
```

The input must be a local, sanitized text log. The command writes classification evidence only; `candidate_fix_generated` is always `false`. Delete the output when it is no longer needed.

Run the included synthetic tests:

```sh
python3 -m unittest tests.test_ci_doctor -v
```

These tests run locally and do not trigger GitHub Actions.

## What it can and cannot establish

- **No customer case:** every included example is fictional and synthetic.
- **No repair guarantee:** output is a best-effort heuristic hypothesis.
- **No GitHub-hosted runner validation:** all recorded checks are local only.
- It can identify the first likely actionable error and apply a small, documented set of heuristic categories.
- It can abstain when signals conflict or do not support a category.
- It cannot parse every workflow expression, inspect repository state, authenticate to GitHub, or validate on a GitHub-hosted runner.
- It does not provide a repair guarantee, security certification, production validation, or automatic candidate fix for user inputs.
- A local result is a hypothesis based only on the supplied sanitized text.

See the [capability and limitation statement](docs/capabilities-and-limitations.md) and [fictional sample index](docs/sample-output-index.md).

## Requesting help without sharing sensitive data

If Issues are enabled after publication, use the CI classification request form only for non-sensitive metadata: public repository URL if applicable, workflow name, runner operating system, broad category, and a short redacted error summary. Do not submit logs, workflow contents, private code, customer data, internal URLs, tokens, secrets, keys, credentials, or attachments.

Formal diagnostic materials are accepted only after a paid relationship and a separate safe-intake process have been established. Opening an Issue is not a purchase, service acceptance, quote, or promise to investigate.

## Proposed paid human services

These are customer-visible drafts and **unvalidated pilot/test prices**, not evidence of demand, sales, or revenue.

| Service | Unvalidated test price | Maximum scope | Target after accepted sanitized intake |
|---|---:|---:|---:|
| CI Triage | USD 79 | 1 workflow | 2 calendar days |
| Workflow Repair | USD 249 | 2 workflows | 5 calendar days |
| CI Hardening | USD 499 | 3 workflows | 7 calendar days |

Each draft includes one in-scope revision. Communication defaults to asynchronous writing in the Asia/Shanghai timezone. The customer applies any candidate patch. Temporary repository access, hosted-runner execution, credentials, deployment, and guaranteed outcomes are excluded. See [service packages](docs/service-packages.md).

## Signed fictional sample boundary

The account holder approved only the unchanged `artifact_upload_path` **FICTIONAL LOCAL DEMO** delivery bundle for portfolio QA. That approval does not approve another sample, service profile, customer delivery, repository publication, price, license, or external claim. The exact sample and signing evidence are indexed in [the sample output index](docs/sample-output-index.md).

## Privacy, security, and contributions

- [Privacy](PRIVACY.md)
- [Security](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [MIT License](LICENSE) and [license summary](docs/license-decision.md)

## Repository scope

This repository is an offline tool and fictional portfolio sample. It does not provide a hosted service, Marketplace action, telemetry, automatic outreach, payment flow, or permission to inspect any repository. Repository Issues, when enabled, are only the non-sensitive information channel described above.
