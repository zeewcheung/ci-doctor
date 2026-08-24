# Fictional artifact-path root-cause report

> FICTIONAL LOCAL DEMO / SYNTHETIC ADVERSARIAL BENCHMARK — local-only evaluation, not customer data, production evidence, or a general accuracy claim.

## Executive summary

- Category: **artifact**
- Confidence: **high**
- First real error: `Error: No files were found with the provided path: build/output/*.tgz. No artifacts will be uploaded.`
- Root-cause hypothesis: the workflow glob does not match the locally produced fictional package.

## Evidence

- `Error: No files were found with the provided path: build/output/*.tgz. No artifacts will be uploaded.`

## Local reproduction guidance

Compare the workflow glob with the known synthetic file in an isolated local directory.

## Candidate fix

Change only the declared workflow path from `build/output/*.tgz` to `dist/*.tgz`.

## Local verification

The local path check changes from zero matches to one match. `github_hosted_run=false`.

## Limitations and safety

This does not validate hosted upload behavior. Account-holder QA remains pending.
