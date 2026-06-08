# AGENTS.md

- Skill names use `<category>-<purpose>`: e.g. `eng-security-assessment`, `sci-write-review`. Keep names explicit; avoid unclear abbreviations.
- Use short category prefixes in skill names; do not create category folders just for organization.
- Be concise: one sentence beats two, one word beats several, and empty phrasing is not allowed.
- Each skill is self-contained: `SKILL.md` is the short index, detailed instructions live under `references/`.
- Each public skill must be listed in `README.md` under its category with a one-sentence description and link to `SKILL.md`.
- Keep skills model- and host-agnostic. Do not depend on a specific provider, CLI, repository, or global config unless the skill is explicitly for that tool.
- When adding host-specific entrypoints such as commands, skills, wrappers, or config loaders, update every supported host surface in the repository in the same change and prefer pointer wrappers for repository skills instead of duplicating instructions.
- For system-level entrypoints managed by setup, add repository templates under `eng-agent-init/references/global-entrypoints/`; do not write directly to user global config paths such as `~/.config/opencode/commands/` unless the user explicitly asks to install them now.
- Do not add unrequested policy preferences, normative constraints, or default source restrictions to skills; limit rules to the user's request, repository conventions, and verifiable tool behavior.
- When adapting templates, include only rules that apply to this repository; do not copy placeholder, optional, or irrelevant rules.
- Do not rewrite wording just to make it sound better; if a problem is not clear, do not edit it.
- For design or architecture decisions, define the target state before discussing migration, compatibility, and implementation constraints.
- Do not add or preserve legacy paths, aliases, transitional wrappers, compatibility shims, partial implementations, or smaller diffs when they conflict with the target model, unless an explicit external contract requires them.
- Treat high-confidence design assumptions as hypotheses and include the cheapest validation step or falsifying condition.
- When creating or updating a skill, include a `SKILL.md` Startup/Bootstrap rule that infers the user's interaction/output language before starting and asks once only if it cannot be inferred confidently.
- Distinguish hard dependencies from soft dependencies. Hard dependencies must be collected or confirmed before execution; soft dependencies should improve output but must not cause repeated user prompts or block progress.
- Use Angular commit message format for commits, e.g. `docs: update agent instructions`.
