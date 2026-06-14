# Architecture

This is a portable skill-packaged workflow. It is not tied to any repository,
language, model provider, scanner, or CLI.

## Control Plane

The skill owns:

- profile selection.
- tool and advisory discovery.
- state/checkpoints.
- role orchestration.
- result normalization.
- independent verification policy.
- reporting and patch review policy.

## Data Plane

The data plane is whatever the selected profile can safely use:

- project-local tests.
- package-manager tools.
- fuzzers.
- static analyzers.
- local service replay.
- local emulators/testnets.
- containers or VMs when available.
- static-only review when execution is unavailable.

## File-Based Contracts

The workflow communicates through files:

```text
security-assessment-workspace/                  assessment workspace root
security-assessment-workspace/results/<target>/<ts>/  run artifacts, reports, checkpoints
security-assessment-workspace/state/            latest-run index and checkpoint mirror
security-assessment-workspace/tools/<run-id>/   downloaded or generated tools
```

This makes the workflow resumable across model providers and sessions.

## Required Separation

Keep these concerns separate:

- discovery vs verification.
- raw tool output vs normalized leads.
- verified findings vs rejected leads.
- reports vs patches.
- generated patch vs human-approved change.

## Portability

If the host lacks a capability, degrade explicitly:

- no web: limited tool discovery.
- no shell: static-only review or write commands for a human/runtime to execute.
- no execution isolation: avoid running untrusted code.
- no child agents: run `agents/<role>.md` workflows sequentially and write the same artifacts.
