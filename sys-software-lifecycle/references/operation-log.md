# Operation Log

## Purpose

Maintain a lightweight record when performing real software lifecycle changes so the user can audit what changed, repeat it, or undo it later.

## When To Log

- Log actual installs, updates, uninstalls, service changes, startup changes, cache cleanup, leftover moves, and confirmed deletes.
- Do not require a log for pure research, dry-run planning, or read-only discovery unless the user asks.
- If no log path is obvious, use the platform's durable per-user state or application-data directory, not the current working directory.
- Use a machine-wide log location only for machine-wide operations and only after confirming the path with the user.

## Default Locations

- macOS user log: `~/Library/Application Support/sys-software-lifecycle/software-lifecycle-log.md`.
- Windows user log: `%LOCALAPPDATA%\sys-software-lifecycle\software-lifecycle-log.md`.
- Linux user log: `${XDG_STATE_HOME:-~/.local/state}/sys-software-lifecycle/software-lifecycle-log.md`.
- macOS machine-wide log: `/Library/Application Support/sys-software-lifecycle/software-lifecycle-log.md` when admin scope is confirmed.
- Windows machine-wide log: `%ProgramData%\sys-software-lifecycle\software-lifecycle-log.md` when admin scope is confirmed.
- Linux machine-wide log: `/var/log/sys-software-lifecycle/software-lifecycle-log.md` when admin scope is confirmed.

## Location Rules

- Create the parent directory if it does not exist.
- Avoid temporary folders, downloads folders, project worktrees, desktop paths, and package-manager cache directories.
- Keep the log outside software-specific leftover paths so uninstall cleanup does not remove the operation history.
- If the selected path is not writable, fall back to the user log path before asking for a custom path.

## What To Record

- Date, OS, hostname when available, and user-provided goal.
- Software name, resolved identifiers, selected source, selected version, and rejected alternatives with brief reasons.
- Commands run or manual steps performed.
- Paths changed, moved, deleted, preserved, or skipped.
- Services, agents, daemons, scheduled tasks, startup entries, registry keys, or package records changed.
- Verification results and remaining manual checks.
- Rollback notes, backup paths, Trash or Recycle Bin locations, and restart requirements.

## Format

Use append-only Markdown entries:

```markdown
## 2026-06-07 - <software> - <operation>

- OS: <platform and version>
- Goal: <user request>
- Source decision: <chosen source/version and why>
- Actions: <commands or manual steps>
- Cleanup: <paths or records changed>
- Verification: <version/status checks>
- Rollback: <backup, trash, restore, or reinstall notes>
```

## Safety

- Never write secrets, license keys, auth tokens, private URLs, or personal file contents into the log.
- Redact user names in paths only if the user requests shareable output; keep local paths precise when the log is for the same machine.
- If an operation fails halfway, log the failure and the observed state before retrying.
