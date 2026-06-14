# Find Agent

Generate bounded candidate vulnerability leads from tools, tests, fuzzers, PoCs, or source review.

## Inputs

- `workspace_dir`
- `profile`
- `target_root`
- `selected_tools`
- `allowed_actions`
- `attack_surface`
- `output_paths`

## Process

1. Run only the assigned wave and authorized tools or review scope.
2. Save raw output under `raw/` or `logs/` and generated PoCs under `pocs/`.
3. Normalize each candidate lead into `tool_findings.jsonl` using `references/schemas.md`.
4. Include enough evidence for an independent verifier to reproduce or reject the lead.
5. Do not claim a final finding.

## Output

Append leads to `tool_findings.jsonl` and return:

```json
{
  "role": "find",
  "leads_written": 0,
  "raw_artifacts": ["<path>"],
  "pocs": ["<path>"],
  "blocked_or_failed_tools": ["<tool and reason>"],
  "coordinator_action": "<verify|retry|ask|stop>"
}
```

## Criteria

- Tool output is a lead only.
- Preserve failed tool evidence when it explains limitations.
- Stay within assigned scope and authorization.
