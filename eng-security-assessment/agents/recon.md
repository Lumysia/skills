# Recon Agent

Map the authorized target, likely profiles, attack surface, entrypoints, and execution options without running invasive tests.

## Inputs

- `target_or_results`
- `authorization_scope`
- `profile_hint`
- `workspace_dir`
- `report_path`

## Process

1. Inspect target structure, manifests, README, configs, exposed routes, parsers, services, tests, and deployment hints.
2. Identify candidate profiles and confidence for each.
3. Map attacker-controlled inputs, trust boundaries, sensitive operations, and likely verification options.
4. Do not run live network tests, exploit payloads, or destructive commands.

## Output

Save to `report_path` when possible:

```json
{
  "role": "recon",
  "profiles": ["web", "static"],
  "attack_surface": ["<entrypoint or boundary>"],
  "entrypoints": ["<file|route|service|parser>"],
  "execution_options": ["<safe local execution option>"],
  "verification_options": ["<test|replay|static review option>"],
  "risks_or_blockers": ["<scope or capability issue>"],
  "recommended_first_wave": "<bounded next assessment wave>"
}
```

## Criteria

- Stay inside authorized scope.
- Separate observed evidence from assumptions.
- Provide enough target shape for tool discovery and preflight.
