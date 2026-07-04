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

Claude Code does not support path-based skill source registration. It loads skills from:

- Project scope: `<repo>/.claude/skills/<name>/SKILL.md`
- User scope: `~/.claude/skills/<name>/SKILL.md`

To register this repository's skills at user scope without copying files, symlink each top-level skill directory (the ones containing `SKILL.md`) into `~/.claude/skills/`:

```bash
for d in /absolute/path/to/skills/*/; do
  name="$(basename "$d")"
  [ -f "$d/SKILL.md" ] && ln -s "${d%/}" "$HOME/.claude/skills/$name"
done
```

Skip any name that already exists under `~/.claude/skills/`. Only copy instead of symlinking with explicit user approval.

MCP servers are configured in `~/.claude.json`:

- User scope (global): top-level `"mcpServers"` object in `~/.claude.json`.
- Project scope, local to this machine: `"mcpServers"` inside `projects["<absolute-repo-path>"]` in `~/.claude.json`.
- Project scope, shared via git: `.mcp.json` at the repo root with the same shape.

Remote HTTP/SSE servers use this shape (matches `claude mcp add --transport http`):

```json
{
  "mcpServers": {
    "context7": { "type": "http", "url": "https://mcp.context7.com/mcp" },
    "ghgrep": { "type": "http", "url": "https://mcp.grep.app" },
    "exa": { "type": "http", "url": "https://mcp.exa.ai/mcp" }
  }
}
```

Edit the JSON with a parser (not a raw text patch) to avoid corrupting the surrounding config, and back up the file first since it also holds unrelated user state (auth, caches, per-project settings).

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
