# Model and Runtime Portability

This assessment workflow must work with different model providers and agent hosts. Do
not assume a specific model provider, IDE, CLI, runtime, or API.

## Model-Agnostic Contract

Every agent invocation should be expressible as:

```json
{
  "role": "recon|tool-discovery|find|verify|report|patch|review",
  "model": "provider/model or host default",
  "prompt": "task instructions",
  "tools": ["host-provided tools"],
  "input_artifacts": ["paths"],
  "output_artifacts": ["paths"],
  "max_budget": "turns/tokens/time if supported",
  "resume_id": "optional host session id"
}
```

The host may implement this with any remote model, local model, IDE agent, CLI
agent, or human-in-the-loop execution. The skill only requires the file-based
protocol.

## Agent Roles

Use role-specific prompts and outputs rather than provider-specific features:

- `recon`: map target, profile, attack surface, and execution options.
- `tool-discovery`: search current tools/advisories and write provenance.
- `find`: produce candidate findings or PoCs.
- `verify`: independently reproduce, reject, or mark static-only.
- `report`: write evidence-grounded reports.
- `patch`: produce candidate fixes and run available verification.
- `review`: critique reports, patches, or workflow changes.

## Tool Runtime Contract

Tools are capabilities supplied by the host. The skill may request classes of
tools, but should not require exact names:

- filesystem read/write/search.
- shell execution.
- web search and web fetch.
- package manager access.
- container or VM execution.
- code-editing capability.
- subagent/task spawning.

If a capability is missing, adapt:

- no web search: use local docs and package manifests, then mark discovery limited.
- no shell: perform static/source-only analysis and write manual commands.
- no container/VM: document the execution risk; use static profile unless the user authorizes local execution or the target is already trusted/local.
- no subagents: run roles sequentially in the main agent and keep outputs on disk.

## Provider-Neutral Structured Output

Prefer JSON files over provider-specific XML tags. If a model is better at tags,
the runtime can translate tags into JSON before writing artifacts.

Canonical files:

```text
results/<target>/<ts>/profile.json
results/<target>/<ts>/tool_findings.jsonl
results/<target>/<ts>/verified_findings.jsonl
results/<target>/<ts>/reports/manifest.jsonl
results/<target>/<ts>/reports/bug_NN/report.json
```

## Resume

Resume is file-based. Provider session resume is optional optimization, not a
requirement.

The required resume data is:

- `.state/progress.json`.
- phase checkpoint JSON files.
- role output artifacts.
- raw logs/transcripts if available.

If provider resume is unavailable, relaunch the role with prior artifacts and a
short continuation prompt.
