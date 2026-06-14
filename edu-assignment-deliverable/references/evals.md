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
- Inspects provided files and obvious workspace context before asking.
- Treats required output format as a hard dependency.
- Asks one concise blocker question and does not ask optional preference questions.
- For non-trivial context, creates or proposes a workspace with `README.md`, `plan.md`, and `status.json` showing `blocked`.

**Failure indicators:**
- Drafts a deliverable without knowing the required format.
- Asks multiple preference questions instead of one hard-dependency question.
- Invents submission constraints.

---

## Eval: Intake And Checklist

**Prompt:**

```text
Use prompt.md and rubric.md to prepare the final PDF report. Stop after planning and checklist creation.
```

**Expected output:** The agent creates a resumable workspace and rubric checklist, then stops before drafting because the user requested planning only.

**Expected artifacts:**
- `<assignment-name>-workspace/README.md`
- `<assignment-name>-workspace/plan.md`
- `<assignment-name>-workspace/status.json`
- `<assignment-name>-workspace/artifacts/rubric-checklist.md`
- `<assignment-name>-workspace/checkpoints/phase-3-rubric-checklist.json`

**Expectations:**
- Converts rubric requirements into traceable checklist items.
- Records required format, final deliverable target, validation method, and next action.
- Leaves final deliverable drafting unstarted.
- Writes resumable state sufficient for a fresh session to continue.

**Failure indicators:**
- Drafts the final report despite the stop condition.
- Creates checklist items not tied to prompt, rubric, template, submission rule, or user instruction.
- Omits resume state or next action.

---

## Eval: Resume Existing Checkpoint

**Initial state:**

- `status.json` says phase is `inspection`, readiness is `complete_but_unverified`.
- Latest checkpoint says candidate deliverable exists.
- Deliverable Check Agent report says PDF export validation is missing.

**Prompt:**

```text
Continue this assignment workspace.
```

**Expected output:** The agent resumes from the saved state and continues with validation or environment recovery instead of rebuilding completed content.

**Expectations:**
- Reads `status.json`, `plan.md`, latest checkpoint, and deliverable-check report.
- Continues with validation or focused revision, not intake or full rewrite.
- Launches or simulates Environment Setup Agent if PDF export tooling is safely provisionable.
- Records new checkpoint and updated `status.json` after the resume action.

**Failure indicators:**
- Starts from intake again without using state files.
- Rewrites completed deliverable content without a failed gate or user request.
- Ignores the missing validation blocker.

---

## Eval: Paid Or Licensed Dependency

**Prompt:**

```text
Validate the final deliverable by running the required proprietary simulator. I do not have credentials available.
```

**Expected output:** The agent records a hard blocker and returns a partial handoff with exact unrun validation and user TODO.

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

## Eval: Finished Sample Readiness

**Prompt:**

```text
The assignment deliverable is complete in final-report.docx. Check it against prompt.md and rubric.md and tell me whether it is ready.
```

**Expected output:** The agent inspects existing work, runs independent deliverable and rubric review passes, and reports readiness without rewriting by default.

**Expectations:**
- Inspects existing deliverable before editing.
- Runs Deliverable Check Agent or a distinct fallback pass.
- Runs Rubric Review Agent or a distinct fallback pass before final readiness.
- Edits only blockers or majors if the user asked the agent to fix issues; otherwise reports findings.
- Final answer states readiness, checks run, remaining risks, and user TODOs.

**Failure indicators:**
- Calls it ready without independent rubric review.
- Rewrites the document by default.
- Loops on minor polish when no blocker or major remains.

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
