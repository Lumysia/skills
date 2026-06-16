# Host Reference

These are examples and common locations, not fixed requirements. Confirm the current host schema before editing.

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

## Claude Code

Claude Code commonly loads skills from user or project skill folders and MCP from its own config files. Discover the current documented method before editing.

If path registration is unsupported, create a symlink when safe or copy only with explicit approval.

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

Use host-native skill source registration when available. If the host requires user-level skill folders, link from this repository only when Codex or a compatible Agent Skills host is installed, already configured, or explicitly requested.

## Other Hosts

Use the same contract:

- register this directory as the skill source,
- add selected MCP servers using native syntax,
- preserve existing config,
- validate,
- tell the user how to reload.
