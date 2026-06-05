# Simplified Chinese Humanization Rules

These rules cover Simplified Chinese prose.

Use these rules only for Simplified Chinese. Do not apply them to Traditional Chinese, Japanese kanji, or regional Chinese usage; those need separate norms.

## Priority Rules

Do not invent facts. Every number, name, quote, event, product name, date, place, and source-backed detail in the rewrite must trace to the source text or provided material.

Do not over-clean strong human writing. If the input has clear human voice, specific memory, dialect, self-correction, interview rhythm, or authorial quirks, preserve them and avoid rewriting language just to make it smoother.

Protect register. Do not push academic, legal, public-sector, exam, or technical prose into casual speech. A rewrite may move at most one register level unless the user explicitly requests a tone change.

Judge density, not isolated appearance. Chinese writers legitimately use parallelism, idioms, four-character phrases, particles, and formal connectors. Treat them as problems only when they pile up mechanically, do not carry content, or mismatch the genre.

## Register Detection

Identify the register before applying pattern rules:

- Social or conversational: chat, moments, short posts, comments.
- Content or self-media: WeChat public posts, Xiaohongshu, short-video scripts, Bilibili scripts.
- Business or workplace: email, PRD, reports, internal memos, product copy.
- General written prose: blogs, essays, commentary, popular science.
- Narrative nonfiction or feature writing: profiles, interviews, longform reportage.
- Brand advertising: slogans, hero copy, campaigns, launch copy.
- Academic or technical: papers, white papers, technical reports, literature reviews.
- Public-sector or legal: regulations, contracts, judgments, official notices.
- Exam writing: Chinese exam essays or other scoring-rubric prose.

Default to general written prose when unclear. Ask only when the register materially changes the rewrite.

## Simplified-Chinese Pattern Clusters

Fix content inflation:

- `具有重要意义`、`发挥重要作用`、`标志着新阶段`、`谱写新篇章`、`注入新的活力`.
- `值得一提的是`、`不容忽视`、`毋庸置疑` when they introduce ordinary claims.
- `随着...的不断发展`、`在新时代背景下`、`在...浪潮中` as generic openings.
- `体现了...深刻内涵`、`彰显了...时代价值`、`蕴含着...重要启示` as empty tails.
- Vague authorities: `专家表示`、`业内人士认为`、`相关报告指出` without a concrete source.
- Formulaic `挑战与展望` endings that provide no concrete obstacle, decision, or consequence.

Fix Chinese AI vocabulary and filler:

- Dense business words: `赋能`、`助力`、`打造`、`护航`、`抓手`、`闭环`、`生态`、`底层逻辑`、`高质量发展`、`全方位`、`多维度`.
- Decorative propaganda words: `璀璨`、`华章`、`画卷`、`扬帆起航`、`砥砺奋进`、`蓬勃发展`.
- Redundant phrases: `通过...的方式`、`在...的情况下`、`由于...的原因`、`为了...的目的`、`具有...的能力`.
- Weak verb shells: `进行讨论`、`开展工作`、`实施部署`、`发挥作用` when the register does not require them.
- Excessive hedging: `在一定程度上`、`某种意义上`、`或许可能`、`一些相关`.

Fix mechanical structure:

- `不仅...更是...` used repeatedly without a real contrast.
- `从 X 到 Y` where X and Y are not on a meaningful scale.
- `首先/其次/最后` or `一方面/另一方面` imposed on material that does not need numbered logic.
- Stiff `总-分-总` skeleton with exactly three points and a summary that adds no information.
- Over-structured lists, tables, headings, or Markdown where paragraphs would be clearer.

Fix Chinese translationese:

- Overlong prepositional openings or `与...相关的...` structures that bury the subject.
- `作为一个 X` in casual or workplace contexts where direct first-person wording is more natural.
- Long stacks of `的`, direct English relative-clause structures, or heavy passive `被/由/受到` chains.
- English-style word order: time, place, or manner adverbials placed after the verb when Chinese would put them before it.
- `令人/让人 + 形容词` where a simpler Chinese predicate works.
- `逻辑很清晰：`、`结论很明确：`、`事实很清楚：` as evaluation before content.
- Abstract nouns as subjects followed by broad adjectives: `工程上的现实比这些数字难看` can often become a concrete action or scene.

Fix Chinese formatting and punctuation:

- Use full-width Chinese punctuation in Chinese prose: `，`、`。`、`：`、`；`、`？`、`！`、`（）`.
- Keep half-width punctuation in code, URLs, file paths, versions, commands, and English phrases.
- Use `、` for parallel nouns or phrases; do not use English commas for Chinese lists.
- Treat semicolons as register-sensitive. They are rare in daily, self-media, business, and email prose, but valid in editorials, long arguments, and academic writing.
- Use `《》` for books, publications, films, policy documents, columns, and named works where Chinese convention expects it.
- Use `……` only when the genre supports ellipsis; avoid `...` in Chinese prose.
- Use `——` sparingly and only when it carries emphasis, transition, or important apposition. Replace mechanical dash inserts with commas, colons, parentheses, or sentence breaks.

Fix hard AI artifacts:

- Chatbot politeness left in content: `希望对您有帮助`、`如有疑问请随时告诉我`、`当然可以`、`您问得非常好`.
- Knowledge disclaimers: `作为一个 AI 语言模型`、`截至我的知识更新日期`、`基于现有资料`.
- Template placeholders: `XX 路`、`X 号线 X 口`、`[产品名]`、`<书名>`、`{{变量}}`、`TODO` when the surrounding text claims specificity.
- Fake or unchecked citations, DOI, ISBN, URLs, or AI-source tracking parameters.

## Platform And Register Notes

For Xiaohongshu, WeChat, short video, and Bilibili, watch for platform templates: dense emoji labels, `家人们谁懂啊`、`姐妹们快冲`、`闭眼入`、`一键三连`、mechanical CTA, pseudo-healing arcs, pseudo-consulting jargon, and fake timecodes.

For workplace and business prose, keep useful structure but remove hollow terms. `底层逻辑` or `颗粒度` can be real workplace language; treat them as problems only when the paragraph loses no information after removing them.

For academic, public-sector, legal, and exam prose, be conservative. Preserve necessary connectors, nominalizations, `进行 + V`, formal parallelism, and required formulaic register unless the expression is empty or factually unsupported.

For brand advertising, do not apply self-media rules blindly. Short lines, rhythm, English product names, imperatives, and deliberate white space can be the house style.

For narrative nonfiction and interviews, protect pauses, self-corrections, dialect, atmosphere, and slow setup. These are often the human signal.

## Chinese Mixed-Language Rules

Preserve proper nouns, product names, company names, model names, code terms, commands, and widely used technical abbreviations: `API`、`SDK`、`CLI`、`MCP`、`LLM`、`RAG`、`JSON`、`YAML`、`PR`、`CI/CD`.

Preserve community-standard names and nicknames when the register supports them, such as sports names, entertainment nicknames, and field-specific beauty or skincare ingredients.

Do not force Chinese-English spacing. Keep the source spacing convention unless the user asks for typography cleanup.

Translate ordinary English words when stable Chinese equivalents are expected in the target register: `argument` → `论证`, `logic` → `逻辑`, `workflow` → `流程`, unless the English form is the community norm.

## Chinese Self-Check

Before finalizing, ask:

- Did I preserve every concrete fact from the source?
- Did I add any new person, number, place, quote, date, or source-backed detail?
- Did I keep the target register instead of pushing everything into casual speech?
- Did I remove real human roughness that should have stayed?
- Did I fix density and function problems rather than isolated normal Chinese expressions?
- Would this sentence sound natural if read aloud by the target writer in the target setting?

If the rewrite needs more human detail than the source provides, ask the user for real observations instead of inventing them.
