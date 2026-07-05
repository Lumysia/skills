# AGENTS.md

- Skill names use `<category>-<purpose>`: e.g. `eng-security-assessment`, `sci-write-review`. Keep names explicit; avoid unclear abbreviations.
- Use short category prefixes in skill names; do not create category folders just for organization.
- Each public skill must be listed in `README.md` under its category with a one-sentence description and link to `SKILL.md`.
- Keep skills model- and host-agnostic. Do not depend on a specific provider, CLI, repository, or global config unless the skill is explicitly for that tool.
- When adding host-specific entrypoints such as commands, skills, wrappers, or config loaders, update every supported host surface in the repository in the same change and prefer pointer wrappers for repository skills instead of duplicating instructions.
- For focused skill creation or refactoring, use `gen-skill-creator`.
- For extremely complex long-running skill creation or refactoring, use `gen-long-running-skill-creator`.
- Use Angular commit message format for commits, e.g. `docs: update agent instructions`.
- Do not add a `Co-Authored-By` trailer to commit messages.
