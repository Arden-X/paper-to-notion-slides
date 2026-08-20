# Paper deck layout contract

## Figure crop gate

Record every source figure used in the deck. The manifest may be either a JSON array or an object with a `figures` array:

```json
{
  "figures": [
    {
      "name": "fig4_workflow",
      "source_page": 6,
      "caption": "Figure 4: Workflow of inference instances.",
      "figure_complete": true,
      "caption_included": true,
      "margin_px": 12
    }
  ]
}
```

Set `figure_complete` to true only after comparing the crop with the source page. Retain every diagram edge, axis, legend, subplot label, and the complete caption. Set `caption_included` to true for every paper figure screenshot used as evidence. Keep at least 8 px of white margin around the crop.

## Background module gate

Name background rectangles with the suffix `-surface`. Name their text children with the same prefix, for example:

- `result-surface`
- `result-title`
- `result-body`

Derive children from the surface bounds. Use 16–20 px left and right padding, at least 12 px bottom clearance, and 12–15 px top padding. Decorative bars may touch the edge and should use the suffix `-bar`.

For a module at `(x, y, w, h)`, every text child `(tx, ty, tw, th)` must satisfy:

```text
tx >= x
ty >= y
tx + tw <= x + w
ty + th <= y + h - 12
```

The validator checks geometric containment and bottom clearance from layout JSON. It cannot guarantee identical wrapping across PowerPoint, LibreOffice, and the authoring renderer, so rendered inspection remains mandatory.

## Layout JSON shape

Create one `*.layout.json` file per slide:

```json
{
  "elements": [
    {"name": "result-surface", "bbox": [100, 80, 420, 210]},
    {"name": "result-title", "bbox": [118, 95, 384, 32], "text": "实验结果"},
    {"name": "result-body", "bbox": [118, 137, 384, 125], "text": "..."}
  ]
}
```

Coordinates may use pixels, points, or another consistent unit. If using PowerPoint inches, convert the 12 px bottom-clearance rule to the same coordinate system before exporting.

## Overflow repair order

1. Shorten the copy while preserving the claim.
2. Increase the module height or width.
3. Move neighboring content or split the slide.
4. Reduce body size only if it remains above the presentation minimum.

Never cover overflowing text with another shape, accept clipped copy, or omit a figure caption to gain space.
