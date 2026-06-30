"""Contracts for the owner's investing-principles house standard."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HOUSE_STANDARD_SKILLS = [
    "idea-generation",
    "company-tearsheet",
    "initiating-coverage",
    "memo-builder",
    "long-short-pitch",
    "thesis-tracker",
    "portfolio-risk-management",
    "dcf-model-builder",
    "three-statement-model-builder",
    "equity-model-update",
    "model-audit-tieout",
    "comps-valuation",
    "scenario-sensitivity-generator",
]


class FcamisaInvestingPrinciplesContractTests(unittest.TestCase):
    def test_house_standard_contains_required_investing_hooks(self) -> None:
        text = (ROOT / "shared" / "fcamisa-investing-principles.md").read_text(
            encoding="utf-8"
        )
        lower = text.lower()
        for phrase in [
            "normalized earnings power",
            "owner earnings",
            "15%+ expected annualized",
            "10% to 12%+",
            "20%+",
            "no leverage",
            "balance sheet resilience",
            "hold cash / no action",
            "do not average down when thesis is broken",
            "fmp ratios are diagnostic",
        ]:
            self.assertIn(phrase, lower)

    def test_core_workflows_load_house_standard(self) -> None:
        for skill in HOUSE_STANDARD_SKILLS:
            text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            lower = text.lower()
            self.assertIn("shared/fcamisa-investing-principles.md", text, skill)
            self.assertIn("House Investing Standard", text, skill)
            for phrase in [
                "owner earnings",
                "normalized earnings power",
                "balance sheet resilience",
                "return-hurdle",
                "hold cash / no action",
                "FMP ratios are diagnostic",
            ]:
                self.assertIn(phrase.lower(), lower, skill)

    def test_valuation_standard_loads_house_standard(self) -> None:
        text = (ROOT / "shared" / "equity-valuation-pm-standard.md").read_text(
            encoding="utf-8"
        )
        for phrase in [
            "shared/fcamisa-investing-principles.md",
            "15%+ expected annualized",
            "10% to 12%+",
            "20%+",
            "hold cash / no action",
            "FMP ratios are diagnostic",
        ]:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
