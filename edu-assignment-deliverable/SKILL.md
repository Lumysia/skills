---
name: edu-assignment-deliverable
description: Create course assignment deliverables from prompts, rubrics, source materials, templates, and submission rules. Use for rubric-graded coursework artifacts in any required format.
---

# Education Assignment Deliverable

Use this skill to produce a finished course assignment deliverable that follows the user's prompt, rubric, source materials, template, and submission constraints.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, assignment prompt, source materials, template, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and deliverable prose unless the user specifies otherwise.

## Flow

The active agent coordinates the workflow directly: gather inputs, identify candidate files, build the checklist, delegate checks to subagents, apply focused fixes, and hand off the final submission state.

1. Gather the prompt, rubric, required deliverable format, submission constraints, source materials, templates, target voice, and validation expectations.
2. Check required inputs before drafting or building; ask one concise question and stop if an essential hard dependency is missing. Treat source materials, templates, and rubrics as hard dependencies only when the prompt or grading criteria require them.
3. If deliverable files already exist, inspect only enough to identify candidate paths and classify the work as partial, complete-but-unverified, or ready. Do not rebuild existing work by default; delegate detailed content, evidence, formatting, execution, export, and artifact checks to the Deliverable Check Agent, then continue only from the missing, weak, or noncompliant parts.
4. Convert the rubric and instructions into a checklist, then build or revise the deliverable from real files and prompt wording.
5. If the Deliverable Check Agent reports missing validation dependencies, launch the Environment Setup Agent before reporting blocked validation. The Environment Setup Agent must provision a temporary local environment when safe, run the required checks or exports, clean up, and return exact commands, artifacts, cleanup, and unresolved blockers.
6. Remove unnecessary content that is not required by the assignment prompt, rubric, requested format, clean submission, execution, verification, or reproducibility. Keep useful support content even when it is not named explicitly, if it is needed to run, submit, verify, or understand the required work.
7. Verify the deliverable exists, is readable, matches the requested format, and has been validated whenever feasible.
8. Run an independent rubric review using the Rubric Review Agent. If subagents are unavailable, state that explicitly and review in a separate main-agent pass. Fix blockers and major issues.
9. Run the Humanization Agent only when requested or clearly needed; preserve factual accuracy, assignment voice, and required evidence.
10. Hand off the final path, checks run, review status, remaining risks, user TODOs, and next step.

Hard dependencies: assignment instructions and required deliverable format. Ask once if either is missing.

For missing-input rules, subagent routing, temporary provisioning, severity calibration, template handling, cleanup, and handoff rules, read `references/workflow.md`. For exact worker subagent roles and prompt templates, read `references/subagents.md`.

When launching a worker subagent, the active agent must first read `references/subagents.md`, select the matching role template, and paste the full template text into the Task prompt with all placeholders replaced by concrete paths, constraints, validation goals, prior findings, and non-modification rules. Do not ask a worker subagent to read `references/subagents.md`, infer its own role, or operate from a shortened summary prompt.
