---
name: eng-agent-init
description: Initialize the current agent host by discovering config, registering skill sources, and configuring requested MCP servers. Use when setting up coding agent config, skill paths, or MCP servers.
---

# Engineering Agent Init

Use this skill to configure an agent host to load this skills repository, repository-managed entrypoints, and requested MCP servers without assuming one provider or host.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and outputs unless the user specifies otherwise.

## Flow

1. Detect the target host from the current runtime, user request, existing config, or installed host directories.
2. Read `references/workflow.md` before editing host config or entrypoints.
3. Locate the target config and preserve existing providers, models, permissions, agents, commands, and MCP entries.
4. Register this repository as a skill source using the host's native config shape.
5. Link repository-managed entrypoints from `references/global-entrypoints/` only for requested or clearly targeted hosts.
6. Add requested MCP servers using the host's native MCP shape.
7. Validate changed config with an available parser or schema, then report reload steps and any unresolved blockers.

Hard dependencies are target host, config scope, writable config or entrypoint destination, and permission to modify user-level config. Do non-destructive discovery first; ask one concise question only when a hard dependency remains unclear.

## Resources

- `references/workflow.md`: execution rules for discovery, config merges, entrypoint linking, MCP setup, validation, and handoff.
- `references/hosts.md`: host-specific examples and common config locations; verify against the active host before editing.
- `references/evals.md`: smoke scenarios for idempotence, host targeting, entrypoint conflicts, MCP preservation, and validation.
- `references/global-entrypoints/`: repository-managed entrypoint templates for supported hosts.
