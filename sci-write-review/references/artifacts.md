# Artifact Reference

## Contents

- Artifact lifecycle
- Common fields
- Large artifact splitting
- Schemas

## Artifact Lifecycle

Statuses:

```text
draft
rejected
approved
locked
reopened
```

Rules:

- Draft artifacts cannot be used for final writing until they pass the relevant critic gate.
- Passing critic decisions approve artifacts.
- Important downstream dependencies should be locked after approval.
- Failed critic decisions reject artifacts and list required changes.
- Revisions should be scoped to the failed gate, not broad rewrites.
- Human decisions can approve, reject, edit, or select versions.
- Quality decisions can select a candidate only in `autonomous_quality_test` mode and only when source-grounding is safe.
- Work-check decisions can block operational transitions when files, paths, manifests, or dependencies are incomplete.
- Locked artifacts can only change through an explicit scoped revision request.
- Downstream agents should receive file paths to locked artifacts, not copied full content.

## Common Fields

Each artifact should include:

- `id`
- `kind`
- `title`
- `content`
- `status`
- `source_refs`
- `citation_anchors`
- `versions`
- `approvals`
- `locks`
- `path`
- `dependencies`
- `summary`

## Large Artifact Splitting

For large source-derived artifacts, split files:

- Extractor-native output directory: `artifacts/extraction/<source-id>/mineru-output/` or `artifacts/extraction/<source-id>/docling-output/`
- Extraction manifest: `artifacts/extraction/<source-id>/extraction-manifest.json`
- Extraction log: `artifacts/extraction/<source-id>/extraction-log.json`
- Supplemental anchor or summary files only when native outputs do not already provide usable equivalents

Downstream agents should normally read registered native Markdown/JSON/text outputs, summaries, and targeted anchors before reading full text.

## Review Framing

```json
{
  "id": "framing-001",
  "kind": "review_framing",
  "status": "draft",
  "path": "artifacts/framing/review-framing.json",
  "question": "bounded review question",
  "scope": "what the review covers",
  "review_type": "scoping",
  "target_audience": "domain researchers and review readers",
  "inclusion_boundaries": ["source or topic boundaries"],
  "exclusion_boundaries": ["out-of-scope material"],
  "expected_contribution": "what the review will clarify or contribute"
}
```

## Text Extraction

```json
{
  "id": "text-extraction-001",
  "kind": "text_extraction",
  "status": "draft",
  "path": "artifacts/extraction/source-001/extraction-manifest.json",
  "source_id": "source-001",
  "source_path": "sources/paper.pdf",
  "extractor": "existing-clean | mineru | docling | manual",
  "extractor_version": "version if available",
  "backend_mode": "gpu | mps | cpu | service | fallback | unknown",
  "native_output_dir": "artifacts/extraction/source-001/mineru-output",
  "native_output_files": ["auto/input.md", "auto/input_content_list.json"],
  "primary_clean_text_path": "artifacts/extraction/source-001/mineru-output/auto/input.md",
  "primary_json_path": "artifacts/extraction/source-001/mineru-output/auto/input_content_list.json",
  "anchor_index_path": "artifacts/extraction/source-001/anchors.json",
  "summary_path": "artifacts/extraction/source-001/summary.md",
  "extraction_log_path": "artifacts/extraction/source-001/extraction-log.json",
  "pages_or_sections": ["detected pages or sections"],
  "tables": ["table summaries or paths"],
  "figures": ["figure summaries or paths"],
  "formulas": ["formula summaries or paths"],
  "reading_order": ["ordered block ids"],
  "warnings": ["OCR uncertainty, missing pages, failed table parse"],
  "extraction_confidence": "low | moderate | high"
}
```

## Work Check Decision

```json
{
  "id": "work-check-001",
  "kind": "work_check_decision",
  "path": "workcheck/work-check-001.json",
  "outcome": "pass | block",
  "checked_node": "project_setup | source_registration | text_extraction_registration | manifest_update | human_plan_registration | quality_bookkeeping | export",
  "checked_paths": ["project.json", "manifest.json"],
  "missing_or_invalid_paths": [],
  "manifest_issues": [],
  "blockers": [],
  "required_fixes": [],
  "next_stage_allowed": true
}
```

## Critic Decision

```json
{
  "id": "critic-decision-001",
  "kind": "critic_decision",
  "path": "critic/critic-decision-001.json",
  "candidate_path": "artifacts/drafts/section-1.point-1.patch.json",
  "artifact_kind": "draft_point_patch",
  "rubric": "drafting",
  "review_scope": "one paragraph commitment patch",
  "review_request_neutrality": {
    "project_manager_provided_direction": false,
    "allowed_inputs_only": true
  },
  "dependency_paths_checked": ["artifacts/plans/section-plan-1.json", "artifacts/evidence/evidence-pack-001.json"],
  "source_anchor_ids_checked": ["source-001:p4:block-03"],
  "outcome": "pass | fail",
  "blocking_findings": [],
  "nonblocking_suggestions": ["minor wording suggestion"],
  "required_changes": [],
  "source_checks": [
    {
      "claim": "claim being checked",
      "anchor_id": "source-001:p4:block-03",
      "result": "supports | does_not_support | missing | unclear"
    }
  ],
  "project_manager_adjudication": {
    "decision": "accept | revise | waive_nonblocking",
    "rationale": "why this feedback blocks or does not block progress"
  },
  "lock_status": "unlocked | should_lock | locked"
}
```

## Evidence Pack

```json
{
  "id": "evidence-pack-001",
  "kind": "evidence_pack",
  "status": "draft",
  "path": "artifacts/evidence/evidence-pack-001.json",
  "dependencies": ["artifacts/extraction/source-001/extraction-manifest.json"],
  "theme": "evidence theme",
  "source_ids": ["source-01", "source-02"],
  "claims": ["claim grounded in source anchors"],
  "methods": ["methods or basis of evidence"],
  "findings": ["key finding"],
  "limitations": ["known limitation"],
  "evidence_strength": "low | moderate | high | mixed",
  "citation_anchors": ["anchor objects or anchor ids"],
  "counter_evidence": ["conflicting or limiting evidence"]
}
```

## Reading Memo

```json
{
  "id": "reading-memo-001",
  "kind": "reading_memo",
  "status": "draft",
  "path": "artifacts/memos/reading-memo-001.json",
  "dependencies": ["artifacts/evidence/evidence-pack-001.json"],
  "interpretive_notes": ["what this evidence means"],
  "emerging_patterns": ["cross-source pattern"],
  "doubts": ["uncertainty or reliability concern"],
  "contradictions": ["source conflict"],
  "candidate_concepts": ["concept that may structure synthesis"],
  "unresolved_questions": ["question for further reading"],
  "requested_actions": ["rescreen | reextract | targeted_search | revise_question"]
}
```

## Source Read Patch

```json
{
  "id": "source-read-patch-001",
  "kind": "source_read_patch",
  "status": "draft",
  "path": "artifacts/patches/source-001.read-patch.json",
  "source_id": "source-001",
  "source_paths_read": ["artifacts/extraction/source-001/extraction-manifest.json"],
  "target_artifacts": ["artifacts/evidence/evidence-pack-001.json", "artifacts/memos/reading-memo-001.json"],
  "operations": [
    {
      "operation": "add | modify | extend | weaken | contradict | remove",
      "target_artifact_id": "evidence-pack-001",
      "target_path": "content.claims[0]",
      "rationale": "why this source changes the cumulative artifact",
      "citation_anchors": ["source-001:p4:block-03"]
    }
  ],
  "source_summary": "What this single source contributed.",
  "new_risks": ["possible OCR issue in table 2"],
  "updated_artifact_paths": ["artifacts/evidence/evidence-pack-001.v2.json"]
}
```

## Synthesis Claim

```json
{
  "id": "synthesis-claim-001",
  "kind": "synthesis_claim",
  "status": "draft",
  "path": "artifacts/synthesis/synthesis-claims.json",
  "dependencies": ["artifacts/evidence/evidence-pack-001.json", "artifacts/memos/reading-memo-001.json"],
  "claim": "analytical cross-source claim",
  "supporting_evidence": ["source-grounded support"],
  "conflicting_evidence": ["source-grounded conflict or limitation"],
  "applicability_conditions": ["when this claim applies"],
  "evidence_strength": "low | moderate | high | mixed",
  "relevance_to_review_thesis": "how this claim supports the review argument",
  "citation_anchors": ["anchor ids"],
  "gap_classification": "optional classified gap, not a vague assertion"
}
```

## Argument Plan

```json
{
  "id": "argument-plan-001",
  "kind": "argument_plan",
  "status": "draft",
  "path": "artifacts/plans/argument-plan.json",
  "dependencies": ["artifacts/synthesis/synthesis-claims.json", "artifacts/synthesis/review-thesis.json"],
  "thesis": "review thesis",
  "approved_claim_ids": ["claim-01"],
  "analytical_contribution": "what the manuscript adds beyond summary",
  "thesis_alignment": "how the sections test or develop the thesis",
  "evidence_coverage": ["anchor ids or evidence pack ids"],
  "summary_structure": false,
  "sections": [
    {
      "title": "section title",
      "role": "argument role",
      "claim_ids": ["claim-01"],
      "evidence_pack_ids": ["evidence-01"],
      "section_type": "theme_analysis | mechanism | limitation | implication"
    }
  ]
}
```

## Draft Point Patch

```json
{
  "id": "draft-point-patch-001",
  "kind": "draft_point_patch",
  "status": "draft",
  "path": "artifacts/drafts/section-1.point-1.patch.json",
  "section_plan_id": "section-plan-001",
  "paragraph_commitment_id": "section-1-commitment-1",
  "assigned_key_point": "Explain why interface instability changes thermal safety interpretation.",
  "dependencies": ["artifacts/plans/section-plan-1.json", "artifacts/synthesis/synthesis-claims.json", "artifacts/evidence/evidence-pack-001.json"],
  "target_draft_text_path": "drafts/section-1.md",
  "operation": "add | modify | extend | weaken | contradict | remove | transition",
  "insert_after": "paragraph-id-or-null",
  "paragraph_text": "Draft paragraph for this one commitment.",
  "claim_ids": ["claim-01"],
  "citation_anchor_ids": ["source-001:p4:block-03"],
  "trace_fragment": {
    "paragraph_id": "section-1-p1",
    "source_ids": ["source-001"],
    "evidence_pack_ids": ["evidence-pack-001"]
  },
  "updated_artifact_paths": [],
  "integration_required": true,
  "drafting_risks": ["causal wording should remain conditional"]
}
```

## Export Trace

```json
{
  "id": "export-trace-001",
  "kind": "export_trace",
  "path": "export/export-trace.json",
  "manuscript_id": "manuscript-01",
  "sections": [
    {
      "section_title": "section title",
      "paragraph_ids": ["paragraph-01"],
      "claim_ids": ["claim-01"],
      "source_ids": ["source-01"],
      "citation_anchor_ids": ["source-01:p4:thermal-runaway-definition"]
    }
  ],
  "workflow_summary": {
    "locked_artifacts": 0,
    "critic_failures": 0,
    "human_escalations": 0
  }
}
```

## Quality Decision

```json
{
  "id": "quality-decision-001",
  "kind": "quality_decision",
  "path": "quality/quality-decision-001.json",
  "intervention_mode": "autonomous_quality_test",
  "outcome": "select | reject_all",
  "selected_candidate_path": "artifacts/drafts/section-1.v3.json or null",
  "candidate_paths": ["artifacts/drafts/section-1.v1.json", "artifacts/drafts/section-1.v2.json"],
  "critic_decision_paths": ["critic/section-1.v1.critic.json", "critic/section-1.v2.critic.json"],
  "source_verification": {
    "fatal_source_failures": [],
    "verified_anchor_ids": ["source-01:p4:thermal-runaway-definition"]
  },
  "reasons": ["selected candidate has no fatal source-grounding failures"],
  "required_changes_if_rejected": []
}
```
