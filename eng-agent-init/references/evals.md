# Agent Init Evals

Use these smoke scenarios to check `eng-agent-init` without modifying real global config. Prefer temporary config files.

---

## Eval: Target Only Current Host

**Prompt:**

```text
Set up this skills repo for OpenCode and add exa MCP.
```

**Expected output:** The agent updates only OpenCode-shaped temporary config, adds this repository as a skill source, adds `exa`, validates syntax, and reports reload instructions.

**Failure indicators:**

- Edits Claude, Codex, or Agent Skills config without being asked.
- Replaces existing provider, permission, model, command, or MCP entries.
- Writes directly to global config during a dry-run or repo-maintenance task.

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
