# Customization

Use customization mode to add a new profile, verifier, report format, or tool
integration. This is generic and does not assume any existing codebase.

## What Can Change

- profile name and selection rules.
- target descriptor fields.
- tool discovery queries and preferred tools.
- PoC format.
- detection oracle.
- verification procedure.
- dedup key.
- report schema extensions.
- patch verification command.

## Interview Checklist

Ask only what is unknown:

- What target type is in scope?
- What vulnerability classes matter?
- What does a PoC look like?
- What is the strongest available verification oracle?
- Can the target run locally, in a container, in an emulator, or only statically?
- What tools are already trusted by the project?
- What output format does the user need?
- What patch verification command should gate candidate fixes?

## Profile Definition Template

```json
{
  "profile": "custom-name",
  "target_indicators": ["files, manifests, frameworks"],
  "attack_surface": ["..."],
  "poc_types": ["..."],
  "detection_oracles": ["..."],
  "verification_methods": ["..."],
  "preferred_tools": ["..."],
  "dedup_key": "...",
  "report_extensions": {},
  "patch_check": "..."
}
```

Save custom profile notes under the run workspace and mirror to `security-assessment-workspace/state/` when useful:

```text
security-assessment-workspace/results/<target>/<ts>/artifacts/custom_profile.json
security-assessment-workspace/state/custom_profile.json
```

## Validation

Before using a custom profile at scale:

- create or identify a small known-vulnerable fixture.
- run tool discovery.
- generate at least one candidate lead.
- verify or reject it independently.
- write a report using `schemas.md`.
- test resume by stopping after a phase and continuing from state.

## Editing Rule

If customization requires editing files outside `security-assessment-workspace/state/`,
`security-assessment-workspace/tools/`, or `security-assessment-workspace/results/`, ask for explicit approval and summarize
the intended files first.
