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

Use this template as a menu, not a checklist. Include only rules supported by the inspected project and useful for future agent behavior.

When `AGENTS.md` already exists, use it as the base and apply this template only to fill gaps, tighten weak rules, or remove obsolete guidance.

Do not promote a user preference, template example, or broadly useful practice into `AGENTS.md` unless it applies to the target project by evidence or explicit user scope.

```markdown
# AGENTS.md

- Respond in the user's language unless code, logs, commands, or external text require otherwise.
- Do not add unrequested policy preferences, normative constraints, or default source restrictions to skills; limit rules to the user's request, repository conventions, and verifiable tool behavior.
- When creating or updating a skill, include a `SKILL.md` Startup/Bootstrap rule that infers the user's interaction/output language before starting and asks once only if it cannot be inferred confidently.
- Be concise: one sentence beats two, one word beats several, and empty phrasing is not allowed.
- Address current-system problems; do not add speculative rules or generic filler.
- Keep naming and layout consistent with nearby files.
- Prefer maintainable fixes over narrow symptom patches.
- Gather evidence before changing unclear code paths.
- Fix shared abstractions or contracts when the bug crosses state, sync, protocol, rendering, or data boundaries.
- For design or architecture decisions, define the target state before discussing migration, compatibility, and implementation constraints.
- Follow SemVer for compatibility: versions before `1.0.0` do not require backward compatibility, and breaking changes after `1.0.0` must be expressed by a major version change.
- Do not add or preserve legacy paths, aliases, transitional wrappers, compatibility shims, partial implementations, or smaller diffs when they conflict with the target model, unless SemVer or an explicit external contract requires them.
- Treat high-confidence design assumptions as hypotheses and include the cheapest validation step or falsifying condition.
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
- Preserve existing valid rules when updating an existing `AGENTS.md`.
- Omit template rules that do not apply to the inspected project.
- Add rules only from existing guidance, inspected repo evidence, or explicit target-project instructions.
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
- Every added rule has a clear source: existing guidance, repo evidence, or explicit target-project instruction.
- No unnecessary user prompts.
- No instructions copied from unrelated projects.
