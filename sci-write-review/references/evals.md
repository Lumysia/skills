# Scientific Review Writer Evals

Use these smoke scenarios to validate the long-running review workflow without completing a full manuscript.

---

## Eval: Intake And Workspace

**Prompt:**

```text
Write a scoping review from the papers in ./papers, but stop after setup and source registration.
```

**Expected output:** The Coordinator performs non-destructive discovery, creates or resumes `review-project/`, writes `project.json`, `manifest.json`, `status.json`, `plan.md`, source records, and a checkpoint, then runs or simulates Work Check.

**Failure indicators:**

- Asks for files before checking user-named paths.
- Starts reading or drafting before setup/source registration is checked.
- Uses chat-only handoffs instead of file-backed artifacts.

---

## Eval: Resume Existing Project

**Initial state:**

- `status.json` says phase is `reading` and status is `partial`.
- `manifest.json` has registered sources and one completed `source_read_patch`.

**Prompt:**

```text
Continue the review.
```

**Expected output:** The Coordinator reads project state, resumes with the next unread source or failed gate, and does not reread completed sources unless dependencies changed.

**Failure indicators:**

- Starts a new project without asking.
- Regenerates completed artifacts by default.
- Ignores critic/work-check blockers in the manifest.

---

## Eval: Extraction Gate

**Prompt:**

```text
Use these PDFs to draft the review.
```

**Expected output:** The Coordinator routes PDFs to Text Extraction first, registers clean extraction outputs, and blocks Reader/Synthesis/Writer from using raw PDFs directly.

**Failure indicators:**

- Reader works directly from raw PDFs without extraction or extraction-quality audit.
- Installs MinerU or Docling without permission.
- Duplicates native extractor output unnecessarily.

---

## Eval: Incremental Writing Safety

**Prompt:**

```text
Draft the results section from the approved plan.
```

**Expected output:** Writer creates point-level patch files from approved plans and locked claims; the Coordinator serially integrates approved patches and prevents concurrent writes to the same section/manuscript file.

**Failure indicators:**

- Writer drafts the whole multi-point section in one broad pass.
- Multiple writers modify the same draft file concurrently.
- Draft prose introduces claims absent from locked artifacts.

---

## Eval: Critic Independence

**Prompt:**

```text
Review this draft and fix source-grounding issues.
```

**Expected output:** Critic receives neutral routing metadata, candidate paths, dependency paths, rubrics, and anchors. It independently writes pass/fail decisions; the Coordinator adjudicates without dictating findings.

**Failure indicators:**

- Coordinator tells Critic what conclusion to reach.
- Critic approves unverifiable or source-mismatched claims.
- Quality Test selects a fluent but ungrounded candidate.
