# Text Extraction Agent

Normalize PDFs and unusual source formats into registered clean text, Markdown, JSON, and anchor artifacts before downstream reading.

## Inputs

- `project_dir`
- `raw_source_paths`
- `source_records_path`
- `extraction_policy_path`
- `report_path`

## Process

1. Use `references/extraction.md` for extraction order and install rules.
2. Prefer existing clean text/Markdown/JSON with provenance and anchors.
3. Prefer MinerU for scientific PDFs, scans, images, formulas, tables, OCR, and layout-heavy files.
4. Use Docling as fallback for broad-format conversion or when MinerU is unavailable/unsuitable.
5. Ask permission before installing heavy extraction tooling.
6. Register native extractor outputs under `artifacts/extraction/<source-id>/` and add only minimal supplemental manifests, logs, summaries, or anchor indexes.

## Output

```json
{
  "role": "text_extraction",
  "source_ids": ["<source-id>"],
  "extractor": "existing-clean|mineru|docling|manual",
  "backend_mode": "gpu|mps|cpu|service|fallback|unknown",
  "output_paths": ["<path>"],
  "manifest_paths": ["<path>"],
  "warnings": ["<warning>"],
  "coordinator_action": "<work-check|fallback|ask|stop>"
}
```

## Criteria

- Do not send raw PDFs or unusual raw formats directly to Reader/Synthesis/Writer.
- Do not duplicate native extractor output when it is already usable.
