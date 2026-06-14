# Project Init Evals

Use these smoke scenarios to check `eng-project-init` without needing a large repository.

---

## Eval: New AGENTS.md From Evidence

**Prompt:**

```text
Initialize this project for agent use.
```

**Expected output:** The agent inspects project files, creates a concise `AGENTS.md`, and includes only rules supported by repo evidence or explicit user instructions.

**Failure indicators:**

- Adds generic coding philosophy not tied to the project.
- Creates `CLAUDE.md`, ADRs, glossaries, or setup docs without being asked.
- Asks for test commands before checking README, scripts, CI, or config files.

---

## Eval: Existing Guidance Cleanup

**Prompt:**

```text
Refresh the existing AGENTS.md for this repo.
```

**Expected output:** The agent uses existing `AGENTS.md` as the base, preserves still-valid project rules, removes obsolete or duplicate guidance, and tightens vague instructions.

**Failure indicators:**

- Replaces valid project-specific rules with a generic template.
- Keeps placeholders such as `<test command>` or vague rules like "write good code".
- Adds unrelated rules copied from another repository.

---

## Eval: Conflicting Evidence

**Prompt:**

```text
Add agent instructions including the package manager and test command.
```

**Expected output:** The agent inspects lockfiles, scripts, CI, and docs. If evidence conflicts, it asks one concise question for the blocking choice instead of guessing.

**Failure indicators:**

- Chooses a package manager despite conflicting lockfiles and no project evidence.
- Adds a test command that does not appear in scripts, docs, CI, or config.
- Blocks on soft preferences unrelated to the requested instructions.

---

## Eval: Scoped Project Root

**Prompt:**

```text
Initialize the frontend package for agent work.
```

**Expected output:** The agent scopes inspection and `AGENTS.md` changes to the frontend package unless existing root guidance requires a root-level update.

**Failure indicators:**

- Writes root-wide rules for a package-scoped request.
- Ignores a nested existing `AGENTS.md`.
- Applies backend commands or conventions to the frontend package without evidence.
