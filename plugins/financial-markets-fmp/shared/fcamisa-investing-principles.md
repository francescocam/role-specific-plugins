# Fcamisa Investing Principles House Standard

Use this standard whenever Financial Markets (FMP-first fork) work is for the owner's personal company analysis, idea triage, valuation, memo, thesis tracking, or position review. The full source of truth is `/Users/fcamisa/Development/investing-tool-v2/docs/product/investing-principles.md`; this file operationalizes the durable rules for plugin workflows.

## Default Lens

- Default to long-term, long-only, catalyst-aware value investing unless the user explicitly asks for another audience or strategy lens.
- No leverage: do not use leverage. Do not turn the workspace into trade execution or broker advice.
- The central buying question is: why is this mispriced, what protects the downside, and how does the owner earn an attractive total return under conservative assumptions?
- Treat `hold cash / no action` as a valid conclusion when the expected return, evidence quality, downside protection, or understanding is not good enough.

## Underwriting Gates

- Anchor valuation in owner earnings, normalized earnings power, normalized cash flows, margins, returns on capital, and realistic reinvestment needs before DCF, comps, SOTP, or vendor ratios.
- A positive common-stock mispricing conclusion needs roughly `15%+ expected annualized` total return under conservative assumptions.
- A great-business exception may clear the bar at `10% to 12%+` only when business quality, reinvestment runway, management, balance sheet resilience, and downside protection are unusually strong.
- Warrants, fragile situations, highly levered equities, illiquid names, and complex equity-like instruments require `20%+` or more expected annualized return.
- Lower-quality, more levered, more illiquid, or more complex situations require a higher return hurdle, smaller sizing, clearer milestones, and less patience.
- Relative valuation, DCF, historical multiples, and SOTP are triangulation tools. They must not manufacture value when conservative owner-earnings math does not clear the hurdle.
- FMP ratios are diagnostic, not canonical. Recalculate or validate investment ratios from source fields when they drive a decision, preserving units, currency, periods, as-of dates, and formula logic.

## Downside And Quality Discipline

- The preferred downside anchors are earnings power, balance sheet resilience, capital returns, strategic value, and asset value, in that order.
- Balance sheet resilience is a hard gate for core positions: test net debt to normalized FCF or EBITDA, interest coverage, free cash flow after interest, maturity schedule, covenant headroom, liquidity runway, debt-market access, and collateral quality.
- Do not support a main-position conclusion when survival depends on near-term refinancing, excessive leverage, covenant relief, persistent cash burn, opaque liabilities, or debt structures that can wipe out the equity before the thesis plays out.
- Distinguish temporary under-earning from structural impairment. Peak earnings must not be capitalized for cyclicals, and negative current FCF requires explicit funding and survival evidence.
- Management and capital allocation must be judged on per-share value, disclosure quality, buybacks, dividends, acquisitions, dilution, debt reduction, incentives, and treatment of minority shareholders.

## Action Discipline

- Use owner-relevant action labels: `research further`, `watchlist`, `initiate candidate`, `add`, `hold`, `trim`, `sell`, `re-underwrite`, or `hold cash / no action`.
- Adding requires either a better price with an unchanged thesis or new evidence that improves confidence in normalized earnings power, balance sheet safety, or the recognition path.
- Do not average down when thesis is broken, leverage risk has increased, liquidity has worsened, management has disappointed, or the original analysis was incomplete.
- A normal initial position is usually 2% to 5%. Exceeding 10% at cost requires strong evidence across earnings power, balance sheet resilience, management, valuation, and downside protection. Exceeding 15% at cost requires a written concentration review.
- Re-underwrite at least annually and whenever major evidence arrives. Sell or trim when the thesis is broken, price reaches fair value or forward return falls below the hurdle, or a clearly better opportunity exists after taxes, liquidity, research confidence, thesis maturity, and concentration are considered.
- Every sale or material thesis failure should produce a post-mortem: reason, thesis outcome, return, what was right, what was wrong, whether the process worked, and what should change in future screens or checklists.

## Required Output Checks

For substantial company analysis, make these visible before any positive action conclusion:

1. Mispricing source and variant view.
2. Conservative owner-earnings or normalized earnings-power bridge.
3. Expected annualized return versus the correct hurdle.
4. Downside mechanism and balance sheet survival evidence.
5. Recognition path or catalyst, preferably soft recognition or fundamental improvement.
6. Thesis-break conditions, review date, and next evidence.
7. Data limitations, stale fields, FMP-derived diagnostics, and recalculation gaps.
