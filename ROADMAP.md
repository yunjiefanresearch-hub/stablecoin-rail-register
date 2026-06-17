# Roadmap

**Cadence commitment:** quarterly `diff` releases, plus ad-hoc patch releases for major
regulatory events. Each release is tagged (semver) and archived to Zenodo with a DOI.

| Version | Scope | Status |
|--------|-------|--------|
| v0.1.0 | Initial scaffold: schema + methodology + build pipeline + corridor layer (1 worked example); spine dimension (`permitted_activity_yield`) seeded for HK and US §404. | superseded |
| v0.2.0 | Dimension framework expanded 10 → 15 (two doctrinal spines); six focus jurisdictions loaded as 30 sourced, schema-valid records; archived to Zenodo for a citable DOI. | released |
| **v0.3.0** | **Depth + interfaces.** Hong Kong, Singapore and the UK deepened to 11 dimensions each — **51 records, 14/15 dimensions** (only `disclosure_reporting` empty across the focus set). **MCP server** shipped (typed query tools over the dataset). Sortable, multi-filter **table view** on the landing page. Brazil and Taiwan added as forthcoming windows. | **current** |
| v0.3.x | **Brazil → full jurisdiction** (the HK→BR USD-settlement corridor anchors it); complete the primary-source verification pass (clause-level URLs) on the Hong Kong anchor cells. | in progress |
| v0.4.0 | **Taiwan** added as an infrastructure jurisdiction; semantic search + a jurisdiction comparison / query API over the MCP layer. | planned |
| later | Broaden instrument coverage; additional jurisdictions once primary-source substrate exists — depth before breadth, always. | planned |

Scope discipline: **depth before breadth.** The differentiator is rigorous, sourced,
corridor-aware coverage of a focused set — not 200 shallow jurisdictions. Planned cells are
visible in `COVERAGE.md` (⬜vX.Y) on purpose: this is an actively-built standard, not a finished table.
