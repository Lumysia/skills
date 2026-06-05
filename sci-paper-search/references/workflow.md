# Paper Search Workflow

## External Tooling

Prefer available external tools over vendoring source code into this skills repository.

Discovery order:

1. Use configured MCP paper-search tools if the host exposes them.
2. Use an installed `paper-search` CLI if present.
3. Use `uvx paper-search-mcp` as an MCP server command if the host can configure MCP servers and the user accepts on-demand package execution.
4. Use a local `paper-search-mcp` clone if the user provides a path or the path is already documented in project artifacts.
5. Fall back to direct web or database search only when no external paper-search tool is available.

`paper-search-mcp` is an MIT-licensed external project from `https://github.com/openags/paper-search-mcp`. Treat it as an optional MCP server or CLI, not as a submodule or copied implementation unless the user explicitly asks.

## CLI Usage

If the CLI is installed globally or in the active environment:

```bash
paper-search sources
paper-search search "<query>" -n <max_per_source> -s <sources> -y <year_or_range>
paper-search download <source> <paper_id> -o <output_dir>
paper-search read <source> <paper_id> -o <output_dir>
```

If using a local clone:

```bash
uv run --directory <paper-search-mcp-path> paper-search sources
uv run --directory <paper-search-mcp-path> paper-search search "<query>" -n <max_per_source> -s <sources> -y <year_or_range>
uv run --directory <paper-search-mcp-path> paper-search download <source> <paper_id> -o <output_dir>
uv run --directory <paper-search-mcp-path> paper-search read <source> <paper_id> -o <output_dir>
```

For MCP server setup, `paper-search-mcp` can be launched by package entrypoint:

```bash
uvx paper-search-mcp
```

After the MCP server is configured, use the host-exposed MCP tools rather than appending CLI subcommands to the server command.

Search and download commands return JSON. Read commands may return plain text. Capture stderr separately when possible because configuration warnings may be written there.

## MCP Usage

When MCP tools are available, prefer the highest-level tool that matches the task:

- Search: multi-source paper search tool, or source-specific search tools when the user named a platform.
- Download: download tool for a known source and paper id, or fallback download tool when metadata contains DOI or URLs.
- Read: read/extract-text tool for a known source and paper id.

Record which MCP tool was used, its input arguments, and whether the result was search-only, downloaded file, or extracted text.

## Source Selection

Use source names supported by the external tool when available, such as `arxiv`, `pubmed`, `biorxiv`, `medrxiv`, `semantic`, `crossref`, `openalex`, `pmc`, `core`, `europepmc`, `dblp`, `openaire`, `citeseerx`, `doaj`, `base`, `zenodo`, `hal`, `ssrn`, and `unpaywall`.

Map targeted source choices to the user's request and the external tool's supported source names:

- Computer science or preprints: `arxiv`, `semantic`, `crossref`, `openalex`, `dblp`.
- Biomedical topics: `pubmed`, `pmc`, `europepmc`, `biorxiv`, `medrxiv`, `semantic`.
- Broad metadata discovery: `openalex`, `crossref`, `semantic`.
- Repository or archived outputs: `core`, `openaire`, `zenodo`, `hal`.

Use broad source sets when the user asks for coverage, scoping, or corpus construction. Do not exclude a source category unless the user request, tool behavior, or unavailable credentials require it.

## Output Records

Return or write normalized records with these fields when available:

```json
{
  "title": "",
  "authors": [],
  "year": null,
  "source": "",
  "source_id": "",
  "doi": "",
  "url": "",
  "abstract": "",
  "query": "",
  "retrieval_status": "search_result",
  "artifact_path": "",
  "notes": ""
}
```

Use `retrieval_status` values such as `search_result`, `downloaded`, `read`, `failed`, or `duplicate`.

## Handoff Rules

For review-writing workflows, write search results and retrieved files under the active project directory when one exists:

```text
review-project/
  sources/
  artifacts/search/
  artifacts/retrieval/
```

For chat-only workflows, return a compact table with title, authors, year, source, DOI or URL, and why the paper is relevant.

Do not invent missing metadata. Mark missing fields as empty or unknown, and include failed searches or download errors when they affect coverage.
