# Parallel Worktree Workflow

Use git worktrees when parallel work is likely to save more time than conflict resolution costs.

## When To Use

Use parallel worktrees for independent subtasks, competing implementations, risky changes where backups help, design exploration, and fresh-context review.

Use sequential work for tightly coupled refactors, shared contract changes that many files depend on, or edits that target the same files.

## Setup

Command snippets are examples; adapt shell syntax, paths, and base branch names to the repository and environment.

Create `.worktrees/` and ignore it if the repository does not already do so:

```sh
mkdir -p .worktrees
printf "\n.worktrees/\n.agent-status/\n" >> .gitignore
```

Create one worktree per branch:

```sh
git fetch origin
git worktree add .worktrees/task-api -b task-api <base-branch>
git worktree add .worktrees/task-ui -b task-ui <base-branch>
git worktree list
```

For competing implementations of the same task:

```sh
git worktree add .worktrees/search-1 -b search-1 <base-branch>
git worktree add .worktrees/search-2 -b search-2 <base-branch>
git worktree add .worktrees/search-3 -b search-3 <base-branch>
```

Copy only non-secret local setup files when needed; do not copy credentials into shared or committed paths.

## Agent Prompt Template

Give each agent explicit boundaries:

```markdown
Work in `.worktrees/<task>/` only.

Goal: <specific outcome>

Scope:
- Modify only <paths or components> unless required for tests.
- Do not touch unrelated files.

Verification:
- Run `<test command>` if available.
- If verification cannot run, explain why.

Completion:
- Write `.worktrees/<task>/RESULTS.md` with summary, changed files, verification, risks, and follow-ups.
- Leave the worktree in a reviewable git state.
```

If agents are asynchronous, also ask them to write `.agent-status/<task>.json` from the orchestrating worktree root:

```json
{
  "status": "COMPLETE",
  "worktree": ".worktrees/task-api",
  "branch": "task-api",
  "summary": "Implemented API endpoints and tests",
  "verification": "<verification command> passed"
}
```

Allowed statuses are `RUNNING`, `COMPLETE`, `FAILED`, and `BLOCKED`.

## Coordination Patterns

Competitive implementation: run several agents on the same prompt, compare quality, tests, edge cases, and maintainability, then merge the strongest result or cherry-pick pieces.

Divide and conquer: split a feature into independent tracks, such as database, API, UI, and docs; merge dependency branches first.

Test-first parallel: one worktree writes failing tests, implementation worktrees branch from that test branch and race to satisfy the same suite.

Review pipeline: one agent implements, another fresh-context agent reviews the same worktree before merge.

Exploration sprint: assign each worktree a different architecture and require an `APPROACH.md` or `RESULTS.md` tradeoff summary.

## Status Checks

Inspect all worktrees:

```sh
git worktree list
```

Inspect one worktree against the base branch:

```sh
git -C .worktrees/task-api status --short
git -C .worktrees/task-api diff --stat <base-branch>...HEAD
git -C .worktrees/task-api log --oneline <base-branch>..HEAD
```

Read result summaries before diff review:

```sh
find .worktrees -name RESULTS.md -maxdepth 2 -print
```

Check status files when present:

```sh
find .agent-status -name "*.json" -maxdepth 1 -print
```

## Merge Rules

Before merging, require a clean or intentionally committed worktree, a written result summary, and verification notes.

Review diffs from the orchestrating worktree:

```sh
git diff --stat <base-branch>...task-api
git diff <base-branch>...task-api
```

Merge completed branches in dependency order:

```sh
git merge task-api
```

If only part of a result is useful, prefer a small manual patch or cherry-pick over merging unwanted changes.

After every merge, rerun the relevant verification in the orchestrating worktree.

## Cleanup

Remove merged or rejected worktrees only after confirming no needed work remains:

```sh
git worktree remove .worktrees/task-api
git branch -d task-api
git worktree prune
```

Use force removal only when the user explicitly accepts losing uncommitted work:

```sh
git worktree remove --force .worktrees/task-api
```

## Pitfalls

Avoid parallel edits to the same files, untracked environment drift, local resource conflicts, uncommitted work before merge, and branches based on a stale base.

Do not treat a background agent status as proof of correctness; verify the selected result in the orchestrating worktree.
