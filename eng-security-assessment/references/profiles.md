# Profile Runbooks

These runbooks make non-C/C++ discovery concrete. Use `schemas.md` for artifacts.

## Web Profile

Setup:

- Identify service start command, base URL, auth model, routes, OpenAPI specs, and test fixtures.
- Prefer local dev server or container. Ask before live-network testing.

Tools to consider through `tool-discovery.md`:

- framework linters and security scanners.
- Semgrep rules.
- route/API enumerators.
- request replay scripts.
- dependency advisories.

PoC format:

```json
{
  "method": "GET|POST|...",
  "url": "http://local/...",
  "headers": {},
  "body": "...",
  "preconditions": "auth role, seed data, config"
}
```

Verification:

- Replay minimal request sequence against clean local instance.
- Show expected vs observed authorization, data exposure, injection, traversal, or SSRF evidence.
- Store raw HTTP transcript under `security-assessment-workspace/results/<target>/<ts>/raw/`.

## Java Profile

Setup:

- Detect Maven/Gradle, test commands, service start commands, parser entrypoints.
- Consider Jazzer or unit-test PoCs when appropriate.

PoC format:

- JUnit test, serialized object, input file, HTTP request, or fuzzer seed.

Verification:

- Run `mvn test`, `gradle test`, a focused JUnit test, or a local service replay.
- For deserialization/RCE claims, use harmless witnesses only, such as controlled exception, marker file in temp dir, or safe command in local sandbox when explicitly authorized.

## Go Profile

Setup:

- Detect `go.mod`, packages, existing tests, fuzz targets.

PoC format:

- Go test, fuzz seed, file input, request sequence.

Verification:

- Run focused `go test` or `go test -run`/`-fuzz` within the target package.
- Use panic, invariant violation, differential mismatch, or unsafe sink evidence.

## Rust Profile

Setup:

- Detect `Cargo.toml`, crates, tests, fuzz targets, `unsafe` hot spots.

PoC format:

- Rust test, cargo-fuzz seed, input file, request sequence.

Verification:

- Run focused `cargo test` or profile-specific fuzz command.
- Use panic, sanitizer, unsafe invariant, or differential mismatch evidence.

## Contracts Profile

Setup:

- Detect Foundry/Hardhat/Brownie, contracts, tests, deployment assumptions.

PoC format:

- transaction sequence, accounts/roles, initial state, expected/observed state transition.

Verification:

- Reproduce in local testnet/fork controlled by the user.
- Use invariant violation, unauthorized state change, value extraction, or reentrancy witness.

## Static Profile

Setup:

- Use when execution is unavailable or not authorized.

PoC format:

- source-witness path with attacker-controlled input reasoning.

Verification:

- Separate verify role attempts to disprove the claim.
- Mark final result `static-only`; never call it execution-verified.

## Patch Checks for General Profiles

A patch can be marked verified only if there is a local command or replay that
proves the original PoC no longer works and existing tests still pass.

If no verifier exists, write `patch_result.json` with `status: "unverified"` and
surface the diff for human review only.
