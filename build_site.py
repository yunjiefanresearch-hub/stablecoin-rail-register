#!/usr/bin/env python3
"""Generate index.html (the GitHub Pages landing page) from dataset.json.

The page fetches ./dataset.json live when served (so it stays in sync), and
falls back to an embedded snapshot when opened from file:// for local preview.
Run after build.py:  python3 build_site.py
"""
import json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent
data = json.loads((ROOT / "dataset.json").read_text())

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cross-Border Stablecoin Register — regulatory intelligence infrastructure</title>
<meta name="description" content="An open, versioned, machine-readable register of cross-jurisdictional stablecoin payment-rail regulation. Every fact sourced, dated, versioned, and confidence-rated.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{
  --canvas:#F1F4F7; --panel:#FFFFFF; --ink:#0C1726; --ink-2:#43526B; --ink-3:#76839A;
  --navy:#0A2540; --navy-2:#103253; --accent:#1C4E80; --accent-2:#2E6FB7;
  --verified:#15784E; --verified-bg:#E4F1EA; --verified-line:#9FCDB5;
  --draft:#955600; --draft-bg:#F8EEDC; --draft-line:#E0C58C;
  --planned:#AAB3C0; --planned-bg:#E9ECF1; --planned-line:#D5DAE2;
  --spine:#9A3D1B;
  --rule:#D9DEE6; --rule-2:#C3CAD5;
  --serif:"IBM Plex Serif",Georgia,"Times New Roman",serif;
  --sans:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--canvas);color:var(--ink);font-family:var(--sans);
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
.mono{font-family:var(--mono)}
:focus-visible{outline:2px solid var(--accent-2);outline-offset:2px;border-radius:2px}

/* ---------- masthead ---------- */
.masthead{background:var(--navy);color:#EAF0F7;border-bottom:3px solid #06182B}
.mast-top{display:flex;align-items:baseline;justify-content:space-between;gap:18px;
  padding:18px 0 4px;flex-wrap:wrap}
.brand{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.wordmark{font-family:var(--serif);font-weight:600;font-size:27px;letter-spacing:-.01em;color:#fff;line-height:1}
.reg-tag{font-family:var(--mono);font-size:11px;letter-spacing:.16em;color:#8FB0D0;
  border:1px solid #2C4D6E;padding:3px 7px;border-radius:3px;text-transform:uppercase;white-space:nowrap}
.mast-links{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.mlink{font-family:var(--mono);font-size:11.5px;letter-spacing:.04em;color:#CFE0F0;
  border:1px solid #2C4D6E;padding:5px 9px;border-radius:4px;background:#0d2c4b}
.mlink:hover{background:#11375c;text-decoration:none;border-color:#3a5a7c}
.mlink b{color:#fff;font-weight:600}
.tagline{font-family:var(--serif);font-size:17px;color:#C5D6E8;padding:6px 0 16px;max-width:760px;font-weight:500}
.statstrip{display:flex;flex-wrap:wrap;gap:0;border-top:1px solid #1d3f60;font-family:var(--mono)}
.stat{padding:11px 18px 12px;border-right:1px solid #1d3f60;display:flex;flex-direction:column;gap:2px}
.stat:last-child{border-right:0}
.stat .n{font-size:18px;font-weight:600;color:#fff;letter-spacing:.01em}
.stat .l{font-size:10px;letter-spacing:.13em;color:#7FA0C2;text-transform:uppercase}
.stat.doi .n{font-size:13px;padding-top:3px}
.stat.doi a{color:#9FC4E8}

/* ---------- generic section ---------- */
section{padding:44px 0;border-bottom:1px solid var(--rule)}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:10px;margin:0 0 10px}
.eyebrow::before{content:"";width:22px;height:2px;background:var(--accent);display:inline-block}
h2.sec{font-family:var(--serif);font-weight:600;font-size:24px;letter-spacing:-.01em;margin:0 0 6px}
.sec-sub{color:var(--ink-2);max-width:740px;margin:0 0 22px}

/* ---------- thesis ---------- */
.thesis{background:var(--panel);border-bottom:1px solid var(--rule)}
.thesis .wrap{padding:34px 24px}
.thesis p{font-family:var(--serif);font-size:20px;line-height:1.5;margin:0;color:var(--ink);max-width:840px;font-weight:500}
.thesis .dual{font-family:var(--sans);font-size:14px;color:var(--ink-2);margin-top:14px;max-width:780px;font-weight:400}
.thesis .dual code{font-family:var(--mono);font-size:12.5px;background:var(--canvas);
  padding:1px 5px;border-radius:3px;border:1px solid var(--rule)}

/* ---------- matrix ---------- */
.mtoolbar{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:16px}
.searchbox{position:relative;flex:1;min-width:240px;max-width:420px}
.searchbox input{width:100%;font-family:var(--mono);font-size:13px;padding:9px 12px 9px 32px;
  border:1px solid var(--rule-2);border-radius:6px;background:var(--panel);color:var(--ink)}
.searchbox input::placeholder{color:var(--ink-3)}
.searchbox svg{position:absolute;left:10px;top:50%;transform:translateY(-50%);opacity:.5}
.matchcount{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);white-space:nowrap}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-family:var(--mono);font-size:11px;color:var(--ink-2);margin-left:auto}
.legend span{display:flex;align-items:center;gap:6px}
.lg{width:12px;height:12px;border-radius:2px;display:inline-block}
.lg.v{background:var(--verified)}
.lg.p{background:var(--panel);border:1px solid var(--planned-line)}
.lg.s{background:var(--panel);border:1px solid var(--spine);box-shadow:inset 0 0 0 1px var(--spine)}

.matrix-scroll{overflow-x:auto;border:1px solid var(--rule-2);border-radius:8px;background:var(--panel)}
table.matrix{border-collapse:collapse;font-family:var(--mono);width:100%}
table.matrix th,table.matrix td{border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}
table.matrix thead th{position:sticky;top:0;background:#F7F9FB;z-index:2}
.corner{text-align:left;padding:10px 12px;font-size:10px;letter-spacing:.1em;color:var(--ink-3);
  text-transform:uppercase;position:sticky;left:0;background:#F7F9FB;z-index:3;min-width:118px}
.dimhead{padding:9px 6px;font-size:10.5px;font-weight:500;color:var(--ink-2);cursor:pointer;
  white-space:nowrap;min-width:38px;text-align:center;letter-spacing:.02em;user-select:none}
.dimhead:hover{background:#EEF3F8;color:var(--accent)}
.dimhead.spine{color:var(--spine)}
.dimhead .star{display:block;font-size:8px;line-height:1;margin-top:1px;color:var(--spine)}
.jurcell{position:sticky;left:0;background:var(--panel);z-index:1;padding:0}
.jurbtn{display:flex;flex-direction:column;align-items:flex-start;gap:1px;padding:9px 12px;width:100%;
  background:none;border:0;cursor:pointer;font-family:var(--mono);text-align:left;border-right:1px solid var(--rule-2)}
.jurbtn:hover{background:#F2F6FA}
.jurbtn .code{font-size:14px;font-weight:600;color:var(--ink);letter-spacing:.02em}
.jurbtn .full{font-size:9.5px;color:var(--ink-3);text-transform:uppercase;letter-spacing:.06em}
td.cell{padding:0;text-align:center;height:42px;vertical-align:middle}
.dot{width:100%;height:42px;border:0;background:none;cursor:default;display:flex;align-items:center;justify-content:center;padding:0}
.dot.v{cursor:pointer}
.dot .mk{width:13px;height:13px;border-radius:3px;background:var(--verified);transition:transform .12s ease}
.dot.v:hover .mk{transform:scale(1.45)}
.dot.v:hover{background:var(--verified-bg)}
.dot.p .mk{width:5px;height:5px;border-radius:50%;background:var(--planned-line)}
.cell.spinecol{background:#FCF6F2}
.dot.dim{opacity:.16;filter:grayscale(1)}
.dot.hit{background:#FFF6E9}
.dot.hit .mk{box-shadow:0 0 0 3px rgba(154,93,0,.25)}

/* ---------- inspector ---------- */
.inspector{margin-top:22px;display:grid;grid-template-columns:1fr;gap:0;border:1px solid var(--rule-2);
  border-radius:8px;overflow:hidden;background:var(--panel)}
.insp-head{display:flex;align-items:center;gap:12px;padding:14px 18px;background:#F7F9FB;
  border-bottom:1px solid var(--rule);flex-wrap:wrap}
.insp-jd{font-family:var(--mono);font-size:13px;font-weight:600;letter-spacing:.04em}
.insp-jd .arr{color:var(--ink-3);margin:0 6px}
.insp-dimfull{font-size:12.5px;color:var(--ink-2);font-family:var(--sans)}
.badge{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;
  padding:3px 8px;border-radius:20px;font-weight:600;white-space:nowrap}
.badge.high{background:var(--verified-bg);color:var(--verified);border:1px solid var(--verified-line)}
.badge.medium{background:var(--draft-bg);color:var(--draft);border:1px solid var(--draft-line)}
.badge.low{background:var(--planned-bg);color:var(--ink-2);border:1px solid var(--planned-line)}
.badge.cref{background:#EAF0F7;color:var(--accent);border:1px solid #C2D5E8}
.badge.spineb{background:#F6E9E1;color:var(--spine);border:1px solid #E0B59E}
.insp-id{margin-left:auto;font-family:var(--mono);font-size:11px;color:var(--ink-3)}
.insp-body{padding:18px 18px 20px}
.insp-summary{font-size:14.5px;line-height:1.62;color:var(--ink);margin:0 0 18px}
.prov{font-family:var(--mono);font-size:12px;border:1px solid var(--rule);border-radius:6px;overflow:hidden;margin-bottom:16px}
.prov-row{display:grid;grid-template-columns:118px 1fr;border-bottom:1px solid var(--rule)}
.prov-row:last-child{border-bottom:0}
.prov-k{background:#F7F9FB;padding:8px 12px;color:var(--ink-3);font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;border-right:1px solid var(--rule)}
.prov-v{padding:8px 12px;color:var(--ink);line-height:1.5;word-break:break-word}
.prov-v .em{color:var(--accent)}
.metaline{display:flex;flex-wrap:wrap;gap:0;font-family:var(--mono);font-size:11.5px;
  border:1px solid var(--rule);border-radius:6px;overflow:hidden;margin-bottom:16px}
.metaline div{padding:8px 12px;border-right:1px solid var(--rule);flex:1;min-width:120px}
.metaline div:last-child{border-right:0}
.metaline .mk2{font-size:9.5px;letter-spacing:.1em;color:var(--ink-3);text-transform:uppercase;display:block;margin-bottom:2px}
.metaline .mv{color:var(--ink);font-weight:500}
details.struct{border:1px solid var(--rule);border-radius:6px;margin-bottom:14px;background:#FAFBFC}
details.struct summary{cursor:pointer;padding:9px 12px;font-family:var(--mono);font-size:11px;
  letter-spacing:.06em;text-transform:uppercase;color:var(--ink-2);user-select:none}
details.struct summary:hover{color:var(--accent)}
details.struct pre{margin:0;padding:12px 14px;border-top:1px solid var(--rule);overflow-x:auto;
  font-family:var(--mono);font-size:12px;line-height:1.55;color:#0B2540;background:#fff}
.note{font-size:13px;color:var(--ink-2);line-height:1.55;border-left:3px solid var(--rule-2);padding-left:14px;margin:2px 0 0}
.note b{color:var(--ink);font-weight:600}
.insp-hint{padding:14px 18px;font-family:var(--mono);font-size:12px;color:var(--ink-3);background:#F7F9FB;border-top:1px solid var(--rule)}
.cmp-list{display:grid;gap:12px}
.cmp-item{border:1px solid var(--rule);border-radius:6px;padding:12px 14px;background:#fff}
.cmp-item .ch{display:flex;align-items:center;gap:10px;margin-bottom:6px;flex-wrap:wrap}
.cmp-item .cj{font-family:var(--mono);font-weight:600;font-size:13px}
.cmp-item p{margin:0;font-size:13.5px;line-height:1.55;color:var(--ink-2)}
.cmp-item .src{font-family:var(--mono);font-size:11px;color:var(--ink-3);margin-top:7px;display:block}

/* ---------- access / cards ---------- */
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--rule-2);border-radius:8px;padding:16px 16px 15px;display:flex;flex-direction:column}
.card .ct{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-bottom:6px}
.card h3{font-family:var(--serif);font-size:16px;margin:0 0 6px;font-weight:600}
.card h3 a{color:var(--ink)}
.card p{margin:0 0 12px;font-size:13px;color:var(--ink-2);line-height:1.5}
.card .go{margin-top:auto;font-family:var(--mono);font-size:12px}
.card code{font-family:var(--mono);font-size:12px;background:var(--canvas);padding:1px 5px;border-radius:3px;border:1px solid var(--rule)}
.agentnote{margin-top:16px;font-family:var(--mono);font-size:12px;color:var(--ink-2);
  background:#0C1726;color:#C9D6E5;border-radius:8px;padding:14px 16px;line-height:1.6}
.agentnote b{color:#fff}
.agentnote .gk{color:#7FB0E0}

/* ---------- methodology ---------- */
.method{display:grid;grid-template-columns:1.3fr 1fr;gap:30px;align-items:start}
.method ul{margin:0;padding:0;list-style:none}
.method li{padding:10px 0;border-bottom:1px solid var(--rule);display:flex;gap:12px}
.method li:last-child{border-bottom:0}
.method li .ix{font-family:var(--mono);font-size:11px;color:var(--accent);padding-top:3px;min-width:20px}
.method li .tx{font-size:13.5px;color:var(--ink-2);line-height:1.5}
.method li .tx b{color:var(--ink)}
.rulebox{background:#0C1726;color:#DBE5F0;border-radius:8px;padding:18px 20px;font-size:13.5px;line-height:1.6}
.rulebox .rk{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:#7FB0E0;margin-bottom:10px}
.rulebox b{color:#fff}

/* ---------- roadmap ---------- */
.jurbtn .jwin{font-family:var(--mono);font-size:9px;letter-spacing:.04em;color:var(--ink-2);background:var(--planned-bg);border:1px solid var(--planned-line);border-radius:10px;padding:1px 6px;margin-left:8px;vertical-align:middle;white-space:nowrap}
.jlabel{cursor:default;background:none!important;display:inline-flex;align-items:center}
tr.jrow-planned .jurcell .code,tr.jrow-planned .jurcell .full{opacity:.72}
tr.jrow-planned{background:repeating-linear-gradient(135deg,transparent,transparent 9px,rgba(170,179,192,.05) 9px,rgba(170,179,192,.05) 18px)}
.rm-note{font-family:var(--mono);font-size:11.5px;letter-spacing:.04em;color:var(--draft);
  background:var(--draft-bg);border:1px solid var(--draft-line);border-radius:6px;padding:9px 13px;display:inline-block;margin-bottom:20px}
.rm{display:grid;gap:0;border:1px solid var(--rule-2);border-radius:8px;overflow:hidden;background:var(--panel)}
.rm-item{display:grid;grid-template-columns:96px 1fr auto;gap:14px;padding:15px 18px;border-bottom:1px solid var(--rule);align-items:start}
.rm-item:last-child{border-bottom:0}
.rm-ver{font-family:var(--mono);font-size:12px;font-weight:600;color:var(--ink)}
.rm-ver.cur{color:var(--verified)}
.rm-txt h4{margin:0 0 3px;font-size:14px;font-weight:600;font-family:var(--sans)}
.rm-txt p{margin:0;font-size:13px;color:var(--ink-2);line-height:1.5}
.rm-txt .feat{font-family:var(--mono);font-size:11.5px;color:var(--accent)}
.tag{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;padding:3px 8px;border-radius:20px;white-space:nowrap;font-weight:600;height:fit-content}
.tag.shipped{background:var(--verified-bg);color:var(--verified);border:1px solid var(--verified-line)}
.tag.planned{background:var(--planned-bg);color:var(--ink-2);border:1px solid var(--planned-line)}

/* ---------- footer ---------- */
footer{background:var(--navy);color:#B9CBDD;padding:34px 0 40px}
footer .fgrid{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:flex-start}
footer .fb{font-family:var(--serif);font-size:18px;color:#fff;font-weight:600;margin-bottom:4px}
footer .fm{font-family:var(--mono);font-size:12px;line-height:1.8;color:#9FB4CA}
footer .fm a{color:#BFD6EC}
footer .cite{font-family:var(--mono);font-size:11.5px;background:#0d2c4b;border:1px solid #1d3f60;
  border-radius:6px;padding:12px 14px;color:#CFE0F0;max-width:420px;line-height:1.6}
footer .cite .ck{color:#7FA0C2;display:block;margin-bottom:5px;letter-spacing:.12em;font-size:9.5px;text-transform:uppercase}

/* ---------- view toggle + filterable table ---------- */
.viewtoggle{display:inline-flex;border:1px solid var(--rule-2);border-radius:7px;overflow:hidden;margin-bottom:16px}
.viewtoggle button{font-family:var(--mono);font-size:12px;letter-spacing:.04em;padding:7px 16px;
  background:var(--panel);border:0;cursor:pointer;color:var(--ink-2);border-right:1px solid var(--rule-2)}
.viewtoggle button:last-child{border-right:0}
.viewtoggle button.on{background:var(--navy);color:#fff}
.filterbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
.filterbar select{font-family:var(--mono);font-size:12px;padding:7px 10px;border:1px solid var(--rule-2);
  border-radius:6px;background:var(--panel);color:var(--ink);cursor:pointer}
.filterbar .fbreset{font-family:var(--mono);font-size:11.5px;color:var(--accent);background:none;border:0;cursor:pointer}
.tbl-scroll{overflow-x:auto;border:1px solid var(--rule-2);border-radius:8px;background:var(--panel)}
table.rtbl{border-collapse:collapse;width:100%;font-size:12.5px}
table.rtbl thead th{position:sticky;top:0;background:#F7F9FB;text-align:left;padding:10px 12px;
  font-family:var(--mono);font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-2);
  border-bottom:1px solid var(--rule-2);cursor:pointer;white-space:nowrap;user-select:none}
table.rtbl thead th:hover{color:var(--accent)}
table.rtbl thead th .sortarrow{opacity:.4;font-size:9px;margin-left:3px}
table.rtbl tbody td{padding:10px 12px;border-bottom:1px solid var(--rule);vertical-align:top;line-height:1.45}
table.rtbl tbody tr{cursor:pointer}
table.rtbl tbody tr:hover{background:#F4F8FC}
table.rtbl .tj{font-family:var(--mono);font-weight:600;color:var(--ink)}
table.rtbl .td-dim{font-family:var(--mono);font-size:11.5px;color:var(--ink-2);white-space:nowrap}
table.rtbl .td-dim .spm{color:var(--spine)}
table.rtbl .td-req{color:var(--ink-2);min-width:280px;max-width:440px}
table.rtbl .td-pin{font-family:var(--mono);font-size:11px;color:var(--ink-3);min-width:180px;max-width:300px}
table.rtbl .cf{font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;padding:2px 7px;border-radius:20px;font-weight:600;white-space:nowrap}
table.rtbl .cf.high{background:var(--verified-bg);color:var(--verified)}
table.rtbl .cf.medium{background:var(--draft-bg);color:var(--draft)}
table.rtbl .cf.low{background:var(--planned-bg);color:var(--ink-2)}
table.rtbl .tcref{font-family:var(--mono);font-size:11px;color:var(--accent)}
.tblcount{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);margin:10px 2px 0}
.hidden{display:none!important}

@media (max-width:760px){
  .method{grid-template-columns:1fr}
  .thesis p{font-size:18px}
  .rm-item{grid-template-columns:1fr;gap:6px}
  .rm-item .tag{justify-self:start}
  .stat{flex:1 0 40%}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style>
</head>
<body>

<header class="masthead">
  <div class="wrap">
    <div class="mast-top">
      <div class="brand">
        <span class="wordmark">Cross-Border Stablecoin Register</span>
        <span class="reg-tag">Open Register · v__VERSION__</span>
      </div>
      <nav class="mast-links">
        <a class="mlink" href="https://doi.org/10.5281/zenodo.20730359">DOI <b>10.5281/zenodo.20730359</b></a>
        <a class="mlink" href="https://github.com/yunjiefanresearch-hub/stablecoin-rail-register">GitHub</a>
        <a class="mlink" href="./dataset.json"><b>dataset.json</b></a>
      </nav>
    </div>
    <p class="tagline">An open, versioned register mapping how jurisdictions regulate stablecoins — clause by clause, across fifteen dimensions and two doctrinal spines (the yield boundary and securities classification).</p>
    <div class="statstrip">
      <div class="stat"><span class="n">__NJUR__</span><span class="l">Jurisdictions</span></div>
      <div class="stat"><span class="n">15</span><span class="l">Dimensions</span></div>
      <div class="stat"><span class="n">__NREC__</span><span class="l">Verified records</span></div>
      <div class="stat"><span class="n">__NCOR__</span><span class="l">Corridor</span></div>
      <div class="stat"><span class="n">2</span><span class="l">Doctrinal spines</span></div>
      <div class="stat doi"><span class="n"><a href="https://doi.org/10.5281/zenodo.20730359">CC-BY-4.0</a></span><span class="l">Data license</span></div>
    </div>
  </div>
</header>

<div class="thesis">
  <div class="wrap">
    <p>Each record is one sourced <span class="mono" style="font-size:.8em;color:var(--ink-2)">(jurisdiction × instrument × dimension)</span> regulatory fact — cited to a primary instrument with a pinpoint, dated, version-stamped, confidence-rated, and validated against a published JSON Schema.</p>
    <p class="dual">Built for humans and machines alike. Browse the live coverage matrix below, or consume <code>dataset.json</code> and <code>record.schema.json</code> directly. Not a 200-country scrape — a depth-first reference whose value is the judgment in the data and the corridor layer that models what clears, and what breaks, at each regulatory boundary.</p>
  </div>
</div>

<section id="coverage">
  <div class="wrap">
    <p class="eyebrow">Coverage matrix</p>
    <h2 class="sec">Six jurisdictions mapped, two forthcoming &times; fifteen dimensions</h2>
    <p class="sec-sub">Each filled cell is a verified, sourced record. Select a cell to inspect it; a column header to compare all jurisdictions on that dimension; a jurisdiction to read its full profile. Empty cells are on the roadmap — this is an actively-built standard, not a finished table.</p>
    <div class="mtoolbar">
      <div class="searchbox">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
        <input id="q" type="search" placeholder="Filter records — keyword (e.g. MiCA, reserve, PIPL)" autocomplete="off" aria-label="Filter records by keyword">
      </div>
      <span class="matchcount" id="matchcount"></span>
      <div class="legend">
        <span><i class="lg v"></i>verified</span>
        <span><i class="lg p"></i>planned</span>
        <span><i class="lg s"></i>spine dimension</span>
      </div>
    </div>
    <div class="viewtoggle" id="viewtoggle">
      <button data-view="matrix" class="on">Matrix</button>
      <button data-view="table">Table</button>
    </div>
    <div id="view-matrix">
      <div class="matrix-scroll">
        <table class="matrix" id="matrix"><thead></thead><tbody></tbody></table>
      </div>
    </div>
    <div id="view-table" class="hidden">
      <div class="filterbar" id="filterbar">
        <select id="f-jur" aria-label="Filter by jurisdiction"><option value="">All jurisdictions</option></select>
        <select id="f-dim" aria-label="Filter by dimension"><option value="">All dimensions</option></select>
        <select id="f-status" aria-label="Filter by status"><option value="">Any status</option></select>
        <select id="f-conf" aria-label="Filter by confidence"><option value="">Any confidence</option></select>
        <button class="fbreset" id="f-reset">reset</button>
      </div>
      <div class="tbl-scroll">
        <table class="rtbl" id="rtbl"><thead></thead><tbody></tbody></table>
      </div>
      <p class="tblcount" id="tblcount"></p>
    </div>
    <div class="inspector" id="inspector"></div>
  </div>
</section>

<section id="access">
  <div class="wrap">
    <p class="eyebrow">Access — humans &amp; agents</p>
    <h2 class="sec">Consume the register</h2>
    <p class="sec-sub">Everything is open, versioned, and machine-readable. Cite the DOI of the version you use.</p>
    <div class="grid">
      <div class="card">
        <span class="ct">Dataset</span>
        <h3><a href="./dataset.json">dataset.json</a></h3>
        <p>The full compiled register — every record with its source, pinpoint, dates, version and confidence, plus the corridor model.</p>
        <span class="go"><a href="./dataset.json">Open dataset →</a></span>
      </div>
      <div class="card">
        <span class="ct">Schema · the standard</span>
        <h3><a href="./record.schema.json">record.schema.json</a></h3>
        <p>The JSON Schema every record validates against — 15 dimensions, constraint references, provenance fields. Vocabulary in <code>taxonomy.md</code>.</p>
        <span class="go"><a href="./record.schema.json">View schema →</a></span>
      </div>
      <div class="card">
        <span class="ct">Coverage</span>
        <h3><a href="./COVERAGE.md">COVERAGE.md</a></h3>
        <p>The full machine-generated coverage grid including planned cells and the roadmap schedule.</p>
        <span class="go"><a href="./COVERAGE.md">Open coverage →</a></span>
      </div>
      <div class="card">
        <span class="ct">Cite</span>
        <h3>DOI 10.5281/zenodo.20730359</h3>
        <p>Each tagged release is archived to Zenodo with a DOI. Citation metadata in <code>CITATION.cff</code>.</p>
        <span class="go"><a href="https://doi.org/10.5281/zenodo.20730359">Resolve DOI →</a></span>
      </div>
      <div class="card">
        <span class="ct">Source</span>
        <h3><a href="https://github.com/yunjiefanresearch-hub/stablecoin-rail-register">GitHub repository</a></h3>
        <p>Records, schema, build pipeline, methodology, corridor layer. Contributions under the verification rule.</p>
        <span class="go"><a href="https://github.com/yunjiefanresearch-hub/stablecoin-rail-register">Open repo →</a></span>
      </div>
      <div class="card">
        <span class="ct">Methodology</span>
        <h3><a href="./METHODOLOGY.md">METHODOLOGY.md</a></h3>
        <p>How a record becomes "verified", the source-level citation rule, and the no-AI-generated-citations firewall.</p>
        <span class="go"><a href="./METHODOLOGY.md">Read method →</a></span>
      </div>
    </div>
    <div class="agentnote">
      <b>For agents.</b> The register is a single JSON document at <span class="gk">/dataset.json</span>, validated against a published JSON Schema, with a stable <span class="gk">id</span> per record and explicit <span class="gk">source.primary</span> · <span class="gk">source.pinpoint</span> · <span class="gk">confidence</span> · <span class="gk">version_added</span> fields. A queryable <span class="gk">MCP server</span> exposes typed query tools over this dataset (query, compare_dimension, jurisdiction_profile, search, coverage) — or fetch and filter the dataset directly.
    </div>
  </div>
</section>

<section id="method">
  <div class="wrap">
    <p class="eyebrow">Methodology</p>
    <h2 class="sec">Why the data can be trusted</h2>
    <div class="method">
      <ul>
        <li><span class="ix">01</span><span class="tx"><b>One fact, one source.</b> Every record cites a primary instrument (statute, regulation, or bill) with a clause-level pinpoint — not a secondary summary.</span></li>
        <li><span class="ix">02</span><span class="tx"><b>Dated and versioned.</b> Each record carries an effective date, a last-reviewed date, and the register version it entered, so staleness is visible.</span></li>
        <li><span class="ix">03</span><span class="tx"><b>Confidence is explicit.</b> Every record states a confidence level; interpretive tensions are flagged rather than smoothed over.</span></li>
        <li><span class="ix">04</span><span class="tx"><b>Verified means checked.</b> A record is verified only when it has no open markers and a human has checked every source and pinpoint against the instrument itself.</span></li>
      </ul>
      <div class="rulebox">
        <div class="rk">Citation firewall</div>
        No citation in this register is ever machine-generated. <b>A single fabricated source is fatal</b> to a reference like this, so every pinpoint is transcribed from primary text and human-verified. Secondary provenance is recorded openly alongside the primary source.
      </div>
    </div>
  </div>
</section>

<section id="roadmap">
  <div class="wrap">
    <p class="eyebrow">Roadmap</p>
    <h2 class="sec">What ships next</h2>
    <span class="rm-note">▲ Items tagged PLANNED are on the roadmap and not yet available.</span>
    <div class="rm">
      <div class="rm-item">
        <span class="rm-ver">v0.2.0</span>
        <div class="rm-txt"><h4>15-dimension framework · DOI</h4><p>Two doctrinal spines (yield boundary + securities classification); six focus jurisdictions; corridor layer; archived to Zenodo for a citable DOI. <span class="feat">— last released version</span></p></div>
        <span class="tag shipped">Shipped</span>
      </div>
      <div class="rm-item">
        <span class="rm-ver cur">v0.3.0-dev</span>
        <div class="rm-txt"><h4>Depth + interfaces</h4><p>Hong Kong, Singapore and the UK deepened to 11 dimensions each (51 records, 14/15 dimensions); sortable multi-filter table view; queryable <b>MCP server</b> now available. <span class="feat">— current working tree</span></p></div>
        <span class="tag shipped">Available</span>
      </div>
      <div class="rm-item">
        <span class="rm-ver">v0.3.x</span>
        <div class="rm-txt"><h4>Brazil → full jurisdiction · Hong Kong verification</h4><p>Promote <b>Brazil</b> from corridor-only to a full jurisdiction (the HK→BR settlement corridor anchors it); complete the primary-source verification pass (clause-level URLs) on the Hong Kong anchor cells.</p></div>
        <span class="tag planned">In progress</span>
      </div>
      <div class="rm-item">
        <span class="rm-ver">v0.4.0</span>
        <div class="rm-txt"><h4>Taiwan + query API</h4><p>Add <b>Taiwan</b> as an infrastructure jurisdiction; semantic search and a jurisdiction comparison / query API over the MCP layer.</p></div>
        <span class="tag planned">Planned</span>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="wrap fgrid">
    <div>
      <div class="fb">Cross-Border Stablecoin Register</div>
      <div class="fm">
        Founder &amp; maintainer: Yunjie Fan<br>
        Data: CC-BY-4.0 · Code: Apache-2.0<br>
        Cadence: quarterly diffs + event patches<br>
        <a href="https://github.com/yunjiefanresearch-hub/stablecoin-rail-register">github.com/yunjiefanresearch-hub/stablecoin-rail-register</a><br>
        <span style="color:#6E86A0">v__VERSION__ · generated __GENERATED__</span>
      </div>
    </div>
    <div class="cite">
      <span class="ck">Cite this version</span>
      Fan, Yunjie. <i>Cross-Border Stablecoin Register</i> (v__VERSION__). Zenodo. https://doi.org/10.5281/zenodo.20730359 — licensed CC-BY-4.0.
    </div>
  </div>
</footer>

<script id="embedded-data" type="application/json">__DATASET_JSON__</script>
<script>
(function(){
  "use strict";
  // 15-dimension spec (order + short code + full name + spine flag) — matches the schema.
  var DIMS=[
    {k:"regulatory_authority",s:"AUTH",f:"Regulatory authority"},
    {k:"issuer_pathway",s:"ISSU",f:"Issuer pathway"},
    {k:"reserve_backing",s:"RESV",f:"Reserve backing"},
    {k:"capital_requirements",s:"CAP",f:"Capital requirements"},
    {k:"permitted_activity_yield",s:"YIELD",f:"Permitted activity / yield",spine:true},
    {k:"securities_classification",s:"SEC",f:"Securities classification",spine:true},
    {k:"bank_nonbank_routing",s:"ROUT",f:"Bank / non-bank routing"},
    {k:"redemption",s:"REDM",f:"Redemption"},
    {k:"custody",s:"CUST",f:"Custody"},
    {k:"aml_kyc",s:"AML",f:"AML / KYC"},
    {k:"cross_border_data",s:"XBD",f:"Cross-border data"},
    {k:"monetary_sovereignty",s:"MSOV",f:"Monetary sovereignty"},
    {k:"disclosure_reporting",s:"DISC",f:"Disclosure / reporting"},
    {k:"distribution",s:"DIST",f:"Distribution"},
    {k:"implementation_status",s:"IMPL",f:"Implementation status"}
  ];
  var JURS=[
    {c:"US",f:"United States"},{c:"HK",f:"Hong Kong"},{c:"EU",f:"European Union"},
    {c:"UK",f:"United Kingdom"},{c:"SG",f:"Singapore"},{c:"CN",f:"Mainland China"},
    {c:"BR",f:"Brazil",planned:"v0.3"},{c:"TW",f:"Taiwan",planned:"v0.4"}
  ];
  var JFULL={}; JURS.forEach(function(j){JFULL[j.c]=j.f;});
  var DMAP={}; DIMS.forEach(function(d){DMAP[d.k]=d;});

  function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}

  function render(data){
    var records=(data&&data.records)||[];
    var byCell={}; records.forEach(function(r){byCell[r.jurisdiction+"__"+r.dimension]=r;});

    // ---- matrix head ----
    var thead=document.querySelector("#matrix thead");
    var tr="<tr><th class='corner'>Jurisdiction</th>";
    DIMS.forEach(function(d){
      tr+="<th class='dimhead"+(d.spine?" spine":"")+"' data-dim='"+d.k+"' title='"+esc(d.f)+(d.spine?" — spine dimension":"")+"' tabindex='0' role='button'>"+d.s+(d.spine?"<span class='star'>★</span>":"")+"</th>";
    });
    thead.innerHTML=tr+"</tr>";

    // ---- matrix body ----
    var tb=document.querySelector("#matrix tbody"),html="";
    JURS.forEach(function(j){
      html+="<tr"+(j.planned?" class='jrow-planned'":"")+">";
      if(j.planned){
        html+="<td class='jurcell'><span class='jurbtn jlabel'><span class='code'>"+j.c+"</span><span class='full'>"+esc(j.f)+"</span><span class='jwin'>"+j.planned+" \u25b8</span></span></td>";
      }else{
        html+="<td class='jurcell'><button class='jurbtn' data-jur='"+j.c+"'><span class='code'>"+j.c+"</span><span class='full'>"+esc(j.f)+"</span></button></td>";
      }
      DIMS.forEach(function(d){
        var rec=byCell[j.c+"__"+d.k];
        var spineCls=d.spine?" spinecol":"";
        if(rec){
          html+="<td class='cell"+spineCls+"'><button class='dot v' data-id='"+esc(rec.id)+"' title='"+esc(j.c+" · "+d.f+" — verified")+"'><span class='mk'></span></button></td>";
        }else{
          html+="<td class='cell"+spineCls+"'><span class='dot p' title='"+esc(j.c+" · "+d.f+" — planned")+"'><span class='mk'></span></span></td>";
        }
      });
      html+="</tr>";
    });
    tb.innerHTML=html;

    // ---- interactions ----
    var insp=document.getElementById("inspector");
    tb.addEventListener("click",function(e){
      var b=e.target.closest(".dot.v"); if(b){selectRecord(b.getAttribute("data-id"));return;}
      var jb=e.target.closest(".jurbtn"); if(jb){compareJur(jb.getAttribute("data-jur"));}
    });
    thead.addEventListener("click",function(e){var h=e.target.closest(".dimhead");if(h)compareDim(h.getAttribute("data-dim"));});
    thead.addEventListener("keydown",function(e){if((e.key==="Enter"||e.key===" ")&&e.target.classList.contains("dimhead")){e.preventDefault();compareDim(e.target.getAttribute("data-dim"));}});

    function badge(conf){conf=conf||"low";return "<span class='badge "+conf+"'>conf: "+conf+"</span>";}

    function selectRecord(id){
      var r=null; for(var i=0;i<records.length;i++){if(records[i].id===id){r=records[i];break;}}
      if(!r)return;
      var d=DMAP[r.dimension]||{f:r.dimension,s:r.dimension};
      var sec=(r.secondary&&r.secondary[0]&&r.secondary[0].citation)||"—";
      var struct=r.requirement_structured?JSON.stringify(r.requirement_structured,null,2):null;
      var h="";
      h+="<div class='insp-head'>";
      h+="<span class='insp-jd'>"+esc(r.jurisdiction)+"<span class='arr'>›</span>"+esc(d.s)+"</span>";
      h+="<span class='insp-dimfull'>"+esc(d.f)+"</span>";
      if(d.spine)h+="<span class='badge spineb'>spine</span>";
      if(r.constraint_ref)h+="<span class='badge cref'>"+esc(r.constraint_ref)+"</span>";
      h+=badge(r.confidence);
      h+="<span class='insp-id'>"+esc(r.id)+"</span>";
      h+="</div><div class='insp-body'>";
      h+="<p class='insp-summary'>"+esc(r.requirement_summary)+"</p>";
      h+="<div class='prov'>";
      h+="<div class='prov-row'><div class='prov-k'>Source</div><div class='prov-v'>"+esc(r.source&&r.source.primary)+"</div></div>";
      h+="<div class='prov-row'><div class='prov-k'>Pinpoint</div><div class='prov-v'><span class='em'>"+esc(r.source&&r.source.pinpoint)+"</span></div></div>";
      h+="<div class='prov-row'><div class='prov-k'>Authority</div><div class='prov-v'>"+esc(r.authority)+"</div></div>";
      h+="<div class='prov-row'><div class='prov-k'>Instrument</div><div class='prov-v'>"+esc(r.instrument_label_local)+"</div></div>";
      h+="<div class='prov-row'><div class='prov-k'>Secondary</div><div class='prov-v'>"+esc(sec)+"</div></div>";
      h+="</div>";
      h+="<div class='metaline'>";
      h+="<div><span class='mk2'>Jurisdiction</span><span class='mv'>"+esc(r.jurisdiction)+" · "+esc(JFULL[r.jurisdiction]||"")+"</span></div>";
      h+="<div><span class='mk2'>Effective</span><span class='mv'>"+esc(r.effective_date||"n/a")+"</span></div>";
      h+="<div><span class='mk2'>Reviewed</span><span class='mv'>"+esc(r.last_reviewed||"—")+"</span></div>";
      h+="<div><span class='mk2'>Version</span><span class='mv'>v"+esc(r.version_added||"—")+"</span></div>";
      h+="<div><span class='mk2'>Status</span><span class='mv'>"+esc(r.status||"—")+"</span></div>";
      h+="</div>";
      if(struct)h+="<details class='struct'><summary>Machine-readable obligation · requirement_structured</summary><pre>"+esc(struct)+"</pre></details>";
      if(r.interpretation_note)h+="<p class='note'><b>Note.</b> "+esc(r.interpretation_note)+"</p>";
      h+="</div>";
      insp.innerHTML=h;
      insp.scrollIntoView({behavior:"smooth",block:"nearest"});
    }

    function compareDim(dimKey){
      var d=DMAP[dimKey]||{f:dimKey,s:dimKey};
      var rs=records.filter(function(r){return r.dimension===dimKey;});
      var h="<div class='insp-head'><span class='insp-jd'>Compare ›</span><span class='insp-dimfull'>"+esc(d.f)+(d.spine?" — spine dimension":"")+"</span><span class='insp-id'>"+rs.length+" jurisdiction"+(rs.length===1?"":"s")+"</span></div><div class='insp-body'>";
      if(!rs.length){h+="<p class='note'>No verified records on this dimension yet — it is on the roadmap.</p>";}
      else{
        h+="<div class='cmp-list'>";
        rs.forEach(function(r){
          h+="<div class='cmp-item'><div class='ch'><span class='cj'>"+esc(r.jurisdiction)+" · "+esc(JFULL[r.jurisdiction]||"")+"</span><span class='badge "+(r.confidence||"low")+"'>conf: "+esc(r.confidence||"low")+"</span>"+(r.constraint_ref?"<span class='badge cref'>"+esc(r.constraint_ref)+"</span>":"")+"</div><p>"+esc(r.requirement_summary)+"</p><span class='src'>▸ "+esc(r.source&&r.source.primary)+" — "+esc(r.source&&r.source.pinpoint)+"</span></div>";
        });
        h+="</div>";
      }
      h+="</div>";
      insp.innerHTML=h; insp.scrollIntoView({behavior:"smooth",block:"nearest"});
    }

    function compareJur(jc){
      var rs=records.filter(function(r){return r.jurisdiction===jc;})
                    .sort(function(a,b){return DIMS.findIndex(function(d){return d.k===a.dimension;})-DIMS.findIndex(function(d){return d.k===b.dimension;});});
      var h="<div class='insp-head'><span class='insp-jd'>Profile ›</span><span class='insp-dimfull'>"+esc(JFULL[jc]||jc)+"</span><span class='insp-id'>"+rs.length+" records</span></div><div class='insp-body'><div class='cmp-list'>";
      rs.forEach(function(r){
        var d=DMAP[r.dimension]||{f:r.dimension};
        h+="<div class='cmp-item'><div class='ch'><span class='cj'>"+esc(d.f)+"</span><span class='badge "+(r.confidence||"low")+"'>conf: "+esc(r.confidence||"low")+"</span>"+(r.constraint_ref?"<span class='badge cref'>"+esc(r.constraint_ref)+"</span>":"")+"</div><p>"+esc(r.requirement_summary)+"</p><span class='src'>▸ "+esc(r.source&&r.source.pinpoint)+"</span></div>";
      });
      h+="</div></div>";
      insp.innerHTML=h; insp.scrollIntoView({behavior:"smooth",block:"nearest"});
    }

    // ---- shared keyword matcher ----
    var q=document.getElementById("q"),mc=document.getElementById("matchcount");
    function hay(r){return [r.jurisdiction,r.dimension,r.authority,r.requirement_summary,r.instrument_label_local,(r.source&&r.source.primary),(r.source&&r.source.pinpoint),(r.tags||[]).join(" "),r.constraint_ref].join(" ").toLowerCase();}

    // ---- matrix keyword dimming ----
    function applyFilter(){
      var term=(q.value||"").trim().toLowerCase();
      var dots=tb.querySelectorAll(".dot.v"),hits=0;
      dots.forEach(function(dot){
        var id=dot.getAttribute("data-id"),r=null;
        for(var i=0;i<records.length;i++){if(records[i].id===id){r=records[i];break;}}
        if(!term){dot.classList.remove("dim","hit");return;}
        if(r&&hay(r).indexOf(term)>=0){dot.classList.add("hit");dot.classList.remove("dim");hits++;}
        else{dot.classList.add("dim");dot.classList.remove("hit");}
      });
      mc.textContent=term?(hits+" record"+(hits===1?"":"s")+" match"):"";
    }

    // ---- filterable / sortable table view ----
    var fJur=document.getElementById("f-jur"),fDim=document.getElementById("f-dim"),
        fStatus=document.getElementById("f-status"),fConf=document.getElementById("f-conf"),
        rtblHead=document.querySelector("#rtbl thead"),rtblBody=document.querySelector("#rtbl tbody"),
        tblcount=document.getElementById("tblcount");
    var sortKey="jurisdiction",sortDir=1;
    var CONF_RANK={high:3,medium:2,low:1};
    var COLS=[
      {k:"jurisdiction",label:"Jur",sortable:true},
      {k:"dimension",label:"Dimension",sortable:true},
      {k:"constraint_ref",label:"C-ref",sortable:true},
      {k:"requirement_summary",label:"Requirement",sortable:false},
      {k:"pinpoint",label:"Source pinpoint",sortable:false},
      {k:"status",label:"Status",sortable:true},
      {k:"confidence",label:"Conf",sortable:true},
      {k:"version_added",label:"Ver",sortable:true}
    ];
    // populate dropdowns
    JURS.forEach(function(j){ if(records.some(function(r){return r.jurisdiction===j.c;})){ var o=document.createElement("option");o.value=j.c;o.textContent=j.c+" — "+j.f;fJur.appendChild(o);} });
    DIMS.forEach(function(d){ var o=document.createElement("option");o.value=d.k;o.textContent=d.f;fDim.appendChild(o); });
    Array.from(new Set(records.map(function(r){return r.status;}))).sort().forEach(function(s){ var o=document.createElement("option");o.value=s;o.textContent=s;fStatus.appendChild(o); });
    ["high","medium","low"].forEach(function(c){ if(records.some(function(r){return r.confidence===c;})){ var o=document.createElement("option");o.value=c;o.textContent=c;fConf.appendChild(o);} });

    function sortVal(r,k){
      if(k==="dimension"){var i=DIMS.findIndex(function(d){return d.k===r.dimension;});return i<0?99:i;}
      if(k==="confidence")return CONF_RANK[r.confidence]||0;
      if(k==="constraint_ref")return r.constraint_ref||"~";
      return (r[k]||"").toString().toLowerCase();
    }
    function filteredRows(){
      var term=(q.value||"").trim().toLowerCase();
      return records.filter(function(r){
        if(fJur.value&&r.jurisdiction!==fJur.value)return false;
        if(fDim.value&&r.dimension!==fDim.value)return false;
        if(fStatus.value&&r.status!==fStatus.value)return false;
        if(fConf.value&&r.confidence!==fConf.value)return false;
        if(term&&hay(r).indexOf(term)<0)return false;
        return true;
      }).sort(function(a,b){var va=sortVal(a,sortKey),vb=sortVal(b,sortKey);return (va<vb?-1:va>vb?1:0)*sortDir;});
    }
    function renderTableHead(){
      var h="<tr>";
      COLS.forEach(function(c){
        var arr=c.sortable?(sortKey===c.k?(sortDir>0?" ▲":" ▼"):" ↕"):"";
        h+="<th data-col='"+c.k+"' "+(c.sortable?"role='button' tabindex='0'":"")+">"+c.label+(c.sortable?"<span class='sortarrow'>"+arr+"</span>":"")+"</th>";
      });
      rtblHead.innerHTML=h+"</tr>";
    }
    function renderTable(){
      renderTableHead();
      var rows=filteredRows(),h="";
      rows.forEach(function(r){
        var d=DMAP[r.dimension]||{f:r.dimension,spine:false};
        var pin=(r.source&&r.source.pinpoint)||"—";
        h+="<tr data-id='"+esc(r.id)+"'>";
        h+="<td class='tj'>"+esc(r.jurisdiction)+"</td>";
        h+="<td class='td-dim'>"+esc(d.f)+(d.spine?" <span class='spm'>★</span>":"")+"</td>";
        h+="<td><span class='tcref'>"+esc(r.constraint_ref||"—")+"</span></td>";
        h+="<td class='td-req'>"+esc(r.requirement_summary)+"</td>";
        h+="<td class='td-pin'>"+esc(pin)+"</td>";
        h+="<td>"+esc(r.status||"—")+"</td>";
        h+="<td><span class='cf "+(r.confidence||"low")+"'>"+esc(r.confidence||"low")+"</span></td>";
        h+="<td>v"+esc(r.version_added||"—")+"</td>";
        h+="</tr>";
      });
      rtblBody.innerHTML=h;
      tblcount.textContent=rows.length+" of "+records.length+" records";
    }
    rtblHead.addEventListener("click",function(e){var th=e.target.closest("th[data-col]");if(!th)return;var k=th.getAttribute("data-col");if(!COLS.find(function(c){return c.k===k&&c.sortable;}))return;if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=1;}renderTable();});
    rtblBody.addEventListener("click",function(e){var tr=e.target.closest("tr[data-id]");if(tr){selectRecord(tr.getAttribute("data-id"));}});
    [fJur,fDim,fStatus,fConf].forEach(function(sel){sel.addEventListener("change",renderTable);});
    document.getElementById("f-reset").addEventListener("click",function(){fJur.value="";fDim.value="";fStatus.value="";fConf.value="";renderTable();});

    // keyword drives both views
    if(q)q.addEventListener("input",function(){applyFilter();renderTable();});

    // ---- view toggle ----
    var vMatrix=document.getElementById("view-matrix"),vTable=document.getElementById("view-table");
    document.getElementById("viewtoggle").addEventListener("click",function(e){
      var b=e.target.closest("button[data-view]");if(!b)return;
      Array.prototype.forEach.call(this.querySelectorAll("button"),function(x){x.classList.remove("on");});
      b.classList.add("on");
      var v=b.getAttribute("data-view");
      if(v==="table"){vMatrix.classList.add("hidden");vTable.classList.remove("hidden");renderTable();}
      else{vTable.classList.add("hidden");vMatrix.classList.remove("hidden");}
    });
    renderTable(); // prime table so it's ready on first toggle

    // default inspector content: the HK yield spine (project core), else first record
    var def=null; for(var i=0;i<records.length;i++){if(records[i].id==="hk-frs-permitted_activity_yield-001"){def=records[i];break;}}
    if(!def)def=records[0];
    if(def)selectRecord(def.id);
    else insp.innerHTML="<div class='insp-hint'>Dataset unavailable in this preview. Open the live site, or view <a href='./dataset.json'>dataset.json</a> directly.</div>";
  }

  // Render from the embedded snapshot immediately (instant + robust, works on file:// too),
  // then upgrade to the live dataset.json when served over http(s) so the page stays in sync.
  var rendered=false;
  try{ render(JSON.parse(document.getElementById("embedded-data").textContent)); rendered=true; }
  catch(e){ /* fall through to fetch */ }

  var ctrl=("AbortController"in window)?new AbortController():null;
  if(ctrl)setTimeout(function(){try{ctrl.abort();}catch(_){}} ,4000);
  fetch("./dataset.json",{cache:"no-store",signal:ctrl?ctrl.signal:undefined})
    .then(function(r){if(!r.ok)throw 0;return r.json();})
    .then(function(d){ if(d&&d.records&&d.records.length) render(d); })
    .catch(function(){
      if(!rendered){
        document.getElementById("inspector").innerHTML="<div class='insp-hint'>Dataset unavailable. View <a href='./dataset.json'>dataset.json</a> directly.</div>";
      }
    });
})();
</script>
</body>
</html>
"""

out = (TEMPLATE
       .replace("__DATASET_JSON__", json.dumps(data, ensure_ascii=False))
       .replace("__VERSION__", str(data.get("version","")))
       .replace("__NJUR__", str(len(set(r["jurisdiction"] for r in data["records"]))))
       .replace("__NREC__", str(data.get("record_count", len(data["records"]))))
       .replace("__NCOR__", str(len(data.get("corridors", []))))
       .replace("__GENERATED__", str(data.get("generated", datetime.date.today()))))

(ROOT / "index.html").write_text(out, encoding="utf-8")
print("wrote index.html  (%d bytes)" % len(out.encode("utf-8")))
