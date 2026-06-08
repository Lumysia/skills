# Assignment Deliverable Workflow

## Missing Inputs

Do not guess or fabricate missing assignment context. Inspect the workspace, user-provided paths, obvious archives, and relevant existing files first. If a required prompt, rubric, starter file, data file, or template is absent, ask one concise question and stop.

Example:

```text
I found the rubric, but it references starter files I do not have: agents/madrl_agent.py and env.py. Please provide the source folder or its path before I continue.
```

Treat these as hard dependencies when required by the prompt or rubric:

- Assignment prompt or task statement
- Rubric or grading criteria
- Required output format or template
- Starter code, notebook, data, figures, or source documents needed to answer the task
- Submission constraints such as page limit, file naming, allowed tools, or required sections

Treat these as soft dependencies unless the assignment requires them:

- Preferred writing voice
- Extra examples or lecture notes
- Raw experiment logs when final summarized results are sufficient
- Optional formatting preferences not tied to marks or submission acceptance

## Rubric Checklist

Turn the prompt and rubric into a checklist before producing the final deliverable. Include only requirements that can be tied to assignment text, rubric criteria, or user instructions.

Track these items when present:

- Required sections, questions, tables, figures, code files, class names, functions, or notebook cells
- Required evidence, calculations, experiments, metrics, plots, citations, or screenshots
- Required explanations of assumptions, algorithms, limitations, setup, seeds, or reproduction steps
- Formatting constraints such as page count, filename, template fields, export type, and included or excluded files
- Mark-weighted criteria and likely rejection conditions

## Draft Or Implement

Work from real files and assignment wording. Keep changes minimal and aligned with the requested deliverable. Do not introduce broad engineering cleanup, extra frameworks, compatibility layers, or unrelated files unless the assignment requires them.

Do not stop at a partial deliverable just because a required capability is missing. Delegate temporary provisioning, required execution or validation, and cleanup to a subagent. If subagents are unavailable, state that explicitly and do the work in the main flow. The main agent remains responsible for deciding what must be produced, reviewing the result, and reporting any blocker honestly.

For measured or code-backed work:

- Record setup, commands, seeds, and data scope when results depend on execution.
- Keep temporary work outside the submission unless requested.
- Keep intermediates only when requested or needed for reproducibility.
- Prefer reversible, local, or temporary provisioning over lasting system changes.
- Ask or report the blocker when provisioning requires user approval, credentials, licenses, payment, unsafe cleanup, or excessive resources.
- Remove non-submission artifacts after validation unless needed for reproducibility.
- Have the subagent return commands run, artifacts produced, cleanup performed, and unresolved blockers; do not rely on unstated assumptions.
- If subagent delegation is unavailable, state that explicitly before using the main-agent fallback. If delegation fails after starting, report the blocker unless a safe retry or fallback is clearly possible.

## Deliverable Creation

Use the requested template when one is provided. Otherwise, create the requested format directly, such as Markdown, PDF, notebook, source code, slide deck text, or a clean folder of required files.

Before calling the deliverable ready:

- Confirm the final file or folder exists and is readable.
- Confirm the format, filename, and included files match the instructions.
- Confirm all required sections or questions are answered.
- Confirm required code, calculations, conversions, screenshots, exports, or experiments were actually run or produced whenever feasible.
- Confirm no extra files are recommended when the instructions say to submit only one file.

## PDF And Template Handling

Visually or textually inspect generated PDFs before saying they are ready. A PDF is not ready if answers overlap prompt text, appear outside fields, are clipped, land on the wrong page, or omit required content.

If a PDF or locked template cannot be filled reliably, do not fake a visually broken overlay. Mark it as manual-fill required, create a concise fill guide with page or field labels and exact text to paste, and tell the user not to submit the failed generated PDF.

## Independent Rubric Review

Use a fresh subagent for the independent rubric review. This review is mandatory before handoff for finished deliverables, not optional polish. If subagents are unavailable, state that explicitly and perform the review as a separate main-agent pass. If delegation fails after starting, report the blocker unless a safe retry or fallback is clearly possible. Do not review from memory of the drafting process.

Prompt shape:

```text
Review this assignment deliverable independently against the rubric.

Inputs:
- Assignment prompt/rubric: <path or text>
- Final deliverable: <path>
- Relevant source/generated files: <paths>

Task:
- Identify missing, weak, incorrect, unsupported, or likely-to-lose-marks items.
- Mark severity as blocker, major, minor, or note.
- Calibrate severity by the actual submission requirements: blockers and serious majors only for issues likely to invalidate the submission or lose substantial marks.
- Include exact page, section, question, cell, or file references where possible.
- Return findings only, ordered by severity, and state whether it is ready to submit.
```

Severity guide:

- Blocker: missing or unreadable final file, unanswered required section, missing essential input, hard submission-format violation, or likely rejection by the platform.
- Serious major: likely substantial mark loss, such as omitted required function, absent required experiment, contradicted result, broken code snippet, missing core mechanism, or unsupported required claim.
- Minor or note: optional improvements, stricter implementation preferences, missing raw logs when not required, limited but stated experiment scope, parameterized code that still gives requested behavior, or helper-file differences that do not affect the final submission.

Only blockers and serious majors require another review loop. Do not loop on minor or note issues unless the user requests polish.

## Humanization Review

Run a humanization review when the user asks for it or when prose quality is part of the deliverable risk. Keep the pass independent: provide only the current text or file, target use, requested voice, and preservation constraints. Do not include prior edits or change history.

Prompt shape:

```text
Humanize this text for the stated assignment deliverable.

Inputs:
- Current text/file: <path or text>
- Target use: <assignment/report/PDF/notebook/etc.>
- Requested voice: <student/plain technical/formal/etc.>
- Preserve: code, equations, numbers, source references, class/function names, rubric coverage, and factual claims.

Task:
- Rewrite only prose that sounds generic, over-polished, or AI-like.
- Preserve meaning and technical accuracy.
- Do not add new claims, citations, experiments, or evidence.
- Return exact replacement text only where changes are needed.
```

For second and later passes, keep the prompt independent and provide only the current text or file plus constraints.

## Final Handoff

Keep the final response short and practical:

- Final deliverable path
- Checks or commands run
- Temporary provisioning and cleanup performed
- Whether rubric review found remaining blockers or serious majors
- Any real remaining risk, such as manual PDF fill required, unrun experiments, unavailable starter files, or format constraints that could not be verified
