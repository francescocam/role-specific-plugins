"""Connector/provider honesty regressions for Public Equity support skills."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class UnsupportedConnectorPromisesTests(unittest.TestCase):
    def test_shared_standard_forbids_implied_vendor_access(self) -> None:
        text = read("shared/equity-research-support-standard.md")
        for phrase in [
            "Never imply live Bloomberg",
            "unless that connector/app/tool is actually callable",
            "use user-provided exports",
            "request the export",
            "missing_required_source",
        ]:
            self.assertIn(phrase, text)

    def test_source_protocol_requires_callable_or_exported_provider_data(self) -> None:
        text = read("skills/financials-normalizer/references/source-protocol.md")
        self.assertIn("Callable connected internal system", text)
        self.assertIn("Trusted financial data provider export or callable provider connector", text)
        self.assertIn("Do not imply live access", text)

    def test_fmp_provider_contract_preserves_evidence_and_hazards(self) -> None:
        text = "\n".join(
            [
                read("skills/public-equity-investing/internal-support/fmp-provider-guide/INTERNAL.md"),
                read(
                    "skills/public-equity-investing/internal-support/fmp-provider-guide/references/connector-playbook.md"
                ),
                read("skills/financials-normalizer/references/source-protocol.md"),
            ]
        )
        for phrase in [
            "stable FMP tool or endpoint name",
            "exact request parameters",
            "symbol plus exchange",
            "CIK, ISIN, CUSIP",
            "retrieval timestamp",
            "provider as-of date",
            "fiscal year",
            "FX rate",
            "listing-level versus operating-company-level",
            "fact_provider_standardized",
            "estimate_consensus",
            "`fact_source_reported` only after checking",
            "Do not promote FMP ratios",
            "Secondary listings",
            "Country or domicile",
            "Pence/pounds",
            "plan-dependent",
            "U.S. SEC coverage is not equivalent to complete global filing",
        ]:
            self.assertIn(phrase, text)

    def test_fmp_source_categories_do_not_expand_to_internal_research(self) -> None:
        config = json.loads(
            read("skills/user-context/plugin-author-config/source-category-config.json")
        )
        categories = config["categories"]
        intended_fmp_categories = {
            "company_filings_ir",
            "earnings_transcripts_presentations",
            "portfolio_models_trackers",
            "market_data_estimates",
        }

        for category_id in intended_fmp_categories:
            self.assertIn(
                "financial_modeling_prep",
                categories[category_id]["preferred_mcp_servers"],
            )
        self.assertNotIn(
            "preferred_mcp_servers",
            categories["internal_research"],
        )

    def test_source_category_hints_do_not_default_to_legacy_paid_providers(self) -> None:
        config = json.loads(
            read("skills/user-context/plugin-author-config/source-category-config.json")
        )
        serialized = json.dumps(config)

        for removed_default in [
            "Alpaca",
            "Daloopa",
            "FactSet",
            "LSEG",
            "Morningstar",
            "Quartr",
            "S&P",
            "Third Bridge",
        ]:
            self.assertNotIn(removed_default, serialized)

        self.assertIn("financial_modeling_prep", serialized)
        self.assertIn("Google Drive", serialized)
        self.assertIn("Microsoft SharePoint", serialized)

    def test_style_sources_do_not_promise_connected_apps(self) -> None:
        text = (
            read("skills/public-equity-investing/internal-support/style-guide-adapter/INTERNAL.md")
            + "\n"
            + read(
                "skills/public-equity-investing/internal-support/style-guide-adapter/references/source-and-safety.md"
            )
        )
        self.assertNotIn("available in connected apps", text)
        self.assertIn("callable runtime apps/connectors", text)
        self.assertIn("Do not imply live access", text)

    def test_app_manifest_has_no_paid_provider_placeholders(self) -> None:
        manifest = json.loads(read(".app.json"))
        apps = manifest["apps"]
        for removed_default in [
            "alpaca",
            "daloopa",
            "factset",
            "lseg",
            "morningstar",
            "pitchbook",
            "quartr",
            "s-p",
            "slack",
            "third-bridge",
        ]:
            self.assertNotIn(removed_default, apps)

        for name, config in apps.items():
            self.assertNotIn("REPLACE_WITH", config["id"], name)
            self.assertTrue(config.get("optional"), name)

    def test_readme_places_fmp_first_without_overclaiming_specialist_coverage(self) -> None:
        text = read("README.md")
        self.assertIn(
            "| Structured public-market data | Financial Modeling Prep through the configured `financial_modeling_prep` MCP server |",
            text,
        )
        self.assertIn("| Optional private-market research |", text)
        self.assertIn("| Optional expert research |", text)
        self.assertIn("| Optional brokerage context |", text)
        self.assertIn("| Optional internal collaboration |", text)
        self.assertIn(
            "FMP is the default structured public-market route",
            text,
        )
        self.assertIn(
            "does not replace private-company datasets, expert networks, brokerage/account systems, or internal document and collaboration repositories",
            text,
        )
        self.assertNotIn(
            "| Market and company data | FactSet, LSEG, S&P, Moody's, Morningstar, Daloopa, Quartr |",
            text,
        )

    def test_fmp_workflow_endpoint_map_covers_required_routes_and_controls(self) -> None:
        text = read(
            "skills/public-equity-investing/internal-support/fmp-provider-guide/references/connector-playbook.md"
        )
        self.assertIn("## Workflow Endpoint Map", text)
        for heading in [
            "Workflow need",
            "FMP route family",
            "Minimum identifiers",
            "Freshness expectation",
            "Pagination / bounds",
            "Empty-result behavior and fallback",
        ]:
            self.assertIn(heading, text)

        for workflow_need in [
            "Current price and market cap",
            "Price and volume history",
            "Company identity and listing metadata",
            "Reported statements",
            "Enterprise value inputs",
            "Consensus and expectation bar",
            "Earnings dates and surprises",
            "Transcripts",
            "SEC filings",
            "Revenue segments",
            "Institutional ownership",
            "Insider activity",
            "ETF/index exposure",
            "Corporate actions",
            "Macro context",
            "News and issuer releases",
        ]:
            self.assertIn(workflow_need, text)

        for route_family in [
            "`quote`",
            "`chart`",
            "`company`",
            "`directory`",
            "`search`",
            "`statements`",
            "`analyst`",
            "`calendar`",
            "`earningsTranscript`",
            "`secFilings`",
            "`form13F`",
            "`insiderTrades`",
            "`etfAndMutualFunds`",
            "`indexes`",
            "`economics`",
            "`news`",
        ]:
            self.assertIn(route_family, text)

        for guardrail in [
            "The live MCP schema remains authoritative",
            "date bounds",
            "page",
            "limit",
            "fallback",
            "missing_required_source",
            "plan-limited",
            "linked SEC/issuer filing",
            "official index data",
        ]:
            self.assertIn(guardrail, text)

    def test_phase5_fmp_acceptance_guardrails_are_explicit(self) -> None:
        text = "\n".join(
            [
                read("README.md"),
                read("shared/equity-research-support-standard.md"),
                read("shared/workflow-source-resolution.md"),
                read("skills/financials-normalizer/references/source-protocol.md"),
                read("skills/financials-normalizer/references/normalization-schema.md"),
                read("skills/public-equity-investing/internal-support/policy.md"),
                read("skills/public-equity-investing/internal-support/fmp-provider-guide/INTERNAL.md"),
                read(
                    "skills/public-equity-investing/internal-support/fmp-provider-guide/references/connector-playbook.md"
                ),
                read(
                    "skills/public-equity-investing/internal-support/fmp-provider-guide/references/workbook-mode.md"
                ),
                read(
                    "skills/public-equity-investing/internal-support/financial-source-of-truth/references/source-discipline-output-patterns.md"
                ),
            ]
        )

        for phrase in [
            "normal structured public-market data route",
            "not as primary-source verification, brokerage/account state, private-market coverage, or internal research access",
            "does not replace private-company datasets, expert networks, brokerage/account systems, or internal document and collaboration repositories",
            "FMP estimates, ratings, price targets, and forecast values as `estimate_consensus`",
            "do not mix them with issuer guidance or analyst/user assumptions",
            "FMP-standardized values use `fact_provider_standardized` unless directly reconciled to a primary source",
            "Do not promote FMP ratios, scores, key metrics, owner earnings",
            "Preserve native currency",
            "Label listing-level data separately from operating-company-level data",
            "missing_required_source",
            "preliminary",
            "screen-grade",
            "Do not load provider guides merely because `.app.json` declares",
            "selects FMP, Quartr, or Daloopa as the concrete route",
            "confirms that route is callable",
        ]:
            self.assertIn(phrase, text)

    def test_app_manifest_and_readme_optional_connectors_stay_consistent(self) -> None:
        manifest = json.loads(read(".app.json"))
        app_names = set(manifest["apps"])
        readme = read("README.md")

        self.assertEqual(
            app_names,
            {
                "google_drive",
                "gmail_connector",
                "outlook_email_connector",
                "sharepoint_connector",
                "teams_connector",
            },
        )
        for name, label in {
            "google_drive": "Google Drive",
            "gmail_connector": "Gmail",
            "outlook_email_connector": "Outlook Email",
            "sharepoint_connector": "SharePoint",
            "teams_connector": "Microsoft Teams",
        }.items():
            self.assertTrue(manifest["apps"][name].get("optional"), name)
            self.assertIn(label, readme)

    def test_phase6_migration_note_and_source_hierarchies_keep_exports_optional(self) -> None:
        text = "\n".join(
            [
                read("../../docs/financial-markets-fmp-migration-plan.md"),
                read("skills/financials-normalizer/references/source-protocol.md"),
                read("skills/company-tearsheet/references/source-and-evidence.md"),
                read("skills/comps-valuation/references/workbook/data-sourcing-and-connectors.md"),
                read("skills/catalyst-calendar/references/source-and-data-protocol.md"),
                read("skills/portfolio-risk-management/references/source-and-context-protocol.md"),
            ]
        )

        for phrase in [
            "FMP is now the default structured public-market data route",
            "removes legacy paid providers from default setup",
            "hints and install-time expectations",
            "remain usable only when the runtime exposes a scoped callable route or the user",
            "provides an export/file",
            "Callable `financial_modeling_prep` for structured public-market data",
            "callable `financial_modeling_prep` for ordinary public-market",
            "Use callable `financial_modeling_prep` first for ordinary public-market data",
            "subject to runtime availability and entitlement",
            "user-provided export",
            "user-provided exports",
        ]:
            self.assertIn(phrase, text)

    def test_migration_playbook_preserves_non_deterministic_refresh_contract(self) -> None:
        text = "\n".join(
            [
                read("../../docs/financial-markets-fmp-migration-playbook.md"),
                read("FORK.md"),
            ]
        )

        for phrase in [
            "Use instructions as a migration compass",
            "patches as acceleration",
            "tests as guardrails",
            "one semantic review pass",
            "not to rediscover the FMP migration",
            "avoid blindly applying an old full-tree patch",
            "clean text that is semantically wrong",
            "FMP is the default structured public-market route",
            "Do not claim that FMP replaces",
            "private-company or private-market datasets",
            "expert-network systems",
            "brokerage, account, order, execution, or buying-power systems",
            "internal document, email, chat, drive, or collaboration repositories",
            "FMP-standardized facts are not primary-source facts unless reconciled",
            "Preserve native currency",
            "listing-level versus operating-company-level distinctions",
            "Canonical smoke prompts",
            "Handoff report template",
        ]:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
