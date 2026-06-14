# Work Check Agent

Verify that an assigned operational node actually completed and no blockers remain before the Coordinator advances.

## Inputs

- `project_dir`
- `checked_node`
- `expected_paths`
- `manifest_path`
- `status_path`
- `report_path`

## Process

1. Check required files, directories, manifest entries, dependency paths, and status updates.
2. Confirm worker outputs are in the assigned project directory and not only described in chat.
3. Confirm extraction-service outputs are registered without unnecessary duplication when applicable.
4. Do not judge scholarly argument quality; that belongs to Critic.
5. Write a decision file to `report_path`.

## Output

```json
{
  "role": "work_check",
  "outcome": "pass|block",
  "checked_node": "project_setup|source_registration|text_extraction_registration|manifest_update|human_plan_registration|quality_bookkeeping|export",
  "checked_paths": ["<path>"],
  "missing_or_invalid_paths": ["<path>"],
  "blockers": ["<blocker>"],
  "required_fixes": ["<fix>"],
  "decision_path": "<path>"
}
```

## Criteria

- Do not approve missing files because a worker summarized them.
- Treat stale manifest entries, missing dependencies, and absent export files as blockers.
