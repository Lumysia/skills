# Assignment Deliverable Schemas

This document defines reusable JSON structures for resumable assignment workspaces, checkpoints, worker summaries, and final handoff reports.

---

## status.json

Machine-readable assignment state. Located at `<assignment-name>-workspace/status.json`.

```json
{
  "skill": "edu-assignment-deliverable",
  "workspace": "<assignment-name>-workspace",
  "assignment": {
    "name": "<short name>",
    "prompt_sources": ["<paths or inline-source labels>"],
    "rubric_sources": ["<paths or inline-source labels>"],
    "required_format": "<format>",
    "submission_constraints": ["<constraint>"],
    "final_deliverable": "<path or null>"
  },
  "state": {
    "phase": "intake|workspace|checklist|inspection|deliverable_work|validation|rubric_review|humanization|handoff",
    "status": "not_started|in_progress|blocked|complete_but_unverified|ready|complete",
    "readiness": "partial|complete_but_unverified|ready|blocked",
    "last_updated": "<ISO-8601 timestamp>",
    "next_action": "<specific next action>"
  },
  "dependencies": {
    "hard_missing": ["<missing item>"],
    "soft_missing": ["<missing item>"],
    "provisioning_blockers": ["<blocker>"]
  },
  "artifacts": {
    "checklist": "artifacts/rubric-checklist.md",
    "drafts": ["<paths>"],
    "validation_evidence": ["<paths>"],
    "reviews": ["<paths>"],
    "reports": ["<paths>"],
    "checkpoints": ["<paths>"]
  },
  "quality_gates": {
    "deliverable_exists": "pass|fail|not_run",
    "format_verified": "pass|fail|not_run",
    "checklist_satisfied": "pass|fail|not_run",
    "deliverable_work": "pass|fail|not_run|blocked",
    "validation_attempted": "pass|fail|not_run|blocked",
    "deliverable_check": "pass|fail|not_run",
    "rubric_review": "pass|fail|not_run",
    "no_blockers_or_majors": "pass|fail|not_run"
  },
  "open_risks": [
    {
      "severity": "blocker|major|minor|note",
      "source": "<review|checklist|user>",
      "description": "<risk>",
      "owner": "agent|user|external"
    }
  ]
}
```

**Fields:**
- `skill`: Skill name matching frontmatter.
- `workspace`: Runtime workspace path or name.
- `assignment`: Source and submission metadata.
- `state`: Current phase, readiness, timestamp, and next action.
- `dependencies`: Missing hard/soft inputs and provisioning blockers.
- `artifacts`: Key files created or referenced during the run.
- `quality_gates`: Latest status of readiness gates.
- `open_risks`: Remaining risks with severity and owner.

---

## checkpoint.json

Phase completion or resume snapshot. Located under `<assignment-name>-workspace/checkpoints/`.

```json
{
  "checkpoint_id": "phase-<n>-<slug>",
  "timestamp": "<ISO-8601 timestamp>",
  "phase": "<phase name>",
  "result": "completed|blocked|failed|superseded",
  "inputs_inspected": ["<paths or labels>"],
  "artifacts_created": ["<paths>"],
  "artifacts_modified": ["<paths>"],
  "worker_reports": ["<paths>"],
  "commands_run": [
    {
      "command": "<command>",
      "purpose": "<why it was run>",
      "result": "pass|fail|blocked"
    }
  ],
  "decisions": ["<decision or assumption>"],
  "blockers": ["<blocker>"],
  "next_action": "<specific next action>"
}
```

**Fields:**
- `checkpoint_id`: Stable phase or timestamp identifier.
- `phase`: Phase covered by this snapshot.
- `result`: Whether the phase completed, blocked, failed, or was superseded.
- `inputs_inspected`: Inputs read during the phase.
- `artifacts_created` / `artifacts_modified`: Files produced or changed.
- `worker_reports`: Review or worker outputs produced during the phase.
- `commands_run`: Commands or validation actions with purpose and result.
- `decisions`: Assumptions, user decisions, and merge decisions.
- `blockers`: Remaining blockers at checkpoint time.
- `next_action`: First action for a fresh session to take.

---

## rubric-checklist item

Checklist item for `artifacts/rubric-checklist.md`. Use JSON, tables, or Markdown bullets as long as these fields remain visible.

```json
{
  "id": "R1",
  "source_type": "prompt|rubric|template|submission_rule|user|source_material",
  "source_ref": "<path/page/section/line/user-message label>",
  "requirement_quote": "<raw quoted requirement text>",
  "priority": "blocker|major|minor|note",
  "evidence": "<file, section, output, command, or review evidence>",
  "verification": "manual_review|command|render|export|test|calculation|file_inspection|source_trace",
  "status": "not_started|in_progress|satisfied|blocked|waived|risk_accepted",
  "notes": "<optional notes>"
}
```

**Fields:**
- `id`: Stable checklist identifier used in reviews.
- `source_type`: Requirement source type.
- `source_ref`: Primary-source path, page, section, line, cell, or explicit user-message label. Do not cite coordinator summaries or plans here.
- `requirement_quote`: Raw quoted assignment expectation from the primary source. Do not rewrite, explain, interpret, combine, or normalize it.
- `priority`: Submission impact severity.
- `evidence`: Where completion can be verified.
- `verification`: Verification method.
- `status`: Current completion status.
- `notes`: Optional assumptions, citations, or links.

---

## worker-report.json

Summary shape for worker reports. Full reports may be Markdown, but include these fields when possible.

```json
{
  "worker_role": "deliverable_work|deliverable_check|environment_setup|rubric_review|humanization",
  "report_path": "<path>",
  "started_at": "<ISO-8601 timestamp>",
  "completed_at": "<ISO-8601 timestamp>",
  "classification": "partial|complete_but_unverified|ready|blocked|not_applicable",
  "blockers": ["<blocker>"],
  "major_findings": ["<finding>"],
  "commands_run": ["<command>"],
  "artifacts_produced": ["<paths>"],
  "next_action": "<specific next action>"
}
```

**Fields:**
- `worker_role`: Role that produced the report.
- `report_path`: Saved report location.
- `classification`: Readiness or applicability classification.
- `blockers`: Issues that prevent progress or readiness.
- `major_findings`: Findings likely to cause substantial mark loss.
- `commands_run`: Commands, exports, renders, or validation actions.
- `artifacts_produced`: Generated evidence or output files.
- `next_action`: Recommended coordinator action.

---

## final-report.json

Structured final handoff summary. Located under `<assignment-name>-workspace/reports/` when a file-backed report is useful.

```json
{
  "final_deliverable": "<path>",
  "ready_to_submit": true,
  "checks_run": ["<check or command>"],
  "reviews": ["<review report paths>"],
  "temporary_provisioning": {
    "performed": false,
    "paths_created": [],
    "cleanup": "<cleanup summary>"
  },
  "remaining_risks": ["<risk>"],
  "user_todos": ["<todo>"],
  "next_step": "<direct action>"
}
```

**Fields:**
- `final_deliverable`: Final file or folder path.
- `ready_to_submit`: Whether no blockers or majors remain.
- `checks_run`: Validation, export, render, execution, or review checks.
- `reviews`: Saved deliverable/rubric/humanization reports.
- `temporary_provisioning`: Setup and cleanup summary.
- `remaining_risks`: Real residual risks.
- `user_todos`: Actions the user must complete.
- `next_step`: Immediate next action.
