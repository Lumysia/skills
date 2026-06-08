---
name: sys-upgrade
description: Update or upgrade operating-system software. Use when the user asks to refresh package metadata, update software, or upgrade installed software; no software name means upgrade all available packages.
---

# Sys Upgrade

Run the repository skill `sys-software-lifecycle` for an update or upgrade request. If the user does not name specific software, treat the request as a global package-manager upgrade for all available packages.

User request: $ARGUMENTS

Read `/Users/vya/Projects/skills/sys-software-lifecycle/SKILL.md` and follow its referenced files. This wrapper only exposes `sys-upgrade` globally for Agent Skills hosts.
