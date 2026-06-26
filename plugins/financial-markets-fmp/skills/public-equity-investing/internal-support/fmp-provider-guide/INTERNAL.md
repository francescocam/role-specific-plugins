# Financial Modeling Prep Provider Guide

> Internal provider guide. Load through `internal-support/policy.md` only after the current workflow selects the callable `financial_modeling_prep` MCP route for an attempted source category. This is not a selectable skill.

## Load Gate

Do not load this guide during user-context preflight, onboarding, or unrelated source setup. A project `.codex/config.toml` entry, preferred-provider hint, or remembered subscription is not proof that FMP is callable in the current runtime.

## Authority And Scope

Use the live `financial_modeling_prep` MCP tool schemas as the source of truth. If they differ from this guide, follow the live schema and retry with the smallest valid read.

Use FMP for scoped public-market data, company profiles, reported financials, estimates, ownership, transcripts, SEC filing discovery, calendars, news, and supported ETF or index context. FMP may supply read-only market and ownership inputs for models or trackers, but it does not supply the user's internal workbook, portfolio account state, orders, approvals, or research notes.

For the `earnings_transcripts_presentations` category, use FMP for transcripts and events when exposed. Do not claim that it provides a complete investor-presentation, webcast, or global IR-document archive.

Before calling FMP, read `references/connector-playbook.md`. For a workbook workflow, also read `references/workbook-mode.md` before editing the workbook.

## Default Sequence

1. Identify the exact listing using the user-provided symbol and exchange context.
2. Select only the FMP tool family needed by the active source category.
3. Make the smallest useful read with explicit symbol, period, and date bounds where supported.
4. Preserve the endpoint, parameters, returned identifiers, source period or as-of date, and retrieval time.
5. Keep FMP-standardized values distinct from primary-source facts, user inputs, and derived calculations.
6. If the required lane is unavailable or empty, use a linked primary source, uploaded material, a user-provided export, or a precise `missing_required_source` gap.

Never invent symbols, exchanges, CIKs, periods, source dates, estimates, filing links, or unsupported provider capabilities.

## Evidence And Normalization Contract

Every FMP-derived material value must carry enough metadata to be reviewed or refreshed later:

- stable FMP tool or endpoint name and the exact request parameters used;
- user-requested symbol plus exchange, CIK, ISIN, CUSIP, company name, or other returned security identifiers where available;
- retrieval timestamp, provider as-of date, reported date, filing date, transcript date, or event date as applicable;
- fiscal year, fiscal period, period end, filing date, currency, and units for financial statements, estimates, KPIs, or per-share values;
- native currency plus explicit FX rate, FX observation date, and FX source for cross-market calculations;
- listing-level versus operating-company-level treatment, including whether the value may duplicate exposure across multiple listings or share classes;
- source URL, SEC accession, filing link, transcript link, or issuer/filing locator when returned by FMP.

Use canonical evidence labels consistently:

- `fact_provider_standardized` for FMP-normalized reported facts, profiles, market data, ownership, ESG, ratings, holders, fund/index data, or other provider-standardized fields;
- `estimate_consensus` for FMP analyst estimates, consensus, ratings, price targets, or forecast fields;
- `fact_source_reported` only after checking the value directly in a linked filing, issuer release, transcript, or other primary source;
- `derived_calculation` for calculations made from cited inputs, with the formula and input source IDs preserved;
- `missing_required_source`, `stale_source`, or `contradicted_source` when FMP lacks the lane, appears stale, or conflicts with another material source.

Do not promote FMP ratios, scores, key metrics, owner earnings, intrinsic value, valuation outputs, or other provider-calculated analytics to canonical plugin metrics unless an owning workflow has an approved formula and cites the raw inputs. FMP-precalculated analytics may be used as diagnostics or screen-grade context only, and must remain labeled as provider-standardized.

Material financial, valuation, catalyst, or sizing conclusions require primary-source reconciliation when practicable. If reconciliation is not performed, state that the value is provider-standardized and identify what source would make it decision-grade.

## Category Boundaries

- `company_filings_ir`: reported statements, company profiles, SEC filing discovery, press releases, and supported disclosure data. Use linked primary filings for decisive verification when material.
- `earnings_transcripts_presentations`: transcripts, earnings dates, and management commentary available through FMP. Request or locate the issuer presentation separately when FMP does not expose it.
- `market_data_estimates`: quotes, price history, market capitalization, estimates, ratings, price targets, ownership, calendars, and supported fund/index data.
- `portfolio_models_trackers`: read-only market, estimate, ownership, and reference inputs. Do not represent FMP as a portfolio system or brokerage.

## Known FMP Hazards

- Secondary listings, ADRs, receipts, OTC variants, and share classes can carry full-company market capitalization or duplicated company exposure; label listing-level work and do not silently aggregate to an operating-company view.
- Country or domicile is company metadata, not a substitute for exchange, venue, or trading-line filters.
- Pence/pounds, GBp/GBP, per-share units, scale, and other currency-unit issues need field-specific treatment; never apply one blanket conversion to every monetary field.
- Estimates, ratings, price targets, and consensus fields are provider aggregates, not broker-level estimate detail or the full underlying model history.
- Transcript, ESG, 13F, insider, ETF, fund, index, news, and other endpoint availability is plan-dependent; empty or denied responses are entitlement/coverage facts, not proof the event or dataset does not exist.
- U.S. SEC coverage is not equivalent to complete global filing, exchange filing, investor-presentation, or issuer-IR document coverage.
- Provider-standardized statements can differ from issuer presentation, restated filings, segment definitions, adjusted metrics, or other vendor exports. Preserve conflicts instead of overwriting them.

## Output And Recovery

Prefer narrow calls over broad bulk reads. If a call fails, inspect the live tool schema, reduce the symbol/date/period scope, and retry once with the smallest valid request. If access is plan-limited or the result is missing, name the exact lane and fallback needed.

Identify FMP as the provider for values returned by FMP. Add visible data-quality flags for stale, missing, conflicting, suspicious, plan-limited, listing-ambiguous, currency-ambiguous, or unreconciled values. Do not imply that linked filings, uploaded documents, internal data, or calculations originated from FMP.
