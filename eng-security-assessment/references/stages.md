# Stages

This is the portable runbook for the main agent. It does not assume any specific
model provider, CLI, repository, or language.

The main agent is the orchestrator. It should dispatch role agents by default.
Only fall back to doing role work itself when the host has no subagent/task
capability, when the user explicitly asks for single-agent mode, or when the
task is trivially small. Any fallback must be recorded in state.

Before running a target, read `model-runtime.md`, `generalization.md`,
`profiles.md`, `schemas.md`, `exploitability.md`, `final-report.md`,
`language.md`,
`tool-discovery.md`, and `state.md`.

## Phase 0: Parse Intent

Parse arguments into:

- target path, repo path, URL, package, or prior results directory.
- mode: `run`, `resume`, `status`, `report`, `patch`, `customize`, or `discover-tools`.
- profile: `auto`, `native`, `web`, `java`, `go`, `rust`, `contracts`, `static`, or `custom`.
- model preference, if the host supports choosing one.
- freshness: resume existing state or start over.

If target or authorization scope is unclear, ask one concise question.

Write `.state/phase0.json`.

## Phase 1: Profile and Tool Discovery

Dispatch a recon role agent and, unless the target/profile is already fully
known, a tool-discovery role agent. These roles own environment scanning and
bootstrap discovery; the main agent only coordinates and reads their artifacts.

Infer or select a profile:

- `native`: use existing project tools/tests/fuzzers.
- `web`: HTTP/API/browser/service attack surface.
- `java`, `go`, `rust`: language-specific code/test/fuzzing workflows.
- `contracts`: local chain/invariant/transaction workflows.
- `static`: source-only when execution is unavailable or not authorized.
- `custom`: user-defined detector and verifier.

The tool-discovery role actively searches current tools, advisories, and
target-specific techniques using `tool-discovery.md`. Record provenance in
`.state/tool_discovery.json`.

Create a results root:

```text
results/<target-name>/<UTC timestamp>/
```

Write `results/<target>/<ts>/profile.json` and `.state/phase1.json`.
If recon/tool-discovery was not delegated, include `delegation_mode` and
`fallback_reason` in `phase1.json`.

## Phase 2: Preflight

Dispatch a preflight/bootstrap role when the host supports subagents. It checks
runtime capabilities and prepares the execution plan. The main agent approves the
plan and records the chosen verifier.

Determine what can safely run:

- available host tools.
- package managers and test commands.
- web search/fetch capability.
- shell capability.
- container/VM/sandbox capability.
- project-local tests/fuzzers.
- local service or emulator startup.
- credentials or secrets required; do not use them unless explicitly authorized.

Choose a verification strategy before finding:

- executable replay.
- focused unit/integration test.
- fuzzer seed reproduction.
- local HTTP request sequence.
- local chain transaction sequence.
- differential/invariant check.
- static-only independent review.

If no safe execution or verifier exists, switch to `static` and mark outputs
`verification: static-only`.

Write `.state/phase2.json`.

## Phase 3: Find and Verify

Run the universal loop:

1. Recon child agent maps attack surface and entrypoints.
2. Tool discovery child agent selects tools/techniques when needed.
3. Find child agent runs tools, tests, fuzzers, generated PoCs, or source review.
4. Normalize leads into `tool_findings.jsonl`.
5. Verify child agent independently reproduces, rejects, or marks static-only.
6. Characterize exploitability depth using `exploitability.md`.
7. Write outcomes to `verified_findings.jsonl`.
8. Deduplicate by root cause using profile-appropriate `dedup_key`.

The find and verify roles must be separate by default. The same role that finds
a candidate should not be the sole verifier. If the host cannot dispatch a
separate verifier, run a separate verification pass with a fresh prompt and
record the limitation.

For each command or tool run:

- save raw output under `raw/` or `logs/`.
- record command, version, environment, and timestamp.
- keep generated PoCs or replay scripts under `results/<target>/<ts>/pocs/`.

Write `.state/phase3.json`.

## Phase 4: Report

Dispatch a report role to produce per-finding reports. The main agent checks
that report content is reader-facing, language-consistent, and backed by
verified artifacts before accepting it.

For each reproduced or static-only finding:

- assign or reuse a semantic `bug_NN` id.
- append `reports/manifest.jsonl`.
- append duplicate decisions to `reports/judge_log.jsonl` when dedup is nontrivial.
- write `reports/bug_NN/report.json` using `schemas.md`.
- include exploitability evidence: offset/control calculations, controlled state,
  primitive, mitigation impact, and ROP/shellcode feasibility where relevant.

Reports must distinguish:

- `verification: reproduced`.
- `verification: static-only`.
- rejected leads, which should not become bug reports unless the user asks for a rejected-leads appendix.

Write `.state/phase4.json`.

## Phase 4.5: Final Report and Export

After per-bug reports are written, generate a campaign-level final report using
`final-report.md`.

Dispatch a final-report role when available. The main agent should review the
final report for duplication, internal-run leakage, language consistency,
professional tone, exploitability depth, and PDF export before completion.

Required outputs:

```text
results/<target>/<ts>/FINAL_REPORT.md
results/<target>/<ts>/FINAL_REPORT.pdf
```

Optional internal dossier:

```text
results/<target>/<ts>/RUN_DOSSIER.md
```

If PDF export is unavailable, keep Markdown and state the missing export reason
in the final response.

## Phase 5: Patch, If Requested

Dispatch a patch role and, when possible, a separate patch-review or verifier
role. The patch role should not be the only judge of its own fix.

Patch only when there is enough evidence and a verifier exists.

Patch loop:

1. Generate a minimal candidate diff.
2. Run project tests or profile-specific verifier.
3. Re-run the original PoC/replay if available.
4. Write `reports/bug_NN/patch.diff` and `patch_result.json`.
5. Mark unverified if no executable verifier exists.

Never present a diff as upstream-safe merely because it was generated. It is a
candidate requiring human review.

Write `.state/phase5.json` and set `progress.json` complete or partial.

## Status and Resume

For status, read `state.md` and `status.md`.

For resume:

- read `.state/progress.json`.
- continue from the next incomplete phase.
- skip role outputs that already exist unless `--fresh` is set.
- use prior artifacts as context instead of relying on provider-specific session resume.

## Safety Stops

Stop and ask before:

- using production credentials or cloud accounts.
- sending private code/logs to hosted scanners.
- testing a live network target.
- installing host-global packages.
- deleting results or killing external processes.
- applying generated patches outside the results directory.
