# Financial Modeling Conventions

Apply these unless the user or an existing template states otherwise.

## Color coding standards (industry-standard)

- **Blue text (RGB: 0,0,255)**: hardcoded inputs, and numbers users will change for scenarios.
- **Black text (RGB: 0,0,0)**: all formulas and calculations.
- **Green text (RGB: 0,128,0)**: links pulling from other worksheets within the same workbook.
- **Red text (RGB: 255,0,0)**: external links to other files.
- **Yellow background (RGB: 255,255,0)**: key assumptions needing attention or cells that need to be updated.

## Number formatting standards

- **Years**: format as text strings (e.g., "2024" not "2,024").
- **Currency**: use `$#,##0` format; always specify units in headers ("Revenue ($mm)").
- **Zeros**: use number formatting to make all zeros "-", including percentages (e.g., `$#,##0;($#,##0);-`).
- **Percentages**: default to `0.0%` format (one decimal).
- **Multiples**: format as `0.0x` for valuation multiples (EV/EBITDA, P/E).
- **Negative numbers**: use parentheses `(123)` not minus `-123`.

## Formula construction

- Place all assumptions (growth rates, margins, multiples, etc.) in separate assumption cells and reference them, rather than hardcoding values into formulas: use `=B5*(1+$B$6)` instead of `=B5*1.05`.

## Documenting hardcodes

Add a comment on the cell, or a note beside it if at the end of a table, in the format:
`"Source: [System/Document], [Date], [Specific Reference], [URL if applicable]"`

Examples:
- "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
- "Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]"
- "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"
- "Source: FactSet, 8/20/2025, Consensus Estimates Screen"
