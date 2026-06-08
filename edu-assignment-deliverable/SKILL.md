---
name: edu-assignment-deliverable
description: Create course assignment deliverables from prompts, rubrics, starter files, and templates. Use for homework reports, notebooks, code answers, PDFs, and rubric-graded coursework artifacts.
---

# Education Assignment Deliverable

Use this skill to produce a finished course assignment deliverable that follows the user's prompt, rubric, source files, template, and submission constraints.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, assignment prompt, source files, template, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and deliverable prose unless the user specifies otherwise.

## Flow

1. Gather the prompt, rubric, required deliverable format, submission constraints, starter files, data, templates, target voice, and validation expectations.
2. Check required inputs before drafting or coding; ask one concise question and stop if an essential prompt, rubric, starter file, data file, or template is missing.
3. Convert the rubric and instructions into a checklist, then build the deliverable from real files and prompt wording.
4. If a required capability is missing, delegate temporary provisioning, required execution, and cleanup to a subagent. If subagents are unavailable, state that explicitly and do it in the main flow.
5. Verify the deliverable exists, is readable, matches the requested format, and has been validated whenever feasible.
6. Run an independent rubric review using a fresh subagent. If subagents are unavailable, state that explicitly and review in a separate main-agent pass. Fix blockers and serious major issues.
7. Run humanization only when requested or clearly needed; preserve technical accuracy and required evidence.
8. Hand off the final path, checks run, cleanup performed, review status, and real remaining risks.

Hard dependencies: assignment instructions and required deliverable format. Ask once if either is missing.

For missing-input rules, temporary provisioning, review prompts, severity calibration, template handling, cleanup, and handoff rules, read `references/workflow.md`.
