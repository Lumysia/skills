# Browser Translation Workflow

Use this workflow when `/browser` asks to translate, summarize in another language, or read a page bilingually.

## Rules

- Translate in-place like immersive translation: keep source text visible and insert the target language immediately after each source segment.
- Translate only already-loaded in-scope DOM content. Do not scroll, paginate, open links, or fetch more text solely to translate unloaded content unless the user asks.
- Work in small batches: one card, one list item, or one to two short paragraphs, with no more than 10 source-text translations per batch. Count the translated source text entries, not DOM insertions or replacements. Insert and verify each batch before continuing.
- Continue automatically through the loaded target boundary without asking whether to continue. Ask only before leaving the boundary, changing page state, or entering login/paywall/sensitive content.
- Add one reusable page-local CSS class for translation blocks before the first insertion. Keep styling light: secondary color, readable line height, modest spacing, and optional subtle border or tinted background.
- Preserve links, names, dates, numbers, source labels, and quotes. For lists or cards, translate only visible text; do not invent hidden details or destination content.
- End when all already-loaded in-scope text is translated or a safety boundary blocks progress. Report the completed boundary and any unloaded content left untouched.
