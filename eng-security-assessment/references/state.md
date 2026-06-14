# State and Checkpoints

This file defines self-contained state. It does not depend on any helper script,
repository layout, model provider, or agent host.

## Directories

```text
security-assessment-workspace/
  README.md
  state/
    progress.json
    phase0.json
    phase1.json
    phase2.json
    phase3.json
    phase4.json
    phase5.json
    tool_discovery.json
  results/<target-name>/<timestamp>/
    README.md
    plan.md
    status.json
    inputs/
    artifacts/
    agents/
    logs/
    raw/
    pocs/
    reviews/
    reports/
    checkpoints/
    profile.json
    tool_findings.jsonl
    verified_findings.jsonl
    FINAL_REPORT.md
    FINAL_REPORT.pdf
    RUN_DOSSIER.md
  tools/<run-id>/
```

`security-assessment-workspace/results/<target>/<timestamp>/status.json` is the run source of truth. `security-assessment-workspace/state/` mirrors the latest run for quick resume. Legacy top-level `.state/`, `.tools/`, and `results/` may be read for migration/resume compatibility but should not receive new artifacts unless the user explicitly chooses that layout.

## Atomic Write Protocol

When the host has no checkpoint helper, write state with this protocol:

```text
1. Write JSON to <path>.tmp.
2. Validate that it parses as JSON.
3. Rename/replace <path>.tmp to <path>.
4. Never append partial JSON objects.
```

If the host has an atomic write helper, it may use it, but the JSON files above
remain the source of truth.

## `progress.json`

```json
{
  "status": "running|complete|partial|failed|blocked",
  "phase_done": 0,
  "workspace_root": "security-assessment-workspace",
  "results_root": "security-assessment-workspace/results/<target>/<timestamp>",
  "profile": "auto|native|web|java|go|rust|contracts|static|custom",
  "updated_at": "ISO-8601"
}
```

## `status.json`

Located at `security-assessment-workspace/results/<target>/<timestamp>/status.json`:

```json
{
  "skill": "eng-security-assessment",
  "run_id": "<target>-<timestamp>",
  "target": {
    "name": "<target>",
    "root": "<path or url>",
    "authorization_scope": "<scope>"
  },
  "state": {
    "phase": "intake|profile_tools|preflight|find_verify|reports|final_report|patch|handoff",
    "status": "not_started|in_progress|blocked|partial|complete|failed",
    "profile": "auto|native|web|java|go|rust|contracts|static|custom",
    "updated_at": "ISO-8601",
    "coordinator_action": "<specific follow-up action>"
  },
  "artifacts": {
    "profile": "profile.json",
    "tool_findings": "tool_findings.jsonl",
    "verified_findings": "verified_findings.jsonl",
    "final_report_md": "FINAL_REPORT.md",
    "final_report_pdf": "FINAL_REPORT.pdf|unavailable",
    "checkpoints": ["checkpoints/<phase>.json"]
  },
  "quality_gates": {
    "authorization_confirmed": "pass|fail|blocked|not_run",
    "profile_selected": "pass|fail|not_run",
    "tool_discovery_recorded": "pass|fail|not_run|limited",
    "verification_separated": "pass|fail|not_run",
    "reports_evidence_backed": "pass|fail|not_run",
    "final_report_exported": "pass|fail|blocked|not_run"
  },
  "blockers": ["<blocker>"],
  "open_risks": ["<risk>"]
}
```

## Phases

Phase 0, init:

```json
{
  "phase": 0,
  "mode": "run|resume|status|report|patch|customize|discover-tools",
  "target_or_results": "...",
  "args": {}
}
```

Phase 1, profile/tool discovery:

```json
{
  "phase": 1,
  "profile": "native|web|java|go|rust|contracts|static|custom",
  "target_shape": "...",
  "detection_oracle": "...",
  "selected_tools": [],
  "verification_strategy": "...",
  "delegation_mode": "subagents|separate-model-calls|scripts|single-agent-fallback",
  "fallback_reason": "..."
}
```

Phase 2, preflight:

```json
{
  "phase": 2,
  "target_name": "...",
  "target_root": "...",
  "workspace_dir": "security-assessment-workspace/results/<target>/<timestamp>",
  "execution_available": true,
  "verification_available": true,
  "notes": []
}
```

Phase 3, run:

```json
{
  "phase": 3,
  "workspace_dir": "security-assessment-workspace/results/<target>/<timestamp>",
  "commands_or_actions": [],
  "log_paths": [],
  "roles_dispatched": ["recon", "tool-discovery", "find", "verify"],
  "roles_run_sequentially": [],
  "status": "running|complete|partial|failed"
}
```

Phase 4, monitor/report:

```json
{
  "phase": 4,
  "workspace_dir": "security-assessment-workspace/results/<target>/<timestamp>",
  "tool_leads": 0,
  "verified_reproduced": 0,
  "verified_static_only": 0,
  "reports_written": 0,
  "final_report": "security-assessment-workspace/results/<target>/<timestamp>/FINAL_REPORT.md",
  "pdf_export": "security-assessment-workspace/results/<target>/<timestamp>/FINAL_REPORT.pdf|unavailable",
  "run_dossier": "security-assessment-workspace/results/<target>/<timestamp>/RUN_DOSSIER.md",
  "latest_artifact": "..."
}
```

Phase 5, summary:

```json
{
  "phase": 5,
  "status": "complete|partial|failed",
  "workspace_dir": "security-assessment-workspace/results/<target>/<timestamp>",
  "coordinator_action": "..."
}
```

## Resume

Resume by reading `status.json`, `security-assessment-workspace/state/progress.json`, and the highest completed checkpoint or `phaseN.json`.

- If run status is `complete`, start a new run unless the user asks to inspect old results.
- If run status is `running`, `partial`, or `blocked`, continue from the first incomplete phase after resolving blockers.
- If role output files already exist, do not regenerate them unless `--fresh` is set.
- Provider/session resume is optional; file artifacts are sufficient.
