# Financial Modeling Prep Workbook Mode

Load this reference only when a routed workflow uses FMP while reading or editing a workbook.

## Source Order

1. Inspect the active workbook first.
2. Preserve current, source-backed workbook data and analyst assumptions.
3. Use FMP only for missing or requested public-market, financial, estimate, ownership, event, or transcript inputs.
4. Keep FMP values, primary-source values, internal data, assumptions, and calculations separately labeled.

## Workbook Rules

- Never overwrite analyst-created formulas, assumptions, notes, or formatting without asking.
- Put imported provider data on a clearly named raw-data tab such as `FMP_Data` unless the user requests another layout.
- Preserve symbol, exchange, endpoint, parameters, period or as-of date, currency, units, retrieval time, and source URL where available.
- Put analyst assumptions on an `Inputs` or `Assumptions` tab.
- Keep formulas on model or output tabs, not in the raw-data area.
- Do not represent FMP as the source of internal portfolio positions or workbook-authored values.
- Preserve the workbook's existing formatting unless the user asks for a redesign.
- After edits, summarize changed tabs and ranges.
