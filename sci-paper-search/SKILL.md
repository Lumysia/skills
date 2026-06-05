---
name: sci-paper-search
description: Search, download, and read academic papers using available external tools such as paper-search-mcp, while recording source metadata and retrieval artifacts for downstream research workflows.
---

# Scientific Paper Search

Use this skill when the user asks to find papers, search academic literature, collect a source corpus, download paper files, or read extracted paper text.

## Startup

Before starting, infer the user's preferred interaction and output language from the request, query terms, existing artifacts, or project conventions. If it cannot be inferred confidently, ask once; then use that language for prompts, summaries, and outputs unless the user specifies otherwise.

## Flow

1. Identify the research question, topic terms, fields, date range, source preferences, and desired output format.
2. Discover available paper-search tooling before manual web search: configured MCP tools, `paper-search` CLI, `uvx paper-search-mcp` as an MCP server, or a local `paper-search-mcp` clone.
3. Use targeted sources first when the user names venues, domains, identifiers, or platforms; use broad multi-source search when coverage matters more than speed.
4. Normalize results into stable source records with title, authors, year, source, id, DOI, URL, abstract or snippet, and retrieval status.
5. Deduplicate by DOI, canonical URL, platform id, and normalized title.
6. Download or read full text only when useful for the task; save files or text artifacts when the host can write files.
7. Return ranked results, saved artifact paths, failed lookups, and suggested next retrieval steps.

Hard dependencies: search query or paper identifier. Ask once if neither can be inferred.

Soft dependencies: preferred sources, date range, max results, output directory, optional API keys, and whether to download or only search.

For external tool discovery, CLI/MCP usage, output records, and handoff rules, read `references/workflow.md`.
