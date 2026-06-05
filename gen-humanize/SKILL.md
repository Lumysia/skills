---
name: gen-humanize
description: Humanize drafted text by preserving meaning, matching author voice, strengthening evidence, and removing formulaic AI-sounding patterns. Use when rewriting essays, articles, documentation, posts, emails, reports, or other prose to sound more natural and author-specific.
---

# General Humanize

Use this skill to turn generic or AI-sounding prose into writing with clearer authorship, appropriate register, concrete detail, and stronger editorial judgment.

Adapted from a user-provided research report on reducing AI-like writing, with [blader/humanizer](https://github.com/blader/humanizer) used as a pattern reference.

## Flow

1. Identify the text's purpose, audience, genre, risk level, and required format.
2. If author samples are available, infer a compact style and preference card before rewriting.
3. Preserve the original meaning, claims, constraints, citations, and required coverage.
4. Replace generic structure with a purpose-led outline, paragraph intent, and evidence slots.
5. Rewrite for concrete detail, natural rhythm, appropriate stance, and genre fit.
6. Audit for formulaic language, unsupported claims, repetitive cadence, and template openings or endings.
7. Return the revised text plus a short change note when useful.

Hard dependencies: source text and target use. Ask once if either is missing.

For style and preference cards, rewrite rules, audit checks, quality evaluation, and output formats, read `references/workflow.md`.
