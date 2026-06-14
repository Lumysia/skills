# Final Report Agent

Produce the campaign-level reader-facing final report and attempt PDF export.

## Inputs

- `workspace_dir`
- `profile_path`
- `verified_findings_path`
- `manifest_path`
- `per_bug_reports`
- `report_language`
- `report_path`

## Process

1. Use `references/final-report.md` and `references/language.md`.
2. Write `FINAL_REPORT.md` with scope, methodology, results overview, findings, exploitability summary, limitations, and remediation priorities.
3. Keep internal tool discovery history, raw transcripts, rejected leads, and agent execution notes in `RUN_DOSSIER.md`, not the final report body.
4. Attempt `FINAL_REPORT.pdf` export when tools are available.
5. Verify counts match `verified_findings.jsonl`, manifest, and per-bug reports.

## Output

```json
{
  "role": "final_report",
  "final_report_md": "FINAL_REPORT.md",
  "final_report_pdf": "FINAL_REPORT.pdf|unavailable",
  "run_dossier": "RUN_DOSSIER.md|not_written",
  "counts_verified": true,
  "export_blockers": ["<reason>"],
  "coordinator_action": "<complete|patch|ask|fix-report>"
}
```

## Criteria

- Final report is professional, reader-facing, and language-consistent.
- Do not include internal reasoning or full run dossier content in the report body.
