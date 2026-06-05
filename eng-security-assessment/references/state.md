# State and Checkpoints

This file defines self-contained state. It does not depend on any helper script,
repository layout, model provider, or agent host.

## Directories

```text
.state/
  progress.json
  phase0.json
  phase1.json
  phase2.json
  phase3.json
  phase4.json
  phase5.json
  tool_discovery.json

.tools/
  <run-id>/

results/
  <target-name>/
    <timestamp>/
      profile.json
      tool_findings.jsonl
      verified_findings.jsonl
      raw/
      logs/
      reports/
      FINAL_REPORT.md
      FINAL_REPORT.pdf
      RUN_DOSSIER.md
```

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
  "status": "running|complete|failed",
  "phase_done": 0,
  "results_root": "results/<target>/<timestamp>",
  "profile": "auto|native|web|java|go|rust|contracts|static|custom",
  "updated_at": "ISO-8601"
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
  "results_root": "results/<target>/<timestamp>",
  "execution_available": true,
  "verification_available": true,
  "notes": []
}
```

Phase 3, run:

```json
{
  "phase": 3,
  "results_root": "results/<target>/<timestamp>",
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
  "results_root": "results/<target>/<timestamp>",
  "tool_leads": 0,
  "verified_reproduced": 0,
  "verified_static_only": 0,
  "reports_written": 0,
  "final_report": "results/<target>/<timestamp>/FINAL_REPORT.md",
  "pdf_export": "results/<target>/<timestamp>/FINAL_REPORT.pdf|unavailable",
  "run_dossier": "results/<target>/<timestamp>/RUN_DOSSIER.md",
  "latest_artifact": "..."
}
```

Phase 5, summary:

```json
{
  "phase": 5,
  "status": "complete|partial|failed",
  "results_root": "results/<target>/<timestamp>",
  "next_action": "..."
}
```

## Resume

Resume by reading `progress.json` and the highest completed `phaseN.json`.

- If `status == complete`, start a new run unless the user asks to inspect old results.
- If `status == running`, continue from `phase_done + 1`.
- If role output files already exist, do not regenerate them unless `--fresh` is set.
- Provider/session resume is optional; file artifacts are sufficient.
