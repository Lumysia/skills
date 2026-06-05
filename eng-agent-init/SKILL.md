---
name: eng-agent-init
description: Initialize agent hosts by discovering config, registering skill sources, and configuring requested MCP servers. Use when setting up coding agents, agent host config, skills paths, or MCP servers.
---

# Engineering Agent Init

Use this skill to configure an agent host without assuming one vendor. Register the current skills repository as a skill source and configure requested MCP servers.

## Flow

1. Detect the target agent runtime and version.
2. Locate its config from docs, existing files, CLI output, or user input.
3. Preserve existing providers, models, permissions, agents, commands, and MCP entries.
4. Add the current repository path as a skill path or equivalent skill source.
5. Add requested MCP servers using the host's config shape.
6. Validate config syntax with the host schema or parser when available.
7. Tell the user how to reload the host.

Hard dependencies: target host and writable config path. Ask once if either is unclear.

For workflow rules, read `references/workflow.md`. For host examples, read `references/hosts.md`.
