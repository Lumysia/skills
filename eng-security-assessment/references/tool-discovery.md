# Tool and Research Discovery

Use this reference whenever current tooling, advisories, or target-specific
techniques could improve a run.

## Principle

Memory is not enough. Actively discover current tools, public advisories, target
release notes, and ecosystem-specific scanners before choosing a campaign.

Do this within the authorized target scope. Do not use the workflow to attack
third-party systems or run tools against infrastructure outside the engagement.

## Research Inputs

Search for:

- target language and framework security tooling.
- fuzzers and test-driver generators for the stack.
- static analyzers and linters for relevant vulnerability classes.
- recent CVEs/advisories for the exact package/framework/version.
- project-specific security notes, changelogs, and bug bounty disclosures.
- GitHub repositories with maintained tools and clear usage docs.

Record provenance:

```json
{
  "tool": "name",
  "source_url": "https://...",
  "version_or_commit": "...",
  "why_selected": "...",
  "profile": "web|java|go|...",
  "install_location": ".tools/<run-id>/<tool>",
  "risk_notes": "..."
}
```

Write provenance to:

```text
.state/tool_discovery.json
```

Tool discovery is an internal reproducibility artifact. Put the full discovery
history in `RUN_DOSSIER.*`. Final reports may summarize the assessment
methodology, but must not include the full discovery history in the main body.

## Tool Selection Criteria

Prefer tools that are:

- actively maintained.
- specific to the target stack or bug class.
- runnable locally or in a container.
- capable of producing machine-readable output.
- easy to reproduce with pinned versions.
- compatible with the user's authorization and environment.

Avoid tools that require sending proprietary code or secrets to third-party
services unless the user explicitly approves.

## Installation Locations

Use one of these, in order:

```text
1. Existing project dev dependencies, if already present.
2. .tools/<run-id>/ for downloaded tools.
3. A disposable Docker image/container.
4. A target-specific Dockerfile/profile runtime.
```

Do not install global tools into the host unless the user explicitly requests it.
Pin versions or commits where possible.

## Allowed Discovery Actions

The skill may:

- search the web for tools, advisories, docs, and examples.
- use GitHub search/API when available, for example `gh search repos`, `gh search code`, or `gh api`.
- clone public tool repositories into `.tools/`.
- install package-manager tools into an isolated environment.
- build disposable Docker images for tool execution.
- run tools against local authorized source or local test instances.
- compare outputs from multiple tools and pick high-signal findings for verification.

The skill must ask before:

- running tools against a live network target.
- sending code, logs, or findings to an external hosted scanner.
- using credentials, cloud accounts, or production infrastructure.
- installing host-global packages.
- exploiting a public CVE outside a local authorized test environment.

## Discovery Workflow

```text
1. Infer target stack and bug classes.
2. Search web/GitHub for current tools and advisories.
3. Pick 2-5 candidate tools or techniques.
4. Record provenance and install plan.
5. Install in isolated workdir/container.
6. Run a smoke test against a tiny fixture or read-only target path.
7. Run against authorized target.
8. Normalize outputs into findings.jsonl.
9. Independently verify promising findings.
10. Keep only evidence-backed results.
```

## Output Normalization

Normalize external tool output to:

```json
{
  "id": "tool-f001",
  "tool": "...",
  "profile": "...",
  "category": "...",
  "severity": "...",
  "file": "...",
  "line": 0,
  "entrypoint": "...",
  "evidence": "...",
  "poc": "...",
  "verification": "unverified|static-only|reproduced|rejected",
  "dedup_key": "..."
}
```

Write normalized outputs under:

```text
results/<target>/<timestamp>/tool_findings.jsonl
```

## Verification Rule

External tool output is not a final finding. Treat it as a lead until the main
agent or verifier reproduces it, proves the source path, or marks it static-only
with explicit confidence limits.
