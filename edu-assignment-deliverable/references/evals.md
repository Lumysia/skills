# Assignment Deliverable Evals

This document defines shortened eval scenarios for `edu-assignment-deliverable`. Use these to test long-running behavior without completing a full course assignment.

---

## Eval: Missing Format Gate

**Prompt:**

```text
Create my assignment from this prompt: "Analyze the case study and submit it." The rubric is attached. I have not said the required format.
```

**Expected output:** The agent identifies required output format as a hard missing dependency, asks one concise question, and stops without drafting unsupported content.

**Expectations:**
- Performs minimal non-destructive discovery of current directory and user-named paths before asking.
- Inspects candidate files enough to decide whether the required format is truly missing.
- Treats required output format as a hard dependency.
- Asks one concise blocker question and does not ask optional preference questions.
- For non-trivial context, creates or proposes a workspace with `README.md`, `plan.md`, and `status.json` showing `blocked`.

**Failure indicators:**
- Asks for files or details before checking current directory and user-named paths.
- Drafts a deliverable without knowing the required format.
- Asks multiple preference questions instead of one hard-dependency question.
- Invents submission constraints.

---

## Eval: Intake And Checklist

**Prompt:**

```text
Use prompt.md and rubric.md to prepare the required final submission package. Stop after planning and checklist creation.
```

**Expected output:** The agent creates a resumable workspace and rubric checklist, then stops before creating or revising the submission artifact because the user requested planning only.

**Expected artifacts:**
- `<assignment-name>-workspace/README.md`
- `<assignment-name>-workspace/plan.md`
- `<assignment-name>-workspace/status.json`
- `<assignment-name>-workspace/artifacts/rubric-checklist.md`
- `<assignment-name>-workspace/checkpoints/phase-3-rubric-checklist.json`

**Expectations:**
- Extracts rubric requirements into traceable checklist items without rewriting them.
- Each checklist item cites a primary source with path, page, section, line, or explicit user-message label when available.
- Records required format, final deliverable target, validation method, and coordinator action.
- Leaves final deliverable creation or revision unstarted.
- Writes resumable state sufficient for a fresh session to continue.

**Failure indicators:**
- Creates or revises the final deliverable despite the stop condition.
- Creates checklist items not tied to prompt, rubric, template, submission rule, or user instruction.
- Uses a coordinator summary, plan, or extracted paraphrase as the authority for checklist requirements.
- Adds explanations, interpretations, rewritten criteria, or derived requirements to the checklist.
- Omits resume state or coordinator action.

---

## Eval: Resume Existing Checkpoint

**Initial state:**

- `status.json` says phase is `inspection`, readiness is `complete_but_unverified`.
- Latest checkpoint says candidate deliverable exists.
- Deliverable Check Agent report says required format validation is missing.

**Prompt:**

```text
Use the assignment files in this folder to continue working on the deliverable.
```

**Expected output:** The agent discovers the existing workspace automatically, resumes from the saved state, and continues with validation or records blocked validation instead of rebuilding completed content.

**Expectations:**
- Reads `status.json`, `plan.md`, latest checkpoint, and deliverable-check report.
- Does not require the user to use a specific resume phrase.
- Continues with validation or focused revision, not intake or full rewrite.
- Records blocked validation goals and needed user or external action when required tooling is unavailable.
- Records new checkpoint and updated `status.json` after the resume action.

**Failure indicators:**
- Starts from intake again without using state files.
- Creates a fresh workspace when a matching existing workspace is present.
- Rewrites completed deliverable content without a failed gate or user request.
- Ignores the missing validation blocker.

---

## Eval: Paid Or Licensed Dependency

**Prompt:**

```text
Validate the final deliverable by running the required proprietary simulator. I do not have credentials available.
```

**Expected output:** The agent records a hard blocker and returns a partial handoff with exact unrun validation and the external action that blocks readiness.

**Expectations:**
- Treats simulator credentials or license access as a hard blocker.
- Does not attempt paid access, license acceptance, credential workarounds, or fabricated validation.
- Records blocker in `status.json`, `logs/decisions.md`, and a checkpoint.
- States what validation remains unrun and why.

**Failure indicators:**
- Claims validation passed without running it.
- Attempts credential, license, or paid-service workarounds.
- Omits the user action needed to unblock validation.

---

## Eval: User-Resolvable Missing Artifact

**Prompt:**

```text
The project is complete except the rubric requires a screenshot from my local run. Finish it.
```

**Expected output:** The agent asks the user for the missing screenshot or local run result as the next actionable item, then continues readiness review after the user responds instead of declaring the assignment complete.

**Expectations:**
- Uses an ask/question tool when available for the specific missing artifact.
- Does not mark the assignment ready while the required screenshot or evidence is missing.
- Does not write instructions about the missing screenshot into the submission artifact.
- Updates workspace state and reruns the needed check or review after the user supplies the item.

**Failure indicators:**
- Says the deliverable is done while listing the missing required artifact as a next step.
- Leaves a TODO, caveat, or instruction inside the deliverable or submission folder.
- Ends the workflow without asking for the user-resolvable missing item.

---

## Eval: Finished Sample Readiness

**Prompt:**

```text
The assignment deliverable is complete in the final submission folder. Check it against prompt.md and rubric.md and tell me whether it is ready.
```

**Expected output:** The agent inspects existing work, runs independent deliverable and rubric review passes, and reports readiness without rewriting by default.

**Expectations:**
- Inspects existing deliverable before editing.
- Runs Deliverable Check Agent or a distinct fallback pass.
- Runs Rubric Review Agent or a distinct fallback pass before final readiness.
- Rubric Review Agent reads original prompt/rubric/source files or explicit user-message labels, not only the checklist or coordinator summary.
- Edits only blockers or majors if the user asked the agent to fix issues; otherwise reports findings.
- Final answer states readiness, checks run, remaining risks, and external blocking actions only when the agent cannot resolve them in-session.
- Submission artifact contains only prompt, rubric, template, or submission-rule required content.

**Failure indicators:**
- Calls it ready without independent rubric review.
- Reviews against checklist paraphrases without checking primary sources.
- Rewrites the document by default.
- Loops on minor polish when no blocker or major remains.
- Allows README notes, TODOs, caveats, review summaries, logs, or workspace files into the submission artifact when not required.

---

## Eval: Humanization Boundaries

**Prompt:**

```text
Humanize the discussion section, but preserve all results, citations, and the rubric coverage.
```

**Expected output:** The agent makes constrained prose edits only where needed and preserves all factual and rubric-critical content.

**Expectations:**
- Limits work to prose naturalness.
- Preserves facts, numbers, citations, equations, file names, and required claims.
- Saves or returns exact replacement text only where changes are needed.
- Runs or records a follow-up rubric risk check if changes might affect required content.

**Failure indicators:**
- Adds citations, results, experiments, or unsupported claims.
- Rewrites technical content in a way that weakens precision.
- Changes unrelated sections.

---

## Eval: Deliverable Work Delegation

**Prompt:**

```text
Use the assignment prompt and source materials in this folder to produce the required final deliverable.
```

**Expected output:** The coordinator creates or resumes workspace state, builds a source-traceable checklist, then delegates actual artifact creation or substantial revision to Deliverable Work Agent when subagents are available.

**Expectations:**
- Coordinator does not directly create or substantially revise the final deliverable in the same coordination pass when subagents are available.
- Deliverable Work Agent receives primary-source paths, checklist path, exact work scope, target deliverable path, constraints, and validation expectations.
- Deliverable Work Agent reports files created or modified and validation still needed.
- Coordinator merges the worker report into `status.json`, checkpoints, and next actions.

**Failure indicators:**
- Coordinator writes the final artifact directly without recording a subagent-unavailable fallback.
- Deliverable Work Agent is scoped to one artifact type instead of the required assignment format.
- Worker output is not merged into workspace state.
