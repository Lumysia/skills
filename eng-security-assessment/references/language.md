# Report Language

Reports must follow the user's requested language.

## Language Selection

Use this priority order:

1. Explicit user instruction, such as "write the report in Chinese" or "English report".
2. Existing engagement or project instruction file, if it specifies report language.
3. The language used by the user in the current request.
4. Ask one short clarification question if the report audience is ambiguous.

Record the selected language in:

```text
reports/bug_NN/report.json language
```

## Scope

Apply the selected language to:

- `FINAL_REPORT.md`.
- `FINAL_REPORT.pdf`.
- section headings.
- executive summary.
- per-finding summaries.
- remediation guidance.
- limitations and next steps.
- methodology labels and phase names.

Raw technical artifacts may remain in their original language:

- command output.
- stack traces.
- source code snippets.
- HTTP transcripts.
- tool names and rule ids.
- CVE/advisory titles.

When raw evidence is in another language, summarize it in the report language
and preserve the original artifact path.

## No Casual Mixed-Language Reports

Do not casually mix English labels into a non-English report. If the target
language is Chinese, headings and prose should be Chinese, not a mix such as
`Recon`, `Tool discovery`, `Find/Verify`, `Exploitability` embedded as section
labels.

Use one of these approaches consistently:

1. Fully localized labels.
2. Localized label with English term in parentheses on first use.
3. English technical term retained only when it is a standard artifact/tool name
   or would be less clear when translated.

Example for Chinese reports:

```text
方法

- 侦察：字符串、导入表、PE 头、安全特性与网络入口点。
- 工具发现：pefile、capstone、PowerShell/.NET。
- 发现与验证：静态反汇编定位漏洞路径，并由独立验证器复核。
- 可利用性分析：计算偏移、受控状态、攻击原语、缓解机制和 ROP/shellcode 可行性。
```

Avoid:

```text
- Recon: ...
- Tool discovery: ...
- Find/Verify: ...
- Exploitability: ...
```

## Terminology Consistency

For technical terms, choose a consistent style at the start of the report:

- Translate common process terms: recon -> 侦察, verification -> 验证,
  exploitability -> 可利用性, primitive -> 攻击原语, mitigation -> 缓解机制.
- Keep canonical tool/library names unchanged: pefile, capstone, Semgrep,
  Foundry, PowerShell/.NET.
- For terms like ROP, shellcode, SSRF, XSS, JWT, CSP, keep the acronym but explain
  it once if the audience may need it.
- Do not alternate between translated and untranslated variants for the same
  concept in the same report.

If a report is long, include a short terminology table near the start or in an
appendix.

## Bilingual Reports

Only produce bilingual output if the user asks for it or the engagement context
requires it. If bilingual output is requested, use this pattern:

```text
Primary language section first.
Short secondary-language summary after each major section or in an appendix.
```

## Consistency

Use the same selected language across Markdown and PDF. Internal JSON/JSONL
artifacts may contain normalized machine-readable values, but reader-facing text
fields should still follow the selected language. Do not export an English PDF
from a Chinese Markdown report unless the user asked for separate language
variants.
