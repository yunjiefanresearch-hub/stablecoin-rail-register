#!/usr/bin/env python3
"""
Cross-Border Stablecoin Register — MCP server.

Exposes the register as typed query tools over the Model Context Protocol so that
agents can query the cross-jurisdictional differential layer directly, instead of
fetching and parsing the raw JSON. Reads the committed dataset.json (no network).

Run (stdio transport, for Claude Desktop / MCP clients):
    pip install "mcp[cli]"
    python mcp_server.py

Or register in an MCP client config (see MCP_SERVER.md).

Every record returned carries its source.primary, pinpoint, confidence, dates and
version — the same provenance fields a human sees. No data is synthesised here;
the server only filters and reshapes the published dataset.
"""
from __future__ import annotations
import json
import pathlib
from typing import Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "The 'mcp' package is required. Install it with:  pip install \"mcp[cli]\""
    ) from e

ROOT = pathlib.Path(__file__).resolve().parent
DATA = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
RECORDS: list[dict] = DATA.get("records", [])
CORRIDORS: list[dict] = DATA.get("corridors", [])

# 15-dimension spec (key -> human description). Mirrors the schema / taxonomy.md.
DIMENSIONS: dict[str, str] = {
    "regulatory_authority": "Authority and statutory basis",
    "issuer_pathway": "Issuer eligibility / licensing pathway (constraint C1)",
    "reserve_backing": "Reserve composition and backing (constraint C2)",
    "capital_requirements": "Issuer capital requirements (constraint C2)",
    "permitted_activity_yield": "Permitted-activity / yield boundary — SPINE 1 (constraint C3)",
    "securities_classification": "Securities classification boundary — SPINE 2 (constraint C4)",
    "bank_nonbank_routing": "Bank / non-bank status and routing prohibitions (constraint C5)",
    "redemption": "Redemption mechanics",
    "custody": "Custody of client assets / reserves (constraint C2 facet)",
    "aml_kyc": "AML / KYC framework",
    "cross_border_data": "Cross-border payment and data sovereignty (constraint C6)",
    "monetary_sovereignty": "Monetary sovereignty / non-domestic-currency caps (constraint C7)",
    "disclosure_reporting": "Disclosure, reporting, supervisory coordination (constraint C8)",
    "distribution": "Distribution and offering restrictions",
    "implementation_status": "Implementation maturity and timeline",
}
JURISDICTIONS: dict[str, str] = {
    "US": "United States", "HK": "Hong Kong", "EU": "European Union",
    "UK": "United Kingdom", "SG": "Singapore", "CN": "Mainland China",
    "BR": "Brazil", "TW": "Taiwan",
}

mcp = FastMCP("cross-border-stablecoin-register")


def _summary(r: dict) -> dict:
    """A compact, provenance-bearing view of a record (use get_record for the full object)."""
    src = r.get("source", {}) or {}
    return {
        "id": r.get("id"),
        "jurisdiction": r.get("jurisdiction"),
        "dimension": r.get("dimension"),
        "constraint_ref": r.get("constraint_ref"),
        "requirement_summary": r.get("requirement_summary"),
        "source": {"primary": src.get("primary"), "pinpoint": src.get("pinpoint"), "url": src.get("url") or None},
        "status": r.get("status"),
        "effective_date": r.get("effective_date"),
        "confidence": r.get("confidence"),
        "last_reviewed": r.get("last_reviewed"),
        "version_added": r.get("version_added"),
    }


@mcp.tool()
def about() -> dict:
    """Register metadata: name, version, record count, license, DOI, and the verification rule."""
    return {
        "name": DATA.get("name"),
        "version": DATA.get("version"),
        "generated": DATA.get("generated"),
        "record_count": DATA.get("record_count"),
        "corridor_count": len(CORRIDORS),
        "doi": "10.5281/zenodo.20730359",
        "license": {"data": "CC-BY-4.0", "code": "Apache-2.0"},
        "spines": ["permitted_activity_yield", "securities_classification"],
        "verification_rule": (
            "A record is verified only when it has no open markers AND a human has checked "
            "every source.primary and pinpoint against the instrument itself. Citations are "
            "never machine-generated. Some records are transcribed from the maintainer's "
            "Compliance Matrix and pending final primary-source verification (source.url empty)."
        ),
    }


@mcp.tool()
def list_jurisdictions() -> list[dict]:
    """List jurisdictions covered, with full name and record count."""
    counts: dict[str, int] = {}
    for r in RECORDS:
        counts[r["jurisdiction"]] = counts.get(r["jurisdiction"], 0) + 1
    return [
        {"code": code, "name": JURISDICTIONS.get(code, code), "records": counts.get(code, 0)}
        for code in sorted(counts, key=lambda c: -counts[c])
    ]


@mcp.tool()
def list_dimensions() -> list[dict]:
    """List the 15 dimensions with descriptions and how many records each has."""
    counts: dict[str, int] = {}
    for r in RECORDS:
        counts[r["dimension"]] = counts.get(r["dimension"], 0) + 1
    return [
        {"key": k, "description": v, "records": counts.get(k, 0),
         "spine": k in ("permitted_activity_yield", "securities_classification")}
        for k, v in DIMENSIONS.items()
    ]


@mcp.tool()
def get_record(record_id: str) -> dict:
    """Return the full record (all fields including requirement_structured and interpretation_note) by its id."""
    for r in RECORDS:
        if r.get("id") == record_id:
            return r
    return {"error": f"No record with id '{record_id}'.",
            "hint": "Use query() or search() to find record ids."}


@mcp.tool()
def query(
    jurisdiction: Optional[str] = None,
    dimension: Optional[str] = None,
    status: Optional[str] = None,
    confidence: Optional[str] = None,
    constraint_ref: Optional[str] = None,
) -> dict:
    """
    Typed filter over the register. All arguments optional and combined with AND.

    Args:
        jurisdiction: e.g. 'US', 'HK', 'EU', 'UK', 'SG', 'CN'.
        dimension: one of the 15 dimension keys (see list_dimensions).
        status: 'in_force' | 'transitional' | 'proposed' | 'consultation'.
        confidence: 'high' | 'medium' | 'low'.
        constraint_ref: e.g. 'C1'..'C8' (or composite like 'C3xC4').
    Returns a count and the matching record summaries.
    """
    j = jurisdiction.upper() if jurisdiction else None
    out = []
    for r in RECORDS:
        if j and r.get("jurisdiction") != j:
            continue
        if dimension and r.get("dimension") != dimension:
            continue
        if status and r.get("status") != status:
            continue
        if confidence and r.get("confidence") != confidence:
            continue
        if constraint_ref and (r.get("constraint_ref") or "") != constraint_ref:
            continue
        out.append(_summary(r))
    return {"count": len(out), "filters": {
        "jurisdiction": j, "dimension": dimension, "status": status,
        "confidence": confidence, "constraint_ref": constraint_ref}, "records": out}


@mcp.tool()
def compare_dimension(dimension: str) -> dict:
    """
    Compare all jurisdictions on a single dimension — the core differential view.
    e.g. compare_dimension('monetary_sovereignty') returns the EU cap vs HK restriction
    vs CN prohibition spectrum, each with its source.
    """
    if dimension not in DIMENSIONS:
        return {"error": f"Unknown dimension '{dimension}'.",
                "valid_dimensions": list(DIMENSIONS.keys())}
    rows = [_summary(r) for r in RECORDS if r.get("dimension") == dimension]
    rows.sort(key=lambda x: x["jurisdiction"])
    return {"dimension": dimension, "description": DIMENSIONS[dimension],
            "jurisdiction_count": len(rows), "records": rows}


@mcp.tool()
def jurisdiction_profile(jurisdiction: str) -> dict:
    """Return all records for one jurisdiction, ordered by the dimension framework."""
    j = jurisdiction.upper()
    if j not in JURISDICTIONS:
        return {"error": f"Unknown jurisdiction '{jurisdiction}'.",
                "valid_jurisdictions": list(JURISDICTIONS.keys())}
    dim_order = list(DIMENSIONS.keys())
    rows = [r for r in RECORDS if r.get("jurisdiction") == j]
    rows.sort(key=lambda r: dim_order.index(r["dimension"]) if r["dimension"] in dim_order else 99)
    return {"jurisdiction": j, "name": JURISDICTIONS[j],
            "record_count": len(rows), "records": [_summary(r) for r in rows]}


@mcp.tool()
def search(keyword: str) -> dict:
    """Keyword search across jurisdiction, dimension, authority, requirement summary, source, and tags."""
    term = (keyword or "").strip().lower()
    if not term:
        return {"error": "Empty keyword."}
    out = []
    for r in RECORDS:
        hay = " ".join([
            r.get("jurisdiction", ""), r.get("dimension", ""), r.get("authority", ""),
            r.get("requirement_summary", ""), r.get("instrument_label_local", ""),
            (r.get("source", {}) or {}).get("primary", ""),
            (r.get("source", {}) or {}).get("pinpoint", ""),
            " ".join(r.get("tags", []) or []), r.get("constraint_ref", "") or "",
        ]).lower()
        if term in hay:
            out.append(_summary(r))
    return {"keyword": keyword, "count": len(out), "records": out}


@mcp.tool()
def get_corridor(corridor_id: Optional[str] = None) -> dict:
    """
    Return corridor model(s) — what clears and what breaks at each regulatory boundary
    along a cross-border flow. Omit corridor_id to list all corridors.
    """
    if corridor_id is None:
        return {"count": len(CORRIDORS),
                "corridors": [{"corridor_id": c.get("corridor_id"), "name": c.get("name")} for c in CORRIDORS]}
    for c in CORRIDORS:
        if c.get("corridor_id") == corridor_id:
            return c
    return {"error": f"No corridor with id '{corridor_id}'.",
            "available": [c.get("corridor_id") for c in CORRIDORS]}


@mcp.tool()
def coverage() -> dict:
    """
    Coverage matrix: for each jurisdiction × dimension, whether a record exists ('verified')
    or not ('planned'). Useful for an agent to know where data is and is not available.
    """
    present = {(r["jurisdiction"], r["dimension"]) for r in RECORDS}
    jur = sorted({r["jurisdiction"] for r in RECORDS})
    grid = {}
    for jcode in jur:
        grid[jcode] = {dim: ("verified" if (jcode, dim) in present else "planned")
                       for dim in DIMENSIONS}
    return {"jurisdictions": jur, "dimensions": list(DIMENSIONS.keys()),
            "verified_cells": len(present), "grid": grid}


if __name__ == "__main__":
    mcp.run()
