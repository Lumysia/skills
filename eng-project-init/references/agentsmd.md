# AGENTS.md

## Hard Dependencies

Ask once when missing and needed:

- commit message format,
- required test/build command,
- protected files or directories,
- package manager when multiple lockfiles conflict,
- release/deploy rule if the user asks for release guidance.

Do not block on soft dependencies: issue tracker, domain glossary, ADRs, labels, preferred prose style, or docs location.

## Template

```markdown
# AGENTS.md

- Respond in the user's language unless code, logs, commands, or external text require otherwise.
- Be concise: one sentence beats two, one word beats several, and empty phrasing is not allowed.
- Address current-system problems; do not add speculative rules or generic filler.
- Keep naming and layout consistent with nearby files.
- Prefer maintainable fixes over narrow symptom patches.
- Gather evidence before changing unclear code paths.
- Fix shared abstractions or contracts when the bug crosses state, sync, protocol, rendering, or data boundaries.
- Keep reusable policy, protocol values, and cross-file literals in registries, config, or typed constants.
- Keep source files under `<line limit>` by default; split by responsibility before adding more behavior.
- Run `<test command>` before claiming code works.
- Run `<format/lint command>` when touching `<files>`.
- Preserve `<important convention>`.
- Do not edit `<protected path>` unless explicitly asked.
- Use Angular-style commit messages.
- Keep commits focused; review the pending diff before committing.

## Skill Rules

- Keep `AGENTS.md` as a routing index; put detailed workflow rules in skills.
- Keep each skill self-contained and transferable.
- Keep main `SKILL.md` files lean; move dense details to one-level `references/` files.
- Keep the main agent as orchestrator for large workflows; delegate when the environment supports it.
- Use positive skill wording where practical.
- Cross-reference another skill only as routing guidance, not as a dependency for the current skill.
```

## Writing Rules

- One rule per bullet.
- Prefer commands over prose.
- Keep only rules that affect future agent behavior.
- Use exact filenames, commands, and paths.
- Preserve project-specific names only when they are part of the contract.
- Mark uncertain rules as questions, not instructions.
- Do not add setup docs, ADRs, CLAUDE.md, or glossaries by default.

## Inspection Checklist

- Existing `AGENTS.md` or agent config.
- README and docs for project commands.
- `package.json`, lockfiles, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, task files.
- Formatter and linter config.
- Test config and CI workflows.
- Git hooks or commit tooling.

## Final Check

- No duplicated rules.
- No vague rules such as "write good code".
- No unverifiable claims.
- No unnecessary user prompts.
- No instructions copied from unrelated projects.
