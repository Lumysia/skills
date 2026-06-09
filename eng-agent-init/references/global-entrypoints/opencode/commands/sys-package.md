---
description: Install, update, upgrade, uninstall, or clean operating-system software using the repository lifecycle skill.
---

Run the repository skill `sys-software-lifecycle` for the requested package-management operation.

User request: $ARGUMENTS

Read `sys-software-lifecycle/SKILL.md` from the skills repository registered in OpenCode `skills.paths` and follow its referenced files. Infer the package-management action from the user request and ask once only if the action cannot be inferred. This wrapper only exposes `/sys-package` globally for OpenCode.
