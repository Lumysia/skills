---
name: gen-xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
---

# XLSX Creation, Editing, and Analysis

## Overview

Use **pandas** for data analysis, bulk operations, and simple export. Use **openpyxl** for formulas, formatting, and other Excel-specific features. See `references/code-examples.md` for snippets of both.

## Requirements for All Outputs

- **Professional font**: use a consistent, professional font (e.g., Arial, Times New Roman) unless the user or an existing template says otherwise.
- **Zero formula errors**: every deliverable with formulas MUST have zero errors (`#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`) after recalculation.
- **Preserve existing templates**: when modifying a file with established formatting, exactly match its existing conventions — existing template conventions always override the defaults below.
- **Financial models**: follow the color coding, number formatting, and formula construction conventions in `references/financial-modeling.md`.

## Core Workflow

1. **Choose a tool**: pandas for data, openpyxl for formulas/formatting.
2. **Create or load** the workbook.
3. **Modify**: add data, formulas, and formatting. Always use Excel formulas (e.g. `=SUM(B2:B9)`) instead of computing a value in Python and hardcoding the result — this keeps the sheet recalculable when source data changes. See `references/code-examples.md`.
4. **Save** the file.
5. **Recalculate — mandatory whenever the file contains formulas**:
   ```bash
   python scripts/recalc.py output.xlsx [timeout_seconds]
   ```
   LibreOffice is required and assumed to be installed; the script configures it automatically on first run, including in sandboxed environments where Unix sockets are restricted (`scripts/office/soffice.py`).
6. **Verify and fix errors**: the script returns JSON with `status` and, if errors were found, an `error_summary` with locations per error type. Fix any reported errors and recalculate again before delivering. See `references/verification-checklist.md` for the full checklist and JSON format.

## Resources

- `scripts/recalc.py <file> [timeout]`: recalculates all formulas across all sheets and scans for Excel errors.
- `references/code-examples.md`: pandas/openpyxl snippets for reading, creating, and editing workbooks.
- `references/financial-modeling.md`: color coding, number formatting, and formula/documentation conventions for financial models.
- `references/verification-checklist.md`: pre/post-build formula checklist and how to interpret `recalc.py` output.

## Code Style Guidelines

- Python for Excel operations: minimal and concise — no unnecessary comments, verbose variable names, or print statements.
- In the Excel file itself: comment complex formulas and important assumptions, and document sources for hardcoded values.
