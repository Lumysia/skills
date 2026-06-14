# General Vulnerability Discovery

This assessment workflow is domain-general. It discovers or selects a profile for the
target, then runs a profile-specific find/verify/report loop.

## Profile Model

Every profile must define the same abstract contract:

```text
target shape -> input/attack surface -> detection oracle -> PoC artifact -> independent verifier -> report -> optional patch check
```

Built-in profile names:

```text
auto          infer from repository and target config
native        use existing local project tools/tests/fuzzers without a predefined profile
web           HTTP/API/web app vulnerabilities
java          JVM services/libraries, deserialization, injection, Jazzer-style fuzzing
go            Go services/libraries, fuzzing, panic/differential/invariant oracles
rust          Rust services/libraries, fuzzing, panic/unsafe/invariant oracles
contracts     smart contracts, invariant/property checks, transaction PoCs
static        source-only review without target execution
custom        user-defined profile from customization mode
```

Profile selection:

- If `--profile` is supplied, use it.
- If `--profile auto`, inspect repo files, build files, Dockerfiles, manifests, target config, and README.
- If multiple profiles fit, choose the safest high-signal first wave and record alternatives.
- If execution is needed and no safe execution environment exists, fall back to `static` or ask before proceeding when the user's authorization decision is required.

## Universal Autonomous Loop

Use this loop for every profile:

```text
1. Scope: identify authorized target, trust boundary, and attack surface.
2. Recon: read code/config/docs and map inputs to sensitive behavior.
3. Tool discovery: search current ecosystem tools/advisories for this stack and bug class.
4. Preflight: choose or build a safe runner, detector, verifier, and artifact directory.
5. Find: generate inputs or tests, run tools/agents, collect candidate findings.
6. Verify: independently reproduce or falsify each finding.
7. Dedup: group by root cause, not just stack trace or endpoint string.
8. Report: write evidence-grounded impact, reachability, constraints, and PoC.
9. Patch: if requested, generate candidate fixes and verify with executable oracles.
10. Resume/status: keep enough state to continue after interruption.
```

## Profile Examples

### web

Target shape: HTTP service, API, frontend/backend app, route handlers.

Inputs: HTTP request sequences, parameters, headers, cookies, uploads, auth state.

Detection oracles:

- response/body/status differential.
- SQLi/XSS/SSRF/path traversal evidence.
- authorization bypass witness.
- server exception with reachable endpoint.
- canary endpoint/file/DNS callback in an authorized lab.

Verifier: replay a minimal request sequence in a clean test instance or mocked
environment. Do not attack third-party systems.

### language library/service profiles

Target shape: package, service, parser, API client, protocol implementation.

Inputs: unit tests, fuzz seeds, generated requests, files, serialized objects.

Detection oracles:

- crash/panic/exception.
- sanitizer/fuzzer finding.
- invariant violation.
- differential mismatch against reference behavior.
- unsafe sink reached with attacker-controlled input.

Verifier: fresh run with a minimized PoC and clear preconditions.

### contracts

Target shape: smart contract project.

Inputs: transaction sequence, account roles, chain state.

Detection oracles:

- invariant violation.
- unauthorized state transition.
- value extraction.
- reentrancy or ordering witness.

Verifier: reproduce in a local testnet/fork controlled by the user.

### static

Target shape: any source tree where execution is unavailable.

Detection oracle: evidence-grounded source reasoning plus independent reviewer.

Verifier: separate verify role attempts to disprove exploitability and ranks
confidence. Mark output as static/unverified; do not call it execution-verified.

## Finding Quality Bar

A candidate finding should include:

- affected component and entry point.
- attacker-controlled input path.
- vulnerable operation or invariant violation.
- concrete PoC artifact or source-level witness.
- independent verification result.
- constraints and false-positive risks.
- dedup/root-cause reasoning.

If the profile cannot produce executable verification, the report must clearly
say `verification: static-only`.

## Independent Discovery

Role agents may discover vulnerabilities by combining code review, tools, tests, fuzzers, and generated PoCs. The Coordinator must still separate:

- discovery agent/tool output.
- independent verification evidence.
- final report claims.

Do not let the same unverified reasoning serve as both finding and verifier.
