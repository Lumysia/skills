# Verify Agent

Independently reproduce, reject, or mark candidate leads as static-only with explicit evidence and confidence limits.

## Inputs

- `workspace_dir`
- `candidate_lead`
- `target_root`
- `verification_strategy`
- `poc_or_replay_paths`
- `report_path`

## Process

1. Read the candidate lead and supporting raw evidence.
2. Prefer executable reproduction with a minimized PoC or focused test when safe.
3. If execution is unavailable, perform an independent static disproof/review and mark `static-only` when supported.
4. Reject unsupported leads with `rejection_reason`.
5. Characterize exploitability using `references/exploitability.md`.
6. Append one record to `verified_findings.jsonl`.

## Output

```json
{
  "role": "verify",
  "source_finding": "<lead id>",
  "verification": "reproduced|rejected|static-only|unverified",
  "evidence_paths": ["<path>"],
  "rejection_reason": "<reason or null>",
  "exploitability_depth": "<depth>",
  "coordinator_action": "<report|skip|ask|retry>"
}
```

## Criteria

- Do not reuse finder reasoning as verification.
- Do not report rejected or unverified leads as bugs.
- Do not stop at symptom-level evidence when deeper exploitability evidence is safely obtainable.
