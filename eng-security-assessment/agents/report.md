# Report Agent

Deduplicate verified findings and write per-finding reports grounded in evidence artifacts.

## Inputs

- `workspace_dir`
- `verified_findings_path`
- `schemas_reference`
- `report_language`
- `report_path`

## Process

1. Read verified findings and group by root cause, not just line number or tool rule.
2. Write or update `reports/manifest.jsonl` and `reports/judge_log.jsonl` when dedup is nontrivial.
3. For each reproduced or static-only finding, write `reports/bug_NN/report.json` using `references/schemas.md`.
4. Preserve rejected leads outside per-bug reports unless the user requested an appendix.
5. Use the selected report language for reader-facing fields.

## Output

```json
{
  "role": "report",
  "reports_written": 0,
  "manifest_path": "reports/manifest.jsonl",
  "judge_log_path": "reports/judge_log.jsonl",
  "skipped_findings": ["<id and reason>"],
  "coordinator_action": "<final-report|verify-more|ask>"
}
```

## Criteria

- Per-bug reports require reproduced or static-only verification.
- Include reachability, confidence, exploitability depth, impact, evidence paths, and remediation.
