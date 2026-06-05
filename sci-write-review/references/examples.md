# Examples Reference

## Contents

- Research review from PDFs
- Human-approved final plan
- Autonomous quality selection
- Agent runtime implementation
- Common workflows

## Research Review From PDFs

User: "Write a review on solid-state battery thermal safety from these papers."

Process:

1. Project Manager frames the review scope and audience.
2. Text Extraction Agent converts PDFs with MinerU when available, or asks to install MinerU and uses Docling fallback when needed.
3. Text Extraction Agent registers MinerU/Docling native outputs under the project and writes minimal extraction manifests/logs.
4. Work Check Agent verifies extraction output paths and manifest dependencies before Reader starts.
5. Reader reads one source, writes `source_read_patch`, updates evidence/memo artifacts, then repeats source by source.
6. Work Check Agent verifies each patch and updated artifact path before the next source.
7. Critic checks whether cumulative evidence artifacts are grounded and complete after the reading batch.
8. Reader memo files evolve through patches about mechanisms, contradictions, safety conditions, and open questions.
9. Synthesis Agent creates cross-source claim files about thermal pathways, interface instability, mitigation strategies, and evidence limits.
10. Writer drafts one paragraph commitment/key point and writes an independent `draft_point_patch`; parallel writers may only write different patch files.
11. Work Check Agent verifies each writing patch and trace fragment.
12. Project Manager runs one serial integration step to merge approved patches into the section draft.
13. Critic reviews risky point patches immediately or the cumulative section draft after commitments are integrated.
14. Project Manager exports manuscript and trace files.
15. Work Check Agent verifies final export files exist and trace dependencies resolve.

Result: A review manuscript whose major claims can be traced back to source anchors.

## Human-Approved Final Plan

User: "I want to approve the structure before you start drafting."

Process:

1. Agents complete framing, reading, evidence extraction, memos, and synthesis.
2. Synthesis Agent creates an argument plan file.
3. Critic reviews the plan for thesis alignment and evidence coverage.
4. Project Manager presents the approved plan summary and file path to the user.
5. User edits or accepts the plan.
6. Writer drafts only from the human-approved plan file.

Result: The manuscript structure reflects human intent before prose generation begins.

## Autonomous Quality Selection

User: "Make sure the review does not invent claims, but do not ask me to choose every failed retry."

Process:

1. Bootstrap stores `intervention_mode` as `autonomous_quality_test`.
2. Writer drafts a section.
3. Critic detects unsupported generalizations and missing limitations.
4. Writer revises with approved anchors.
5. Critic fails again because one anchor does not support the causal claim.
6. Writer creates multiple revised candidate versions.
7. Project Manager sends candidate paths, critic decision paths, dependency paths, and targeted anchor paths to Quality Test Agent.
8. Quality Test Agent selects only a source-grounded candidate or rejects all.
9. Project Manager approves the selected candidate or requests scoped regeneration.

Result: The final section is selected for evidence faithfulness, not just fluency. Fabricated or source-mismatched claims are not approved.

## Agent Runtime Implementation

User: "Turn this workflow into a CrewAI or multi-agent implementation."

Process:

1. Define artifact schemas and lifecycle states.
2. Implement tools for source registration, MinerU/Docling extraction, reading artifacts, writing artifacts, locking artifacts, listing versions, requesting human approval, quality-testing candidates, and exporting traces.
3. Create Project Manager, Work Check, Text Extraction, Reader, Synthesis, Writer, Critic, and Quality Test agents.
4. Define sequential tasks with typed outputs.
5. Insert critic tasks after every major artifact.
6. Add retry and escalation policy.
7. Test with deterministic clean-text fixtures and at least one PDF/Office-format extraction fixture where practical.

Result: A review-writing agent system that enforces evidence grounding through tools, gates, locks, and traceability.

## Common Workflows

### Blog-Style Review

1. Frame a narrower thesis for a general audience.
2. Extract fewer but stronger evidence anchors.
3. Build a concise argument plan.
4. Draft with readable examples and transparent limitations.
5. Export with source notes or footnotes.

### Scholarly Review

1. Define review type and inclusion boundaries.
2. Screen sources explicitly.
3. Extract methods, limitations, evidence strength, and anchors.
4. Create synthesis claims and counter-evidence tables.
5. Draft sections with citation-rich paragraphs.
6. Export manuscript, references, and trace.

### Technical Documentation Review

1. Frame the review around implementation decisions or technical tradeoffs.
2. Extract version-specific behavior, constraints, examples, and caveats.
3. Synthesize best practices and failure modes.
4. Draft guidance with citations to authoritative sources.
5. Critic checks for outdated, unsupported, or version-ambiguous claims.

### Audit Workflow

1. Parse the existing draft into claims.
2. Map claims to sources and anchors.
3. Flag unsupported, overbroad, duplicated, or contradicted claims.
4. Recommend scoped revisions.
5. Produce an evidence trace and risk report.
