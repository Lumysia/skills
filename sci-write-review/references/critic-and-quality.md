# Critic And Quality Reference

## Contents

- Retry policy
- Human intervention modes
- Hard source-grounding failures
- Rubrics

## Retry Policy

Use this rule for every critic-gated artifact:

1. Producing agent writes a candidate artifact file.
2. Producing agent updates the manifest with candidate path, dependencies, status, and summary.
3. Coordinator sends Critic Agent the candidate path plus the same relevant dependency/source context used by the producing agent.
4. Critic Agent evaluates only the assigned candidate span/artifact against the active rubric and declared context.
5. Critic Agent writes a critic decision file separating blocking findings from nonblocking suggestions.
6. Coordinator adjudicates whether the critic finding is valid, in scope, and blocking.
7. If findings are nonblocking or out of scope, record a waiver/rationale and approve or continue when safe.
8. If valid blocking findings remain, pass required changes and file paths back to the producing agent.
9. Producing agent writes a new version file or patch according to the host workflow.
10. Retry with scoped revisions up to the configured maximum.
11. If retries are exhausted and `intervention_mode` is `human_detailed`, present candidate version paths and critic feedback paths to the human.
12. If retries are exhausted and `intervention_mode` is `autonomous_quality_test`, launch Quality Test Agent with candidate paths, critic decision paths, dependency paths, and targeted anchor paths.
13. Quality Test Agent writes a `quality_decision` file selecting the strongest source-grounded candidate, or rejecting all candidates if none are safe to approve.
14. If Quality Test Agent selects a candidate, Coordinator approves that candidate only when the decision explains source-grounding and critic issues are not blocking fabrication/source failures.
15. If Quality Test Agent rejects all candidates, Coordinator requests scoped regeneration from the producing agent; if the failure repeats, ask the human for direction even in autonomous mode.
16. Record the human, quality, or waiver decision and continue only from the accepted artifact file.

Default retry count: `3`.

Never skip a gate because the output looks plausible.

## Critic Context And Adjudication

Critic Agent should not inspect random or unrelated content. It should receive:

- candidate artifact or patch path,
- artifact kind and active rubric,
- the producing agent's dependency paths,
- relevant extraction manifests and source summaries,
- targeted citation anchors used in the candidate,
- approved evidence/claim/section-plan files that the producing agent used,
- explicit scope of review, such as one paragraph patch, one evidence pack, or one section plan.

Coordinator must not provide criticism direction. It may not tell Critic Agent what to find, which issue to focus on, whether the candidate is probably good/bad, or whether the expected outcome is pass/fail. It should send neutral routing metadata and content only.

Neutral review request format:

```json
{
  "candidate_path": "path/to/candidate.json",
  "artifact_kind": "draft_point_patch",
  "rubric": "drafting",
  "review_scope": "one paragraph commitment patch",
  "dependency_paths": ["path/to/section-plan.json", "path/to/evidence-pack.json"],
  "anchor_ids": ["source-001:p4:block-03"],
  "source_context_paths": ["path/to/extraction-manifest.json"]
}
```

Disallowed leading review request examples:

- "This paragraph probably overclaims; verify that."
- "Find citation problems in this patch."
- "This looks good; approve if possible."
- "The previous agent likely fabricated this claim."
- "Please be lenient unless there is a huge problem."

The same independence rule applies to Quality Test Agent and Work Check Agent. Coordinator may provide candidate paths, dependency paths, expected files, and rubrics/checklists, but not preferred findings or desired outcomes.

Coordinator remains responsible for deciding what happens after criticism:

- Hard source-grounding failures are blocking and must be fixed.
- Missing required schema fields are blocking when downstream agents need them.
- Scope-breaking, unsupported, fabricated, or source-mismatched claims are blocking.
- Style suggestions, preference issues, minor wording improvements, or broad recommendations outside the assigned span are nonblocking unless they affect correctness or traceability.
- Out-of-scope critic comments should be recorded and waived with rationale.
- A waiver must be written to the decision/artifact record; do not silently ignore critic feedback.

## Human Intervention Modes

Ask at bootstrap whether the user wants detailed human intervention or autonomous candidate selection.

`human_detailed` means:

- Ask the human when critic retries are exhausted.
- Ask the human when final argument plan approval was requested.
- Ask the human when scope decisions, private data, external cost, or unsuitable sources require judgment.

`autonomous_quality_test` means:

- Do not interrupt the human for routine retry exhaustion.
- Launch Quality Test Agent to compare candidate versions.
- Ask the human only if all candidates fail repeatedly, scope must change, sources are missing, cost/privacy issues arise, or the user requested final plan approval.

Human approval prompt:

```text
The critic could not approve this artifact after [N] attempts.

Artifact: [kind/title]
Failed rubric: [rubric]
Main issues: [required changes]

Options:
1. Accept a source-grounded candidate version
2. Edit the artifact manually to remove or ground failed claims
3. Change the review scope or source set
4. Switch to autonomous quality testing for this artifact
5. Stop this workflow

Do not offer acceptance for candidates with unresolved fabricated, unverifiable, or source-mismatched claims.
```

## Hard Source-Grounding Failures

These are hard failures:

- A cited source cannot be found in declared source files.
- A citation anchor cannot be found in declared anchor files.
- A quote does not exist in the cited source span.
- A page, section, method, result, dataset, or finding is invented.
- A real source is used to support a claim it does not support.
- A synthesis pattern is asserted without evidence across the cited sources.
- A draft introduces claims absent from locked evidence or approved synthesis artifacts.
- Reader, Synthesis, or Writer agents use raw PDFs/unusual files directly after extraction should have been run.
- Extraction output omits pages, sections, tables, formulas, or anchors needed to support downstream claims and does not record the limitation.
- Reader Agent waits to read the whole corpus before writing evidence/memo outputs when the corpus is long enough to require incremental reading.
- A source-level patch changes cumulative artifacts without recording whether it added, modified, weakened, contradicted, or removed prior content.
- Writer Agent drafts an entire multi-point section in one task instead of producing point-level patches when the section plan has multiple commitments.
- A draft point patch changes prior prose without recording whether it added, modified, weakened, contradicted, removed, or transitioned from prior content.
- Multiple Writer Agents write to the same section draft or manuscript file concurrently.
- A point-level Writer Agent modifies a shared draft/manuscript file instead of writing an independent patch file.

Fabricated, unverifiable, or source-mismatched claims must not be approved by human bypass, quality testing, or Coordinator judgment unless removed or grounded in verified sources.

## Rubrics

### Framing Rubric

- Question is bounded and inspectable.
- Scope, audience, review type, boundaries, and contribution are explicit.
- The review is not framed as "all literature" or an impossible total survey.

### Evidence Rubric

- Claims are grounded in sources and anchors.
- Methods and limitations are captured.
- Evidence strength is stated.
- Contradictory or limiting evidence is preserved.
- Any claim, quote, method, result, page reference, or citation that cannot be verified in declared source files is a hard failure.
- Source-mismatched evidence is a hard failure even when the cited source exists.
- For long corpora, cumulative evidence should be traceable to source-level patches and should not appear as one late all-corpus summary.

### Extraction Rubric

- Extraction output has clean text or Markdown suitable for downstream reading.
- Structured JSON records extractor, backend mode, source path, clean text path, anchor path, summary path, and warnings.
- Anchor index preserves source id, source path, page/section when available, and extracted text spans.
- Tables, figures, formulas, and reading order are preserved or limitations are explicitly logged.
- Fallback decisions between MinerU and Docling are recorded.
- Missing pages, OCR uncertainty, failed tables, or formula loss are not hidden.

### Memo Rubric

- Memo goes beyond summary.
- It names patterns, doubts, contradictions, candidate concepts, and unresolved questions.
- It proposes concrete follow-up actions when evidence is weak or incomplete.

### Synthesis Rubric

- Claims synthesize across sources.
- Support, conflict, conditions, evidence strength, and anchors are present.
- Gaps are classified rather than asserted vaguely.
- Each synthesis claim must be verifiably supported by cited evidence packs and anchors.
- Fabricated cross-source patterns are hard failures.

### Argument Plan Rubric

- The plan is thesis-led and analytical.
- Every section connects to approved claims.
- Evidence coverage is explicit.
- The plan is not a paper-by-paper summary.

### Section Plan Rubric

- Section goal and section argument are distinct.
- Paragraph commitments are specific.
- Claim ids and anchors are preserved.
- Order rationale explains analytical progression.

### Drafting Rubric

- Paragraphs are traceable to approved claims and anchors.
- Claims are not overstated.
- Limitations and contradictions are integrated where relevant.
- Prose is coherent and matches requested audience and language.
- Every citation must support the sentence or paragraph it is attached to.
- Invented citations, quotes, page numbers, or source findings are hard failures.
- For multi-point sections, draft prose should be traceable to `draft_point_patch` files and should not appear as one late all-section draft.
- Integrated draft sections should be produced by a serial integration step from approved point patches, not by concurrent writer updates to the same file.

### Manuscript Rubric

- Manuscript develops the thesis across sections.
- Sections are integrated rather than stitched together.
- References and anchors remain traceable.
- The conclusion reflects evidence strength and scope limits.
- The manuscript must not include claims that only appeared during writing and are absent from locked source-grounded artifacts.

### Quality Selection Rubric

- Prefer source-grounding and downstream safety over fluency.
- Select a candidate only if it has no fatal source-grounding failures.
- Penalize unresolved critic issues by severity, especially source verification failures.
- Reject all candidates when all available versions fabricate, distort, or fail to verify important claims.
