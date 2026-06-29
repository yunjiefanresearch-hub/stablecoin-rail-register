# MCP server

`mcp_server.py` exposes the register as **typed query tools** over the [Model Context
Protocol](https://modelcontextprotocol.io), so an agent can query the cross-jurisdictional
differential layer directly instead of fetching and parsing `dataset.json`. The server reads the
committed `dataset.json` and makes **no network calls**; it only filters and reshapes published
records (no data is synthesised at query time).

## Install

```bash
pip install "mcp[cli]"
```

The server needs the `mcp` package available to whichever Python runs it. If you use a virtual
environment, install it there and point the client at that environment's interpreter.

## Run

```bash
python mcp_server.py          # stdio transport — what MCP clients speak
```

Test interactively with the MCP Inspector:

```bash
mcp dev mcp_server.py
```

## Register with Claude Desktop

Easiest — let the CLI write the config for you:

```bash
mcp install mcp_server.py --name "Cross-Border Stablecoin Register"
```

Or add it manually to `claude_desktop_config.json`
(macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`):

```json
{
  "mcpServers": {
    "cross-border-stablecoin-register": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/stablecoin-rail-register/mcp_server.py"]
    }
  }
}
```

Use an absolute path, and if you installed `mcp` into a venv, set `"command"` to that venv's
`python` (e.g. `/path/.venv/bin/python`). Restart the client after editing the config.

## Tools

| Tool | Purpose |
|---|---|
| `about()` | Register metadata: version, record count, DOI, license, verification rule |
| `list_jurisdictions()` | Jurisdictions covered + record counts |
| `list_dimensions()` | The 15 dimensions, descriptions, spine flag, record counts |
| `get_record(record_id)` | Full record (all fields incl. `requirement_structured`, `interpretation_note`) |
| `query(jurisdiction?, dimension?, status?, confidence?, constraint_ref?)` | Typed filter, AND-combined; returns provenance-bearing summaries |
| `compare_dimension(dimension)` | All jurisdictions on one dimension — the core differential view |
| `jurisdiction_profile(jurisdiction)` | All records for one jurisdiction, ordered by the framework |
| `search(keyword)` | Keyword search across summary, source, authority, tags |
| `get_corridor(corridor_id?)` | Corridor model(s): what clears / breaks at each boundary |
| `coverage()` | Jurisdiction × dimension grid: where data exists vs. is planned |
| `citable_law(jurisdiction?, dimension?)` | **Lawyer-citable subset.** Only records that are a proposition of law (`claim_class=tier1_legal`), in force (`status=in_force`), AND confirmed against the official text (`evidence_tier=resolution_text`); each row returns the binding instrument, pinpoint, and official URL. Optional jurisdiction/dimension filters. The "show me only what I could cite" view |
| `compatibility(jurisdiction?, other?, category?)` | **Analysis layer.** The §5.14 pairwise compatibility matrix (66 pairs); filter by jurisdiction, a specific pair, or category (I / I/II / II / III) |
| `interaction_sets()` | **Analysis layer.** The six constraint-interaction sets (§2.9, A–F): constraint pair, mechanism, worked example |
| `architectural_patterns()` | **Analysis layer.** The PRC three-pattern typology (§3.3), the three-layer routing architecture (§4/§6), the §4.4 five-factor test, the six design principles |
| `open_questions()` | **Analysis layer.** The four open regulatory questions (§7) with conditional-status flags |
| `compose_corridor(origin, destination, as_of?)` | **Computed layer.** COMPUTES a directed corridor's feasibility from the signal table + Atlas algorithm (not a lookup); returns class, rule fired, interaction sets, and the computed-vs-authored comparison. Pass `as_of` (ISO date) to evaluate as of that date — every scheduled change in law effective by then is applied first (returns the as-of class, the base class, and whether it changed) |
| `explain_feasibility(origin, destination)` | **Computed layer.** Explains WHY a corridor falls in its class: rule fired, each side's justifying node-record basis, and computed-vs-authored agreement |
| `corridor_timeline(origin, destination)` | **Time engine.** The dated future of a directed edge: today's class, the scheduled transitions that change it (with effective dates), and contingent "if enacted" branches. Answers "Category T today, Category I after the regime is operative" |
| `event_calendar(jurisdiction?)` | **Time engine.** The dated/contingent `tier1_legal` changes in law that move a jurisdiction's compose() signal (scheduled / contingent / in_force), with event provenance. A market launch is never an event |
| `constraint_substrate(jurisdiction?, constraint?)` | **Constraint substrate.** Each `(jurisdiction × constraint C1–C8)` as a structured pole citing the `tier1_legal` record it is transcribed from, plus coverage. Poles exist only where a record backs them |
| `compose_via_substrate(origin, destination)` | **Constraint substrate.** DERIVES a corridor's class by composing two jurisdictions' C1–C8 poles through the interaction-set rules (not the inbound-gate shortcut); returns per-set verdicts and the cross-check vs the signal compose(), or `indeterminate` with the missing poles |
| `verification_report()` | **Verification queue.** Records bucketed by `evidence_tier`, the largest backlog (legacy `unset`), and records lacking a `source.url` |
| `verification_worklist(jurisdiction?)` | **Verification harness.** Per-cell gap analysis for the primary-source pass: for each unverified cell, the instrument + pinpoint and exactly what is missing to reach each tier. `evidence_tier` is enforced by the build (earned, not asserted). Verification is external work, never fabricated — this scopes it |

**23 tools.** Every returned record summary carries `source.primary`, `pinpoint`, `claim_class`,
`evidence_tier`, `confidence`, dates and `version_added` — the two evidence axes (`claim_class` = kind
of claim; `evidence_tier` = provenance strength) let an agent separate *binding law* from
*well-sourced market fact*. The lawyer-citable subset (`tier1_legal` + `in_force` + `resolution_text`)
is available via `citable_law()` and as `citable_subset` in `dataset.json`. Per the methodology, some
records are transcribed from the maintainer's Compliance Matrix and are pending final primary-source
verification (`source.url` empty); treat `confidence` and `interpretation_note` accordingly.
