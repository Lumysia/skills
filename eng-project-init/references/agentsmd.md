# AGENTS.md Guidance

Use `AGENTS.md` to give future agents concise, project-specific operating rules. It is not a place for broad philosophy, personal preferences, onboarding prose, or unrelated policy.

## Discovery

Inspect before writing:

- Existing `AGENTS.md` and any scoped nested instruction files.
- README, docs, scripts, task runners, and package/build files.
- Test, lint, format, typecheck, and CI configuration.
- Lockfiles and package-manager evidence.
- Git hooks, release config, commit tooling, and protected paths.

Infer rules from repository evidence or explicit target-project instructions. Do not promote broadly useful habits, personal preferences, or template examples into instructions unless they apply to this project.

## Hard Dependencies

Ask one concise question only when required information cannot be inferred after discovery:

- Target project root when multiple roots are plausible.
- Required test/build command when the user wants it enforced and repo evidence is conflicting.
- Protected files or directories when the user asks for protection but the repo does not reveal them.
- Commit message format when the user wants a rule and repo evidence is absent or conflicting.

Do not block on soft dependencies: issue tracker, domain glossary, ADR style, labels, prose preferences, optional docs locations, or future process choices.

## Template Menu

Use these categories as a menu, not a checklist. Include only rules supported by the inspected project or explicit target-project scope.

```markdown
# AGENTS.md

- Use `<package manager>` for dependency and script commands.
- Run `<test command>` before claiming behavior works.
- Run `<format/lint/typecheck command>` when touching `<file patterns>`.
- Keep changes within `<project layout or package boundary>` unless the task requires cross-package edits.
- Preserve `<important generated/protected path>` unless explicitly asked.
- Follow `<commit message format>` for commits.
- Keep commits focused; inspect status and diff before committing.
- Do not edit `<external/vendor/generated path>`.
- Document `<project-specific artifact or API contract>` when changing it.
```

For skills repositories, include only evidence-backed skill rules, such as naming conventions, README registration requirements, host-agnostic constraints, or required resource layout.

## Update Rules

- If `AGENTS.md` exists, use it as the base.
- Preserve valid current rules that still match the project.
- Remove obsolete, duplicate, empty, placeholder, vague, or unrelated rules.
- Merge overlapping rules instead of adding near-duplicates.
- Use exact filenames, commands, paths, and scopes.
- Mark unresolved uncertainty as a question in the final response, not as an instruction in `AGENTS.md`.
- Keep instructions short and actionable.

## Output Rules

- Default output is only `AGENTS.md`.
- Do not create `CLAUDE.md`, ADRs, glossaries, setup docs, command wrappers, or broad process docs unless explicitly requested.
- Do not edit global agent config, user profile files, or repository files outside the target project scope unless explicitly requested.

## Final Check

- Every added rule has a source: existing guidance, repo evidence, or explicit target-project instruction.
- No duplicated or vague rules remain.
- No unrelated project, host, model, provider, or personal setup assumptions are included.
- The file is concise enough for future agents to read before acting.
