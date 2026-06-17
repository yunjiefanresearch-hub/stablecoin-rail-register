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

Every returned record carries `source.primary`, `pinpoint`, `confidence`, dates and `version_added`
— the same provenance a human sees. Per the methodology, some records are transcribed from the
maintainer's Compliance Matrix and are pending final primary-source verification (`source.url`
empty); treat `confidence` and `interpretation_note` accordingly.
