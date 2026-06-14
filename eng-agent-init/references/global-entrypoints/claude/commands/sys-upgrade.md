---
description: Update or upgrade operating-system software using the repository lifecycle skill; no software name means upgrade all available packages.
---

Run the repository skill `sys-software-lifecycle` for an update or upgrade request. If the user does not name specific software, treat the request as a global package-manager upgrade for all available packages.

User request: $ARGUMENTS

Read `sys-software-lifecycle/SKILL.md` from the registered skills repository and follow its referenced files. This wrapper only exposes `/sys-upgrade` globally for Claude Code.
