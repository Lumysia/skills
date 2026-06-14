# Tool Discovery Agent

Discover current tools, advisories, and target-specific techniques for the selected profile and record provenance.

## Inputs

- `profile`
- `target_stack_evidence`
- `vulnerability_classes`
- `workspace_dir`
- `tool_root`
- `report_path`

## Process

1. Use `references/tool-discovery.md` for discovery rules and safety limits.
2. Search current docs, advisories, maintained tools, and ecosystem examples when web/GitHub tools are available.
3. Prefer local/project tools before downloaded tools.
4. Record provenance, version or commit, install location, risk notes, and why each tool was selected or rejected.
5. Do not send private code/logs to hosted scanners or install global packages without approval.

## Output

Save to `report_path` and mirror selected provenance into `security-assessment-workspace/state/tool_discovery.json` when possible:

```json
{
  "role": "tool_discovery",
  "selected_tools": [
    {
      "tool": "<name>",
      "source_url": "<url>",
      "version_or_commit": "<version>",
      "profile": "<profile>",
      "install_location": "security-assessment-workspace/tools/<run-id>/<tool>",
      "why_selected": "<reason>",
      "risk_notes": "<risk>"
    }
  ],
  "rejected_tools": ["<tool and reason>"],
  "discovery_limits": ["<missing web|shell|policy limit>"],
  "coordinator_action": "<install|skip|ask|continue>"
}
```

## Criteria

- Tool discovery is evidence, not final findings.
- Keep full history in internal artifacts, not the final report body.
