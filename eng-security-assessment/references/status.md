# Status

Status mode is read-only over state and result artifacts.

## Locate Run

Use, in order:

- explicit results directory.
- `security-assessment-workspace/results/<target>/<timestamp>/status.json` when present.
- `security-assessment-workspace/state/progress.json` `results_root`.
- newest `security-assessment-workspace/results/<target>/<timestamp>/` matching the target.

A valid results directory may contain:

```text
profile.json
tool_findings.jsonl
verified_findings.jsonl
reports/manifest.jsonl
reports/judge_log.jsonl
reports/bug_NN/report.json
reports/bug_NN/patch_result.json
logs/
raw/
pocs/
```

## Count Findings

- `tool_findings.jsonl`: leads only.
- `verified_findings.jsonl`: reproduced, rejected, static-only, or unverified outcomes.
- `reports/bug_NN/report.json`: reportable bugs.
- `patch_result.json`: patch attempts and verification status.

Count separately:

```text
leads
reproduced findings
static-only findings
rejected leads
reports written
patches verified
patches unverified/rejected
```

## Read Reports

Use the profile-neutral fields in `schemas.md`:

- `bug_id`.
- `profile`.
- `status`.
- `finding_id`.
- `signature.dedup_key`.
- `verdict.severity_rating`.
- `verdict.confidence`.
- `verdict.verification`.
- `verdict.reachability_verdict`.
- `report`.
- `evidence_paths`.

## Stuck or Partial Runs

Check:

- latest phase in `security-assessment-workspace/state/progress.json`.
- modification times of `logs/`, `raw/`, and result JSONL files.
- whether a role output exists but later phases are missing.
- whether findings are all unverified because a verifier is unavailable.

If no files have changed and no process/log evidence suggests activity, report
the run as partial and suggest resume or inspect logs.

## Response Shape

```text
Status: running|complete|partial|failed
Profile: <profile>
Results: <results_root>
Leads: <n>
Verified: <reproduced n>, <static-only n>, <rejected n>
Reports: <n>
Patches: <verified n>/<attempted n>
Newest: <path>
Coordinator action: <resume|verify leads|report|patch|inspect logs|no action>
```
