# Financial Markets Plugin: FMP Migration Plan

## Objective

Make Financial Modeling Prep (FMP) the default external market-data provider for
the Financial Markets plugin, remove unnecessary paid-provider connector
requirements, and retain only integrations that supply capabilities FMP cannot
replace.

This is a migration plan, not an assertion that every FMP field is equivalent to
the corresponding field from FactSet, LSEG, S&P Capital IQ, Morningstar,
Daloopa, or Quartr. Provider-standardized values must retain their source,
retrieval time, period, currency, and evidence classification.

## Current State

- The repository-level `.codex/config.toml` configures the
  `financial_modeling_prep` MCP server.
- The Financial Markets plugin does not currently declare an FMP route in its
  plugin metadata, source-category configuration, workflow routing, or provider
  guides.
- `plugins/financial-markets-fmp/.app.json` currently declares placeholder
  integrations for PitchBook, FactSet, Morningstar, LSEG, S&P, Third Bridge,
  Daloopa, Quartr, and Alpaca. Because these entries are not marked optional,
  the plugin appears to require services that are not necessary for an
  FMP-first installation.
- The plugin has provider-specific routing guides for Daloopa and Quartr, but no
  equivalent FMP guide.

## Verified FMP Entitlement

Live MCP checks performed on June 25, 2026 confirmed that the configured FMP
subscription can currently access:

- real-time stock quotes and market capitalization;
- annual standardized financial statements;
- analyst financial estimates and analyst counts;
- earnings transcript availability;
- SEC filing discovery and source links;
- Form 13F institutional ownership summaries;
- ESG ratings;
- ETF holdings with weights and update timestamps.

The MCP tool catalog also exposes company profiles, peers, float, executives,
historical prices, corporate-action calendars, earnings calendars, news and
press releases, insider trades, economic data, index constituents, revenue
segments, price targets, analyst grades, fund data, and M&A records. Each lane
must still be acceptance-tested for the relevant exchanges, securities, history,
freshness, and rate limits before being treated as production-ready.

## Replacement Matrix

| Existing service | FMP replacement level | Use FMP for | What FMP does not replace |
| --- | --- | --- | --- |
| FactSet | High for core public-equity workflows | Quotes, price history, profiles, statements, estimates, ratings, price targets, calendars, ownership, ETF holdings, news, transcripts, SEC discovery, and basic peers | FactSet workstation breadth, proprietary broker research, advanced ownership and fund analytics, official index data and licensing, risk/factor models, portfolio analytics, symbology depth, fixed-income coverage, and enterprise support/SLA |
| LSEG / Refinitiv | High for core public-equity workflows | The same primary FMP lanes above, including market data, fundamentals, estimates, news, and events | Reuters editorial and archive depth, proprietary consensus and estimates detail, instrument master, global corporate-actions depth, fixed income, deals, risk analytics, and enterprise-grade feeds |
| S&P Capital IQ / S&P | High for basic listed-equity research; partial overall | Financials, estimates, profiles, peers, market data, SEC filings, and historical S&P 500/Nasdaq/Dow constituents where exposed by FMP | Capital IQ transaction and private-company depth, proprietary classifications and estimates, credit data, official forward index changes/rebalance files, licensed index methodology/data, and broader S&P datasets |
| Morningstar | Moderate | Public-company fundamentals, quotes, estimates, and basic ETF/fund holdings and allocation data | Morningstar analyst research and moat ratings, stewardship analysis, fund category/rating methodology, portfolio look-through depth, style boxes, and manager/fund research |
| Daloopa | Moderate to high for standard financials; low for specialist KPI extraction | Standard and as-reported statements, segments, SEC filing links, estimates, and model inputs that can be mapped reliably | Daloopa's granular source-linked KPI extraction, filing-page-level citations per datapoint, specialist company/sector KPIs, reviewed model-ready mappings, and provider-specific audit trail |
| Quartr | Moderate to high for transcripts and U.S. filings | Earnings transcripts, transcript dates, SEC filing discovery, press releases, statements, and event calendars | Investor presentations and capital-markets-day decks as a dependable corpus, audio/webcast experience, global filing and IR-document coverage, document-level search, page references, and Quartr event/document metadata |
| Alpaca | High for read-only public market data; none for brokerage | Quotes and historical prices used in research | Brokerage accounts, positions, orders, executions, paper trading, portfolio state, and broker-specific buying power or transaction history |
| Moody's | Low | General company financial context and some market information | Credit ratings, rating actions, outlooks, methodologies, default studies, recovery analysis, and licensed credit research |
| PitchBook | Low | Public-company profiles, market prices, public financials, and a limited M&A feed | Private-company coverage, funding rounds, investors, cap tables, private valuations, private-company financials, VC/PE fund data, deal participants, and private-market comparables |
| Third Bridge | None | No meaningful substitute | Expert-call transcripts, primary research interviews, expert-network access, and proprietary channel checks |
| Datasite | None | No meaningful substitute | Virtual data rooms, permissioned diligence documents, deal workflow, audit logs, and controlled document exchange |
| Hebbia | None as a data source | FMP can supply structured market data for a separate document workflow | Cross-document diligence, user-controlled document corpora, document reasoning, and workspace/document search |
| Slack, Google Drive, Gmail, Outlook, SharePoint, Teams | None | No substitute | Internal research, communications, source documents, models, notes, approvals, and collaboration context |

## Recommended Target Configuration

### Keep

- FMP MCP as the default route for market data, company fundamentals,
  estimates, transcripts, public ownership, fund holdings, calendars, news, and
  SEC filing discovery.
- Google Drive, Gmail, Outlook, SharePoint, Teams, and Slack only where internal
  context and controlled document handoff are desired.
- Optional user-provided exports from any institutional provider. An FMP-first
  plugin should not prevent a user from supplying FactSet, LSEG, S&P,
  Morningstar, Daloopa, Quartr, or broker exports.

### Remove from default installation

- FactSet
- LSEG
- S&P
- Morningstar
- Daloopa
- Quartr
- Alpaca, unless brokerage/account workflows are explicitly required

### Retain only as explicit optional capabilities

- PitchBook for private markets and transaction intelligence.
- Third Bridge for expert-network research.
- Alpaca for brokerage state and execution.
- Any collaboration/document connector the user actually uses.

Services retained as optional must have `"optional": true` in `.app.json` and
must never be treated as callable merely because they appear in the manifest.

## Implementation Plan

### Phase 0: Secure the FMP credential

The current `.codex/config.toml` is ignored by Git and is not tracked, but it
contains the API key directly in the MCP URL.

Implementation status:

1. **Complete:** Removed the literal FMP API key from the local
   `.codex/config.toml`.
2. **Complete:** Moved the credential to macOS Keychain and configured Codex to
   launch the FMP connection through `scripts/start-fmp-mcp.sh`.
3. **Waived by the repository owner:** No key rotation is required. The existing
   key remains stored in macOS Keychain.
4. **Complete:** Added a sanitized `.codex/config.example.toml`.
5. **Complete:** Updated `.gitignore` so the local configuration remains ignored
   while the safe example is tracked.

Acceptance criteria:

- Git history and tracked files contain no FMP key or secret-bearing MCP URL.
- FMP remains callable in Codex after a clean restart.
- Setup documentation explains the required Keychain entry without containing
  a credential.

### Phase 1: Make FMP a first-class source route

Implementation status: **Complete on June 25, 2026.**

1. **Complete:** Added FMP to the source-category catalog:
   - `company_filings_ir`
   - `earnings_transcripts_presentations`, with an explicit warning that FMP
     does not fully replace presentation/document coverage
   - `market_data_estimates`
   - `portfolio_models_trackers` for read-only market and ownership inputs, not
     brokerage state
2. **Complete:** Updated `shared/workflow-source-resolution.md` to recognize the callable
   `financial_modeling_prep` MCP route.
3. **Complete:** Added an internal `fmp-provider-guide` beside the Daloopa and Quartr guides.
4. **Complete:** Registered the guide in `internal-support/policy.md`.
5. **Complete:** Preserved the existing rule that runtime callability and entitlement must be
   verified before claiming access.

Acceptance criteria:

- A workflow can resolve a semantic source category to FMP without naming a
  legacy provider.
- The router does not load FMP tools for unrelated categories.
- Missing FMP coverage falls back to primary sources, user files, or an
  explicitly requested provider export.

### Phase 2: Define the FMP evidence and normalization contract

Status: **complete** as of June 26, 2026.

The FMP provider guide now requires:

- **Complete:** stable FMP tool or endpoint name and request parameters.
- **Complete:** symbol, exchange, CIK/ISIN/CUSIP, and other returned identifiers.
- **Complete:** retrieval timestamp and source/provider as-of date.
- **Complete:** fiscal year, period, filing date, currency, and units for financials.
- **Complete:** native currency and explicit FX metadata for cross-market calculations.
- **Complete:** a distinction between listing-level and operating-company-level data.
- **Complete:** `fact_provider_standardized` for FMP-normalized fields.
- **Complete:** `estimate_consensus` for FMP estimates, ratings, price targets, and forecasts.
- **Complete:** `fact_source_reported` only when the value is verified directly in a linked
  filing or issuer document;
- **Complete:** primary-source reconciliation for material values.
- **Complete:** no promotion of FMP ratios, scores, key metrics, owner earnings, or valuation
  outputs to canonical plugin metrics without an approved formula;
- **Complete:** visible data-quality flags for stale, missing, conflicting, or suspicious
  values.

The guide also documents known FMP hazards:

- **Complete:** secondary listings can carry full-company market capitalization.
- **Complete:** country is not a substitute for exchange/venue.
- **Complete:** pence/pounds and other currency-unit issues need field-specific treatment.
- **Complete:** estimates and ratings are provider aggregates, not a substitute for
  broker-level estimate detail;
- **Complete:** transcript, ESG, 13F, and other endpoint availability is plan-dependent.
- **Complete:** U.S. SEC coverage is not equivalent to complete global filing coverage.

Acceptance criteria:

- FMP-sourced material values have endpoint/request, identifier, period, currency,
  unit, retrieval, as-of, evidence-label, and quality-flag requirements.
- FMP provider-standardized fields and FMP estimates are not confused with
  primary-source facts or issuer guidance.
- Cross-market, secondary-listing, and endpoint-entitlement hazards are explicit
  in both the provider guide and normalization protocol.

### Phase 3: Replace connector requirements

Status: **complete** as of June 26, 2026.

1. **Complete:** Removed the default placeholder entries for FactSet, LSEG, S&P, Morningstar,
   Daloopa, and Quartr from `.app.json`.
2. **Complete:** Removed the Alpaca placeholder from `.app.json`; brokerage remains
   documented only as an optional export or callable route for account, position,
   order, execution, and buying-power context.
3. **Complete:** Removed PitchBook and Third Bridge placeholders from `.app.json`;
   the README keeps private-market and expert-network routes optional via
   user-provided exports or callable routes.
4. **Complete:** Marked installed collaboration/document app connectors optional
   and removed placeholder collaboration entries.
5. **Complete:** Updated the README integration table to place FMP first and separate:
   - structured public-market data;
   - primary/IR documents;
   - private-market research;
   - expert research;
   - brokerage;
   - internal collaboration.

Acceptance criteria:

- Installing the FMP-first plugin does not request credentials for unused paid
  providers.
- No README or onboarding text implies FMP supplies private-company,
  expert-network, brokerage, or internal-document capabilities.

### Phase 4: Map workflows to FMP endpoints

Status: **complete** as of June 26, 2026.

Created a tested mapping table in the FMP provider guide. At minimum:

| Workflow need | FMP route |
| --- | --- |
| **Complete:** Current price and market cap | quote / company market-cap |
| **Complete:** Price and volume history | historical stock chart |
| **Complete:** Company identity and listing metadata | company profile, directory, and search |
| **Complete:** Reported statements | standardized and as-reported statements |
| **Complete:** Enterprise value inputs | enterprise values plus cited statement, share-count, and market inputs |
| **Complete:** Consensus and expectation bar | financial estimates, price targets, ratings |
| **Complete:** Earnings dates and surprises | earnings calendar/company earnings |
| **Complete:** Transcripts | earnings transcript search/date routes |
| **Complete:** SEC filings | SEC filing search and linked primary filing |
| **Complete:** Revenue segments | product and geographic segmentation |
| **Complete:** Institutional ownership | Form 13F endpoints |
| **Complete:** Insider activity | insider-trade endpoints |
| **Complete:** ETF/index exposure | ETF holdings and supported index constituents |
| **Complete:** Corporate actions | dividend, split, and IPO calendars |
| **Complete:** Macro context | economics calendar, indicators, treasury rates, risk premium |
| **Complete:** News and issuer releases | stock news, general news, and press releases |

For every mapping, the guide defines freshness, minimum required identifiers,
pagination or date bounds, empty-result behavior, and fallback source.

### Phase 5: Add coverage and regression tests

Add tests that verify:

Status: **complete** as of June 26, 2026.

Added deterministic regression tests that verify:

1. **Complete:** FMP is listed in the intended source categories.
2. **Complete:** FMP is not presented as a brokerage, private-market, expert-network, or
   internal-document source.
3. **Complete:** Provider values receive the correct evidence labels.
4. **Complete:** Estimates remain distinct from reported facts and user assumptions.
5. **Complete:** Provider ratios and scores are not silently used as canonical calculations.
6. **Complete:** Cross-listed securities preserve listing grain and currency.
7. **Complete:** Workflows downgrade gracefully to `missing_required_source`,
   `preliminary`, or `screen-grade` when FMP lacks required evidence.
8. **Complete:** Legacy Daloopa and Quartr guides are loaded only if those routes remain
   installed, callable, and explicitly selected.
9. **Complete:** The plugin contains no mandatory placeholder IDs for removed providers.
10. **Complete:** Documentation and `.app.json` remain consistent.

Representative live FMP MCP checks performed on June 26, 2026:

| Coverage lane | Check performed | Result |
| --- | --- | --- |
| Large U.S. issuer | AAPL quote and annual income statement | Route returned quote, market cap, fiscal-year statement, filing date, CIK, currency, and period metadata. |
| Non-U.S. primary listing | SAP.DE company profile | Route returned XETRA listing metadata, EUR currency, ISIN, exchange, and country fields. |
| ADR or secondary listing | NVD.DE company profile | Route returned a XETRA secondary listing with EUR currency and full-company-scale market cap, confirming the listing-grain hazard the guide now flags. |
| Bank or insurer | JPM annual balance sheet | Route returned bank balance-sheet fields with fiscal-year, filing date, CIK, currency, and period metadata. |
| ETF | SPY holdings | Route returned holdings, weights, ISIN/CUSIP, market values, and `updatedAt` timestamps. |
| Non-calendar fiscal year | WMT annual income statement | Route returned FY2026 period ending January 31, 2026, validating non-calendar fiscal-year metadata preservation. |
| Small-cap sparse estimates | RKLB annual financial estimates | Route returned provider estimates with low analyst counts, validating `estimate_consensus` labeling and sparse-estimate caveats. |
| Recent IPO / newly public company | ARM company profile | Route returned IPO date, ADR flag, identifiers, exchange, and listing metadata. |

### Phase 6: Decommission legacy defaults

Status: **complete** as of June 26, 2026.

After the acceptance suite passes:

1. **Complete:** Removed legacy providers from onboarding preference hints.
2. **Complete:** Retained Daloopa/Quartr provider guides because optional support for
   those providers is not intentionally discontinued; the guides now remain
   optional and load only after a route is installed, callable, and selected.
3. **Complete:** Updated examples, source hierarchies, unsupported-connector warnings, and
   tests to mention FMP as the normal structured-data route.
4. **Complete:** Kept generic language allowing user-provided institutional-provider exports.
5. **Complete:** Published the migration note below explaining the capabilities that now require a
   primary-source fallback or an optional specialist provider.

#### Migration note: post-FMP-first specialist coverage

FMP is now the default structured public-market data route for Public Equity
Investing workflows when `financial_modeling_prep` is callable. It is suitable
for ordinary public-company profiles, quotes, price history, statements,
estimates, ownership, transcripts, SEC filing discovery, calendars, news, and
supported ETF/index context, subject to entitlement and coverage.

The migration intentionally removes legacy paid providers from default setup
hints and install-time expectations. FactSet, LSEG, S&P Capital IQ,
Morningstar, Daloopa, Quartr, Bloomberg-like systems, broker sources, Alpaca,
PitchBook, Third Bridge, Datasite, Hebbia, and collaboration/document systems
remain usable only when the runtime exposes a scoped callable route or the user
provides an export/file. FMP does not replace those sources for private-company
datasets, expert networks, broker-by-broker estimate detail, brokerage account
state, official licensed index files, specialist KPI extraction, complete IR
document/webcast archives, internal research repositories, or transaction data
rooms.

When FMP lacks a required lane, workflows should request the precise primary
source, user export, or optional specialist route and label the gap as
`missing_required_source`, `preliminary`, or `screen-grade` rather than
silently substituting unsupported data.

## Capability Gaps Requiring a Non-FMP Source

The FMP-first plugin must explicitly request another source for:

- private-company funding, cap tables, investors, and private valuations;
- expert-call transcripts and proprietary channel checks;
- credit ratings, rating actions, and rating-agency research;
- broker research documents and broker-by-broker estimate detail;
- official licensed index data, announced rebalance files, and methodology
  determinations not exposed by FMP;
- portfolio risk/factor models and institutional portfolio analytics;
- brokerage account positions, orders, executions, and buying power;
- investor presentations, audio/webcasts, and global IR-document archives when
  FMP does not return the required material;
- granular, source-linked specialist KPIs not present in FMP statements or
  segments;
- internal emails, chats, research notes, models, approvals, and controlled
  document repositories;
- virtual data rooms and permissioned transaction-diligence workflows.

These gaps should produce a precise source request rather than a generic
failure—for example, “provide the latest PitchBook company export,” “connect a
brokerage route for positions,” or “upload the investor presentation.”

## Definition of Done

Status: **done** as of June 26, 2026.

- **Complete:** FMP is the default callable structured-data route for public-equity workflows.
- **Complete:** The plugin installs without requiring unrelated paid-provider credentials.
- **Complete:** All FMP-derived data has explicit provenance, period, currency, freshness, and
  evidence labels;
- **Complete:** Primary filings outrank conflicting standardized provider values.
- **Complete:** Specialist capabilities are clearly optional and never attributed to FMP.
- **Complete:** Representative U.S., international, cross-listed, sparse-data, and fund
  workflows passed live FMP MCP checks and deterministic regression tests.
- **Complete:** The repository contains no exposed FMP credential.

Phase 0 was completed on June 25, 2026. Key rotation was explicitly waived by
the repository owner.

Final validation on June 26, 2026:

- `.app.json` and source-category JSON parsed successfully.
- Focused Public Equity/FMP tests passed.
- Full `plugins/financial-markets-fmp` test discovery passed.
- `git diff --check` passed.
