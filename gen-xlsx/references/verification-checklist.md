# Formula Verification Checklist

## Before building
- Confirm column mapping (e.g., column 64 = BL, not BK).
- Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6).
- Verify dependencies: check that all cells referenced in formulas exist.

## While building
- Test formulas on 2-3 sample cells before applying broadly; verify they pull the correct values.
- Keep formulas consistent across all projection periods.
- Check denominators before dividing, to avoid `#DIV/0!`.
- Double-check every cell reference points to the intended cell, to avoid `#REF!`.
- Use `Sheet1!A1` syntax for cross-sheet references.
- Watch for far-right columns — FY data often lands in columns 50+.
- Search all occurrences of a value, not just the first match.
- Handle nulls explicitly with `pd.notna()` before feeding values into formulas.
- Test edge cases: zero, negative, and very large values.
- Verify no unintended circular references.

## After recalculating (`scripts/recalc.py`)

The script returns JSON:

```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,              // Total error count
  "total_formulas": 42,           // Number of formulas in file
  "error_summary": {              // Only present if errors found
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

If `status` is `errors_found`, use `error_summary` to find and fix each error, then recalculate again:
- `#REF!`: invalid cell references
- `#DIV/0!`: division by zero
- `#VALUE!`: wrong data type in formula
- `#NAME?`: unrecognized formula name
