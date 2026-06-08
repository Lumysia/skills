# Host Examples

These are examples, not fixed requirements. Confirm the current host schema before editing.

## opencode

Global config is usually:

```text
~/.config/opencode/opencode.json
```

Shape with example remote MCP servers:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["/absolute/path/to/skills"]
  },
  "mcp": {
    "exa": {
      "type": "remote",
      "url": "https://mcp.exa.ai/mcp",
      "enabled": true
    },
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "enabled": true
    },
    "ghgrep": {
      "type": "remote",
      "url": "https://mcp.grep.app",
      "enabled": true
    }
  }
}
```

Keep existing provider, permission, plugin, command, and agent fields.

Global command wrappers usually live in:

```text
~/.config/opencode/commands/
```

For repository-managed wrappers, link or copy from `references/global-entrypoints/opencode/commands/` only when OpenCode is installed or `~/.config/opencode/` already exists.

## Claude Code

Claude Code commonly loads skills from user or project skill folders and MCP from its own config commands/files. Discover the current documented method before editing.

If path registration is unsupported, copy only on explicit approval or create a symlink when safe.

Global command wrappers commonly live in:

```text
~/.claude/commands/
```

For repository-managed wrappers, link or copy from `references/global-entrypoints/claude/commands/` only when Claude Code is installed or `~/.claude/` already exists.

## Codex

Codex primarily uses instruction files such as `AGENTS.md`; skill and MCP support may depend on runtime or wrapper. Discover the active config and adapt.

If native skills are unsupported, add a concise `AGENTS.md` pointer to this skills repository only when the user asks.

Codex uses Agent Skills for reusable workflows. User-level portable Agent Skills usually live in:

```text
~/.agents/skills/
```

Codex-specific user skills may live in:

```text
~/.codex/skills/
```

For repository-managed wrappers, link or copy from `references/global-entrypoints/agents/skills/` or `references/global-entrypoints/codex/skills/` only when Codex or a compatible Agent Skills host is installed or already configured.

## Other Hosts

Use the same contract:

- register this directory as the skill source,
- add selected MCP servers using native syntax,
- preserve existing config,
- validate,
- tell the user how to reload.
