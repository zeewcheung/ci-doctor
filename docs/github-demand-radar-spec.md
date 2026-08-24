# Post-publication GitHub demand radar specification

Status: **NOT RUN — read-only specification only**. Running the radar, opening links, contacting maintainers, or inspecting a repository requires the applicable authorization at that time.

## Goal

Find public inbound or openly solicited GitHub Actions / CI diagnosis opportunities without treating ordinary maintenance activity as paid demand. The radar records evidence; it never claims, contacts, bids, clones, runs, or changes a repository.

## Eligible public signals

- Explicit compensation language: `bounty`, `paid`, a currency amount, `contract`, or a named funded program.
- Explicit request language: `help wanted`, `seeking help`, `looking for contributor`, or a maintainer request for assistance.
- CI relevance: GitHub Actions, workflow YAML, runner, permissions, dependency installation, tests, cache, matrix, timeout, artifact, or environment failure.
- Freshness: open status plus a visible recent maintainer update or future deadline.

## Scoring

Score evidence independently; never infer missing facts.

| Signal | Points |
|---|---:|
| Explicit amount and payment mechanism | +5 |
| Explicit `paid`, `bounty`, or `contract` wording without amount | +4 |
| Maintainer explicitly requests outside help | +2 |
| Failure clearly concerns GitHub Actions / CI | +3 |
| Public reproduction or redacted error evidence is already present | +1 |
| Open with activity in the last 30 days or future deadline | +1 |
| Ordinary `help wanted` with no compensation evidence | 0 paid-evidence points |
| Compensation, authorization, or scope is ambiguous | -3 and manual review |
| Requires credentials, private access, secret handling, hosted execution, or broad redesign | exclude |

Interpretation:

- 8–12: high-fit public lead with explicit commercial evidence; still requires account-holder approval before any action.
- 5–7: potentially relevant; verify compensation and authority manually.
- 1–4: informational/open-source contribution signal, not a paid order.
- 0 or excluded: do not pursue.

An ordinary `help wanted` label is never recorded as a paid order, customer, revenue opportunity, or authorization to work.

## Required record per candidate

- Public URL and repository owner/name.
- Exact short quotation or faithful evidence summary with page date.
- Open/closed state and last visible activity date.
- Compensation amount, mechanism, and deadline, or `not stated`.
- Evidence that the poster can authorize the work, or `unverified`.
- CI category, workflow count if stated, fit score, exclusions, and risks.
- Explicit flags: `contacted=false`, `claimed=false`, `code_accessed=false`, `workflow_triggered=false`.

## Exclusions

Exclude private repositories, credential requests, security testing, production access, self-hosted runner administration, broad app development, unpaid contribution requests presented as paid demand, stale/closed items, contests requiring payment, and any item whose terms prohibit the proposed work. Do not clone, download, scan, execute, or inspect code beyond the public request text without separate account-holder approval.
