---
name: eng-security-assessment
description: Run autonomous security assessment workflows with profile selection, active tool discovery, child-agent orchestration, fixed runtime directories, logs, checkpoints, resume, validation, reporting, and patching.
argument-hint: "<target|results-dir> [--mode run|resume|status|report|patch|customize|discover-tools] [--profile auto|native|web|java|go|rust|contracts|static|custom] [--runs N] [--model M] [--fresh]"
---

# Engineering Security Assessment

This skill is the index for a portable security assessment workflow. Keep this file short:
load the relevant reference, then execute that runbook.

Core idea:

```text
SKILL.md = entrypoint and router
references/ = workflow implementation
profiles = target/domain-specific execution strategies
tools/runtime = whatever capabilities the host can provide
.state/ = portable checkpoint state
results/<target>/<ts>/ = portable artifacts
```

## Startup

Before routing or starting a mode, infer the user's preferred interaction and report language from the request, target materials, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, artifacts, and reports unless the user specifies otherwise.

## Routing

- New run or first-time setup: read `references/stages.md`, then `references/state.md`.
- Resume or status check: read `references/state.md`, then `references/status.md`.
- Model/runtime portability: read `references/model-runtime.md`.
- Status-only requests: read `references/status.md`.
- General vulnerability-discovery flow and profiles: read `references/generalization.md`.
- Concrete non-C/C++ profile runbooks: read `references/profiles.md`.
- General artifact schemas: read `references/schemas.md`.
- Exploitability depth requirements: read `references/exploitability.md`.
- Final report and PDF export: read `references/final-report.md`.
- Report language and localization: read `references/language.md`.
- Active tool/news/research discovery: read `references/tool-discovery.md`.
- Main/child agent design: read `references/subagents.md`.
- Architecture and portability boundaries: read `references/architecture.md`.
- Customizing profiles or porting domains: read `references/customization.md`.
- Failures, retries, and safety stops: read `references/failure-handling.md`.

## Operating Rules

- The main agent is an orchestrator, not the default worker. For a normal run it must dispatch role agents for recon, tool discovery, find, verify, report, and patch as applicable.
- Do not perform recon, environment bootstrap, finding, verification, and reporting all in the main agent unless the host lacks subagent/task capability or the task is explicitly tiny; record this fallback in `.state/phase1.json` or `phase3.json`.
- Do not assume any specific model provider, agent host, repository, scanner, or CLI exists. Use whatever model/tool runtime the host provides.
- Tool discovery is first-class: search current docs/news/tools, record provenance, and run tools through the selected runtime.
- Keep default state, downloaded tools, and reports under `.state/`, `.tools/`, and `results/`; if a profile needs generated tests, PoCs, fixtures, exports, or runtime files elsewhere, record the reason and artifact path.
- Use `.state/` for skill-level checkpoints; use `results/<target>/<ts>/` for execution artifacts.
- If modifying profile logic, do it as a separate customization phase before launching a run.

## Default Flow

If the user gives a target and no mode, run the flow in `references/stages.md`:

```text
init -> profile/tool discovery -> preflight -> recon/focus -> run/validate -> reports -> final report/export -> optional patch
```

If the user gives a results directory, infer status/report/patch mode from its contents.
