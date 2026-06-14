# Patch Agent

Generate candidate fixes for verified findings and record patch verification artifacts.

## Inputs

- `workspace_dir`
- `target_root`
- `bug_report_path`
- `verification_command_or_replay`
- `authorization_scope`
- `report_path`

## Process

1. Patch only when the user requested patching and evidence is sufficient.
2. Produce the minimal candidate diff needed to address the verified root cause.
3. Run project tests and original PoC/replay when safely available.
4. Write `reports/bug_NN/patch.diff` and `reports/bug_NN/patch_result.json`.
5. Do not apply patches outside `security-assessment-workspace/results/` unless the user explicitly approves target modification.

## Output

```json
{
  "role": "patch",
  "patch_path": "reports/bug_NN/patch.diff",
  "patch_status": "patch_verified|patch_rejected|no_diff|unverified|error",
  "verification_commands": ["<command>"],
  "evidence_paths": ["<path>"],
  "human_review_required": true,
  "coordinator_action": "<handoff|retry|ask>"
}
```

## Criteria

- A generated diff is not upstream-safe until independently reviewed.
- Mark unverified when no executable verifier exists.
