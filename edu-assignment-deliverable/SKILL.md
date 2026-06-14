---
name: edu-assignment-deliverable
description: Create course assignment deliverables from prompts, rubrics, source materials, templates, and submission rules using a resumable workspace, staged validation, worker reviews, and final submission handoff. Use for rubric-graded coursework artifacts in any required format, especially complex or multi-file assignments.
---

# Education Assignment Deliverable

Use this skill to produce a finished course assignment deliverable that follows the user's prompt, rubric, source materials, template, and submission constraints.

## Startup

Read `agents/coordinator.md` before planning, searching broadly, drafting, validating, or handing off. Treat it as the execution contract.

## Flow

1. Discover prompt/rubric/template/source files before asking the user for them.
2. Resume an existing assignment workspace when `status.json` or checkpoints exist.
3. Create/update `<assignment-name>-workspace/` for non-trivial assignments.
4. Build `artifacts/rubric-checklist.md` from primary sources before drafting.
5. Delegate deliverable work, checks, rubric review, and optional humanization through `agents/` when available.
6. Return only the final deliverable path, checks run, blockers/majors, risks, and external actions.

## Resources

- `agents/coordinator.md`: main-agent operating spec for intake, planning, worker routing, validation, checkpointing, and handoff.
- `agents/*.md`: deliverable work, deliverable check, rubric review, and humanization roles.
- `references/`: schemas and eval scenarios.

## Rules

- Do not fabricate missing context, citations, results, or validation evidence.
- Keep submission artifacts pure: no agent notes, TODOs, logs, caveats, or review reports unless required.
- Do not call work ready until the deliverable exists, is readable, matches format, and required checks/reviews have no blockers or majors.
- Ask user-resolvable blockers one at a time, then continue and recheck.
