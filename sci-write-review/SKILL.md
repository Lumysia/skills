---
name: sci-write-review
description: Create evidence-grounded literature reviews, research syntheses, technical reviews, and long-form manuscripts from source documents using file-backed artifacts, long-running coordination, worker roles, critic gates, quality checks, and export traceability.
---

# Scientific Review Writer

Use this skill to run a resumable, evidence-grounded review-writing workflow that creates file-backed artifacts, delegates bounded worker roles, enforces critic/work-check gates, and exports a manuscript with traceability to sources and citation anchors.

## Startup

Read `agents/coordinator.md` before planning, reading sources, launching workers, drafting, revising, or exporting. Treat it as the execution contract.

## Flow

1. Identify or resume the review workspace and core inputs.
2. Create/update `project.json`, `manifest.json`, `status.json`, `plan.md`, and checkpoints.
3. Delegate extraction, reading, synthesis, writing, criticism, quality selection, and work checks through `agents/`.
4. Draft only from approved/locked evidence artifacts.
5. Export `manuscript.md`, references, `export-trace.json`, and `workflow-summary.json`.

## Resources

- `agents/coordinator.md`: phases, state, resume, worker routing, gates, handoff.
- `agents/*.md`: bounded worker role specs.
- `references/`: workflow details, schemas, extraction policy, critic rules, evals, examples.

## Operating Rules

- Use files, not chat, as durable handoffs.
- Parallelize independent worker batches when available; serialize shared writes and integration.
- Route paper discovery or source acquisition to `sci-paper-search` when useful.
- Extract PDFs/unusual formats before Reader/Synthesis/Writer use them.
- Treat fabricated, unverifiable, or source-mismatched claims as hard failures.
- Preserve citation anchors across evidence, claims, drafts, manuscript, and export trace.
