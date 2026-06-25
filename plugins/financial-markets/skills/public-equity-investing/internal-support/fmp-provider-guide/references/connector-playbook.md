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

## Call Rules

- Start from an exact symbol; preserve exchange and security identity when ambiguity exists.
- Use explicit annual or quarterly periods and date bounds where supported.
- Use narrow limits and pagination rather than unconstrained broad results.
- Preserve the requested endpoint, parameters, retrieval time, returned as-of date, fiscal period, filing date, currency, units, and source links where available.
- Treat FMP output as provider-standardized unless directly verified in the linked primary source.
- Keep estimates separate from reported actuals.
- Do not use FMP as proof of internal portfolio positions, brokerage state, private-company facts, expert research, or internal documents.

## Fallbacks

- For missing or disputed filing facts, follow the linked issuer or SEC source.
- For missing investor presentations or webcast materials, use issuer IR or user-provided documents.
- For missing internal models, trackers, notes, or positions, request the exact user-controlled source.
- For plan-limited endpoints, state the entitlement gap and continue with available primary or uploaded evidence.

If a call remains blocked after one minimal retry, record the missing lane as `missing_required_source` when it prevents a decision-grade conclusion.
