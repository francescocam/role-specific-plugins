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

## Category Boundaries

- `company_filings_ir`: reported statements, company profiles, SEC filing discovery, press releases, and supported disclosure data. Use linked primary filings for decisive verification when material.
- `earnings_transcripts_presentations`: transcripts, earnings dates, and management commentary available through FMP. Request or locate the issuer presentation separately when FMP does not expose it.
- `market_data_estimates`: quotes, price history, market capitalization, estimates, ratings, price targets, ownership, calendars, and supported fund/index data.
- `portfolio_models_trackers`: read-only market, estimate, ownership, and reference inputs. Do not represent FMP as a portfolio system or brokerage.

## Output And Recovery

Prefer narrow calls over broad bulk reads. If a call fails, inspect the live tool schema, reduce the symbol/date/period scope, and retry once with the smallest valid request. If access is plan-limited or the result is missing, name the exact lane and fallback needed.

Identify FMP as the provider for values returned by FMP. Do not imply that linked filings, uploaded documents, internal data, or calculations originated from FMP.
