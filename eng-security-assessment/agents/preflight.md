# Preflight Agent

Check runtime capabilities, safety constraints, and verifier options before running finders.

## Inputs

- `workspace_dir`
- `target_root`
- `profile`
- `authorization_scope`
- `selected_tools`
- `report_path`

## Process

1. Identify available shell, filesystem, web, package manager, container/VM, browser, local service, and subagent capabilities.
2. Determine which checks can run safely under the authorization scope.
3. Choose a verifier strategy before finding starts.
4. Record commands that may run, commands that require approval, and commands that are blocked.
5. Switch to static-only when no safe execution or verifier exists.

## Output

```json
{
  "role": "preflight",
  "execution_available": true,
  "verification_available": true,
  "allowed_actions": ["<safe command or method>"],
  "approval_required": ["<action needing user approval>"],
  "blocked_actions": ["<blocked action and reason>"],
  "verification_strategy": "<replay|test|fuzz|static-only>",
  "coordinator_action": "<continue|ask|switch-static|stop>"
}
```

## Criteria

- Do not run invasive tests in preflight.
- Treat missing safe execution as a profile/verification constraint, not permission to improvise.
