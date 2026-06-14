# General Artifact Schemas

Use these schemas for all profiles.

## `profile.json`

```json
{
  "profile": "web|java|go|rust|contracts|static|custom",
  "target_name": "...",
  "target_root": "...",
  "target_shape": "...",
  "attack_surface": ["..."],
  "detection_oracle": "...",
  "verification_strategy": "...",
  "tool_discovery": "security-assessment-workspace/state/tool_discovery.json"
}
```

## `tool_findings.jsonl`

One JSON object per lead:

```json
{
  "id": "tool-f001",
  "tool": "...",
  "profile": "...",
  "category": "...",
  "severity": "UNKNOWN|LOW|MEDIUM|HIGH|CRITICAL",
  "confidence": "LOW|MEDIUM|HIGH",
  "file": "...",
  "line": 0,
  "entrypoint": "...",
  "evidence": "...",
  "raw_output_path": "security-assessment-workspace/results/<target>/<ts>/raw/...",
  "poc": "...",
  "dedup_key": "...",
  "verification": "unverified"
}
```

## `verified_findings.jsonl`

One JSON object per verified, rejected, or static-only finding:

```json
{
  "id": "vf001",
  "source_finding": "tool-f001|manual-f001",
  "profile": "...",
  "category": "...",
  "severity": "LOW|MEDIUM|HIGH|CRITICAL|UNKNOWN",
  "confidence": "LOW|MEDIUM|HIGH",
  "verification": "reproduced|rejected|static-only",
  "affected_component": "...",
  "entrypoint": "...",
  "file": "...",
  "line": 0,
  "poc_type": "http-sequence|file|test|transaction|source-witness|other",
  "poc": "...",
  "reproduction_command": "...",
  "verifier_environment": "...",
  "evidence": "...",
  "exploitability": {
    "depth": "crash-only|offset-known|state-control|pc-control|write-primitive|code-exec-feasible|code-exec-demonstrated|not-applicable|unknown",
    "attacker_control": "...",
    "reachability": "...",
    "offsets": {},
    "controlled_state": {},
    "primitive": "...",
    "escalation_path": "...",
    "mitigations": [],
    "rop_shellcode_feasibility": "not-applicable|not-assessed|blocked|feasible|demonstrated",
    "constraints": "...",
    "reliability": "...",
    "blast_radius": "...",
    "profile_specific": {}
  },
  "raw_evidence_paths": ["security-assessment-workspace/results/<target>/<ts>/raw/..."],
  "rejection_reason": "...",
  "constraints": "...",
  "dedup_key": "...",
  "created_at": "ISO-8601"
}
```

Rules:

- `rejection_reason` is required when `verification == "rejected"`.
- `reproduction_command` is required when `verification == "reproduced"` and a command exists.
- Static-only findings must not be counted as execution-verified.

## `reports/manifest.jsonl`

For general profiles, use semantic dedup keys:

```json
{
  "bug_id": 0,
  "finding_id": "vf001",
  "profile": "web",
  "dedup_key": "endpoint:param:vuln-type",
  "category": "IDOR",
  "severity": "HIGH"
}
```

## `reports/judge_log.jsonl`

```json
{
  "finding_id": "vf001",
  "judgment": "NEW|DUP_BETTER|DUP_SKIP",
  "bug_id": 0,
  "reasoning": "..."
}
```

## `reports/bug_NN/report.json`

Profile-neutral report shape:

```json
{
  "bug_id": 0,
  "profile": "web",
  "status": "report_submitted|no_report|agent_failed",
  "finding_id": "vf001",
  "signature": {
    "dedup_key": "...",
    "category": "...",
    "entrypoint": "..."
  },
  "title": "...",
  "summary": "...",
  "affected_assets": ["..."],
  "affected_versions": ["..."],
  "weakness_ids": ["CWE-..."],
  "severity_rationale": "...",
  "verdict": {
    "severity_rating": "LOW|MEDIUM|HIGH|CRITICAL|NOT-A-BUG|UNKNOWN",
    "confidence": "LOW|MEDIUM|HIGH",
    "verification": "reproduced|static-only",
    "reachability_verdict": "REACHABLE|HARNESS_ONLY|UNCLEAR",
    "novelty_status": "FIXED|UNFIXED|UNKNOWN|NOT_CHECKED",
    "total_score": 0.0
  },
  "exploitability": {
    "depth": "...",
    "attacker_control": "...",
    "reachability": "...",
    "controlled_state": {},
    "primitive": "...",
    "escalation_path": "...",
    "mitigations": [],
    "rop_shellcode_feasibility": "...",
    "constraints": "...",
    "reliability": "...",
    "blast_radius": "...",
    "profile_specific": {}
  },
  "report": "evidence-grounded report text",
  "reproduction": {
    "preconditions": "...",
    "steps": ["..."],
    "expected_result": "...",
    "observed_result": "...",
    "safe_poc": "..."
  },
  "impact": "...",
  "remediation": {
    "recommendation": "...",
    "validation_steps": ["..."],
    "patch_status": "not-attempted|candidate|verified|unverified"
  },
  "references": ["..."],
  "poc": "...",
  "evidence_paths": ["..."]
}
```

## Patch Artifacts

If a general profile can patch and verify, use the same paths:

```text
reports/bug_NN/patch.diff
reports/bug_NN/patch_result.json
```

General `patch_result.json`:

```json
{
  "status": "patch_verified|patch_rejected|no_diff|unverified",
  "verification_command": "...",
  "tests_pass": true,
  "poc_stops": true,
  "evidence": "...",
  "human_review_required": true
}
```

## Final User-Facing Outputs

The final user-facing outputs are Markdown and PDF only:

```text
FINAL_REPORT.md
FINAL_REPORT.pdf
```

Do not require `FINAL_REPORT.json` or `FINAL_REPORT.html` unless the user asks
for them. Internal state remains in the JSON/JSONL artifacts above.

Optional internal dossier:

```text
RUN_DOSSIER.md
```
