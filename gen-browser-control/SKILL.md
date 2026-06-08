---
name: gen-browser-control
description: Browser control via Playwright MCP extension mode. Use when controlling existing Chrome, Edge, or Chromium-family tabs, logged-in sessions, or installed extensions.
---

# General Browser Control

Use this skill when the user wants an agent to browse, search, inspect, test, debug, translate, or automate a real browser session through Playwright MCP extension mode.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and outputs unless the user specifies otherwise.

Infer the target browser before asking: use the user's wording, an already connected extension tab, existing MCP configuration, or the currently opened page. Ask for the browser only when inference fails or when changing host configuration for a real browser profile.

## Flow

1. Parse `/browser` arguments as the browser task: open/search/navigate, inspect, test, debug, translate, extract, or operate a page.
2. Identify the target browser from context when possible; confirm only if ambiguous or before changing host configuration for a live profile.
3. Ensure the Playwright MCP Bridge extension is installed and enabled in the target browser profile.
4. Reuse an existing working Playwright MCP extension-mode entry; otherwise configure the agent host to run `npx @playwright/mcp@latest --extension`, adding browser path flags when the target is not the default Chrome or Edge profile.
5. Route specialized tasks to their reference files; for translation, read `references/translation.md` before operating the page.
6. Ask the user to open the target page or tab and approve/select it on first connection only when no suitable tab is already available.
7. Smoke-test control with a read-only action such as taking a snapshot, reading the URL, or identifying the page title.
8. Use accessibility snapshots and stable element references before clicking, typing, editing, or asserting page state.
9. Pause for confirmation before submitting forms, changing account state, making purchases, deleting data, or exposing secrets.
10. Report the tab used, actions taken, verification evidence, and any manual follow-up.

Hard dependencies: target browser, target page or task, installed extension, and an MCP-capable agent host. Ask once if any are missing.

For setup, operating workflow, and safety rules, read `references/workflow.md`. For translation tasks, also read `references/translation.md`.
