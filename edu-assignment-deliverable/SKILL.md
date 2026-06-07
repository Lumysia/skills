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
3. Convert the rubric and instructions into a checklist of required sections, files, functions, experiments, evidence, explanations, and formatting constraints.
4. Draft, implement, or fill the deliverable using real files and prompt wording; keep temporary environments, caches, and experiments outside the submission folder unless requested.
5. Create the requested deliverable file and verify it exists, is readable, and matches the requested format.
6. Run an independent rubric review on the final deliverable and relevant source files; fix blockers and serious major issues, then rerun only when necessary.
7. Run an independent humanization review only when requested or clearly needed for prose quality; preserve technical accuracy, rubric coverage, numbers, citations, code, and equations.
8. Hand off the final path, checks run, and any real remaining risk.

Hard dependencies: assignment instructions and required deliverable format. Ask once if either is missing.

For missing-input rules, review prompts, severity calibration, PDF/template handling, and handoff rules, read `references/workflow.md`.
