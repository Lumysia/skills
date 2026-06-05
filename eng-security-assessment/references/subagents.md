# Agent Roles

This file defines provider-neutral roles. A normal run should use child agents
or separate model calls for these roles. Sequential main-agent execution is a
fallback, not the default.

## Main Agent

Responsibilities:

- Parse intent and maintain `.state/`.
- Select profile and runtime strategy.
- Launch role agents for recon, tool discovery, find, verify, report, and patch as applicable.
- Keep all role communication file-based.
- Normalize outputs to `schemas.md`.
- Separate discovery claims from independent verification.
- Summarize status and next steps.
- Record `delegation_mode` as `subagents`, `separate-model-calls`, `scripts`, or `single-agent-fallback`.

## Delegation Policy

Default delegation:

```text
main orchestrator
  -> recon role
  -> tool-discovery role
  -> preflight/bootstrap role
  -> find role(s)
  -> verify role(s), separate from find
  -> dedup/judge role
  -> report role
  -> final-report role
  -> patch role, if requested
  -> patch verifier/reviewer, if requested
```

Rules:

- Environment scanning and bootstrap discovery belong to recon/preflight roles, not the main agent.
- Finding and verification must be separated by role or by a fresh verification pass.
- The main agent may summarize, approve plans, route artifacts, and enforce gates; it should not replace every role with its own reasoning.
- If subagents are unavailable, write `single-agent-fallback` and the reason to state before doing the work sequentially.

Fallback state example:

```json
{
  "delegation_mode": "single-agent-fallback",
  "fallback_reason": "host has no task/subagent capability",
  "roles_run_sequentially": ["recon", "tool-discovery", "find", "verify"]
}
```

## Recon Role

Inputs:

- target path or description.
- profile hint.

Outputs:

```json
{
  "profiles": ["web", "static"],
  "attack_surface": ["..."],
  "entrypoints": ["..."],
  "execution_options": ["..."],
  "verification_options": ["..."],
  "recommended_first_wave": "..."
}
```

## Tool Discovery Role

Inputs:

- profile.
- target stack evidence.
- vulnerability classes of interest.

Outputs:

- `.state/tool_discovery.json`.
- selected tools with provenance, versions, install paths, and risk notes.

## Find Role

Inputs:

- profile.
- selected tools/techniques.
- target and execution strategy.

Outputs:

- raw logs under `results/<target>/<ts>/raw/` or `logs/`.
- candidate leads in `tool_findings.jsonl`.
- generated PoCs under `pocs/` when applicable.

Rules:

- Tool output is a lead, not a final finding.
- Include enough evidence for a verifier to reproduce or reject.

## Verify Role

Inputs:

- one candidate lead.
- PoC/replay/test if available.
- clean execution or static review strategy.

Outputs:

- one line in `verified_findings.jsonl`.
- exploitability characterization fields from `exploitability.md`.

Rules:

- Prefer executable reproduction.
- If execution is unavailable, mark `static-only`.
- If evidence fails, mark `rejected` with `rejection_reason`.
- Do not reuse the find role's reasoning as verification.
- Do not stop at "it crashes" when deeper control evidence is obtainable.
- For memory corruption, attempt to measure offset, controlled bytes/registers,
  instruction pointer/program counter influence, write/read primitive, and
  exploitability constraints.

## Dedup/Judge Role

Inputs:

- verified findings.
- existing manifest.

Outputs:

- `reports/manifest.jsonl`.
- `reports/judge_log.jsonl` when decisions are nontrivial.

Judgments:

```text
NEW
DUP_BETTER
DUP_SKIP
```

Dedup by root cause: vulnerable operation, entrypoint, precondition, and impact.
Do not rely only on line number or tool rule id.

## Report Role

Inputs:

- verified finding.
- raw evidence paths.
- dedup decision.

Outputs:

- `reports/bug_NN/report.json`.

Report fields follow `schemas.md` and must include verification mode,
reachability, impact, PoC, constraints, confidence, and exploitability depth.

## Patch Role

Inputs:

- report.
- source tree.
- verifier command or replay.

Outputs:

- `reports/bug_NN/patch.diff`.
- `reports/bug_NN/patch_result.json`.

Rules:

- If no verifier exists, mark patch result `unverified`.
- Do not apply patches outside the results directory unless the user explicitly enters customization/apply mode.
