# Changelog

All notable changes to the **Cross-Border Stablecoin Register** are recorded here. The register
doubles as a regulatory-diff log: each version states what changed. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning is [SemVer](https://semver.org/).
Each tagged release is archived to Zenodo for a citable DOI.

## [0.3.0] — 2026-06-17
### Added
- **Singapore, the United Kingdom and Mainland China deepened** to 11 / 11 / 9 dimensions
  (from 2 / 3 / 5) — **51 records total, 14 of 15 dimensions populated**. Transcribed from the
  maintainer's Compliance Matrix v0.9.3 (cited as secondary provenance).
- **`custody` dimension** populated for the first time (UK 24-hour custody rule).
- **MCP server** (`mcp_server.py`) — typed query tools over the dataset (`query`,
  `compare_dimension`, `jurisdiction_profile`, `search`, `coverage`, …) for agent access.
  See [`MCP_SERVER.md`](MCP_SERVER.md).
- **Sortable, multi-filter table view** on the landing page, alongside the coverage matrix.
- **Brazil and Taiwan** added as forthcoming jurisdiction *windows* on the landing page and in
  the roadmap (planned cells; no records yet).
- This `CHANGELOG.md`.

### Changed
- **Renamed** from *Stablecoin Rail Register* to **Cross-Border Stablecoin Register** — the name
  foregrounds the cross-jurisdictional differentiator and drops payments-vendor jargon ("rail").
  Updated across `README.md`, `CITATION.cff`, the dataset, the schema, the landing page, and the
  MCP server.
- `README.md` coverage snapshot, `ROADMAP.md`, and `roadmap.yaml` synced to the 51-record state.

### Pending verification
- Clause-level `source.url` is not yet populated. Each record carries its primary instrument and a
  pinpoint, sourced to the Compliance Matrix v0.9.3; **no citation is machine-generated**. Records
  are pending the primary-source verification pass (visiting each instrument to confirm the
  pinpoint and capture the canonical URL). The Hong Kong anchor cells are the first target (v0.3.x).

## [0.2.0] — 2026-06-17
### Added
- Dimension framework expanded **10 → 15**: split `reserve_backing` / `capital_requirements`;
  added `securities_classification`, `bank_nonbank_routing`, `monetary_sovereignty`,
  `disclosure_reporting` — giving two doctrinal spines.
- Six focus jurisdictions loaded as **30 sourced, schema-valid records** (US, HK, EU, UK, SG, CN).
- Dual-license: CC-BY-4.0 (data) + Apache-2.0 (code).
- Archived to Zenodo — **DOI 10.5281/zenodo.20730359**.

### Changed
- Jurisdiction set reoriented to the verified written substrate (Brazil → corridor-only;
  Taiwan parked).

## [0.1.0]
### Added
- Initial scaffold: `record.schema.json`, methodology, build pipeline, controlled vocabulary,
  and a corridor worked example. Spine dimension (`permitted_activity_yield`) seeded for Hong Kong
  and US §404.
