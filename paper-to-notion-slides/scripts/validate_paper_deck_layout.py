#!/usr/bin/env python3
"""Validate source-figure metadata and text/background containment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


def inside(child: list[Any], parent: list[Any], bottom_clearance: float = 12.0, tolerance: float = 0.5) -> bool:
    cx, cy, cw, ch = map(float, child)
    px, py, pw, ph = map(float, parent)
    return (
        cx >= px - tolerance
        and cy >= py - tolerance
        and cx + cw <= px + pw + tolerance
        and cy + ch <= py + ph - bottom_clearance + tolerance
    )


def load_figures(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        figures = data
    elif isinstance(data, dict):
        figures = data.get("figures", [])
    else:
        raise ValueError("figure manifest must be a JSON array or object")
    if not isinstance(figures, list):
        raise ValueError("'figures' must be a JSON array")
    return figures


def validate_figures(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        figures = load_figures(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"invalid figure manifest {path}: {exc}"]
    if not figures:
        return [f"no figures found in {path}"]
    for item in figures:
        if not isinstance(item, dict):
            errors.append("figure manifest entries must be objects")
            continue
        name = item.get("name", "<unnamed>")
        if not item.get("figure_complete"):
            errors.append(f"{name}: figure_complete is not true")
        if not item.get("caption_included"):
            errors.append(f"{name}: caption_included is not true")
        caption = str(item.get("caption", ""))
        if not re.match(r"^Figure\s+\d+\s*:", caption, flags=re.IGNORECASE):
            errors.append(f"{name}: caption must start with 'Figure N:'")
        try:
            margin = float(item.get("margin_px", 0))
        except (TypeError, ValueError):
            margin = 0
        if margin < 8:
            errors.append(f"{name}: margin_px must be at least 8")
        if not item.get("source_page"):
            errors.append(f"{name}: source_page is required")
    return errors


def validate_layouts(layout_dir: Path) -> list[str]:
    errors: list[str] = []
    files = sorted(layout_dir.glob("*.layout.json"))
    if not files:
        return [f"no *.layout.json files found in {layout_dir}"]
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid layout file {path}: {exc}")
            continue
        elements = [
            e for e in data.get("elements", [])
            if isinstance(e, dict) and e.get("name") and e.get("bbox")
        ]
        by_name = {e["name"]: e for e in elements}
        for surface in (e for e in elements if e["name"].endswith("-surface")):
            prefix = surface["name"][:-8]
            children = [
                e for name, e in by_name.items()
                if name.startswith(prefix + "-")
                and name != surface["name"]
                and not name.endswith("-bar")
                and e.get("text") is not None
            ]
            if not children:
                errors.append(f"{path.name}:{surface['name']}: no text children found")
                continue
            for child in children:
                try:
                    contained = inside(child["bbox"], surface["bbox"])
                except (TypeError, ValueError):
                    contained = False
                if not contained:
                    errors.append(
                        f"{path.name}:{child['name']}: bbox {child['bbox']} exceeds "
                        f"module {surface['name']} {surface['bbox']} or its 12 px bottom clearance"
                    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layout-dir", required=True, type=Path)
    parser.add_argument("--figure-manifest", required=True, type=Path)
    args = parser.parse_args()
    errors = validate_layouts(args.layout_dir) + validate_figures(args.figure_manifest)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed: complete figure captions and contained background modules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
