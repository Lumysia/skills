---
name: gen-long-running-skill-creator
description: Design, refactor, and evaluate skills for extremely complex long-running agent work. Use when a task may run for hours, requires staged autonomy, checkpoints, resumability, child-agent orchestration, artifact directories, audit logs, quality gates, or recovery from partial progress.
---

# General Long-Running Skill Creator

Use this skill to create or refactor skills for tasks that are too complex to complete as a short interactive workflow and may require hours of autonomous execution.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, source text, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and outputs unless the user specifies otherwise.

## What Long-Running Means

A long-running skill is defined by execution complexity, not topic breadth. Use this skill when the target workflow needs several of these properties:

- Runs for hours or across many tool/agent cycles.
- Has many dependent phases with go/no-go gates.
- Produces substantial intermediate artifacts, logs, and final deliverables.
- Needs checkpoints, resume, rollback, or partial-result recovery.
- Requires parallel subagents or worker batches with synthesis.
- Must track assumptions, evidence, decisions, risks, and unresolved items.
- Needs periodic user updates without blocking on constant user input.
- Has quality gates that prevent shipping incomplete or low-confidence output.

For a focused short workflow, use `gen-skill-creator` instead.

## Target State

Define the target operating model before writing instructions:

- **Mission**: the final outcome and non-negotiable success criteria.
- **Runtime contract**: where artifacts, logs, checkpoints, and reports live.
- **Phase map**: ordered stages, entry criteria, exit criteria, and failure handling.
- **Autonomy budget**: what the agent may do without asking, and what requires user confirmation.
- **Dependency model**: hard prerequisites that block work and soft inputs that improve quality.
- **Verification model**: tests, audits, critic passes, human review gates, or evidence checks.
- **Resume model**: how a later session determines state and continues safely.

Treat these as hypotheses. Include the cheapest validation step or falsifying condition before committing to a long run.

## Flow

1. Capture the mission, expected runtime, deliverables, hard dependencies, risk level, and stop conditions.
2. Study this creator skill's own structure and file content patterns before designing the target skill: `SKILL.md` as the short entrypoint, `agents/` as role workflow files, `references/` as shared schemas and state contracts, `scripts/` as repeatable tooling, and runtime workspaces as resumable execution state.
3. Design the runtime directory layout before execution starts.
4. Split the workflow into phases with checkpoints, artifacts, status files, and validation gates.
5. Define what gets logged: prompts, commands, sources, decisions, errors, assumptions, and outputs.
6. Specify worker/subagent workflows under `agents/<role>.md` when parallelism is useful; define exact return schemas and merge rules.
7. Add progress-update rules that keep the user informed without interrupting long autonomous stretches.
8. Add recovery rules for crashes, timeouts, missing dependencies, partial outputs, and failed quality gates.
9. Build a small dry-run or smoke eval before recommending a full multi-hour run.

## Runtime Layout

Every long-running skill should create or name a fixed runtime directory for each run:

```text
<task>-workspace/
├── README.md              # mission, status, resume instructions
├── plan.md                # phase plan and current checkpoint
├── status.json            # machine-readable current state
├── logs/                  # commands, agent notes, errors, timestamps
├── inputs/                # copied or referenced source inputs
├── artifacts/             # intermediate outputs by phase
├── agents/                # role workflow specs used by workers/subagents
├── reviews/               # critic passes, user feedback, QA notes
├── reports/               # final or staged deliverables
└── checkpoints/           # resumable snapshots and phase completion markers
```

The layout may be adapted, but the skill must state where state is stored and how to resume.

## Phase Design

Each phase should include:

- **Goal**: what this phase proves or produces.
- **Inputs**: required files, decisions, credentials, or prior artifacts.
- **Actions**: bounded work the agent can execute.
- **Outputs**: exact artifacts and status updates.
- **Exit gate**: objective check or review condition.
- **Failure path**: retry, degrade, ask user, or stop.

Avoid phase names like “do research” unless the output and exit gate are explicit.

## Checkpoints And Resume

Long-running skills must be resumable. Include rules to:

- Write `status.json` after every phase and major worker batch.
- Record completed, in-progress, blocked, and abandoned work separately.
- Store enough context to continue without rereading everything.
- On startup, inspect existing runtime state before doing new work.
- Never overwrite prior artifacts without versioning or recording the replacement.
- Summarize what changed since the last checkpoint.

## Parallel Work

Use child agents or worker batches only when their work can be independently verified or merged. Define:

- Role workflow file under `agents/`, one file per role.
- Worker scope and forbidden scope.
- Input files and output directory.
- Required final schema.
- Evidence requirements.
- Timeout or retry policy.
- Merge order and conflict resolution.

Do not launch open-ended workers without a bounded deliverable.

Do not put all role workflows into one large reference file. Use `agents/` for executable role instructions, and keep `references/` for shared schemas, rubrics, state contracts, and background material.

## Quality Gates

Long runs need explicit gates so the agent does not drift. Choose gates appropriate to the task:

- Build/test/lint/typecheck for code.
- Source traceability and claim checks for research.
- Schema validation for structured outputs.
- Critic or adversarial review for strategy and writing.
- Sample-based manual review before scaling a batch.
- Final consistency check across all deliverables.

If a gate fails, the skill should say whether to retry, narrow scope, escalate to the user, or stop with a partial report.

## User Interaction

Minimize repeated prompts. Ask once for hard missing dependencies. Treat optional preferences as soft inputs.

Progress updates should happen at meaningful checkpoints: phase start, phase completion, major discovery, blocker, quality-gate failure, and final handoff. For multi-hour runs, include an estimated next check-in condition rather than a clock promise the agent cannot keep.

## Evaluation

Evaluate long-running skills with shortened simulations before full runs:

```json
{
  "skill_name": "example-long-running-skill",
  "smoke_evals": [
    {"prompt": "Run only phase 1 on sample input", "expected_artifacts": ["status.json", "plan.md"]}
  ],
  "resume_evals": [
    {"state": "checkpoint after phase 2", "expected_next_action": "start phase 3 validation"}
  ],
  "failure_evals": [
    {"condition": "missing required credential", "expected_behavior": "stop and ask once"}
  ]
}
```

Do not require full multi-hour evals for every revision. Use representative dry-runs, artifact inspections, and resume tests.

## Bundled Resources

Use the copied creator resources when they fit the environment:

- `references/schemas.md` defines example structures for evals, grading, timing, and benchmarks.
- `agents/grader.md`, `agents/comparator.md`, and `agents/analyzer.md` support review and comparison workflows; new long-running skills should add their own role workflow files under `agents/`.
- `eval-viewer/generate_review.py` can build a human review UI for saved eval outputs.
- `scripts/package_skill.py` packages a skill folder into a distributable archive.

## Deliverable

Return the long-running skill design or patch with:

- Runtime directory contract.
- Phase map and checkpoints.
- Autonomy and escalation rules.
- Worker/subagent specs if used.
- Quality gates and resume rules.
- Smoke/resume/failure evals.
- Any remaining risks before a full long run.
