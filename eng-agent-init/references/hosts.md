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

No arbitrary multi-path skill config exists (no `skills.paths` array like opencode). Skill sources are fixed locations:

- User scope: `~/.claude/skills/<name>/`
- Project scope: `<repo>/.claude/skills/<name>/`

**Verified: a bare `SKILL.md` is not enough.** A folder containing only `SKILL.md` (e.g. plain symlinked in) does not get picked up — `claude plugin list` won't show it and invoking it by name errors `Unknown skill`. Each `<name>/` needs its own `.claude-plugin/plugin.json`:

```json
{
  "name": "<name>",
  "version": "0.1.0",
  "description": "<trigger description, matched against user requests>",
  "skills": ["./"]
}
```

`skills` is an array of relative directory paths, each containing its own `SKILL.md` (use `"./"` when `SKILL.md` sits at the plugin root; use a subpath like `"skills/foo"` when it's nested). Object-shaped entries (`{"name":..,"path":..}`) are an old schema and fail validation.

To register this repository's skills at user scope without copying files:

1. Symlink (POSIX: `ln -s`) or junction (Windows: `New-Item -ItemType Junction`) each top-level skill directory — or the whole repo root — into `~/.claude/skills/`.
2. For every skill folder lacking `.claude-plugin/plugin.json`, generate one from that folder's `SKILL.md` frontmatter (`name`, `description`).
3. Verify with `claude plugin list --json` — each entry shows `enabled` and any `errors`. Newly added/fixed manifests are picked up live in an already-running session; no restart required.

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

Claude Code's own project-doc convention is `CLAUDE.md`, separate from `AGENTS.md`. If both this repo's skills and Claude Code's native docs are in play, keep both files rather than assuming one substitutes for the other.

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
