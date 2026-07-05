---
name: gen-skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, optimize, package, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# General Skill Creator

Use this skill to create, refine, evaluate, package, and maintain portable skills for agent workflows.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, source text, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and outputs unless the user specifies otherwise.

## Flow

1. Capture the intended task, trigger conditions, expected outputs, hard dependencies, and success criteria.
2. Study this creator skill's own structure and file content patterns before designing the target skill: `SKILL.md` as the short entrypoint, `agents/` as reusable agent files, `references/` as shared schemas and examples, `scripts/` as repeatable tooling, and `assets/` as reusable static material.
3. Read the target skill's relevant files before editing; use search only to find candidates, not as a substitute for reading structure and content.
4. Inspect any existing target skill, examples, files, or repo conventions before drafting changes.
5. Draft or update `SKILL.md` with concise frontmatter, a clear startup rule, and only the instructions needed for the workflow.
6. Move detailed guidance into `references/`, repeatable operations into `scripts/`, reusable materials into `assets/`, and reviewer prompts into `agents/` when useful.
7. Create realistic test prompts when behavior is verifiable; skip heavy evals for subjective or one-off drafting unless the user wants them.
8. Run the smallest useful validation loop, compare outputs against the success criteria, and revise until the user is satisfied.
9. Package or present the final skill only after the user accepts the behavior and metadata.

## Skill Shape

Keep skills self-contained and progressively disclosed:

```text
skill-name/
├── SKILL.md
├── references/
├── scripts/
├── assets/
└── agents/
```

`SKILL.md` should be the short index: frontmatter, startup rule, core flow, dependency notes, and pointers to optional resources. Put long schemas, examples, and implementation details in supporting files. Keep new and revised instructions concise; merge similar rules and remove filler.

## Metadata

- `name`: Use a short, explicit identifier that matches the repository naming convention.
- `description`: State what the skill does and when to use it; include enough trigger context for an agent to select it reliably.
- `compatibility`: Add only when the skill has real host, tool, model, or runtime requirements.

## Evaluation

For verifiable workflows, create a small `evals/evals.json` with realistic prompts and expected outcomes. Add objective assertions only when they can be checked consistently; use human review for subjective writing, design, strategy, or judgment-heavy outputs.

When comparing versions, keep outputs in a workspace next to the skill, separated by iteration and test case. Record prompts, produced files, timing or token data if available, grades, and user feedback so later changes can be traced.

Use the bundled resources when they fit the environment:

- `references/schemas.md` defines example JSON structures for evals, grading, and benchmarks.
- `agents/grader.md`, `agents/comparator.md`, and `agents/analyzer.md` provide reviewer prompts for assessment workflows.
- `scripts/quick_validate.py` sanity-checks a skill's frontmatter and structure.
- `scripts/run_eval.py` and `scripts/run_loop.py` run trigger evals for a skill description, optionally looping with `scripts/improve_description.py` until they pass.
- `scripts/aggregate_benchmark.py` and `scripts/generate_report.py` turn raw benchmark/loop runs into summary stats and an HTML report.
- `eval-viewer/generate_review.py` can build a human review UI for saved eval outputs.
- `scripts/package_skill.py` packages a skill folder into a distributable archive.

## Improvement

When revising a skill, generalize from observed failures instead of overfitting to one prompt. Prefer clearer intent, better resource placement, and reusable deterministic helpers over long instruction lists. Remove instructions that cause wasted work, ambiguity, or unnecessary host coupling.

After the skill is stable, review the frontmatter description for trigger accuracy: it should activate for relevant multi-step or specialized requests and avoid adjacent but unrelated tasks.
