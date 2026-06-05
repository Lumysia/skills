# Text Extraction Reference

## Contents

- When to use Text Extraction Agent
- Extraction priority
- MinerU policy
- Docling fallback policy
- Installation and capability checks
- Output registration
- Clean-text-only downstream rule

## When To Use Text Extraction Agent

Launch Text Extraction Agent before Reader Agent when user inputs include:

- PDFs, scanned PDFs, or image-heavy PDFs
- PNG, JPEG, TIFF, BMP, WEBP, or other document images
- DOCX, PPTX, XLSX, CSV, HTML, Markdown, LaTeX, XML, or mixed document folders
- Audio/video files when transcription tooling is available and the user explicitly wants them included
- Any source format whose clean text, reading order, tables, formulas, or figure captions are not already available

If the user provides already-clean Markdown, text, or validated JSON with source provenance and anchors, skip extraction and register those files directly as clean sources.

## Extraction Priority

Use this order:

1. Existing clean text/Markdown/JSON with clear provenance and anchors.
2. MinerU for PDFs, scanned/layout-heavy sources, scientific documents, tables, formulas, images, and OCR-heavy material.
3. Docling as fallback when MinerU is missing, unsuitable, fails, or when the source format is better handled by Docling's broad converter.
4. Manual/user-provided extraction only when automated extraction fails or installation is not allowed.

## MinerU Policy

MinerU is preferred for complex PDF-style extraction because it is designed for structure-preserving document parsing and can output Markdown/JSON with reading order, OCR, tables, formulas, and layout-aware content.

Supported input categories to route to MinerU when available:

- PDF
- Document images
- DOCX, PPTX, XLSX where the local MinerU version supports them
- Scanned or OCR-heavy documents
- Scientific papers with formulas, tables, figures, and multi-column layout

MinerU may support CPU execution and GPU/MPS acceleration depending on platform, hardware, Python version, backend, model mode, and installation extras.

## Docling Fallback Policy

Use Docling when:

- MinerU is not installed and the user does not approve installation.
- MinerU fails on a file.
- The machine does not meet the chosen MinerU backend requirements.
- The source format is Office, HTML, Markdown, CSV, image, audio/video transcription setup, or another broad-format conversion task Docling handles well.
- A lightweight conversion to Markdown/JSON/Text is sufficient.

Docling is especially useful as a broad document converter that can normalize many input formats into Markdown, JSON, or text for downstream agents.

## Installation And Capability Checks

Do not silently install heavy extraction tooling. If MinerU or Docling is missing, ask permission before installing.

When MinerU is missing and the user approves installation:

1. Detect operating system.
2. Detect Python version and package environment.
3. Detect NVIDIA GPU, CUDA availability, Apple Silicon/MPS availability, VRAM, RAM, and disk space when possible.
4. If the machine appears compatible with GPU/MPS acceleration, choose the accelerated MinerU installation/backend recommended for that environment.
5. If GPU/MPS acceleration is unavailable or uncertain, choose CPU-compatible MinerU mode or a service/client mode.
6. If MinerU installation is unsafe, unsupported, too large, or likely to fail, explain the constraint and use Docling fallback if allowed.
7. Record all install decisions, detected capabilities, backend choice, and failures in `artifacts/extraction/extraction-log.json`.

When Docling is missing and needed as fallback, ask permission before installing it. Prefer a local isolated environment when the host supports one.

Never install tools when:

- The user denied installation.
- The environment appears managed/read-only.
- The install would require secrets, privileged access, or external cost not approved by the user.
- Hardware/software compatibility is clearly insufficient for the intended backend.

## Output Registration

Extraction tools may export their own folders and files. Do not duplicate or re-render these outputs just to fit a preferred filename. Treat the extractor's native output folder/files as the source of truth when they contain usable clean text, Markdown, JSON, tables, figures, formulas, or anchor-like spans.

For each raw source, Text Extraction Agent should place or register extractor output under the project, for example:

```text
artifacts/extraction/<source-id>/mineru-output/...
artifacts/extraction/<source-id>/docling-output/...
artifacts/extraction/<source-id>/extraction-manifest.json
artifacts/extraction/<source-id>/extraction-log.json
```

If MinerU/Docling already produced Markdown/JSON/text files, register those paths in the extraction manifest instead of creating new duplicate files. Only create supplemental files when the native output lacks a necessary manifest, summary, or anchor index.

The extraction manifest should include:

- `source_id`
- `source_path`
- `extractor`: `existing-clean | mineru | docling | manual`
- `extractor_version` when available
- `backend_mode`: `gpu | mps | cpu | service | fallback | unknown`
- `native_output_dir`
- `native_output_files`
- `primary_clean_text_path`
- `primary_markdown_path`
- `primary_json_path`
- `anchor_index_path` when available or supplemented
- `summary_path` when available or supplemented
- `pages_or_sections`
- `tables`
- `figures`
- `formulas`
- `reading_order`
- `warnings`
- `extraction_confidence`

Supplemental anchor indexes, when needed, should preserve source provenance without replacing native output:

```json
{
  "anchor_id": "source-01:p4:block-03",
  "source_id": "source-01",
  "source_path": "sources/paper.pdf",
  "page": 4,
  "section": "Methods",
  "text": "Extracted source span.",
  "extractor": "mineru"
}
```

## Clean-Text-Only Downstream Rule

After extraction, Reader/Synthesis/Writer/Critic agents should use only registered extraction outputs:

- native MinerU/Docling Markdown/text/JSON files,
- extraction manifests,
- anchor indexes when native output provides them or Text Extraction Agent supplements them,
- extraction summaries when available,
- extraction logs when diagnosing failures.

They should not use raw PDFs or unusual raw source files directly unless specifically auditing extraction quality. If clean extraction is unavailable, stop and either run fallback extraction, ask the user for clean text, or narrow the source set.
