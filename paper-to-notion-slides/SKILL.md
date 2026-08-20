---
name: paper-to-notion-slides
description: Analyze an academic paper PDF or official online preprint and produce a source-grounded five-section Notion reading note or Markdown fallback plus an editable PowerPoint poster or multi-slide presentation. Use for paper reading, innovation extraction, formula derivation, experiment synthesis, original-paper figure cropping, Notion capture under 论文阅读, Markdown notes, and editable PPT/PPTX delivery.
---

# Paper to Notion & Slides

Turn one paper into two coordinated artifacts: a detailed reading note and a concise visual deck. Treat the original paper as the factual source and preserve traceability to its pages, equations, tables, and figures.

## Resolve and analyze the source

1. Use the user-provided PDF when available. Otherwise retrieve the exact official preprint or publisher version the user requested and retain the PDF used for analysis.
2. Extract title, authors, venue or preprint status, research problem, assumptions, method, formulas, innovations, experiments, limitations, and implications from that PDF.
3. Keep numerical and methodological claims traceable to a page, equation, table, or figure. Do not silently combine evidence from different paper versions or the user's prior notes.
4. Stay within paper analysis and artifact production. Do not add unsolicited submission, reviewer-response, rewriting, or research-direction advice.

## Create the Notion reading note

Treat Notion as an optional integration. When a connected Notion MCP/app is available, search for `论文阅读`, fetch the exact parent page or database and its schema, read the connected Notion enhanced-Markdown specification, create the page with an explicit parent, and fetch the result once to verify it. If more than one destination matches, ask the user which one to use.

When Notion tools are unavailable, save a UTF-8 `.md` file with the paper title and the same five-section content as a final deliverable. Do not claim that a Notion page was created. Mention only that the Markdown can be imported later.

Use exactly these five top-level sections unless the user overrides them:

1. 论文信息
2. 问题背景与难点
3. 核心思路与创新点
4. 实验数据与结果分析
5. 对该领域的启示

Keep the note detailed but cohesive. Explain formulas and derivations inside `核心思路与创新点` with defined symbols, intermediate reasoning, assumptions, and an interpretation of what the equation accomplishes. Prefer connected prose and a few purposeful lists over excessive subheadings or fragmented bullets. In `实验数据与结果分析`, distinguish reported measurements from interpretation and cite the relevant table or figure.

## Build the editable presentation

Scale the slide count with paper length and information density: use a single poster or a small number of slides for short papers, and a multi-slide deck for long papers. Never force a long paper into one dense poster. Preserve the established visual system unless the user supplies another template:

- Use a pale green background with dark, high-contrast text. Avoid light gray body copy.
- Use `SimHei` for Chinese text and `Times New Roman` for non-Chinese text. Split mixed-language runs when needed so each script uses the correct font.
- Keep titles, body copy, shapes, tables, and charts editable. Original paper figure crops may be raster images.
- Use original paper figures rather than redrawing them unless the user explicitly asks for a redraw.
- A valid crop includes the complete figure body, axes, legends, panel labels, full `Figure N:` caption, and a small white margin on every edge.
- When the crop already includes its figure number and caption, do not add an external `Fig. N` label. Add only a short interpretation outside the image when useful.

Treat every background panel and its text as one bounded module. Define the panel first, derive all child text boxes from its inner rectangle, keep at least 12 px bottom clearance and 16–20 px horizontal padding, and never allow text bounds to extend outside the panel. Do not rely on authoring-time autofit alone. Render with the final fonts, inspect actual line wrapping, then shorten copy, enlarge the module, move neighboring content, or split the slide. Keep one-line banners and titles on one line.

Read [references/layout-contract.md](references/layout-contract.md) before building or revising a deck.

## Required QA and delivery

1. Render the final PPTX using the intended fonts.
2. Run the presentation overflow test, such as `slides_test.py`, when available in the presentation toolchain.
3. Inspect every slide at full size, not only a montage.
4. Compare every paper figure crop against its source PDF page.
5. Export layout JSON for the deck, create the figure manifest described in the layout contract, and run:

```bash
python3 scripts/validate_paper_deck_layout.py \
  --layout-dir <artifact-layout-json-directory> \
  --figure-manifest <figure-manifest.json>
```

Do not deliver until the automated checks and visual inspection pass. Return the Notion page link or Markdown artifact and the editable `.pptx`; identify the PDF version used when it was retrieved online.
