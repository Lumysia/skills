---
name: eng-security-assessment
description: Run autonomous security assessment workflows with profile selection, active tool discovery, child-agent orchestration, fixed runtime directories, logs, checkpoints, resume, validation, reporting, and patching.
argument-hint: "<target|results-dir> [--mode run|resume|status|report|patch|customize|discover-tools] [--profile auto|native|web|java|go|rust|contracts|static|custom] [--runs N] [--model M] [--fresh]"
---

# Engineering Security Assessment

Use this skill to run a resumable, evidence-grounded security assessment with scoped authorization, profile selection, tool discovery, role-agent orchestration, verification gates, reporting, and optional patch generation.

## Startup

Read `agents/coordinator.md` before planning, scanning, resuming, reporting, patching, or checking status. Treat it as the execution contract.

## Routing

- New run: use `agents/coordinator.md`, then consult `references/stages.md`, `references/state.md`, and relevant profile/tool references only as needed.
- Resume/status/report/patch: use `agents/coordinator.md`, then the specific reference for that mode.
- If no mode is given with a target, run: intake -> profile/tools -> preflight -> find/verify -> reports -> final report -> optional patch.

## Operating Rules

- Coordinator routes work; it is not the default worker.
- Parallelize independent worker batches when subagents/separate model calls exist; record merge order.
- Use `security-assessment-workspace/` for `state/`, `results/`, and `tools/`.
- Tool output is only a lead until independently verified.
- Ask before live testing, credentials, hosted scanners, global installs, destructive actions, or patching outside the workspace.
