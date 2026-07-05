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

**Verified: a bare `SKILL.md` is not enough.** A folder with only `SKILL.md` (e.g. plain symlinked in) is invisible to Claude Code — `claude plugin list` won't show it, and invoking it errors `Unknown skill`. Each `<name>/` needs `.claude-plugin/plugin.json`:

```json
{
  "name": "<name>",
  "version": "0.1.0",
  "description": "<trigger description, matched against user requests>",
  "skills": ["./"]
}
```

`skills` is an array of directory paths, each holding a `SKILL.md` — `"./"` if it's at the plugin root, `"skills/foo"` if nested. Object-shaped entries (`{"name":..,"path":..}`) are an old schema and fail validation.

To register this repo's skills at user scope:

1. Symlink/junction each skill directory, or the whole repo root, into `~/.claude/skills/`. Skip names that already exist there; copy instead of linking only with explicit approval.
2. Add `.claude-plugin/plugin.json` to any folder missing one, generated from its `SKILL.md` frontmatter.
3. Verify with `claude plugin list --json` (`enabled`/`errors` per entry) — picked up live, no restart needed.

MCP servers live in `~/.claude.json`:

- Global: top-level `"mcpServers"`.
- Project, local-only: `"mcpServers"` inside `projects["<absolute-repo-path>"]`.
- Project, shared via git: `.mcp.json` at repo root, same shape.

Remote HTTP/SSE shape (matches `claude mcp add --transport http`):

```json
{
  "mcpServers": {
    "context7": { "type": "http", "url": "https://mcp.context7.com/mcp" }
  }
}
```

Edit via a JSON parser, not a text patch — `~/.claude.json` also holds unrelated user state (auth, caches, settings) that a bad patch can corrupt. Back it up first.

`CLAUDE.md` is Claude Code's own doc convention, separate from `AGENTS.md` — keep both rather than assuming one substitutes for the other.

### Telemetry / non-essential traffic opt-out

Only apply when the user explicitly asks. Merge into the target `settings.json` (user scope: `~/.claude/settings.json`):

```json
{
  "env": {
    "DISABLE_TELEMETRY": "1",
    "DISABLE_ERROR_REPORTING": "1",
    "DISABLE_AUTOUPDATER": "1",
    "DISABLE_BUG_COMMAND": "1",
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1"
  },
  "autoUploadSessions": false,
  "feedbackSurveyRate": 0
}
```

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
