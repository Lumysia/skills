# AGENTS.md

- Skill names use `<category>-<purpose>`: e.g. `eng-security-assessment`, `sci-write-review`. Keep names explicit; avoid unclear abbreviations.
- Use short category prefixes in skill names; do not create category folders just for organization.
- Be concise: one sentence beats two, one word beats several, and empty phrasing is not allowed.
- Each skill is self-contained: `SKILL.md` is the short index, detailed instructions live under `references/`.
- Each public skill must be listed in `README.md` under its category with a one-sentence description and link to `SKILL.md`.
- Keep skills model- and host-agnostic. Do not depend on a specific provider, CLI, repository, or global config unless the skill is explicitly for that tool.
- Distinguish hard dependencies from soft dependencies. Hard dependencies must be collected or confirmed before execution; soft dependencies should improve output but must not cause repeated user prompts or block progress.
- Use Angular commit message format for commits, e.g. `docs: update agent instructions`.
