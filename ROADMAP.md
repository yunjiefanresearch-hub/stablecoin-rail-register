# Roadmap

**Cadence commitment:** quarterly `diff` releases, plus ad-hoc patch releases for major
regulatory events. Each release is tagged (semver) and archived to Zenodo with a DOI.

| Version | Scope | Status |
|--------|-------|--------|
| v0.1.0 | Initial scaffold: schema + methodology + working build pipeline + corridor layer (1 worked example); spine dimension (`permitted_activity_yield`) seeded for HK and US §404. | superseded by 0.2.0 |
| **v0.2.0** | **Dimension framework expanded 10 → 15** (split reserve/capital; added `securities_classification`, `bank_nonbank_routing`, `monetary_sovereignty`, `disclosure_reporting`), giving two doctrinal spines. **Six focus jurisdictions loaded** — US, HK, EU, UK, SG, CN — as **30 sourced, schema-valid records** (HK near-complete). Jurisdiction set reoriented (BR → corridor-only, TW parked). | **current** |
| v0.3.0 | Fill remaining cells on the focus set: `custody` across jurisdictions; dedicated `disclosure_reporting` cells (EU/US); `securities_classification` applied comparatively beyond the US. Add a **second corridor** built from focus jurisdictions (e.g. HK↔EU or US↔SG). | planned |
| v0.4.0 | **MCP server** (agent-queryable register); richer `requirement_structured` facets per dimension. | planned |
| v0.x | Backfill BR / TW once primary-source substrate exists; broaden instrument coverage. | planned |

Scope discipline: **depth before breadth.** The differentiator is rigorous, sourced,
corridor-aware coverage of a focused set — not 200 shallow jurisdictions. Planned cells are
visible in `COVERAGE.md` (⬜vX.Y) on purpose: this is an actively-built standard, not a finished table.
