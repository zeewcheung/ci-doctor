# Proposed paid human service packages

Customer-visible pilot offer. All prices and delivery targets are **unvalidated pilot/test parameters** and do not imply demand, customers, revenue, or guaranteed results. Timezone: Asia/Shanghai. Default communication: asynchronous written messages. Each profile includes one in-scope revision round.

## CI Triage — USD 79

USD 79 is a proposed pilot/test price and remains unvalidated. It is not evidence of a customer price, sale, or revenue.

For one failed GitHub Actions job in one workflow.

- Review one redacted failed-job log and relevant workflow file.
- Extract the first actionable error and classify the failure.
- Deliver a concise root-cause hypothesis, confidence, evidence, and next action.
- No repository write access, code change, hosted rerun, or guaranteed fix.
- Maximum scope: 1 workflow.
- Deliver a diagnosis report and local reproduction guidance.
- Target: 2 calendar days after sanitized intake is accepted.

## Workflow Repair — USD 249

For a locally reproducible primary failure across no more than 2 workflows.

- Everything in CI Triage, within the service's 2-workflow maximum.
- One minimal candidate fix covering the evidenced failure.
- Local before/after verification where runner behavior can be represented safely.
- Before/after commands, exit codes, limitations, and rollback note.
- Excludes application redesign, broad dependency upgrades, production deploys, secrets, and organization settings.
- Target: 5 calendar days after sanitized intake is accepted.

## CI Hardening — USD 499

For diagnosis and bounded hardening review of no more than 3 workflows.

- Diagnosis, candidate fix, local verification evidence, and prioritized risk/improvement backlog.
- Review permissions, action pinning, cache keys/scope, matrix behavior, timeouts, environment portability, concurrency, and deterministic installs.
- Prioritized hardening backlog with severity, effort, and rationale.
- One minimal candidate patch set, limited to the accepted workflows and locally testable changes.
- Excludes security certification, penetration testing, self-hosted runner administration, cloud IAM changes, and ongoing monitoring.
- Target: 7 calendar days after sanitized intake is accepted.

## Commercial guardrails

- Inputs must be authorized, minimized, and redacted before transfer.
- Initial inputs are limited to sanitized logs, a minimal reproduction, and a sanitized repository archive voluntarily supplied by the customer.
- Credentials are never accepted. The customer applies patches or uses their own approved workflow.
- Findings are best-effort engineering analysis, not a warranty of uptime, security, or compatibility.
- Scope expansion is quoted before work; ambiguous multi-root failures are not silently absorbed.
- Any public portfolio item, testimonial, or case study requires explicit written permission and accurate labeling. The fictional demo cannot be presented as a customer result.
- Delivery targets pause while required sanitized evidence or customer clarification is unavailable; they are not repair guarantees.
- Working files are deleted 7 days after delivery, or earlier on request. Only necessary activity and financial records containing no customer data are retained under the approved default policy.
- A candidate fix may modify multiple files only when they address one root cause, are confirmed workflow files within profile scope, pass local before/after verification, and receive account-holder QA approval.
- Temporary repository access is excluded and requires a separately approved future scope.
