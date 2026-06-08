# Agent Host Init Workflow

## Scope

Configure the target agent host to use this skills directory and MCP servers.

Do not configure model providers, API keys, permissions, prompts, themes, telemetry, or global shell settings unless the user asks.

## Skill Directory

Use the current skills repository path as the skill source.

Rules:

- Prefer absolute paths for global host config.
- Prefer relative paths only for project-local config.
- Preserve existing skill paths and URLs unless the user asks to replace them.
- Do not copy skill files into another directory unless the host cannot load paths.
- After editing config, tell the user to restart or reload the host.

## Global Entrypoints

Setup is idempotent: it may be run repeatedly to detect missing pieces and fill gaps without duplicating entries or overwriting user-managed files.

Rules:

- Default to the agent host currently running the setup request.
- Install or link entrypoints only for the target host unless the user explicitly names additional hosts.
- Do not inspect or create entrypoints for other hosts just because this repository supports them.
- Use repository-managed sources under `references/global-entrypoints/`.
- Prefer symlinks from global host locations to repository-managed source files when the host supports them.
- If symlinks are not safe or supported, copy only missing files and preserve existing different files.
- Treat an existing correct symlink or identical file as complete.
- If an existing destination differs from the repository source and is not a managed symlink, report the conflict and ask before replacing it.
- For commands that invoke repository skills, keep wrappers as pointers and do not duplicate skill instructions.
- After syncing entrypoints, tell the user which target host was updated or skipped due to conflicts.

## MCP Servers

Start from user-requested servers. If the user asks for a default research/code-search setup, this catalog is a useful seed:

```text
exa       https://mcp.exa.ai/mcp
context7  https://mcp.context7.com/mcp
ghgrep    https://mcp.grep.app
```

Rules:

- Use the host's native MCP shape.
- Prefer user-requested MCP servers over examples.
- Keep server names short and stable.
- Enable selected remote MCP servers by default when the host supports remote MCP and policy allows it.
- Preserve existing server entries; update only missing or obviously stale URL fields.
- Do not add secrets or Authorization headers unless the user provides them for that server.

## Hard Dependencies

Ask once when missing:

- target host,
- global vs project config,
- config path if discovery fails,
- whether live remote MCP connections are allowed when policy is unclear.

Soft dependencies must not block progress: preferred server names, additional MCP servers, model choice, permission policy, custom agents, or UI settings.

## Validation

- Parse JSON/JSONC/YAML/TOML with an available parser.
- If the host publishes a schema, validate against it.
- If no parser is available, preserve formatting and report that validation is manual.
- Never overwrite config wholesale when a targeted merge is possible.
