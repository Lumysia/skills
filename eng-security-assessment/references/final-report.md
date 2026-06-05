# Final Report and Export

The workflow must produce both per-finding reports and a campaign-level final
report. Per-finding reports explain individual bugs; the final report explains
what was tested, how, what was found, how trustworthy the findings are, and what
to do next.

Follow `language.md` for report language. The final report, per-finding report
summaries, PDF, and HTML exports must use the user-requested language unless the
user asks for bilingual output.

Section headings and methodology labels must also follow the selected language.
Technical terms may remain in English only when they are canonical tool names,
acronyms, code identifiers, or intentionally defined in a terminology table.

## Canonical Outputs

Always write:

```text
results/<target>/<ts>/FINAL_REPORT.md
results/<target>/<ts>/FINAL_REPORT.pdf
```

Optional internal artifact:

```text
results/<target>/<ts>/RUN_DOSSIER.md
```

`FINAL_REPORT.md` and `FINAL_REPORT.pdf` are the required reader-facing outputs.
`RUN_DOSSIER.md` is optional internal run provenance and must not be merged into
the final report body.

## Final Report Structure

`FINAL_REPORT.md` should contain:

```text
# Security Assessment Final Report

## Executive Summary
Brief result, top risks, reproduced vs static-only count.

## Scope
Target, commit/version/environment, assumptions, authorization boundary.

## Methodology
Concise assessment approach, profiles used, test/replay/fuzz/static verification strategy. Do not list every tool discovery step in the main body.

## Results Overview
Counts: leads, reproduced findings, static-only findings, rejected leads,
reports, patches.

## Top Findings
Table with bug id, title, severity, verification, exploitability depth, report path.

## Detailed Findings
Short summary for each `reports/bug_NN/report.json`; link to full per-bug report.

## Exploitability Summary
Attacker control, primitives, escalation paths, constraints, mitigations, blast radius.

## Limitations
What could not be tested, missing runtime capabilities, static-only areas, flaky repros.

## Recommended Next Steps
Fix order, verification commands, additional testing, monitoring, hardening.

## Evidence References
Short list of evidence artifacts needed to support the findings. Keep this concise.
```

## Professional Report Rules

The final report should read like a professional security assessment, not an
agent execution log.

Main body should include:

- Executive summary and business/security risk.
- Scope, target/version/environment, and authorization assumptions.
- Concise methodology and verification standard.
- Findings table ordered by severity and confidence.
- Per-finding summaries with impact, exploitability, affected component,
  reproduction summary, and remediation.
- Limitations and areas not tested.
- Recommended next steps.

Main body should not include by default:

- Full tool search history.
- Every tool considered but not used.
- Raw scanner logs.
- Long command transcripts.
- Internal agent reasoning.
- Rejected leads unless requested as an appendix.
- Full artifact index.
- Tool provenance tables.

Put those in `RUN_DOSSIER.*`, not in `FINAL_REPORT.*`.

## Internal Run Dossier

Write internal provenance separately:

```text
results/<target>/<ts>/RUN_DOSSIER.md
```

The dossier may include:

- tool discovery history.
- tools considered but not used.
- exact versions, source URLs, install locations.
- raw scanner logs and command transcripts.
- rejected leads.
- full artifact index.
- internal role/agent execution notes.
- environment limitations and failed tool attempts.

Do not import dossier sections into the final report unless the user explicitly
asks for an appendix version.

## PDF Export

Export `FINAL_REPORT.md` to `FINAL_REPORT.pdf`. If PDF export is unavailable,
keep `FINAL_REPORT.md` and state the reason in the final response.

Acceptable approaches:

- Markdown -> HTML -> PDF.
- Markdown -> PDF via a document converter.
- Programmatic PDF generation from report content.
- Host-provided PDF/document tool.

PDF export rules:

- Preserve headings, tables, code blocks, and artifact paths.
- Include generation timestamp and target/profile metadata.
- Do not omit exploitability depth or limitations.
- Do not export `RUN_DOSSIER.*` as part of `FINAL_REPORT.pdf`.
- If attachments are not embedded, list only concise evidence references.
- If export fails, keep Markdown and report the export failure reason.

## Final Report Inputs

Use these artifacts:

- `profile.json`.
- `.state/tool_discovery.json`.
- `tool_findings.jsonl`.
- `verified_findings.jsonl`.
- `reports/manifest.jsonl`.
- `reports/judge_log.jsonl`.
- `reports/bug_NN/report.json`.
- `reports/bug_NN/patch_result.json` when present.
- `raw/`, `logs/`, and `pocs/` indexes.

Use tool discovery artifacts to support methodology and reproducibility, but put
the detailed record in `RUN_DOSSIER.*`, not the main report body.

## Quality Gate

Before finalizing:

- Verify counts match source files.
- Separate reproduced from static-only findings.
- Do not include rejected leads as findings.
- Include exploitability depth for every reported bug, or explain why unknown.
- Include limitations and missing coverage.
- Include next steps that are actionable.
- Keep internal provenance separate from reader-facing findings.
- Confirm no `RUN_DOSSIER` content was copied into `FINAL_REPORT` except concise
  methodology/evidence references.
