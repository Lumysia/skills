# Workflow Reference

## Contents

- Project layout
- Manifest rules
- Context-control rules
- Text extraction stage
- Work-check gates
- Incremental reading loop
- Incremental writing loop
- Concurrent writing safety
- Stage-gated workflow
- File handoff format

## Project Layout

Use this structure when the host environment supports files:

```text
review-project/
  project.json
  manifest.json
  sources/
  artifacts/
    framing/
    sources/
    extraction/
    documents/
    screening/
    evidence/
    memos/
    synthesis/
    plans/
    drafts/
    manuscript/
  critic/
    decisions.json
    escalations.json
  workcheck/
    decisions.json
  quality/
    decisions.json
  export/
    manuscript.md
    references.md
    export-trace.json
    workflow-summary.json
```

Use forward slash paths in skill instructions even on Windows.

## Manifest Rules

The Project Manager Agent should keep a compact manifest and use it as the active context object:

```json
{
  "project_id": "review-project-id",
  "topic": "review topic",
  "intervention_mode": "human_detailed | autonomous_quality_test",
  "artifacts": [
    {
      "id": "evidence-pack-001",
      "kind": "evidence_pack",
      "status": "draft",
      "path": "artifacts/evidence/evidence-pack-001.json",
      "summary": "Evidence on interface-driven thermal instability.",
      "dependencies": ["artifacts/extraction/source-001/extraction-manifest.json"],
      "citation_anchor_count": 8
    }
  ]
}
```

Manifest entries should include artifact id, kind, status, path, summary, dependencies, source ids, citation anchor count, and latest work-check/critic/quality decision path where applicable.

## Context-Control Rules

- Keep only project goal, manifest, artifact statuses, summaries, and next decisions in the Project Manager Agent's active context.
- Do not paste full source documents or full artifact contents into chat unless needed for targeted diagnosis.
- Prefer targeted reads by artifact id, section, source id, or citation anchor id.
- Ask subagents to return concise summaries, not full generated artifacts.
- Spawn a critic subagent for review instead of reviewing every detail in the main context.
- If an artifact is large, require a companion summary file and anchor index.

## Incremental Reading Loop

For long corpora, do not ask Reader Agent to read every source before writing. Use a one-source-at-a-time loop:

1. Project Manager selects the next unread source from the manifest.
2. Reader Agent reads only that source's registered extraction outputs, summaries, and targeted anchors.
3. Reader Agent writes `source_read_patch` for that source immediately.
4. Reader Agent applies the patch to cumulative evidence and memo artifacts, either by updating the existing artifact file or writing a new version file according to the host workflow.
5. Work Check Agent verifies the patch file, updated cumulative artifact path, manifest status, dependencies, and source coverage.
6. Project Manager repeats for the next source.
7. Critic Agent reviews cumulative evidence and memo artifacts only after the relevant batch or corpus pass is complete, unless a patch contains obvious source-grounding risks that need immediate critic review.

This prevents context blowups and avoids the failure mode where a subagent reads too much and produces one vague, late summary.

## Incremental Writing Loop

Do not ask Writer Agent to draft an entire section or manuscript in one task when the section plan contains multiple paragraph commitments or key points. Use a one-key-point-at-a-time loop:

1. Project Manager selects the next undrafted `paragraph_commitment` or key point from an approved `section_plan`.
2. Writer Agent reads only the approved section plan, relevant locked synthesis claims, targeted evidence packs, and citation anchors for that commitment.
3. Writer Agent writes `draft_point_patch` immediately for that one commitment.
4. Writer Agent must not write the shared section draft or manuscript file directly.
5. Work Check Agent verifies the patch file, manifest status, dependencies, and trace fragment.
6. Project Manager or a dedicated integration step serially applies approved patches to the cumulative draft section in section-plan order.
7. Critic Agent reviews a point patch immediately when the point introduces sensitive claims, dense citations, surprising synthesis, or source-grounding risk. Otherwise Critic Agent reviews the cumulative draft section after the section's commitments are complete.
8. Project Manager repeats for the next commitment.

This prevents long drafting tasks from drifting, inventing unsupported prose, or losing anchor traceability.

## Concurrent Writing Safety

Never run multiple Writer Agents that write to the same `drafts/section-<n>.md`, `artifacts/drafts/section-<n>.json`, `export/manuscript.md`, or manuscript artifact at the same time.

Allowed parallelism:

- Multiple Writer Agents may draft different `draft_point_patch` files in parallel when their assigned commitments are independent.
- Multiple Writer Agents may draft different section-specific patch files in parallel when each output path is unique.
- Critic or Work Check Agents may inspect patch files in parallel because they write separate decision files.

Disallowed parallelism:

- Two Writer Agents writing or updating the same section draft file.
- Two Writer Agents writing or updating the same manuscript file.
- A Writer Agent applying patches while another Writer Agent is still writing a patch for the same target file.
- Any agent silently overwriting a draft file instead of producing a versioned file or patch.

Integration rule:

- Writer Agents produce patch files only.
- Project Manager selects a deterministic merge order, usually section order then paragraph commitment order.
- One serial integration step applies patches to `drafts/section-<n>.md` and `artifacts/drafts/section-<n>.json`.
- Work Check Agent verifies the integrated section path and trace fragments.
- Manuscript integration is also serial and should read approved section files, not live patch files.

## Work-Check Gates

Work Check Agent protects important operational nodes that do not primarily need scholarly criticism. It checks whether assigned work was actually completed and whether the project can safely continue.

Use Work Check Agent after:

- Project setup and bootstrap persistence.
- Source registration and source copying/linking into the project.
- Text extraction installation/capability decisions.
- MinerU/Docling output placement or registration.
- Manifest updates that route downstream agents.
- Human-edited plan file registration.
- Quality Test Agent candidate selection bookkeeping.
- Final export file generation.

Work Check Agent does not replace Critic Agent. Critic Agent judges scholarly/content quality and source grounding. Work Check Agent judges operational completeness, file existence, path consistency, dependency availability, and whether there are blockers.

If Work Check Agent reports blockers, Project Manager Agent must fix them or relaunch the responsible worker before moving to the next stage.

Subagents should:

- Read only assigned source files and dependency artifacts.
- Write complete outputs to assigned files.
- Use machine-readable JSON for intermediate artifacts where practical.
- Use Markdown for manuscript prose.
- Preserve ids and citation anchors exactly.
- Never use unapproved or rejected artifact files as source material unless diagnosing them.

## Stage-Gated Workflow

1. Intake

First ask for interaction/output language. Then create `review_project` from topic, review type, audience, language, source plan, project directory, and intervention mode.

Write: `project.json` and `manifest.json`.

Work check: project files exist, language is recorded before other bootstrap values, intervention mode is recorded, and required directories are available.

2. Framing

Create `review_framing` with question, scope, inclusion boundaries, exclusion boundaries, audience, review type, and expected contribution.

Write: `artifacts/framing/review-framing.json`.

Gate: framing critic.

3. Source Intake

Create `source_record` artifacts for each document, paper, note, dataset, or web source.

Write: `artifacts/sources/source-records.json`.

Work check: source records exist, source paths resolve or are explicitly marked unavailable, and manifest dependencies are usable.

Gate: source relevance critic when screening is required.

4. Text Extraction

For PDFs, scans, document images, Office files, HTML, CSV, Markdown, LaTeX, XML, and other messy formats, run Text Extraction Agent before Reader Agent.

Preferred order: existing clean text, MinerU, Docling fallback, manual/user-provided extraction.

Register extractor-native outputs under `artifacts/extraction/<source-id>/`, such as `mineru-output/` or `docling-output/`. Write only minimal supplemental metadata such as `extraction-manifest.json`, `extraction-log.json`, and an anchor/summary file when the extractor did not already provide usable equivalents.

Work check: native output directories/files exist under the project, extraction manifest points to valid files, fallback/install decisions are logged, and downstream primary text/JSON paths are available.

Gate: extraction quality critic when extraction warnings, OCR uncertainty, table/formula dependence, or source quality risks exist.

5. Document Intelligence

Create `document_intelligence` from registered extraction output paths and structured extraction artifacts, not raw PDFs or unusual raw formats.

Write lightweight `document_intelligence` only if needed for review-specific claims/methods/limitations. Do not duplicate extractor output; reference extraction manifest and native output paths.

Gate: document-intelligence critic.

6. Screening

Create `screening_decision` with include/exclude decision and rationale.

Write: `artifacts/screening/screening-decisions.json`.

Gate: screening critic.

7. Evidence Pack

Create `evidence_pack` artifacts grouped by theme, mechanism, method, result, limitation, or controversy. Build them incrementally from `source_read_patch` files rather than waiting until all sources have been read.

Write: `artifacts/evidence/evidence-pack-<n>.json`.

Gate: evidence critic.

8. Reading Memo

Create `reading_memo` with interpretation, patterns, contradictions, doubts, candidate concepts, unresolved questions, and follow-up actions. Patch it after each source so patterns and contradictions evolve progressively.

Write: `artifacts/memos/reading-memo-<n>.json`.

Gate: memo critic.

9. Synthesis Claim

Create `synthesis_claim` artifacts that connect multiple sources.

Write: `artifacts/synthesis/synthesis-claims.json`.

Gate: synthesis critic.

10. Thesis

Create `review_thesis` from approved synthesis claims.

Write: `artifacts/synthesis/review-thesis.json`.

Gate: thesis critic or project manager approval.

11. Argument Plan

Create `argument_plan` with sections, analytical contribution, claim coverage, evidence coverage, and thesis alignment.

Write: `artifacts/plans/argument-plan.json`.

Gate: argument-plan critic.

Optional: human final-plan approval before drafting.

12. Section Planning

Create `section_plan` artifacts with goals, arguments, paragraph commitments, claim ids, anchors, and order rationale.

Write: `artifacts/plans/section-plan-<n>.json`.

Gate: section-plan critic.

13. Drafting

Create `draft_section` artifacts from approved section plans. Build each draft section incrementally from `draft_point_patch` files, one paragraph commitment or key point per Writer Agent task, then merge patches serially.

Write: `drafts/section-<n>.md` and `artifacts/drafts/section-<n>.json`.

Gate: writing critic.

14. Manuscript Integration

Create `manuscript` by integrating approved draft sections.

Write: `artifacts/manuscript/manuscript.json` and `export/manuscript.md`.

Gate: manuscript critic.

15. Export

Create `export_trace` and final outputs.

Write: `export/export-trace.json`, `export/workflow-summary.json`, and any requested reference files.

Work check: required export files exist, export trace references known manuscript/claim/source/anchor ids, and workflow summary includes lock/failure/escalation counts.

## File Handoff Format

Subagent final responses should be short:

```json
{
  "artifact_kind": "evidence_pack",
  "artifact_id": "evidence-pack-001",
  "output_path": "artifacts/evidence/evidence-pack-001.json",
  "dependencies_read": ["artifacts/extraction/source-001/extraction-manifest.json"],
  "summary": "Created evidence pack for interface instability.",
  "risks": ["Only two sources cover low-temperature behavior."],
  "suggested_next_gate": "evidence critic"
}
```
