# Assignment Deliverable Workflow

## Missing Inputs

Do not guess or fabricate missing assignment context. Inspect the workspace, user-provided paths, obvious archives, and relevant existing files first. If an input that the prompt or grading criteria make essential is absent, ask one concise question and stop.

Treat these as hard dependencies when required by the prompt or rubric:

- Assignment prompt or task statement
- Rubric or grading criteria
- Required output format or template
- Source materials needed to answer or build the task
- Submission constraints such as page limit, file naming, allowed tools, or required sections

Treat these as soft dependencies unless the assignment requires them:

- Preferred writing voice
- Extra reference materials
- Raw logs or intermediate materials when final summarized results are sufficient
- Optional formatting preferences not tied to marks or submission acceptance

## Existing Work And Resume

When assignment files or deliverables already exist, inspect them before creating or replacing anything. Determine whether the current work is partial, complete but unverified, or ready.

- If the work is partial, continue from the missing or weak requirements rather than rebuilding completed parts.
- If the work appears complete but unverified, run the required validation and independent review before editing.
- If the work appears ready, run the check/review agents first and only edit if they find blockers, major issues, or user-requested changes.
- Preserve useful existing files unless they conflict with the assignment, fail validation, or add unnecessary submission content.
- Do not overwrite existing user work just to make it match a preferred structure.

## Rubric Checklist

Turn the prompt and rubric into a checklist before producing the final deliverable. Include only requirements that can be tied to assignment text, rubric criteria, or user instructions.

Track any required items when present:

- Required sections, questions, artifacts, named components, or structured fields
- Required evidence, calculations, execution results, measurements, references, or captured outputs
- Required explanations of assumptions, methods, limitations, setup, parameters, or reproduction steps
- Formatting constraints such as length, filename, template fields, export type, and included or excluded content
- Mark-weighted criteria and likely rejection conditions

## Subagent Routing

The active agent coordinates the assignment workflow directly. It gathers inputs, identifies files, builds the checklist, applies focused fixes, and makes final handoff decisions. It should not perform detailed deliverable validation or final rubric review itself while subagents are available.

Use the prompt templates in `references/subagents.md` for every delegated role. Do not rely on ad hoc prompts for the core workflow agents.

Required delegation points:

- Launch Deliverable Check Agent before declaring existing work ready, complete-but-unverified, or blocked by validation.
- Launch Environment Setup Agent when Deliverable Check Agent reports missing tools, local capabilities, source data, credentials/licenses, or validation/export/execution dependencies.
- Launch Rubric Review Agent before final handoff after the deliverable has been built or revised.
- Launch Humanization Agent only when requested or when prose quality is a material submission risk.

If subagents are unavailable, state that explicitly before doing the same work in a separate main-agent pass. Keep the separation visible: finish the coordination pass, then run a distinct check/review pass from files and prompt wording rather than memory.

Deliverable Check Agent must return:

- Files checked and checks performed
- Commands run and outputs relevant to submission readiness
- Missing dependencies, tooling gaps, source gaps, export blockers, or execution blockers
- Whether Environment Setup Agent is required
- Missing, weak, extra, malformed, or unreadable deliverable parts
- A readiness classification: `partial`, `complete_but_unverified`, `ready`, or `blocked`

## Draft Or Implement

Work from real files and assignment wording. Keep changes minimal and aligned with the requested deliverable. Do not introduce broad cleanup, extra tooling, compatibility layers, or unrelated content unless the assignment requires them.

Do not stop at a partial deliverable just because a required capability is missing. If validation dependencies are missing, launch Environment Setup Agent to provision a temporary local environment when safe, run the required checks, render/export the required artifact, or execute the required workflow, and clean up. If subagents are unavailable, state that explicitly and do the work in a separate main-agent fallback pass. Report unrun validation only when Environment Setup Agent or the fallback pass finds provisioning blocked by approval, credentials, licenses, payment, unsafe cleanup, or excessive resources.

For work that depends on local processing, generated evidence, or exported files:

- Record setup, commands, parameters, tool versions when relevant, and source scope when results depend on local processing.
- Keep temporary work outside the submission unless requested.
- Keep intermediates only when requested or needed for reproducibility.
- Prefer reversible, local, temporary, portable, or containerized provisioning over lasting system changes. Use a temporary directory outside the submission folder for dependencies, runtimes, draft outputs, validation files, and disposable intermediates whenever possible.
- Ask or report the blocker when provisioning requires user approval, credentials, licenses, payment, unsafe cleanup, or excessive resources.
- Remove non-submission artifacts after validation unless needed for reproducibility.
- Have Environment Setup Agent return commands run, artifacts produced, cleanup performed, and unresolved blockers; do not rely on unstated assumptions.
- If subagent delegation is unavailable, state that explicitly before using the main-agent fallback. If delegation fails after starting, report the blocker unless a safe retry or fallback is clearly possible.

## Deliverable Creation

Use the requested template when one is provided. Otherwise, create the requested format directly.

Remove content that is not required by the assignment prompt, rubric, requested format, clean submission, execution, verification, or reproducibility of the required deliverable. This applies to any content type.

Do not delete useful support content only because the prompt does not name it. Keep content that makes the submission clean, runnable, verifiable, or reproducible. When pruning, distinguish "not explicitly named" from "not useful."

Before calling the deliverable ready:

- Confirm the final file or folder exists and is readable.
- Confirm the format, filename, and included files match the instructions.
- Confirm all required sections or questions are answered.
- Confirm each required component was checked or produced whenever feasible, including generated outputs and evidence.
- Confirm no extra content is recommended when the instructions restrict the submission contents.

## Format And Template Handling

Inspect generated deliverables before saying they are ready. A deliverable is not ready if required content is missing, unreadable, misplaced, clipped, malformed, or in the wrong format.

If a required template cannot be filled reliably, do not fake a broken output. Mark it as manual-fill or manual-export required, create a concise fill guide with exact content and locations, and tell the user not to submit the failed generated artifact.

## Independent Rubric Review

Use Rubric Review Agent for the independent rubric review. This review is mandatory before handoff for finished deliverables, not optional polish. If subagents are unavailable, state that explicitly and perform the review as a separate main-agent pass. If delegation fails after starting, report the blocker unless a safe retry or fallback is clearly possible. Do not review from memory of the drafting process.

Prompt shape:

```text
Review this assignment deliverable independently against the rubric.

Inputs:
- Assignment prompt/rubric: <path or text>
- Final deliverable: <path>
- Relevant source/generated files: <paths>

Task:
- Identify missing, weak, incorrect, unsupported, unnecessary, over-included, or likely-to-lose-marks items.
- Mark severity as blocker, major, minor, or note.
- Calibrate severity by the actual submission requirements: blockers and majors only for issues likely to invalidate the submission or lose substantial marks.
- Include exact locations where possible.
- Check whether the deliverable includes unnecessary content beyond what is required for clean submission, verification, reproducibility, or required execution/export.
- Return findings only, ordered by severity, and state whether it is ready to submit.
```

Severity guide:

- Blocker: missing or unreadable final deliverable, unanswered required item, missing essential input, hard submission-format violation, or likely rejection by the submission platform.
- Major: likely substantial mark loss, such as omitted required artifact, absent required validation, contradicted result, broken submitted work, missing core mechanism, unsupported required claim, or unnecessary content that violates submission rules.
- Minor: optional improvements, stricter implementation preferences, missing raw evidence when not required, limited but stated scope, parameterized work that still gives requested behavior, or support-content differences that do not affect the final submission.
- Note: observations, residual risks, or context that do not require changes before submission.

Only blockers and majors require another review loop. Do not loop on minor or note issues unless the user requests polish.

## Humanization Review

Run a humanization review when the user asks for it or when prose quality is part of the deliverable risk. Keep the pass independent: provide only the current content, target use, requested voice, and preservation constraints. Do not include prior edits or change history.

Prompt shape:

```text
Humanize this text for the stated assignment deliverable.

Inputs:
- Current content: <path or text>
- Target use: <deliverable purpose>
- Requested voice: <voice constraints>
- Preserve: required facts, numbers, references, names, rubric coverage, calculations, evidence, and domain-specific claims.

Task:
- Rewrite only prose that sounds generic, over-polished, or AI-like.
- Preserve meaning, factual accuracy, and domain-specific precision.
- Do not add new claims, citations, experiments, or evidence.
- Return exact replacement text only where changes are needed.
```

For second and later passes, keep the prompt independent and provide only the current content plus constraints.

## Final Handoff

Keep the final response short and practical:

- Final deliverable path or location
- Checks or commands run
- Temporary provisioning and cleanup performed
- Whether rubric review found remaining blockers or majors
- Any real remaining risk, such as manual completion required, unrun validation, unavailable source materials, or format constraints that could not be verified
- User TODOs
- Next step as a direct action
