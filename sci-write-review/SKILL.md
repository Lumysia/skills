---
name: sci-write-review
description: Create evidence-grounded literature reviews, research syntheses, technical reviews, and long-form manuscripts from source documents using file-backed artifacts, specialized subagents, critic gates, quality checks, and export traceability.
---

# Scientific Review Writer

Use this skill to run an evidence-grounded review-writing workflow without relying on chat-only handoffs. The Project Manager Agent keeps context small, assigns file paths, launches specialized subagents, routes artifact files through critic gates, and exports a manuscript with traceability back to sources and citation anchors.

## Core Principles

- Use files as the durable handoff between agents; do not pass long artifacts through chat.
- Keep the Project Manager Agent out of full-corpus reading unless targeted diagnosis is needed.
- The Project Manager Agent remains accountable for subagent outputs and must verify operational completion before advancing.
- Normalize PDFs and unusual formats through a Text Extraction Agent before Reader/Synthesis/Writer agents run.
- Read long corpora incrementally: Reader Agent should process one source at a time, write a patch immediately, then move to the next source instead of reading everything before writing.
- Write manuscripts incrementally: Writer Agent should handle one section-plan commitment or key point per task, write a patch immediately, then move to the next commitment.
- Avoid concurrent writes: parallel Writer tasks may only write independent patch files; a single integrator step serially merges patches into section/manuscript files.
- Require subagents to write complete outputs to assigned files and return only paths, dependencies, summaries, risks, and next-step recommendations.
- Let downstream agents read approved artifact files, summaries, and targeted anchors rather than relying on copied chat snippets.
- Treat fabricated, unverifiable, or source-mismatched claims as hard failures.
- Use artifact locks so final writing depends only on approved evidence and claims.
- Use Work Check Agent for important operational nodes that do not have a scholarly Critic gate.
- Preserve reviewer independence: Project Manager may provide content, dependencies, rubric, and scope, but must not prescribe the criticism, quality-test conclusion, or work-check outcome.
- Ask the user at bootstrap whether they want detailed human intervention or autonomous quality selection after retry exhaustion.
- For paper discovery or source acquisition, route to `sci-paper-search` when external paper-search tools are useful; do not make it a hard dependency for review writing.

## Bootstrap

Before any other bootstrap question, infer the language to use for interaction and final outputs from the request, source corpus, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once. Use that language for subsequent prompts, artifact summaries, critic reasons, quality decisions, and manuscript prose unless the user specifies separate interaction/output languages.

Then collect the remaining minimal missing inputs:

- Interaction/output language, if not already inferred or specified
- Topic or research question
- Review type: narrative, scoping, systematic, critical, theoretical, methods, or technical
- Target audience
- Source corpus or source acquisition plan
- Project/output directory for artifacts and exports
- Citation style or source reference format
- Whether the human wants to approve the final argument plan before drafting
- Intervention mode: `human_detailed` or `autonomous_quality_test`

If sources are provided but no save path is provided, ask for a project directory. If the host environment cannot write files, state that the workflow will use in-memory artifacts, but prefer file-backed artifacts whenever possible.

Store bootstrap decisions in `project.json` and `manifest.json`. The manifest is the Project Manager Agent's primary context object.

## Default Flow

1. Create the project directory, `project.json`, and `manifest.json`; then run Work Check Agent for setup completeness.
2. Assign source paths and create source records; then run Work Check Agent for source registration completeness.
3. If inputs are PDFs, scans, images, Office files, HTML, tables, or other unusual formats, launch Text Extraction Agent first.
4. Text Extraction Agent runs/collects MinerU or Docling outputs, places their native output folders/files under the project, registers those outputs as clean sources, and adds only minimal missing metadata; then run Work Check Agent for extraction registration completeness.
5. Launch Reader Agent only on registered extraction outputs and clean text artifacts, not raw PDFs or messy formats; Reader must process one source at a time and patch evidence/memo artifacts after each source.
6. Launch Critic Agent to review Reader artifacts.
7. Retry scoped fixes when critic gates fail.
8. Launch Synthesis Agent only from approved evidence and memos.
9. Critic-review synthesis claims, thesis, and argument plan.
10. If requested, ask the human to approve or edit the final argument plan before drafting.
11. Launch Writer Agent in a one-key-point-at-a-time loop to create independent draft patch files; then serially integrate patches into section/manuscript files.
12. Critic-review section plans, drafts, and manuscript integration.
13. If retries are exhausted, follow `intervention_mode`: ask the human in `human_detailed`, or launch Quality Test Agent in `autonomous_quality_test`.
14. Export `manuscript.md`, references, `export-trace.json`, and `workflow-summary.json`; then run Work Check Agent for export completeness.

For the complete stage-gated file workflow, read `references/workflow.md`.

## File Handoffs

Every substantial subagent output must be written to a file. A subagent's final response should include only:

- Artifact kind
- Artifact id
- Output file path
- Dependency file paths read
- Short summary
- Known risks or unresolved questions
- Suggested next gate or task

Use a portable project layout:

```text
review-project/
  project.json
  manifest.json
  sources/
  artifacts/
  critic/
  quality/
  workcheck/
  export/
```

For detailed file layout, manifest rules, and context-control rules, read `references/workflow.md`.

## Subagents

Use these roles as real subagents, separate tasks, separate prompts, or mental roles in one agent runtime:

- Project Manager Agent: maintains scope, manifest, artifact paths, statuses, locks, retries, intervention mode, and export.
- Work Check Agent: verifies that non-critic operational tasks actually completed, files exist, manifest entries are consistent, and blockers are resolved before the next stage.
- Text Extraction Agent: runs or registers MinerU/Docling outputs, normalizes their output folders/files under the project, and exposes clean text/Markdown/JSON/anchors as downstream sources.
- Reader Agent: reads assigned sources and writes source-grounded extraction artifacts, evidence packs, and memos.
- Synthesis Agent: reads approved evidence artifacts and writes synthesis claims, thesis, and argument plans.
- Writer Agent: reads approved plans and locked claims, then writes section plans, draft sections, manuscript files, and trace fragments.
- Critic Agent: verifies candidate artifact files against rubrics, dependencies, and targeted source anchors.
- Quality Test Agent: compares retry-exhausted candidate versions in autonomous mode and selects only source-grounded candidates.

For exact agent prompts, read `references/subagents.md`.

## Text Extraction

If the user supplies PDFs or unusual formats, do not let Reader/Synthesis/Writer agents work directly from raw files. Run Text Extraction Agent first.

Default extraction order:

1. Use existing clean text/Markdown/JSON when already available and source provenance is clear.
2. Prefer MinerU for PDFs, scans, images, and layout-heavy scientific documents.
3. If MinerU is unavailable, ask whether to install it. If the user agrees, detect OS, Python, GPU/MPS availability, VRAM, RAM, and disk before choosing GPU/MPS, CPU, or client/service mode.
4. Use Docling as fallback or for broad-format conversion such as Office, HTML, Markdown, CSV, images, audio/video transcription setups, or when MinerU is unavailable/unsuitable.
5. Use the extractor's native output files as source artifacts whenever possible; do not create duplicate clean-text files if the extractor already exported usable Markdown/JSON/text.

For complete extraction policy, install decision rules, and extraction outputs, read `references/extraction.md`.

## Artifact Rules

Create explicit artifacts rather than free-floating prose. Common artifact kinds include:

```text
review_project
review_framing
source_record
document_intelligence
text_extraction
screening_decision
evidence_pack
reading_memo
source_read_patch
synthesis_claim
review_thesis
argument_plan
section_plan
draft_point_patch
draft_section
manuscript
critic_decision
work_check_decision
quality_decision
human_decision
export_trace
```

Artifact statuses are `draft`, `rejected`, `approved`, `locked`, and `reopened`.

Downstream agents should receive paths to locked artifacts, not copied full content. Large artifacts should be split into full text, structured JSON, anchor index, and summary files.

For artifact fields, lifecycle rules, and JSON schemas, read `references/artifacts.md`.

## Critic And Quality Gates

Never skip a gate because an output looks plausible. The critic must receive the same dependency/source context as the producing agent, critique only the assigned candidate span/artifact, and strictly verify source grounding for claims, quotes, citations, page references, methods, findings, and limitations.

Retry rule summary:

1. Producing agent writes a candidate artifact file and updates the manifest.
2. Critic Agent receives candidate path plus the same relevant dependency paths, source summaries, extraction manifests, evidence packs, and targeted anchors used by the producing agent. Project Manager must not suggest what the critic should find.
3. Critic Agent writes a critic decision file with blocking and nonblocking findings separated.
4. Project Manager adjudicates the critic decision.
5. Passing artifacts may be approved and locked.
6. Blocking valid failures are revised with scoped changes; nonblocking suggestions may be recorded and waived.
7. After retry exhaustion, use `human_detailed` or `autonomous_quality_test` according to bootstrap preference.
8. Quality Test Agent may approve only candidates without fatal source-grounding failures.

For complete retry policy, human intervention rules, quality selection rules, and rubrics, read `references/critic-and-quality.md`.

## Citation Anchors

Every source-backed evidence unit should have a stable anchor:

```json
{
  "anchor_id": "source-01:p4:thermal-runaway-definition",
  "source_id": "source-01",
  "page": 4,
  "section": "Introduction",
  "text": "Quoted or paraphrased source span used as evidence."
}
```

Preserve anchor ids exactly across evidence packs, synthesis claims, section plans, paragraphs, manuscript files, and export traces.

## Examples

For concrete examples of PDF review, human-approved final plans, autonomous quality selection, and multi-agent runtime implementation, read `references/examples.md`.
