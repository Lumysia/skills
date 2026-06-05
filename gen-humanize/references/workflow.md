# Humanization Workflow

Humanization is not synonym swapping. The goal is to make prose more author-specific, grounded, and fit for its genre while preserving meaning.

## Inputs

Required inputs are the source text and target use, such as article, email, report, documentation, social post, application material, or academic prose.

Soft inputs improve quality but should not block progress: author samples, disliked examples, brand voice, reader profile, source material, citations, length target, and words or phrases to avoid.

For high-stakes contexts, preserve required disclosures, citations, institutional rules, and legal or academic constraints.

## Style And Preference Cards

When samples exist, infer a short style card:

```text
Sentence rhythm: short, long, mixed, clipped, flowing
Register: casual, technical, academic, literary, executive, conversational
Stance: neutral, skeptical, warm, opinionated, restrained
Structure: direct thesis, narrative lead, question-first, evidence-first
Transitions: explicit connectors, quiet jumps, section headers, no signposting
Punctuation: plain, parenthetical, semicolon-heavy, dash-heavy, sparse
Texture: examples, numbers, anecdotes, quotes, sensory detail, source notes
Avoid: phrases, formats, endings, claims, or tones the author would not use
```

Also infer a preference card when there are multiple samples or explicit preferences:

```text
Likes: direct thesis, concrete examples, mild skepticism
Dislikes: generic openings, balanced-for-no-reason structure, inflated claims
Decision rules: lead with conclusion, qualify only when evidence is incomplete, end on consequence rather than summary
```

Use disliked examples as negative references when available. They are often more useful than positive examples for avoiding generic tone.

Do not imitate private quirks blindly. Use the cards to guide rhythm and choices, not to create caricature.

Few examples help most in structured genres such as email, reports, and documentation. For informal, personal, or highly idiosyncratic writing, expect samples to be incomplete and rely more on preference rules plus human review.

## Rewrite Process

First pass: map the draft.

Identify the core claim, required facts, weak claims, repeated transitions, generic framing, and paragraph-level purpose.

Classify problems across four layers:

- Surface: repeated words, uniform sentence length, filler, punctuation habits, and formatting artifacts.
- Discourse: template introductions, mechanical transitions, over-neat sectioning, and generic conclusions.
- Content: missing evidence, vague authority, weak grounding, and claims without mechanism or consequence.
- Author fit: tone that reverts to an average voice instead of the target writer or genre.

Second pass: rebuild structure.

Prefer an outline that assigns each paragraph a job. Each paragraph should add a new point, example, qualification, or consequence.

Third pass: rewrite.

Use the author's style card if present. Otherwise choose the most natural register for the genre. Keep technical, legal, academic, and reference writing plain when neutrality is the right human voice.

Fourth pass: audit.

Read the rewrite as an editor. Remove padding, verify claims, vary cadence, and replace generic summaries with specific consequences or a clean stop.

Do not use randomness as a substitute for judgment. More variation can reduce mechanical rhythm, but random wording, excessive temperature, or decorative mess can damage clarity, facts, and voice.

## Language Rule References

After the general audit, load the language-specific rule file that matches the text:

- English or mostly English prose: `references/english.md`.
- Simplified Chinese prose: `references/simplified-chinese.md`.
- Mixed-language prose: apply the dominant language first, then preserve proper nouns, code, quotes, and field-specific terms.

If the text uses Traditional Chinese or another language without a dedicated rule file, apply only the general workflow and avoid importing English- or Simplified-Chinese-specific punctuation, syntax, or idiom rules.

## Evidence And Grounding

Prefer facts, names, numbers, examples, source notes, quotes, scenes, constraints, and tradeoffs over broad claims.

If a fact is missing, mark it as needing verification or cut the claim. Do not invent citations, quotations, dates, personal history, credentials, or source-backed details.

Grounding should match the genre. A memoir can use a sensory detail; a technical note may need a file path, benchmark, failure mode, or exact behavior; an academic paragraph may need a citation and careful scope.

Use evidence slots before drafting when the text needs factual support:

```text
Paragraph goal: <what this paragraph must do>
Needed evidence: <fact, quote, example, citation, number, or source note>
Status: verified | provided | missing | needs human check
```

## Genre Rules

Essays and posts can use stance, selective emphasis, concrete scenes, unresolved tension, and sharper endings.

Reports should keep structure clear, but replace generic executive-summary filler with decisions, evidence, uncertainty, and implications.

Technical documentation should be direct, current-state oriented, and specific about behavior. Avoid writing as if narrating a diff unless the document is a changelog or migration guide.

Academic writing should preserve citations, scope, definitions, and uncertainty. Improve clarity and specificity without adding unsupported claims.

Emails should sound like a person with a purpose. Cut pleasantries that do not match the relationship, but keep courtesy where it matters.

Marketing copy should avoid generic hype. Use concrete benefits, constraints, proof, and reader-relevant outcomes.

## Human Review Rubric

Use this rubric for substantial rewrites:

- Meaning fidelity: the rewrite preserves the source's intended claims and constraints.
- Author fit: rhythm, stance, and word choice match the sample or requested voice.
- Genre fit: the text sounds natural for its actual use, not generically conversational.
- Grounding: important claims have evidence, examples, or clear uncertainty.
- Information density: each paragraph earns its place.
- Cadence: sentence and paragraph rhythm varies where the genre allows it.
- Edit cost: a human editor would make fewer changes after this pass.

Do not use a detector score as a quality measure. If detection tools are involved in a separate evaluation context, treat them as one weak signal alongside meaning fidelity, evidence, author fit, and human editing cost.

## Style Data Guidance

If the user wants a reusable style system rather than one rewrite, prefer a small, high-quality, representative sample set over many weak examples.

Good style data includes final edited prose, source material when available, explicit preferences, negative examples, and notes explaining why edits were accepted or rejected.

Avoid training or prompting from repetitive samples. Repetition teaches template behavior and can make later prose less human, not more.

## Output Formats

Default output:

```text
Revised text:
<rewrite>

Changes made:
- <1-3 short notes about structure, voice, evidence, or cuts>
```

For larger edits, include a brief audit before the rewrite:

```text
Audit:
- <main issue>
- <main issue>

Revised text:
<rewrite>

Notes:
- <verification needs or preserved constraints>
```

For style calibration, include the style card only when it helps the user review the rewrite.

For high-stakes writing, include verification notes for claims that need human checking.

## Quality Bar

The final text should keep the same intended meaning, sound appropriate for its genre, contain fewer empty abstractions, use more specific evidence where available, and read as if an editor made deliberate choices.

Do not flatten strong human writing just because it is polished. Preserve unusual details, defensible opinions, mixed feelings, local phrasing, and purposeful rhythm.
