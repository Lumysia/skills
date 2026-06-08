---
name: sys-software-lifecycle
description: Install, update, uninstall, and clean operating-system software across platforms. Use when the user wants package-manager commands, clean removal, leftover cleanup, or reinstall preparation.
---

# System Software Lifecycle

Use this skill to manage software installation, update, uninstall, and cleanup on an operating system without assuming one platform, package manager, installer type, or cleanup model.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and outputs unless the user specifies otherwise.

## Flow

1. Identify the OS, software name, install source, current state, and requested operation.
2. Search package managers, official vendor sources, source repositories, and release channels before choosing an install or update source.
3. Read the matching platform reference when available: `references/macos.md`, `references/windows.md`, or `references/linux.md`; adapt when the host platform or package manager differs.
4. Build a dry-run style plan showing source choice, lifecycle actions, candidate leftovers, risk level, and rollback options.
5. Execute only confirmed writes or deletes; prefer reversible moves for user data and caches.
6. Run standard package-manager cleanup for the platform after install, update, or uninstall when appropriate.
7. Record performed operations, verify the final state, and report remaining manual checks.

Hard dependencies: target OS, software identifier, operation, and whether user data should be preserved or removed. Ask once if any hard dependency is missing.

For cross-platform lifecycle rules, read `references/workflow.md`. For operation records, read `references/operation-log.md`. For platform-specific managers and cleanup locations, read the relevant platform reference as examples and verify current behavior before acting.
