---
name: eng-project-init
description: Initialize a software project for agent use by inspecting repo conventions and creating or tightening AGENTS.md. Use when setting up a project, adding agent instructions, refreshing repo guidance, or asking for project initialization.
---

# Engineering Project Init

Use this skill to create concise, repo-specific agent instructions. Do not create CLAUDE.md, ADRs, glossaries, or broad process docs unless the user asks.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and outputs unless the user specifies otherwise.

## Flow

1. Inspect existing guidance: `AGENTS.md`, README, package/build files, test config, formatter/linter config, CI, scripts, and docs.
2. Infer commands, style rules, project layout, safety rules, and commit rules from files, not guesses.
3. Ask only for hard dependencies that cannot be inferred, such as preferred commit format or required test command.
4. Treat naming preferences, issue tracker, domain terms, and optional docs as soft dependencies; skip them if absent.
5. Write or update `AGENTS.md` with short, actionable rules.
6. Preserve existing valid rules; remove duplication and empty phrasing.
7. Verify the final file is concise and matches the repository.

## Output

Default output is only `AGENTS.md`. Add other files only on explicit request.

For the template and checks, read `references/agentsmd.md`.
