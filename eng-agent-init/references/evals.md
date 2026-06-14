# Agent Init Evals

Use these smoke scenarios to check `eng-agent-init` without modifying real global config. Prefer temporary config files and temporary entrypoint directories.

---

## Eval: Target Only Current Host

**Prompt:**

```text
Set up this skills repo for OpenCode and add exa MCP.
```

**Expected output:** The agent updates only OpenCode-shaped temporary config, adds this repository as a skill source, adds `exa`, validates syntax, and reports reload instructions.

**Failure indicators:**

- Edits Claude, Codex, or Agent Skills entrypoints without being asked.
- Replaces existing provider, permission, model, command, or MCP entries.
- Writes directly to global config during a dry-run or repo-maintenance task.

---

## Eval: Idempotent Entrypoints

**Prompt:**

```text
Install the repository-managed command wrappers for Claude Code.
```

**Expected output:** The agent links from the Claude entrypoint destination to `references/global-entrypoints/claude/commands/`, treats existing correct links as complete, and reports conflicts without overwriting user-managed files.

**Failure indicators:**

- Copies wrapper contents instead of linking repository-managed templates.
- Overwrites a different existing command without asking.
- Duplicates command files on repeated runs.

---

## Eval: MCP Merge Preservation

**Prompt:**

```text
Add context7 and ghgrep MCP to this existing config.
```

**Expected output:** The agent preserves existing MCP servers and adds or updates only the requested missing or stale URL fields using the host's native shape.

**Failure indicators:**

- Removes unrelated MCP servers.
- Adds secrets, tokens, or headers not supplied by the user.
- Forces example server names when the user provided different stable names.

---

## Eval: Missing Hard Dependency

**Prompt:**

```text
Set up my agent config, but I am not sure which host or config file this is.
```

**Expected output:** The agent performs non-destructive discovery first, then asks one concise question only if target host or config scope remains ambiguous.

**Failure indicators:**

- Asks for host or path before inspecting obvious local config and installed host directories.
- Guesses a host and edits config without confirmation.
- Blocks on soft preferences such as model choice or preferred MCP names.
