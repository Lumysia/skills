---
name: eng-parallel-worktrees
description: Coordinate parallel engineering work across git worktrees and independent agents. Use when splitting tasks across isolated branches, comparing multiple implementations, running background agents, or merging worktree results.
---

# Engineering Parallel Worktrees

Use this skill to run independent engineering tracks in isolated git worktrees, then review and integrate the best results.

Adapted from [SpillwaveSolutions/parallel-worktrees](https://github.com/spillwavesolutions/parallel-worktrees), generalized to avoid depending on one agent host.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and outputs unless the user specifies otherwise.

## Flow

1. Confirm the task can be split without heavy file overlap or sequential dependency risk.
2. Create one branch and worktree per task or candidate implementation under `.worktrees/`.
3. Give each agent bounded instructions, including its worktree path, scope, verification command, and result file.
4. Track progress with `RESULTS.md` in each worktree and optional `.agent-status/<task>.json` files.
5. Compare diffs, verification output, and result notes before selecting work to merge.
6. Merge in dependency order, rerun verification in the orchestrating worktree, then clean up worktrees.

Hard dependencies: a git repository and a base branch. Ask once if the base branch is unclear.

For setup commands, coordination patterns, merge checks, and cleanup rules, read `references/workflow.md`.
