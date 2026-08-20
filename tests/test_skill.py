from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "paper-to-notion-slides"
VALIDATOR_PATH = SKILL / "scripts" / "validate_paper_deck_layout.py"

spec = importlib.util.spec_from_file_location("paper_deck_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class SkillContractTests(unittest.TestCase):
    def test_required_contract_language(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for heading in (
            "论文信息",
            "问题背景与难点",
            "核心思路与创新点",
            "实验数据与结果分析",
            "对该领域的启示",
        ):
            self.assertIn(heading, text)
        for requirement in ("SimHei", "Times New Roman", "Figure N:", "12 px", "Notion MCP", "`.md`"):
            self.assertIn(requirement, text)
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertNotIn("dependencies:", metadata)

    def test_good_array_manifest_and_contained_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest = root / "figures.json"
            manifest.write_text(json.dumps([{
                "name": "fig2",
                "source_page": 3,
                "caption": "Figure 2: Complete figure.",
                "figure_complete": True,
                "caption_included": True,
                "margin_px": 12,
            }]), encoding="utf-8")
            layout = root / "slide-01.layout.json"
            layout.write_text(json.dumps({"elements": [
                {"name": "result-surface", "bbox": [0, 0, 120, 120]},
                {"name": "result-body", "bbox": [16, 20, 88, 70], "text": "Contained"},
            ]}), encoding="utf-8")
            self.assertEqual([], validator.validate_figures(manifest))
            self.assertEqual([], validator.validate_layouts(root))

    def test_incomplete_crop_and_overflow_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest = root / "figures.json"
            manifest.write_text(json.dumps({"figures": [{
                "name": "broken",
                "source_page": 0,
                "caption": "Fig. 2 cropped",
                "figure_complete": False,
                "caption_included": False,
                "margin_px": 2,
            }]}), encoding="utf-8")
            layout = root / "slide-01.layout.json"
            layout.write_text(json.dumps({"elements": [
                {"name": "result-surface", "bbox": [0, 0, 100, 100]},
                {"name": "result-body", "bbox": [10, 20, 90, 80], "text": "Overflow"},
            ]}), encoding="utf-8")
            self.assertTrue(validator.validate_figures(manifest))
            self.assertTrue(validator.validate_layouts(root))


if __name__ == "__main__":
    unittest.main()
