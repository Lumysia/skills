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
- **Source-trace model**: which files, records, user messages, or evidence are authoritative for requirements and claims.
- **Resume model**: how a later session determines state and continues safely.

Treat these as hypotheses. Include the cheapest validation step or falsifying condition before committing to a long run.

## Flow

1. Capture the mission, expected runtime, deliverables, hard dependencies, risk level, and stop conditions.
2. Study this creator skill's own structure and file content patterns before designing the target skill: `SKILL.md` as the short entrypoint, `agents/` as role workflow files, `references/` as shared schemas and state contracts, `scripts/` as repeatable tooling, and runtime workspaces as resumable execution state.
3. Read the target skill's relevant files before editing; use search only to find candidates, not as a substitute for reading structure and content.
4. Create `agents/coordinator.md` as the required main-agent operating spec before designing optional worker roles.
5. Make `SKILL.md` require reading `agents/coordinator.md` as the first execution step before planning, todos, workspace discovery, drafting, validation, or worker launch.
6. Design the runtime directory layout before execution starts.
7. Split the workflow into phases with checkpoints, artifacts, status files, and validation gates.
8. Define what gets logged: prompts, commands, sources, decisions, errors, assumptions, and outputs.
9. Specify worker/subagent workflows under `agents/<role>.md` when parallelism is useful; define exact return schemas and merge rules.
10. Add progress-update rules that keep the user informed without interrupting long autonomous stretches.
11. Add recovery rules for crashes, timeouts, missing dependencies, partial outputs, and failed quality gates.
12. Run a small dry-run or smoke eval before recommending a full multi-hour run.

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
├── agents/                # coordinator plus worker/subagent role specs
├── reviews/               # critic passes, user feedback, QA notes
├── reports/               # final or staged deliverables
└── checkpoints/           # resumable snapshots and phase completion markers
```

The layout may be adapted, but the skill must state where state is stored and how to resume.

Every long-running skill must include `agents/coordinator.md`. `SKILL.md` must explicitly instruct the agent to read `agents/coordinator.md` before creating a plan, todo list, workspace search, draft, validation run, or worker task.

Resume behavior must be automatic: when a runtime workspace already exists, the coordinator should inspect its state files and continue from the first incomplete phase or failed gate. A specific user phrase should not be required.

## Coordinator Design

`agents/coordinator.md` is the main-agent operating spec. It should define:

- Intake and hard-dependency gate.
- Runtime workspace setup and resume behavior.
- Phase sequence, checkpoints, artifacts, and status updates.
- Autonomy limits and escalation rules.
- Worker routing, mandatory delegation gates, fallback rules when subagents are unavailable, and merge rules.
- Primary-source rules that prevent summaries, plans, extracted paraphrases, or worker handoffs from becoming the source of truth for requirements.
- Separation between coordination and actual artifact/content creation when the workflow produces substantial deliverables.
- Quality gates and failure paths.
- Final handoff requirements.

Keep `SKILL.md` as the short trigger and index. Put the detailed long-running execution contract in `agents/coordinator.md`, not in `references/` and not only in optional worker files.

Keep new and revised instructions concise; merge similar rules and remove filler.

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
- Which gates require delegation when subagents are available.
- Which workers own artifact/content creation versus review, validation, setup, synthesis, or human-facing handoff.
- Fallback behavior when subagents are unavailable, including how the fallback is recorded.
- Input files and output directory.
- Required final schema.
- Evidence requirements.
- Timeout or retry policy.
- Merge order and conflict resolution.

Do not launch open-ended workers without a bounded deliverable.

Do not put all role workflows into one large reference file. Use `agents/` for executable role instructions, and keep `references/` for shared schemas, rubrics, state contracts, and background material.

## Quality Gates

Long runs need explicit gates so the agent does not drift. Choose gates appropriate to the task:

- Artifact-specific checks such as render/export/open/readback, build/test/lint/typecheck, schema validation, or dry-run execution.
- Source traceability and claim checks for research.
- Primary-source traceability for rubric, compliance, legal, academic, or user-provided requirements.
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
- `scripts/quick_validate.py` sanity-checks a skill's frontmatter and structure before a full run.
- `scripts/run_eval.py` and `scripts/run_loop.py` run trigger evals for a skill description, optionally looping with `scripts/improve_description.py` until they pass.
- `scripts/aggregate_benchmark.py` and `scripts/generate_report.py` turn raw benchmark/loop runs into summary stats and an HTML report.
- `eval-viewer/generate_review.py` can build a human review UI for saved eval outputs.
- `scripts/package_skill.py` packages a skill folder into a distributable archive.

## Deliverable

Return the long-running skill design or patch with:

- Runtime directory contract.
- Required `agents/coordinator.md` main-agent spec.
- `SKILL.md` first-step instruction to read `agents/coordinator.md`.
- Worker role specs for substantial artifact/content creation when the long-running workflow produces deliverables.
- Phase map and checkpoints.
- Autonomy and escalation rules.
- Worker/subagent specs if used.
- Quality gates and resume rules.
- Smoke/resume/failure evals.
- Any remaining risks before a full long run.
