# Agent Host Init Workflow

Configure a target agent host to use this skills repository and requested MCP servers while preserving existing user configuration.

## Scope

Default to the host currently running the request. Configure additional hosts only when the user names them.

Do not change model providers, API keys, permissions, prompts, themes, telemetry, shell profiles, or global package-manager state unless the user explicitly asks.

Do not write directly to global host config or global entrypoint directories unless the user asked to install or update setup now. For repo maintenance work, update only the templates under `references/global-entrypoints/`.

## Discovery

1. Identify the target host and config scope from the runtime, user request, known config files, installed host directories, or user-provided path.
2. Read the existing config before editing. If multiple configs could apply, ask one concise disambiguation question.
3. Identify whether the host supports path-based skills, copied skills, command wrappers, native MCP config, and remote MCP URLs.
4. Read `references/hosts.md` for examples, but verify the active host shape before editing.

Hard dependencies are target host, global vs project scope, writable config or entrypoint path, and permission to modify user-level config. Preferred server names, additional MCP servers, model choices, permission policy, custom agents, and UI settings are soft dependencies.

## Skill Source

Use the current repository root as the skill source.

Rules:

- Prefer absolute paths for global config and relative paths only for project-local config.
- Preserve existing skill paths, URLs, and source lists unless the user asks to replace them.
- Do not copy skill files unless the host cannot load paths and the user approves copying.
- Keep path registration host-agnostic; do not mention a specific provider unless configuring that host.

## Entrypoints

Setup is idempotent: reruns fill missing pieces without duplicating entries or overwriting user-managed files.

Rules:

- Link entrypoints only for the target host unless the user names additional hosts.
- Use repository-managed sources under `references/global-entrypoints/`.
- Prefer symlinks from host entrypoint locations to repository-managed source files or directories.
- On Windows, if file symlinks require elevation, use an NTFS directory junction for the containing entrypoint directory with `cmd /c mklink /J <global-entrypoint-dir> <repo-entrypoint-dir>`.
- Never copy repository-managed entrypoints as a fallback; use another link type or report a blocker.
- Treat an existing correct symlink, junction, or identical file as complete.
- If a destination differs and is not a managed link, report the conflict and ask before replacing it.
- Keep wrappers as pointers to repository skills; do not duplicate skill instructions in wrapper files.

## MCP Servers

Start from user-requested servers. If the user asks for a default research or code-search setup, this catalog is a useful seed:

```text
exa       https://mcp.exa.ai/mcp
context7  https://mcp.context7.com/mcp
ghgrep    https://mcp.grep.app
```

Rules:

- Use the host's native MCP shape and preserve existing server entries.
- Prefer user-requested MCP servers over examples.
- Keep server names short and stable.
- Enable selected remote MCP servers by default only when the host supports remote MCP and policy allows it.
- Update only missing or clearly stale URL fields.
- Do not add secrets, tokens, or Authorization headers unless the user provides them for that server.

## Validation And Handoff

- Parse JSON, JSONC, YAML, or TOML with an available parser after editing.
- Validate against the host schema when one is available.
- If no parser or schema is available, preserve formatting and report manual validation.
- Never overwrite config wholesale when a targeted merge is possible.
- Report changed files, entrypoints linked or skipped, MCP servers added or left untouched, validation attempted, blockers, and reload instructions.
