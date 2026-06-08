---
name: eng-agent-init
description: Initialize agent hosts by discovering config, registering skill sources, and configuring requested MCP servers. Use when setting up coding agents, agent host config, skills paths, or MCP servers.
---

# Engineering Agent Init

Use this skill to configure an agent host without assuming one vendor. Register the current skills repository as a skill source and configure requested MCP servers.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and outputs unless the user specifies otherwise.

## Flow

1. Detect the current agent runtime first, then detect other locally installed agent hosts.
2. Locate its config from docs, existing files, CLI output, or user input.
3. Preserve existing providers, models, permissions, agents, commands, and MCP entries.
4. Add the current repository path as a skill path or equivalent skill source.
5. Add repository-managed global entrypoints only for installed hosts, prioritizing the current host.
6. Add requested MCP servers using the host's config shape.
7. Validate config syntax with the host schema or parser when available.
8. Tell the user how to reload the host.

Hard dependencies: target host and writable config path. Ask once if either is unclear.

For workflow rules, read `references/workflow.md`. For host examples, read `references/hosts.md`. For repository-managed global entrypoint sources, read `references/global-entrypoints/`.
