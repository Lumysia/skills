---
name: edu-assignment-deliverable
description: Create course assignment deliverables from prompts, rubrics, source materials, templates, and submission rules using a resumable workspace, staged validation, worker reviews, and final submission handoff. Use for rubric-graded coursework artifacts in any required format, especially complex or multi-file assignments.
---

# Education Assignment Deliverable

Use this skill to produce a finished course assignment deliverable that follows the user's prompt, rubric, source materials, template, and submission constraints.

This skill supports both compact one-pass assignments and long-running coursework workflows with runtime state, checkpoints, validation gates, and independent reviews.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, assignment prompt, source materials, template, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and deliverable prose unless the user specifies otherwise.

Inspect existing assignment files before writing. If an assignment workspace already exists, resume from its `status.json` and latest checkpoint instead of starting over.

## Flow

1. Capture the assignment prompt, required format, submission constraints, source materials, hard dependencies, and success criteria.
2. Inspect existing files and prior workspace state before drafting, rebuilding, or replacing work.
3. For non-trivial assignments, create or resume `<assignment-name>-workspace/` with `README.md`, `plan.md`, `status.json`, `logs/`, `artifacts/`, `reviews/`, `reports/`, and `checkpoints/`.
4. Convert the prompt, rubric, template, and submission rules into `artifacts/rubric-checklist.md` before building or revising the final deliverable.
5. Use `agents/coordinator.md` as the main operating spec for phase rules, autonomy limits, worker routing, validation recovery, checkpointing, and final handoff.
6. Use worker role specs under `agents/` for deliverable checks, temporary environment setup, rubric review, and optional humanization when those gates apply.
7. Keep `references/` for shared schemas and eval scenarios; use `references/schemas.md` for runtime state fields and `references/evals.md` for smoke/resume/failure checks.

## Runtime Contract

For substantial assignments, use this run directory layout:

```text
<assignment-name>-workspace/
├── README.md
├── plan.md
├── status.json
├── inputs/
├── artifacts/
├── agents/
├── logs/
├── reviews/
├── reports/
└── checkpoints/
```

Write `status.json` after every phase and major worker batch. Never overwrite existing user work or prior run artifacts without versioning or recording the replacement in `logs/decisions.md` and `status.json`.

## Agent Specs

- `agents/coordinator.md`: main-agent operating spec for intake, planning, build/revise, validation, checkpointing, and handoff.
- `agents/deliverable-check.md`: independent file/readiness inspection without modifying files.
- `agents/environment-setup.md`: reversible temporary provisioning for blocked validation/export/execution.
- `agents/rubric-review.md`: independent final rubric and submission-readiness review.
- `agents/humanization.md`: constrained prose naturalization when requested or materially needed.

## Quality Gates

Do not call the assignment ready until the final file or folder exists, is readable, matches the requested format, required validation has been attempted, worker findings are resolved or recorded, and rubric review reports no blockers or majors unless the final handoff clearly labels accepted risks.

Only blockers and major issues require another fix/review loop. Do not loop on minor or note findings unless the user requests polish.

## Evaluation

Use `references/evals.md` for concrete smoke, resume, failure, readiness, and humanization eval scenarios. Do not require full multi-hour evals for every revision; use representative dry-runs, artifact inspections, and resume tests.

## Final Handoff

Return the final deliverable path, checks or reviews run, temporary provisioning and cleanup, remaining blockers or majors, real risks, user TODOs, and the next direct action.
