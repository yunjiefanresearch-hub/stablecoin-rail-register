#!/usr/bin/env python3
"""run_invariants.py — the CBSR structural invariant suite (shipped, reproducible).

These are read-only assertions over the built register (dataset.json, the record YAMLs, and the
analysis/*.json computed layers). They are the standing properties the build is supposed to preserve;
unlike build.py's internal gates (which fail the build), this prints an explicit, countable pass/fail
report so "N invariants hold" is a concrete, runnable claim rather than a number in prose.

Run from the register root AFTER a build:
    python build.py && python run_invariants.py
Exit code 0 iff every invariant holds.
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O passes encoding="utf-8" explicitly throughout.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json, glob, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECT_VERSION = "0.9.7"

def load_json(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))

# --- load the built register -------------------------------------------------------------------
ds = load_json("dataset.json")
records = [r for r in ds.get("records", []) if isinstance(r, dict) and "id" in r]
byid = {r["id"]: r for r in records}
an = ds.get("analysis", {})
ledger = load_json("analysis/verification_ledger.json")
comp = load_json("analysis/computed_compatibility.json")
timeline = load_json("analysis/computed_timeline.json")
substrate = load_json("analysis/computed_substrate.json")
skeletons = load_json("analysis/computed_corridor_skeletons.json")

BLOCKED = {"prohibition", "no_regime", "pending_proposal", "made_not_commenced", "finalized_policy_pending"}
BINDING_ENUM = {"in_force_enacted", "made_not_commenced", "finalized_policy_pending",
                "pending_proposal", "prohibition", "no_regime"}
TIER_ENUM = {"resolution_text", "mixed", "firm_summary", "unset"}

results = []
def inv(name, cond, detail=""):
    results.append((bool(cond), name, "" if cond else detail))

def src(r):
    return r.get("source") or {}

# === STRUCTURE & AXES ==========================================================================
inv("S1  dataset has 152 records", len(records) == 152, f"got {len(records)}")
inv("S2  every record carries a valid binding_status",
    all(r.get("binding_status") in BINDING_ENUM for r in records),
    str([r["id"] for r in records if r.get("binding_status") not in BINDING_ENUM][:5]))
cc = {}
for r in records: cc[r.get("claim_class")] = cc.get(r.get("claim_class"), 0) + 1
inv("S3  claim_class split is 143 tier1_legal / 9 tier2_operational",
    cc.get("tier1_legal") == 143 and cc.get("tier2_operational") == 9, str(cc))
inv("S4  every record has a valid evidence_tier",
    all((r.get("evidence_tier") or "unset") in TIER_ENUM for r in records))

# === CITABILITY DISCIPLINE =====================================================================
rt = [r for r in records if r.get("evidence_tier") == "resolution_text"]
inv("C1  every resolution_text cell is binding_status=in_force_enacted (the cap)",
    all(r.get("binding_status") == "in_force_enacted" for r in rt),
    str([r["id"] for r in rt if r.get("binding_status") != "in_force_enacted"][:5]))
inv("C2  no blocked-binding cell is resolution_text",
    all(r.get("binding_status") not in BLOCKED for r in rt))
inv("C3  every resolution_text cell has url + pinpoint + last_reviewed",
    all(src(r).get("url") and src(r).get("pinpoint") and r.get("last_reviewed") for r in rt),
    str([r["id"] for r in rt if not (src(r).get("url") and src(r).get("pinpoint") and r.get("last_reviewed"))][:5]))
fs = [r for r in records if r.get("evidence_tier") == "firm_summary"]
inv("C4  every firm_summary cell has source.pinpoint",
    all(src(r).get("pinpoint") for r in fs),
    str([r["id"] for r in fs if not src(r).get("pinpoint")][:5]))
citable = [r for r in records if r.get("claim_class") == "tier1_legal"
           and r.get("status") == "in_force" and r.get("evidence_tier") == "resolution_text"]
inv("C5  citable subset == 46", len(citable) == 46, f"got {len(citable)}")
inv("C6  dataset.citable_subset.count agrees with the recomputed set",
    ds.get("citable_subset", {}).get("count") == len(citable),
    f"dataset={ds.get('citable_subset',{}).get('count')} recomputed={len(citable)}")

# === VERIFICATION LEDGER =======================================================================
inv("L1  ledger schema + version", ledger.get("schema") == "cbsr/verification_ledger"
    and ledger.get("version") == f"v{EXPECT_VERSION}", f"version={ledger.get('version')}")
led_entries = ledger.get("entries", [])
drift = [e for e in led_entries if e.get("id") in byid
         and e.get("binding_status") and byid[e["id"]].get("binding_status") != e["binding_status"]]
inv("L2  no ledger drift (every committed binding_status matches the live record)", not drift,
    str([(e["id"], e.get("binding_status"), byid[e["id"]].get("binding_status")) for e in drift][:5]))

# === ANALYSIS / COMPUTED LAYERS ================================================================
inv("A1  analysis layer present (66 pairs, 6 interaction sets, 5 open questions)",
    len(an.get("compatibility", {}).get("pairs", [])) == 66
    and len(an.get("interaction_sets", {}).get("sets", [])) == 6
    and len(an.get("open_questions", {}).get("questions", [])) == 5,
    f"pairs={len(an.get('compatibility',{}).get('pairs',[]))} "
    f"sets={len(an.get('interaction_sets',{}).get('sets',[]))} "
    f"oq={len(an.get('open_questions',{}).get('questions',[]))}")
inv("A2  substrate 80/96 cells, cross-check clean",
    substrate.get("coverage", {}).get("cells_populated") == 80 and substrate.get("cross_check", {}).get("clean") is True,
    str(substrate.get("coverage", {}).get("cells_populated")))
inv("A3  edge layer 124/132 with a record, cross-check clean",
    skeletons.get("coverage", {}).get("edges_with_a_record") == 124
    and skeletons.get("cross_check", {}).get("clean") is True,
    str(skeletons.get("coverage", {})))
prc = comp.get("pre_regime_crosscheck", {})
inv("A4  pre_regime cross-check stays {KR,TW}, consistent",
    prc.get("consistent") is True
    and sorted(prc.get("from_signals", [])) == ["KR", "TW"]
    and sorted(prc.get("from_records", [])) == ["KR", "TW"],
    f"signals={prc.get('from_signals')} records={prc.get('from_records')} consistent={prc.get('consistent')}")

# === TIME ENGINE ===============================================================================
events = an.get("event_calendar", {}).get("events", [])
inv("T1  event calendar has 6 events, provenance clean",
    len(events) == 6 and timeline.get("event_provenance", {}).get("clean") is True, f"events={len(events)}")
inv("T2  every event is tier1_legal; contingent events carry no effective_date",
    all(e.get("claim_class") == "tier1_legal" for e in events)
    and all(not e.get("effective_date") for e in events if e.get("status") == "contingent"))
ot = timeline.get("undirected_agreement_over_time", [])
inv("T3  UK transition caveat: 8 today -> 0 at the 2027-10-25 horizon",
    ot and ot[0]["transition_caveated_pairs"]["count"] == 8
    and ot[-1]["transition_caveated_pairs"]["count"] == 0 and ot[-1]["as_of"] == "2027-10-25",
    f"first={ot[0]['transition_caveated_pairs']['count'] if ot else '?'} "
    f"last={ot[-1]['transition_caveated_pairs']['count'] if ot else '?'}@{ot[-1]['as_of'] if ot else '?'}")
dated = {e["effective_date"] for e in events if e.get("effective_date")}
horizons = {x["as_of"] for x in ot}
inv("T4  compose horizons are exactly the dated events (no contingent date leaked in)",
    horizons <= (dated | {ot[0]["as_of"]}) and all(h in dated or h == ot[0]["as_of"] for h in horizons),
    f"horizons={sorted(horizons)} dated={sorted(dated)}")

# === v0.9.7 NATIVE-LANGUAGE PASS ===============================================================
br_rt = [i for i in byid if i.startswith("br-vasp-") and byid[i].get("evidence_tier") == "resolution_text"]
inv("N1  BR: exactly 10 resolution_text cells, each with url+pinpoint",
    len(br_rt) == 10 and all(src(byid[i]).get("url") and src(byid[i]).get("pinpoint") for i in br_rt),
    f"count={len(br_rt)}")
bry = byid.get("br-vasp-permitted_activity_yield-001", {})
inv("N2  BR yield: in_force_enacted + firm_summary + pass-through unsettled noted",
    bry.get("binding_status") == "in_force_enacted" and bry.get("evidence_tier") == "firm_summary"
    and "pass-through" in (bry.get("interpretation_note") or "").lower())
cn4 = ["cn-prc-monetary_sovereignty-001", "cn-prc-issuer_pathway-001",
       "cn-prc-regulatory_authority-001", "cn-prc-securities_classification-001"]
inv("N3  CN: the 4 directly-addressed cells all cite 银发〔2026〕42号",
    all("银发〔2026〕42号" in json.dumps(byid.get(i, {}), ensure_ascii=False) for i in cn4))
cn_all = [i for i in byid if i.startswith("cn-prc-")]
inv("N4  CN: no cell summary contains 'verbal' or 'remain in force'",
    all("verbal" not in (byid[i].get("requirement_summary") or "")
        and "remain in force" not in (byid[i].get("requirement_summary") or "") for i in cn_all),
    str([i for i in cn_all if "verbal" in (byid[i].get("requirement_summary") or "")][:5]))
inv("N5  CN: every prohibition-binding cell stays prohibition (no re-classification)",
    all(byid[i].get("binding_status") == "prohibition" for i in cn4))
inv("N6  CN C7 carries the written RMB-pegged-stablecoin overseas-issuance ban quote",
    "不得在境外发行挂钩人民币的稳定币" in json.dumps(byid.get("cn-prc-monetary_sovereignty-001", {}), ensure_ascii=False))
krs = byid.get("kr-frs-implementation_status-001", {}).get("requirement_summary", "")
inv("N7  KR: '12 May'/'off the subcommittee' removed; 51% dispute added; DABA cells stay pending_proposal",
    "12 May" not in krs and "off the subcommittee" not in krs
    and ("51%" in krs or "issuer-eligibility" in krs)
    and byid.get("kr-frs-issuer_pathway-001", {}).get("binding_status") == "pending_proposal")
twa = byid.get("tw-frs-aml_kyc-001", {})
inv("N8  TW: aml_kyc resolution_text on the MOJ text; issuer_pathway stays pending_proposal",
    twa.get("evidence_tier") == "resolution_text" and "law.moj.gov.tw" in (src(twa).get("url") or "")
    and byid.get("tw-frs-issuer_pathway-001", {}).get("binding_status") == "pending_proposal")
evd = {e["id"]: e for e in events}
inv("N9  KR/TW contingent events note their differing procedural stages",
    "51%" in (evd.get("kr-daba-enacted", {}).get("date_basis") or "")
    and "初審" in (evd.get("tw-vas-act-enacted", {}).get("date_basis") or ""))

# === PORTABILITY (the v0.9.7 engineering fix) ==================================================
py_files = sorted(glob.glob(str(ROOT / "*.py")) + glob.glob(str(ROOT / "scripts" / "*.py")))
def io_calls_have_encoding(text):
    for m in re.finditer(r"\.(read_text|write_text)\(", text):
        i = m.end() - 1; depth = 0; j = i; n = len(text)
        while j < n:
            c = text[j]
            if c in "\"'":
                q = c
                if text[j:j+3] == q*3:
                    k = text.find(q*3, j+3); j = (k+3) if k != -1 else n; continue
                j += 1
                while j < n:
                    if text[j] == "\\": j += 2; continue
                    if text[j] == q: j += 1; break
                    j += 1
                continue
            if c == "(": depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0: break
            j += 1
        if "encoding=" not in text[m.start():j+1]:
            return False
    return True
all_enc = all(io_calls_have_encoding(Path(f).read_text(encoding="utf-8")) for f in py_files)
inv("P1  every read_text/write_text in the shipped scripts passes encoding=\"utf-8\"", all_enc)
all_recfg = all("force UTF-8 for console output" in Path(f).read_text(encoding="utf-8") for f in py_files)
inv("P2  every shipped script has the guarded UTF-8 stdout/stderr reconfigure", all_recfg)

# === VERSION ===================================================================================
build_src = (ROOT / "build.py").read_text(encoding="utf-8")
inv("V1  REGISTER_VERSION == 0.9.7 in build.py", f'REGISTER_VERSION = "{EXPECT_VERSION}"' in build_src)
inv("V2  dataset.register_version == 0.9.7",
    (ds.get("register_version") or ds.get("version")) == EXPECT_VERSION,
    str(ds.get("register_version") or ds.get("version")))

# === report ====================================================================================
passed = sum(1 for ok, _, _ in results if ok)
total = len(results)
print("CBSR invariant suite — v%s\n" % EXPECT_VERSION + "=" * 60)
for ok, name, detail in results:
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   -> " + detail) if detail else ""))
print("=" * 60)
print("RESULT: %d/%d invariants hold." % (passed, total)
      + ("" if passed == total else "  (%d FAILED)" % (total - passed)))
_sys.exit(0 if passed == total else 1)
