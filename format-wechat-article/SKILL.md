---
name: format-wechat-article
description: Turn Chinese long-form articles, Markdown, plain text, and supplied illustrations into polished WeChat Official Account layouts. Use when Codex needs to analyze article structure, recommend multiple visual styles, create style previews, apply a selected style, or deliver copy-ready WeChat-compatible inline-styled HTML while preserving the author's content.
---

# Format WeChat Article

Create mobile-first公众号排版 from source text and supplied images. Preserve meaning and wording unless the user explicitly requests editing.

## Workflow

1. Inspect the complete source and all supplied images. Identify title, standfirst, sections, lists, quotations, examples, warnings, conclusion, and likely image placements.
2. Read [references/content-structure.md](references/content-structure.md) before restructuring the article.
3. If the user has not selected a style, read [references/style-selection.md](references/style-selection.md), rank three of the five bundled themes, and explain each in one sentence. Always provide a lightweight comparison using the same representative excerpt: generate a side-by-side HTML or image preview when visual tools are available, otherwise show three concise styled specifications. Do not lay out the full article three times.
4. Pause for a style choice when the user asked to choose. If the user says to decide autonomously, use the top-ranked style. If a style is already selected, skip directly to rendering.
5. Load only the selected JSON file from `assets/themes/`. Treat its values as defaults; adjust restrainedly for article length, image colors, or explicit brand requirements.
6. Build a complete mobile preview and a clean article fragment:
   - `preview.html`: standalone browser preview, 375 px reading column, optional copy control outside the article.
   - `article.html`: only the pasteable article body, with inline styles and no scripts.
   - `validation.json`: validator output.
7. Read [references/wechat-compatibility.md](references/wechat-compatibility.md), then run:

```bash
python3 scripts/validate_wechat_html.py article.html --json validation.json
python3 scripts/wrap_preview.py article.html preview.html --title "文章预览"
```

8. Open or screenshot `preview.html` when browser tooling is available. Check at approximately 375 px and one narrower Android viewport. Correct overflow, weak contrast, crowded headings, orphaned captions, and awkward image crops.
9. Deliver the selected style name, the two HTML files, validation status, and any image-upload caveat. Do not claim that local image paths are publish-ready.

## Content Rules

- Keep every factual claim, qualification, heading, list item, quotation, and conclusion unless editing was requested.
- Improve visual hierarchy by wrapping and styling; do not silently summarize or invent content.
- Use one H1-equivalent title and preserve the source section order.
- Break dense paragraphs only at semantic boundaries. Use emphasis sparingly.
- Place supplied images beside the section they explain; add concise captions only when useful.
- Prefer text over decorative cards for long reading. Reserve cards for definitions, key takeaways, processes, comparisons, examples, and warnings.
- Avoid emoji as structural icons unless the chosen theme explicitly calls for them.

## Theme Catalog

- `minimal.json`: 简约留白 — calm editorial reading for essays and commentary.
- `professional.json`: 专业报告 — restrained, credible structure for research and business topics.
- `card.json`: 知识卡片 — modular explanations, tutorials, and highly scannable knowledge posts.
- `clear-tech.json`: 清透科技杂志 — blue-violet technology editorial; the validated default for AI and digital topics.
- `warm-life.json`: 温暖生活 — approachable beige and coral for personal growth and lifestyle topics.

## Output Quality Bar

- Body text must remain comfortable at phone width; default to 16–17 px and line-height 1.75–1.9.
- Maintain strong title/body contrast and at least 24 px visual separation between major sections.
- Keep images responsive with explicit `width:100%; height:auto; display:block`.
- Use inline CSS in `article.html`; do not depend on classes, JavaScript, external stylesheets, external fonts, hover states, or viewport units.
- Keep decorative complexity subordinate to reading. A good layout still works when accent backgrounds are removed.
- Treat validator warnings as review items; resolve errors before delivery.

## Resources

- Read [references/style-selection.md](references/style-selection.md) only when choosing or comparing styles.
- Read [references/content-structure.md](references/content-structure.md) whenever transforming source content into layout nodes.
- Read [references/wechat-compatibility.md](references/wechat-compatibility.md) before final output or API preparation.
- Use `scripts/validate_wechat_html.py` to detect incompatible or fragile HTML.
- Use `scripts/wrap_preview.py` to create a safe local preview without contaminating the article fragment.
