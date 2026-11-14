"""Shared page shell for the portfolio's interactive web reports.

Standard library only. Each project's tools/build_web_report.py supplies the
data, copy and report-specific script; this module supplies the design system
used across the portfolio (midnight navy, electric blue, warm orange).
"""
from __future__ import annotations

import html
import json

CSS = r"""
:root{--ink:#EAF0FC;--muted:#A2B2CC;--blue:#66A0FF;--orange:#FFAD72;--prior:#7891B6;--line:#263B57;--paper:#0B1423;--card:#142339;--soft:#1A3252;--rail:#111D33;--good:#6FD3A6}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:14px/1.6 'Segoe UI',system-ui,-apple-system,Arial,sans-serif;display:grid;grid-template-columns:216px minmax(0,1fr)}
a{color:var(--blue)}button,select{font:inherit;color:inherit;cursor:pointer}
:focus-visible{outline:3px solid var(--orange);outline-offset:3px}
.rail{background:var(--rail);padding:32px 24px;position:sticky;top:0;height:100dvh;display:flex;flex-direction:column;gap:30px}
.brand{font-size:32px;font-weight:600;color:#8DB2FF;text-decoration:none;letter-spacing:-1.5px}
.rail-name{font-size:24px;font-weight:600;line-height:1.15;letter-spacing:-.7px}
.rail nav{display:grid;gap:8px}.rail nav a{padding:12px;border-radius:10px;text-decoration:none;font-size:13px;color:#BECCE1;transition:background .2s,transform .2s}
.rail nav a[aria-current]{background:#294F89;color:#fff}.rail nav a:hover{background:var(--soft);transform:translateX(3px)}
.rail-window{color:var(--muted);font-size:12px;line-height:1.8}.rail-window span{display:block;font-size:11px;letter-spacing:1px;margin-bottom:10px}.rail-window strong{display:block;color:var(--ink);font-weight:500}
.rail-credit{margin-top:auto;font-size:11px;line-height:1.8;color:var(--muted)}
main{max-width:1650px;min-width:0;width:100%;margin:0 auto;padding:26px 44px 0}
.masthead{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;padding-bottom:20px;border-bottom:1px solid var(--line)}
.identity{color:var(--muted);font-size:11px;letter-spacing:1.2px;font-weight:500;text-decoration:none}
.period{display:flex;align-items:center;gap:10px;font-size:11px;letter-spacing:.7px;color:var(--muted);padding:8px 13px;border:1px solid var(--line);border-radius:20px}
.period i{width:6px;height:6px;border-radius:50%;background:var(--blue)}
.controls{display:flex;flex-wrap:wrap;gap:14px 22px;align-items:end;padding:22px 0 0}
.control{display:grid;gap:6px}.control>span{font-size:11px;letter-spacing:1px;color:var(--muted)}
.seg{display:inline-flex;background:var(--soft);border-radius:10px;padding:3px;gap:3px;flex-wrap:wrap}
.seg button{border:0;background:transparent;padding:7px 13px;border-radius:8px;font-size:13px;color:#BECCE1}
.seg button[aria-pressed=true]{background:#294F89;color:#fff}
select{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:8px 12px;font-size:13px;min-width:150px}
.overview{display:grid;grid-template-columns:minmax(300px,.85fr) minmax(0,1.5fr);gap:34px;padding:34px 0 42px;align-items:start}
.eyebrow{font-size:11px;font-weight:700;letter-spacing:1px;color:var(--muted)}
.num{display:inline-grid;place-items:center;width:27px;height:27px;border-radius:8px;background:var(--soft);color:var(--blue);margin-right:8px}
h1{font-size:clamp(40px,4.1vw,64px);font-weight:600;line-height:1.05;letter-spacing:-2.4px;margin:20px 0 16px;text-wrap:balance}h1 span{color:var(--blue)}
h2{font-size:25px;line-height:1.25;letter-spacing:-.6px;margin:10px 0 0;font-weight:600;text-wrap:balance}
h3{font-size:17px;letter-spacing:-.3px;margin:0;font-weight:600}
.standfirst{color:var(--muted);font-size:14px;line-height:1.7;max-width:420px;margin:0 0 26px}
.big-label{font-size:11px;letter-spacing:1px;font-weight:650}.big-label span{color:var(--muted);font-weight:400;letter-spacing:0;margin-left:8px}
.big{font-size:52px;font-weight:500;letter-spacing:-2px;line-height:1.25;font-variant-numeric:tabular-nums}
.context{font-size:12px;color:var(--muted);display:flex;gap:10px;align-items:center;flex-wrap:wrap}.context b{color:var(--ink);font-weight:600}
.pill{color:var(--orange);background:#3C302D;padding:5px 10px;border-radius:7px;font-weight:650;font-size:12px;white-space:nowrap}
.kpis{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line);margin-top:24px;padding-top:18px;gap:0}
.kpis>div{padding:4px 0}.kpis>div:nth-child(even){border-left:1px solid var(--line);padding-left:22px}
.kpis>div:nth-child(n+3){border-top:1px solid var(--line);margin-top:12px;padding-top:14px}
.kpis span{font-size:11px;letter-spacing:.5px;color:var(--muted);display:block}.kpis strong{font-size:28px;font-weight:550;letter-spacing:-.8px;display:block;font-variant-numeric:tabular-nums}.kpis small{font-size:11px;color:var(--muted)}
.card{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:26px;min-width:0}
.card-head{display:flex;justify-content:space-between;gap:12px;align-items:start}
.legend{display:flex;gap:18px;flex-wrap:wrap;color:var(--muted);font-size:11px;margin:18px 0 6px}.legend span{display:inline-flex;gap:7px;align-items:center}.legend i{width:16px;height:4px;border-radius:2px;display:inline-block}
.chart{position:relative;touch-action:pan-y}.chart svg{display:block;width:100%;height:auto;overflow:visible}
.grid-line{stroke:var(--line);stroke-width:1}.axis{fill:var(--muted);font-size:11px}
.detail{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-top:14px;padding:14px 12px;background:var(--soft);border-radius:10px;font-size:11px;color:var(--muted)}
.detail b{display:block;color:var(--ink);font-size:18px;font-weight:550;font-variant-numeric:tabular-nums}
.note{font-size:11px;color:var(--muted);margin:14px 0 0;line-height:1.6}
.section-intro{display:flex;justify-content:space-between;align-items:end;gap:24px;border-top:1px solid var(--line);padding-top:30px;flex-wrap:wrap}
.section-intro p{margin:0;color:var(--muted);font-size:12px;max-width:440px}.section-intro b{color:var(--ink);font-weight:500}
.panels{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:24px 0 36px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:24px;min-width:0;transition:border-color .25s}
.panel:hover{border-color:#45648C}
.panel-title{display:flex;justify-content:space-between;align-items:center;gap:12px;border-bottom:1px solid var(--line);padding-bottom:14px;flex-wrap:wrap}.panel-title>span{font-size:11px;color:var(--muted)}
.row{padding:13px 0 3px;border-radius:6px}
.row-top{display:flex;justify-content:space-between;gap:12px;font-size:13px}.row-top strong{font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap}
.track{height:10px;background:var(--soft);border-radius:4px;margin:9px 0 5px;overflow:hidden}
.track>span{display:block;height:100%;border-radius:4px;background:var(--blue);transform-origin:left;animation:grow .7s cubic-bezier(.2,.7,.3,1) both}
.track>span.alt{background:var(--orange)}.track>span.muted{background:var(--prior)}
.row-meta{font-size:11px;color:var(--muted)}
.row.flag .row-top span:first-child:after{content:' · below display threshold';color:var(--muted);font-size:11px}
.decision{display:grid;grid-template-columns:120px 1fr 230px;gap:28px;align-items:center;background:var(--soft);border:1px solid var(--line);border-radius:18px;padding:28px;margin-bottom:32px}
.decision-index{font-size:25px;color:var(--blue);line-height:1.3}.decision-index span{display:block;font-size:11px;letter-spacing:.5px;margin-top:6px;font-weight:600}
.decision h2{font-size:22px;margin:0 0 8px}.decision p{font-size:13px;color:var(--muted);line-height:1.7;margin:0}
.decision-note{font-size:12px;color:var(--muted);border-left:1px solid #45648C;padding-left:22px}.decision-note b{color:var(--ink);font-weight:500}
.links{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 30px}
.links a{display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border:1px solid var(--line);border-radius:10px;text-decoration:none;font-size:13px;color:var(--ink);background:var(--card)}
.links a:hover{border-color:var(--blue)}
footer{padding:0 0 30px;color:var(--muted);font-size:11px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px 20px}footer p{flex:1 1 100%;margin:4px 0}
.headline{animation:arrive .8s cubic-bezier(.16,.8,.2,1) both}.overview .card{animation:arrive .9s .1s cubic-bezier(.16,.8,.2,1) both}
.bar-mark{transition:opacity .2s}.dim{opacity:.35}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes arrive{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@media(max-width:1200px){body{grid-template-columns:180px minmax(0,1fr)}.rail{padding:28px 18px}main{padding:24px 28px 0}.overview{grid-template-columns:1fr}.decision{grid-template-columns:90px 1fr}.decision-note{grid-column:2}}
@media(max-width:760px){body{display:block}.rail{position:static;height:auto;display:grid;grid-template-columns:54px 1fr;gap:16px;padding:20px 16px}.brand{font-size:25px}.rail-name{font-size:20px}.rail-name br{display:none}.rail nav{grid-template-columns:repeat(3,1fr);grid-column:1/-1;gap:6px}.rail nav a{text-align:center;padding:10px 4px;font-size:12px}.rail-window,.rail-credit{display:none}main{padding:20px 16px 0}h1{font-size:44px;letter-spacing:-1.8px}.big{font-size:44px}.card{padding:20px 16px}.panels{grid-template-columns:1fr}.panel{padding:20px}.decision{grid-template-columns:1fr;padding:22px;gap:14px}.decision-note{grid-column:auto;border:0;padding:0}.kpis strong{font-size:24px}select{min-width:0}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.headline,.overview .card,.track>span{animation:none}.rail nav a{transition:none}.rail nav a:hover{transform:none}}
"""

HELPERS_JS = r"""
'use strict';
const $=id=>document.getElementById(id);
const DATA=JSON.parse($('report-data').textContent);
const int=v=>Math.round(v).toLocaleString('en-US');
const pct=(v,d=1)=>v==null||!isFinite(v)?'—':(v*100).toFixed(d)+'%';
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function seg(id,options,value,onChange){
  const el=$(id);el.innerHTML=options.map(([v,l])=>`<button type="button" data-v="${esc(v)}" aria-pressed="${v===value}">${esc(l)}</button>`).join('');
  el.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;el.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b));onChange(b.dataset.v);});
}
function bars(rows,{value,label,right,meta,cls,max}){
  const m=max??Math.max(1,...rows.map(value));
  return rows.map((r,i)=>`<div class="row${r.flag?' flag':''}" tabindex="0" title="${esc(label(r)+': '+right(r))}"><div class="row-top"><span>${esc(label(r))}</span><strong>${esc(right(r))}</strong></div><div class="track" aria-hidden="true"><span class="${cls?cls(r):''}" style="width:${(100*Math.max(0,value(r))/m).toFixed(2)}%;animation-delay:${i*.04}s"></span></div><div class="row-meta">${esc(meta(r))}</div></div>`).join('');
}
function watchSections(ids){
  const links=[...document.querySelectorAll('.rail nav a')];
  const update=()=>{let current=ids[0];for(const id of ids){if($(id).getBoundingClientRect().top<innerHeight*.4)current=id;}
    if(innerHeight+scrollY>=document.documentElement.scrollHeight-4)current=ids[ids.length-1];
    links.forEach(a=>a.toggleAttribute('aria-current',a.hash==='#'+current));};
  addEventListener('scroll',update,{passive:true});addEventListener('resize',update);update();
}
"""


def page(*, title: str, description: str, rail_name: str, nav: list[tuple[str, str]],
         window_label: str, window_value: str, credit: str, identity: str, period: str,
         body: str, data: dict, script: str) -> str:
    """Assemble a complete, self-contained HTML document."""
    rail_name = rail_name.replace("<br>", " <br>")
    nav_html = "".join(f'<a href="#{i}">{html.escape(l)}</a>' for i, l in nav)
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<meta name=\"author\" content=\"Zak Rademacher\">"
        f"<meta name=\"description\" content=\"{html.escape(description)}\">"
        f"<title>{html.escape(title)}</title><style>{CSS}</style></head>\n"
        "<body><aside class=\"rail\" aria-label=\"Report navigation\">"
        f"<a href=\"#{nav[0][0]}\" class=\"brand\">ZR /</a><div class=\"rail-name\">{rail_name}</div>"
        f"<nav>{nav_html}</nav><div class=\"rail-window\"><span>{html.escape(window_label)}</span>{window_value}</div>"
        f"<div class=\"rail-credit\">{credit}</div></aside><main>\n"
        f"<header class=\"masthead\"><a href=\"#{nav[0][0]}\" class=\"identity\">{html.escape(identity)}</a>"
        f"<div class=\"period\"><i></i>{period}</div></header>\n"
        f"{body}\n</main>"
        f"<script type=\"application/json\" id=\"report-data\">{payload}</script>"
        f"<script>{HELPERS_JS}\n{script}</script></body></html>\n"
    )
