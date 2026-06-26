# Financial Markets FMP-first fork

This is a local FMP-first fork of OpenAI’s Financial Markets plugin. It is not the official OpenAI distribution.

## Upstream source

- Upstream repository: <https://github.com/openai/role-specific-plugins>
- Upstream plugin path: `plugins/financial-markets`

## Fork point

- Fork date: June 26, 2026
- Base plugin id: `financial-markets`
- Base plugin version: `0.1.27`
- Local fork id: `financial-markets-fmp`
- Local display name: `Financial Markets (FMP-first fork)`

## Local changes

- Financial Modeling Prep is the default structured public-market data provider through the configured `financial_modeling_prep` MCP server.
- FMP is preferred for public-company profiles, quotes, price history, statements, estimates, calendars, earnings transcripts, SEC filing discovery, 13F ownership, insider activity, ETF/index context, supported macro series, and supported news/release context.
- Paid or specialist providers are no longer advertised as default required integrations.
- Optional document, collaboration, private-market, expert-network, brokerage, and specialist data sources remain explicitly optional and are used only when provided or callable.
- Local MCP setup reads the FMP API key from macOS Keychain through `scripts/start-fmp-mcp.sh`.
- The plugin metadata, marketplace entry, README, brand color, and composer icon identify this as an FMP-first fork rather than the official OpenAI plugin.

See `docs/financial-markets-fmp-migration-plan.md` for the completed migration record and validation history. See `docs/financial-markets-fmp-migration-playbook.md` for the reusable refresh workflow: instructions as migration compass, patches as acceleration, tests as guardrails, and one semantic review pass as the final sanity check.

## Rebase or reapply against a newer upstream

Keep a clean upstream copy or branch available, then replay this fork as a focused overlay instead of rediscovering the migration. Do not blindly apply a full-tree patch as proof of correctness; the plugin is Markdown-heavy, so patch replay must be followed by tests and a semantic review pass.

```bash
git remote add upstream https://github.com/openai/role-specific-plugins.git
git fetch upstream

git format-patch upstream/main..HEAD \
  -- plugins/financial-markets-fmp \
     docs/financial-markets-fmp-migration-plan.md \
     docs/financial-markets-fmp-migration-playbook.md \
     scripts/start-fmp-mcp.sh \
     .codex/config.example.toml \
     .agents/plugins/marketplace.json \
     .gitignore \
  -o patches/financial-markets-fmp-overlay
```

To apply the fork to a newer upstream snapshot:

```bash
git checkout -b codex/financial-markets-fmp-first-refresh upstream/main
mv plugins/financial-markets-fmp plugins/financial-markets-fmp.previous-refresh 2>/dev/null || true
cp -R plugins/financial-markets plugins/financial-markets-fmp
git am --3way patches/financial-markets-fmp-overlay/*.patch
python3 -m unittest discover -s plugins/financial-markets-fmp/tests -p 'test_*.py'
```

If `git am --3way` reports conflicts, resolve only the conflicted files, continue with `git am --continue`, and rerun the focused FMP/source-routing tests plus full plugin test discovery. Finish with the semantic review checklist in `docs/financial-markets-fmp-migration-playbook.md`.

For local-only use, keep this repository as your personal plugin source and install/enable the plugin from the local marketplace entry. You do not need to publish the fork to any external marketplace.
