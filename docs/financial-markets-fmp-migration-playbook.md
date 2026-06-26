# Financial Markets FMP fork migration playbook

Use this playbook when refreshing the local `financial-markets-fmp` fork from a newer upstream OpenAI `financial-markets` plugin.

The goal is not to rediscover the FMP migration. The goal is to preserve upstream improvements, reapply the FMP-first fork invariants, and verify the result with tests plus one semantic review pass.

The operating principle:

> Use instructions as a migration compass, patches as acceleration, tests as guardrails, and one semantic review pass as the final sanity check.

## Migration compass: invariants to preserve

### 1. Fork identity

- Plugin id: `financial-markets-fmp`
- Folder: `plugins/financial-markets-fmp`
- Display name: `Financial Markets (FMP-first fork)`
- Author/developer: `Francesco Camisa`
- README and `FORK.md` must clearly say:
  - This is a local FMP-first fork of OpenAI’s Financial Markets plugin.
  - It is not the official OpenAI distribution.
- Marketplace entry must use `financial-markets-fmp`, not `financial-markets`.
- Local marketplace policy keeps `authentication: "ON_USE"`.
- Brand color/icon should remain visually distinguishable from the official plugin.

### 2. FMP is the default structured public-market route

Financial Modeling Prep is the default structured public-market data provider through the configured `financial_modeling_prep` MCP server.

Prefer FMP for:

- company profiles and listing metadata;
- quotes, market cap, price history, and trading data;
- reported financial statements and statement-derived structured data;
- analyst estimates, ratings, price targets, and consensus/expectation-bar inputs;
- earnings dates, surprises, and transcripts when available;
- SEC filing discovery and linked filing metadata;
- institutional ownership / 13F, insider activity, ETF/index context;
- supported macro series, news, and issuer-release context.

Primary filings, issuer IR materials, and uploaded or pasted user materials remain higher-authority evidence when the task requires source-of-truth verification.

### 3. Explicit non-replacements

Do not claim that FMP replaces:

- private-company or private-market datasets;
- expert-network systems;
- brokerage, account, order, execution, or buying-power systems;
- internal document, email, chat, drive, or collaboration repositories;
- specialist vendor exports when the user provides them or a scoped callable route exists.

These sources stay optional and must be requested, used from a user-provided export/file, or used only when the runtime exposes a callable route.

### 4. Evidence discipline

Keep evidence labels distinct:

- FMP structured data;
- issuer filings / company IR;
- uploaded, pasted, or user-provided materials;
- estimates / consensus / ratings / price targets;
- model assumptions and user assumptions.

Required caveats to preserve:

- FMP-standardized facts are not primary-source facts unless reconciled.
- FMP estimates, ratings, and price targets are `estimate_consensus`, not reported actuals.
- FMP ratios, scores, key metrics, and owner-earnings style fields are not canonical without reconciliation.
- Preserve native currency, fiscal period, fiscal year, listing exchange, symbol, CIK/ISIN/CUSIP when available, provider as-of date, retrieval timestamp, and listing-level versus operating-company-level distinctions.
- Treat empty, sparse, stale, or entitlement-limited FMP results as graceful downgrade conditions, not silent failures.

### 5. Local-only installation

This fork is intended for local use. Do not add marketplace publishing assumptions.

Local refresh flow:

```bash
codex plugin add financial-markets-fmp@role-specific-plugins
```

After reinstalling or refreshing, start a new Codex thread so the app reloads plugin metadata, skills, and MCP tools.

## Patches as acceleration, not proof

Patch replay should save time; it is not the authority. The authority is the invariant list above plus the regression tests and semantic review checklist below.

Because the fork directory is `plugins/financial-markets-fmp` while upstream is `plugins/financial-markets`, avoid blindly applying an old full-tree patch that replaces the entire fork directory. That can erase upstream Markdown improvements.

Preferred refresh workflow:

1. Fetch the newer upstream.
2. Create a refresh branch.
3. Copy or rename the newer upstream plugin tree into the fork path.
4. Apply the focused FMP overlay changes.
5. Resolve only real upstream conflicts.
6. Run tests.
7. Perform the semantic review pass.

Example:

```bash
git fetch upstream
git checkout -b codex/financial-markets-fmp-refresh upstream/main

mv plugins/financial-markets-fmp plugins/financial-markets-fmp.previous-refresh 2>/dev/null || true
cp -R plugins/financial-markets plugins/financial-markets-fmp

git am --3way patches/financial-markets-fmp-overlay/*.patch
```

If a patch conflicts, prefer preserving upstream additions unless they violate a fork invariant. Then continue:

```bash
git am --continue
```

If patch replay is too noisy, reapply manually from the playbook instead of forcing a bad patch. The point is to avoid rediscovery, not to worship the patch gremlin.

After a successful refresh, remove `plugins/financial-markets-fmp.previous-refresh` only after validation passes and you no longer need the backup.

## Suggested overlay contents

The overlay should be focused on fork behavior, not a snapshot of every upstream file:

- plugin metadata and local marketplace identity;
- README and `FORK.md` fork notices;
- FMP provider guide and source-routing docs;
- `.app.json` optional connector posture;
- source-category configuration;
- evidence/normalization/source-of-truth guardrails;
- tests that encode FMP-first behavior;
- local FMP MCP helper script and safe `.codex` example config;
- migration docs.

Recommended export shape:

```bash
mkdir -p patches/financial-markets-fmp-overlay

git format-patch <upstream-base-or-refresh-point>..HEAD \
  -- .agents/plugins/marketplace.json \
     .gitignore \
     .codex/config.example.toml \
     scripts/start-fmp-mcp.sh \
     docs/financial-markets-fmp-migration-plan.md \
     docs/financial-markets-fmp-migration-playbook.md \
     plugins/financial-markets-fmp/.app.json \
     plugins/financial-markets-fmp/.codex-plugin/plugin.json \
     plugins/financial-markets-fmp/README.md \
     plugins/financial-markets-fmp/FORK.md \
     plugins/financial-markets-fmp/assets/composerIcon.svg \
     plugins/financial-markets-fmp/skills/user-context/plugin-author-config/source-category-config.json \
     plugins/financial-markets-fmp/skills/public-equity-investing/internal-support/fmp-provider-guide \
     plugins/financial-markets-fmp/shared/equity-research-support-standard.md \
     plugins/financial-markets-fmp/shared/workflow-source-resolution.md \
     plugins/financial-markets-fmp/skills/financials-normalizer/references/source-protocol.md \
     plugins/financial-markets-fmp/skills/financials-normalizer/references/normalization-schema.md \
     plugins/financial-markets-fmp/tests/test_unsupported_connector_promises.py \
  -o patches/financial-markets-fmp-overlay
```

Review the generated patches before relying on them. If they contain broad, unrelated Markdown rewrites from upstream, split or shrink them.

## Tests as guardrails

Run at least:

```bash
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
python3 -m json.tool plugins/financial-markets-fmp/.codex-plugin/plugin.json >/dev/null
python3 -m json.tool plugins/financial-markets-fmp/.app.json >/dev/null
python3 -m unittest plugins/financial-markets-fmp/tests/test_unsupported_connector_promises.py
python3 -m unittest discover -s plugins/financial-markets-fmp/tests -p 'test_*.py'
git diff --check
```

If plugin metadata changed, update the Codex cachebuster before local reinstall:

```bash
python3 /Users/fcamisa/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py \
  plugins/financial-markets-fmp
```

The tests are intentionally not the whole truth. They catch high-risk regressions such as overclaiming providers, losing FMP-first routing, breaking metadata, or letting legacy paid-provider defaults creep back in.

## Semantic review pass

After tests pass, inspect the Markdown as executable-ish prose. Look for clean text that is semantically wrong.

Review these areas:

- README integration table and fork notice.
- `.codex-plugin/plugin.json` identity, author/developer, description, display name, and brand color.
- `.app.json` optional connectors and absence of legacy paid-provider placeholders.
- `skills/user-context/plugin-author-config/source-category-config.json`.
- FMP provider guide:
  - `INTERNAL.md`
  - `references/connector-playbook.md`
  - `references/workbook-mode.md`
- Financials normalizer source protocol and normalization schema.
- Shared equity research support standard and workflow source-resolution docs.
- Any upstream-new skill that mentions providers, connectors, source hierarchy, estimates, transcripts, filings, or market data.

For each reviewed area, ask:

- Does it still say FMP is the default structured public-market route?
- Does it avoid implying FMP replaces private markets, expert networks, brokerage systems, or internal repositories?
- Does it distinguish primary evidence from FMP-standardized structured data?
- Does it preserve currency/listing/fiscal-period/source timestamp caveats?
- Does it request missing sources instead of hallucinating unavailable provider access?
- Does it preserve useful upstream improvements that do not conflict with the fork?

## Canonical smoke prompts

Use a new Codex thread with the refreshed plugin installed and try a small representative set:

1. `@Financial Markets (FMP-first fork) Help me get started`
2. `Build a public-equity tearsheet for AAPL using FMP where appropriate and label source limits.`
3. `Normalize the latest annual financials for SAP.DE and preserve native currency/listing caveats.`
4. `Build an earnings preview for RKLB and distinguish consensus estimates from assumptions.`
5. `Explain what FMP cannot replace for a private-company diligence workflow.`

The expected behavior is not that every answer is complete. The expected behavior is honest routing, source labeling, graceful downgrade when data is missing, and no claims of unavailable vendor access.

## Handoff report template

Use this shape when reporting a completed refresh:

```md
Refreshed `financial-markets-fmp` from upstream `<source/ref/date>`.

Preserved:
- FMP-first structured public-market routing.
- Fork identity and local-only marketplace posture.
- Optional-only posture for private-market, expert-network, brokerage, internal-doc, and specialist vendor sources.
- Evidence labeling and currency/listing/fiscal-period caveats.

Upstream changes preserved:
- ...

Conflicts resolved:
- ...

Could not preserve / needs human review:
- ...

Validation:
- JSON checks: ...
- Focused FMP tests: ...
- Full plugin tests: ...
- `git diff --check`: ...
- Semantic review: ...
```
