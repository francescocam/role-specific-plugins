# Financial Modeling Prep MCP Playbook

Load this reference only after the owning workflow selects a callable `financial_modeling_prep` MCP route.

## Authority Order

1. The live FMP MCP tool schemas exposed in the current runtime.
2. The route and category boundaries in this playbook.
3. The owning analytical workflow.
4. The user's latest explicit instruction when it does not conflict with data integrity.

## Route By Need

Use only the smallest relevant tool family:

- company identity and listing context: directory or company;
- price and market context: quote or chart;
- reported financials and segments: statements;
- estimates, ratings, and price targets: analyst;
- earnings, dividends, splits, and IPO events: calendar;
- earnings-call transcripts: earnings transcript;
- SEC filing discovery: SEC filings;
- ownership: Form 13F or insider trades;
- ETF and fund context: ETF and mutual funds;
- issuer and market news: news;
- macro context: economics;
- supported index context: indexes.

The exact callable names and parameters come from the live MCP schema. Do not copy a remembered endpoint shape when the schema differs.

## Workflow Endpoint Map

Use this map to choose the first FMP route family. The live MCP schema remains authoritative for exact callable names, required arguments, and entitlement messages.

| Workflow need | FMP route family | Minimum identifiers | Freshness expectation | Pagination / bounds | Empty-result behavior and fallback |
| --- | --- | --- | --- | --- | --- |
| Current price and market cap | `quote` for current trading data; `company` market-cap endpoints for market capitalization | Symbol; exchange or security type when ambiguous | Intraday/current at retrieval time; preserve quote timestamp or retrieval time | Prefer single-symbol or bounded batch reads; avoid full-exchange reads unless the workflow is explicitly market-wide | Retry once with the exact symbol or exchange variant; fall back to exchange/issuer/approved market-data export and mark `missing_required_source` if current price is decision-critical |
| Price and volume history | `chart` historical EOD or intraday route family | Symbol; date range; adjustment basis when relevant | Current through requested end date; state if the latest bar is delayed or partial | Always use `from_date`/`to_date`; choose full/light/intraday route only for needed granularity | If no bars return, check symbol variant and listing status; fall back to exchange data, uploaded price file, or another callable market-data route |
| Company identity and listing metadata | `company` profile route family plus `directory` and `search` route families | Symbol or CIK/ISIN/CUSIP/name; exchange where needed | Current at retrieval time, with provider as-of/retrieval time preserved | Use exact symbol/profile first; use search/directory only to disambiguate | If identity remains ambiguous, stop and ask for listing/exchange/identifier; do not merge share classes or listings by name |
| Reported statements | `statements` standardized statement and as-reported statement route families | Symbol; annual/quarter period; fiscal year or limit | Latest filed/reporting period for current work; `acceptable_for_period` for user-specified historical periods | Use annual/quarter period and narrow limit/year where supported | If missing or conflicting, use linked SEC/issuer filing, earnings release, uploaded statements, or provider export; keep FMP values `fact_provider_standardized` until reconciled |
| Enterprise value inputs | `statements` enterprise-values route plus cited balance sheet, cash flow, share count, and quote/company inputs | Symbol; period/date; currency; share-count basis | Align EV date with market price and latest balance-sheet date; flag stale debt/cash or share counts | Use bounded annual/quarter statement pulls and single-symbol market data | If EV components do not tie, rebuild from cited inputs or mark the EV bridge `screen-grade` / `missing_required_source` |
| Consensus and expectation bar | `analyst` financial-estimates, ratings, grades, price-target route families | Symbol; forecast period; estimate type/basis when returned | Use provider as-of/retrieval time; stale if the company has reported since the estimate snapshot | Use period and limit/page where supported; keep estimate horizon explicit | If unavailable or stale, request broker/consensus export or use user-provided bar; never substitute issuer guidance for consensus |
| Earnings dates and surprises | `calendar` earnings-calendar and earnings-company route families | Symbol or date range; event date; fiscal period if returned | Current event calendar at retrieval time; post-print data is preliminary until filing/transcript support exists | Use date bounds for calendars and symbol route for company history | If missing, use issuer IR calendar, exchange calendar, earnings release, or uploaded event file |
| Transcripts | `earningsTranscript` search, dates-by-symbol, latest, and available-symbol route families | Symbol; fiscal year; quarter; transcript date when returned | Current when transcript exists for the reported quarter; plan-limited if entitlement blocks access | Use symbol/year/quarter for direct pulls; use dates/list routes only to locate available transcripts | If absent or plan-limited, use issuer webcast/transcript, user upload, Quartr/export, or mark transcript evidence missing |
| SEC filings | `secFilings` search-by-symbol/CIK/form-type and company-profile route families | Symbol or CIK; form type; filing date/accession/link when returned | Current for the requested filing window; U.S. SEC coverage only | Use form type, date bounds, page, and limit for searches | If missing, go to SEC EDGAR or issuer filing page; for non-U.S. issuers use local exchange/issuer IR/source export |
| Revenue segments | `statements` revenue-product-segmentation and revenue-geographic-segments route families | Symbol; fiscal year/period; segment taxonomy/date | Current through latest disclosed period returned; compare with issuer segment definitions | Use year/period/limit where supported; avoid extrapolating undisclosed periods | If missing or definition-changed, use issuer filing/deck segment note and create a comparability bridge rather than inventing history |
| Institutional ownership | `form13F` positions-summary, filings, holder analytics, and industry summary route families | Symbol or holder CIK; year; quarter | 13F data is delayed; preserve filing/report quarter and retrieval time | Use year/quarter, holder/symbol, limit, and page; do not broad-pull all holders unnecessarily | If plan-limited or absent, use SEC 13F filings, ownership export, or label ownership gap; do not infer current positions |
| Insider activity | `insiderTrades` search/statistics/latest route families | Symbol or company/reporting CIK; transaction type/date if needed | Current through returned filing date; preserve transaction/report dates | Use symbol/CIK/date/type and page/limit | If missing, use SEC Form 3/4/5 or issuer insider filings; treat absence as coverage-limited, not proof of no activity |
| ETF/index exposure | `etfAndMutualFunds` holdings/exposure/weighting route families; `indexes` constituent route families | ETF/index symbol; issuer symbol; constituent date/period when returned | ETF holdings as of fund disclosure date; index constituents as of returned effective/current date | Use symbol-specific holdings/exposure first; use index current/historical routes with dates where supported | If missing or official index precision matters, request ETF sponsor holdings, official index data, or user export |
| Corporate actions | `calendar` dividends/splits/IPOs route families | Symbol or date range; event type; ex/effective/payment dates when returned | Current event calendar at retrieval time; preserve event-status/date fields | Use date bounds for calendars and symbol route for company history | If missing, use issuer IR, exchange notices, SEC filings, transfer-agent data, or user export |
| Macro context | `economics` calendar, indicators, treasury-rates, and market-risk-premium route families | Country or indicator name; date range; currency/tenor when relevant | Current through latest release/observation; label preliminary releases | Use date bounds and specific indicator/country/tenor; avoid broad calendars unless needed | If missing, use official statistical agency, central bank, treasury, or other primary macro source |
| News and issuer releases | `news` stock-news, search-stock-news, general-news, press-releases, and search-press-releases route families | Symbol(s); date range; article/release date and URL | Current through retrieval time; source timestamp controls | Use symbol/date filters, page, and limit; avoid broad news dumps | If missing or material, use issuer press releases, regulatory filings, trusted news source, or user-provided article/export |

## Call Rules

- Start from an exact symbol; preserve exchange and security identity when ambiguity exists.
- Use explicit annual or quarterly periods and date bounds where supported.
- Use narrow limits and pagination rather than unconstrained broad results.
- Preserve the requested tool or endpoint name, parameters, retrieval time, returned as-of date, fiscal period, filing date, currency, units, and source links where available.
- Preserve symbol, exchange, CIK, ISIN, CUSIP, company name, security type, and other returned identifiers rather than collapsing them into a company label.
- Preserve native currency. When converting across markets, record FX rate, FX observation date, FX source, and whether the source field was price, per-share, statement value, or market capitalization.
- Label listing-level data separately from operating-company-level data; do not sum market capitalization or ownership across trading lines unless the owning workflow defines a canonicalization policy.
- Treat FMP output as provider-standardized unless directly verified in the linked primary source.
- Keep estimates separate from reported actuals.
- Label FMP estimates, ratings, price targets, and forecast values as `estimate_consensus`; label FMP-normalized actuals, market data, ownership, ESG, ETF, fund, index, and profile fields as `fact_provider_standardized`.
- Use `fact_source_reported` only after checking the linked filing, issuer release, transcript, or other primary source directly.
- Do not promote FMP ratios, scores, key metrics, owner earnings, valuation outputs, or provider-calculated analytics to canonical plugin metrics without an approved formula and sourced raw inputs.
- Flag stale, missing, conflicting, suspicious, plan-limited, listing-ambiguous, currency-ambiguous, or unreconciled values before downstream use.
- Do not use FMP as proof of internal portfolio positions, brokerage state, private-company facts, expert research, or internal documents.

## Hazard Checks

Run these checks before presenting an FMP-backed conclusion as decision-grade:

- Is the value tied to the requested listing, exchange, share class, and security type?
- Could a secondary listing, ADR, OTC line, or receipt duplicate full-company market capitalization or ownership exposure?
- Is country or domicile being used incorrectly as an exchange or venue filter?
- Are price units, statement units, per-share units, pence/pounds labels, and currency codes handled field by field?
- Are consensus fields clearly separated from issuer guidance, company-reported actuals, and analyst/user assumptions?
- Is the requested endpoint plan-limited or coverage-limited, especially for transcripts, ESG, 13F, insider, ETF, fund, index, news, or non-U.S. filing data?
- Is U.S. SEC filing coverage being incorrectly treated as complete global filing or investor-presentation coverage?

## Fallbacks

- For missing or disputed filing facts, follow the linked issuer or SEC source.
- For missing investor presentations or webcast materials, use issuer IR or user-provided documents.
- For missing internal models, trackers, notes, or positions, request the exact user-controlled source.
- For plan-limited endpoints, state the entitlement gap and continue with available primary or uploaded evidence.

If a call remains blocked after one minimal retry, record the missing lane as `missing_required_source` when it prevents a decision-grade conclusion.
