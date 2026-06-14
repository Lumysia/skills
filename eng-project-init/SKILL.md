---
name: eng-project-init
description: Initialize a software project for agent use by inspecting repo conventions and creating or tightening AGENTS.md. Use when setting up a project, adding agent instructions, refreshing repo guidance, or asking for project initialization.
---

# Engineering Project Init

Use this skill to initialize or tighten project-specific agent instructions by inspecting repository evidence and writing a concise `AGENTS.md`.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and outputs unless the user specifies otherwise.

## Flow

1. Read `references/agentsmd.md` before creating, rewriting, or appending agent instructions.
2. Inspect existing guidance, README, build files, test config, formatter/linter config, CI, scripts, and docs.
3. Infer commands, style rules, project layout, safety rules, and commit rules from repository evidence or explicit target-project instructions.
4. Ask one concise question only when a hard dependency remains unclear after inspection.
5. Use existing `AGENTS.md` as the base when present; otherwise create one focused file for the target project.
6. Preserve valid rules and remove obsolete, duplicate, placeholder, vague, or unrelated guidance.
7. Verify the final `AGENTS.md` is concise, evidence-backed, and scoped to future agent behavior in this repository.

Hard dependencies are target project root, permission to create or edit `AGENTS.md`, and any required command or protected path the user wants enforced but the repository does not reveal. Naming preferences, issue tracker, domain glossary, ADRs, labels, prose style, and optional docs are soft dependencies.

## Output

Default output is only `AGENTS.md`. Do not create `CLAUDE.md`, ADRs, glossaries, local setup docs, or broad process docs unless explicitly requested.

## Resources

- `references/agentsmd.md`: AGENTS.md construction rules, evidence sources, template menu, and final checks.
- `references/evals.md`: smoke scenarios for project initialization, existing guidance cleanup, and prompt minimization.
