"""Build the interactive web version of the hotel cancellation review.

Reads data/processed/comparison-cells.csv and controls.json and writes
report/index.html, a self-contained page for GitHub Pages. Standard library only.

    python tools/build_web_report.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from web_report_shell import page

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUT = ROOT / "report" / "index.html"


def load() -> dict:
    cells = []
    with open(PROCESSED / "comparison-cells.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cells.append([
                0 if r["hotel"] == "City Hotel" else 1,
                r["period"],
                r["segment"],
                r["lead_band"],
                int(r["bookings"]),
                int(r["cancellations"]),
                int(r["canceled_booked_nights"]),
            ])
    controls = json.loads((PROCESSED / "controls.json").read_text(encoding="utf-8"))
    total_bookings = sum(c[4] for c in cells)
    total_cancellations = sum(c[5] for c in cells)
    if total_bookings != controls["all"]["bookings"] or total_cancellations != controls["all"]["cancellations"]:
        raise SystemExit("comparison cells do not reconcile to control totals")
    return {"cells": cells, "controls": controls}


BODY = r"""
<div class="controls" aria-label="Report filters">
  <div class="control"><span>HOTEL</span><div class="seg" id="f-hotel"></div></div>
  <div class="control"><span>ARRIVAL YEAR</span><div class="seg" id="f-year"></div></div>
  <div class="control"><label for="f-month"><span class="eyebrow">ARRIVAL MONTH</span></label><select id="f-month"></select></div>
</div>
<section class="overview" id="overview">
  <div class="headline">
    <div class="eyebrow"><span class="num">01</span>THE CANCELLATION STORY</div>
    <h1>Most cancellations.<br><span>Not the highest rate.</span></h1>
    <p class="standfirst">The segment that creates the most cancellation work and the segment most likely to cancel are different groups. Use the filters to compare them for any hotel, year or month.</p>
    <div class="big-label">CANCELLATION RATE <span id="scope-label"></span></div>
    <div class="big" id="k-rate">—</div>
    <div class="context"><span class="pill" id="k-cancel">—</span><span>cancellations among <b id="k-book">—</b> bookings</span></div>
    <div class="kpis">
      <div><span>LARGEST WORKLOAD</span><strong id="k-work">—</strong><small id="k-work-n"></small></div>
      <div><span>HIGHEST RATE (100+ BOOKINGS)</span><strong id="k-hi">—</strong><small id="k-hi-n"></small></div>
      <div><span>CANCELED BOOKED NIGHTS</span><strong id="k-nights">—</strong><small>workload, not lost revenue</small></div>
      <div><span>AVERAGE NIGHTS PER CANCELLATION</span><strong id="k-npc">—</strong><small>booked nights ÷ cancellations</small></div>
    </div>
  </div>
  <section class="card" aria-labelledby="trend-title">
    <div class="card-head"><div><div class="eyebrow" id="trend-eyebrow">BY ARRIVAL MONTH</div><h2 id="trend-title">Cancellations and rate through the year</h2></div></div>
    <div class="legend"><span><i style="background:var(--blue)"></i>Cancellations</span><span><i style="background:var(--orange)"></i>Cancellation rate</span><span>Select a month to filter the report</span></div>
    <div id="trend" class="chart"></div>
    <div class="detail" aria-live="polite"><span>Month <b id="d-month">—</b></span><span>Bookings <b id="d-book">—</b></span><span>Cancellations <b id="d-cancel">—</b></span><span>Rate <b id="d-rate">—</b></span></div>
    <p class="note">2016 is the only complete year; July 2015 to August 2017 is covered. Each bar is the arrival month. Exact repeats in the source are kept because it has no booking ID that would prove them duplicates.</p>
  </section>
</section>
<section id="segments">
  <div class="section-intro"><div><div class="eyebrow"><span class="num">02</span>COUNT VERSUS RATE</div><h2>Where the follow-up work sits</h2></div>
  <div class="control"><span>SORT AND SIZE BARS BY</span><div class="seg" id="f-measure"></div></div></div>
  <div class="panels">
    <section class="panel"><div class="panel-title"><h3>Market segment</h3><span id="seg-unit"></span></div><div id="seg-bars"></div></section>
    <section class="panel"><div class="panel-title"><h3>Lead time before arrival</h3><span id="lead-unit"></span></div><div id="lead-bars"></div></section>
  </div>
</section>
<section class="decision" id="decision"><div class="decision-index">03<span>THE NEXT CHECK</span></div>
  <div><h2>Treat Online TA and Groups as two separate leads.</h2><p>For the City Hotel in 2016, Online TA produced 7,149 cancellations, the largest workload. Groups cancelled at 74.7%, the highest rate among segments with 100 or more bookings. Before trialling a confirmation process, compare lead times, deposit terms and arrival-month mix for each group.</p></div>
  <div class="decision-note">Historical differences.<br><b>They don't show how much a new process would reduce cancellations.</b></div></section>
<nav class="links" aria-label="Project links"><a href="https://github.com/ZakJRademacher/hotel-booking-cancellation-analysis">Project repository</a><a href="https://github.com/ZakJRademacher/hotel-booking-cancellation-analysis/blob/main/docs/DECISION_MEMO.md">Decision memo</a><a href="https://github.com/ZakJRademacher/hotel-booking-cancellation-analysis/blob/main/docs/METHOD.md">Method</a><a href="https://github.com/ZakJRademacher/hotel-booking-cancellation-analysis/raw/main/deliverables/Hotel%20Cancellation%20Review.twbx">Tableau workbook (.twbx)</a></nav>
<footer><span id="foot-totals"></span><span>Independent portfolio analysis of historical public data</span>
<p>Source: Antonio, de Almeida &amp; Nunes (2019), “Hotel booking demand datasets”, <i>Data in Brief</i> 22, 41–49, CC BY 4.0; adapted into grouped reporting tables. Full attribution is in <a href="https://github.com/ZakJRademacher/hotel-booking-cancellation-analysis/blob/main/docs/SOURCES.md">docs/SOURCES.md</a>. Canceled booked nights describe workload and booking volume; they don't establish lost revenue or capacity. The interactive figures are computed in the browser from the project's published comparison cells and reconcile to its control totals.</p></footer>
"""

SCRIPT = r"""
const MONTHS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const HOTELS=['City Hotel','Resort Hotel'];
const cells=DATA.cells.map(([h,p,s,l,b,c,n])=>({h,y:p.slice(0,4),m:+p.slice(5),s,l,b,c,n}));
const state={hotel:'0',year:'2016',month:0,measure:'count'};
const yearsPresent=[...new Set(cells.map(c=>c.y))].sort();
function inScope(c,ignoreMonth){return(state.hotel==='all'||c.h===+state.hotel)&&c.y===state.year&&(ignoreMonth||!state.month||c.m===state.month);}
function sum(rows){return rows.reduce((a,c)=>(a.b+=c.b,a.c+=c.c,a.n+=c.n,a),{b:0,c:0,n:0});}
function groupBy(rows,key){const g=new Map();for(const r of rows){const k=r[key];const a=g.get(k)||{key:k,b:0,c:0,n:0};a.b+=r.b;a.c+=r.c;a.n+=r.n;g.set(k,a);}return[...g.values()].map(a=>({...a,rate:a.b?a.c/a.b:null}));}
function scopeName(){const h=state.hotel==='all'?'Both hotels':HOTELS[+state.hotel];return h+', '+(state.month?MONTHS[state.month-1]+' ':'')+state.year+(state.year==='2016'?'':' (partial year)');}
const monthSel=$('f-month');
function fillMonths(){
  const present=[...new Set(cells.filter(c=>inScope(c,true)).map(c=>c.m))].sort((a,b)=>a-b);
  if(state.month&&!present.includes(state.month))state.month=0;
  monthSel.innerHTML='<option value="0">All months</option>'+present.map(m=>`<option value="${m}">${MONTHS[m-1]}</option>`).join('');
  monthSel.value=String(state.month);
}
monthSel.addEventListener('change',()=>{state.month=+monthSel.value;render();});
function trend(){
  const rows=cells.filter(c=>inScope(c,true));
  const byM=new Map(groupBy(rows,'m').map(r=>[r.key,r]));
  const months=[...byM.keys()].sort((a,b)=>a-b);
  const W=720,H=290,L=52,R=46,T=16,B=34,maxC=Math.max(1,...months.map(m=>byM.get(m).c));
  const step=(W-L-R)/Math.max(months.length,1),bw=Math.min(38,step*.62);
  const nice=Math.pow(10,Math.floor(Math.log10(maxC)));const top=Math.ceil(maxC/nice)*nice;
  const y=v=>T+(1-v/top)*(H-T-B),yr=v=>T+(1-v)*(H-T-B),x=i=>L+step*(i+.5);
  let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Cancellations and cancellation rate by arrival month for ${esc(scopeName())}">`;
  for(let k=0;k<=4;k++){const v=top*k/4;s+=`<line class="grid-line" x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}"/><text class="axis" x="${L-10}" y="${y(v)+4}" text-anchor="end">${int(v)}</text><text class="axis" x="${W-R+10}" y="${y(v)+4}">${k*25}%</text>`;}
  months.forEach((m,i)=>{const r=byM.get(m);const sel=state.month===m;
    s+=`<rect class="bar-mark${state.month&&!sel?' dim':''}" data-m="${m}" x="${x(i)-bw/2}" y="${y(r.c)}" width="${bw}" height="${H-B-y(r.c)}" rx="4" fill="var(--blue)" tabindex="0" role="button" aria-label="${MONTHS[m-1]}: ${int(r.c)} cancellations of ${int(r.b)} bookings, ${pct(r.rate)}"><title>${MONTHS[m-1]} — ${int(r.c)} of ${int(r.b)} (${pct(r.rate)})</title></rect>`;
    s+=`<text class="axis" x="${x(i)}" y="${H-12}" text-anchor="middle">${MONTHS[m-1]}</text>`;});
  if(months.length>1)s+=`<path d="${months.map((m,i)=>(i?'L':'M')+x(i).toFixed(1)+','+yr(byM.get(m).rate).toFixed(1)).join(' ')}" fill="none" stroke="var(--orange)" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>`;
  months.forEach((m,i)=>{s+=`<circle cx="${x(i)}" cy="${yr(byM.get(m).rate)}" r="${state.month===m?6:4}" fill="var(--orange)" stroke="var(--card)" stroke-width="2"/>`;});
  $('trend').innerHTML=s+'</svg>';
  $('trend').querySelectorAll('.bar-mark').forEach(b=>{const pick=()=>{const m=+b.dataset.m;state.month=state.month===m?0:m;monthSel.value=String(state.month);render();};b.addEventListener('click',pick);b.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();pick();}});});
  const d=state.month?byM.get(state.month):sum(rows);
  $('d-month').textContent=state.month?MONTHS[state.month-1]+' '+state.year:'All '+state.year;$('d-book').textContent=int(d.b);$('d-cancel').textContent=int(d.c);$('d-rate').textContent=pct(d.b?d.c/d.b:null);
}
function panel(id,unitId,key,sortKey){
  let rows=groupBy(cells.filter(c=>inScope(c)),key).filter(r=>r.b>0);
  const byRate=state.measure==='rate';
  rows.forEach(r=>r.flag=byRate&&r.b<100);
  rows.sort(sortKey||((a,b)=>byRate?((b.flag?-1:b.rate)-(a.flag?-1:a.rate)):b.c-a.c));
  $(unitId).textContent=byRate?'CANCELLATION RATE':'CANCELLATIONS';
  $(id).innerHTML=bars(rows,{value:r=>byRate?r.rate:r.c,max:byRate?1:undefined,label:r=>key==='l'?r.key.slice(4):r.key,right:r=>byRate?pct(r.rate):int(r.c),cls:r=>byRate?(r.flag?'muted':'alt'):'',meta:r=>`${int(r.c)} of ${int(r.b)} bookings · ${pct(r.rate)} · ${int(r.n)} canceled nights`});
}
function kpis(){
  const rows=cells.filter(c=>inScope(c)),t=sum(rows),segs=groupBy(rows,'s');
  $('scope-label').textContent=scopeName();$('k-rate').textContent=pct(t.b?t.c/t.b:null);$('k-cancel').textContent=int(t.c);$('k-book').textContent=int(t.b);
  $('k-nights').textContent=int(t.n);$('k-npc').textContent=t.c?(t.n/t.c).toFixed(1):'—';
  const work=[...segs].sort((a,b)=>b.c-a.c)[0],hi=segs.filter(s=>s.b>=100).sort((a,b)=>b.rate-a.rate)[0];
  $('k-work').textContent=work?work.key:'—';$('k-work-n').textContent=work?int(work.c)+' cancellations':'';
  $('k-hi').textContent=hi?hi.key:'—';$('k-hi-n').textContent=hi?pct(hi.rate)+' of '+int(hi.b):'No segment with 100+ bookings';
}
function render(){fillMonths();kpis();trend();panel('seg-bars','seg-unit','s');panel('lead-bars','lead-unit','l',state.measure==='rate'?null:(a,b)=>a.key.localeCompare(b.key));}
seg('f-hotel',[['0','City Hotel'],['1','Resort Hotel'],['all','Both']],state.hotel,v=>{state.hotel=v;render();});
seg('f-year',yearsPresent.map(y=>[y,y==='2016'?'2016':y+' (partial)']),state.year,v=>{state.year=v;state.month=0;render();});
seg('f-measure',[['count','Cancellations'],['rate','Rate']],state.measure,v=>{state.measure=v;render();});
const ct=DATA.controls;$('foot-totals').textContent=`${int(ct.source_rows)} booking records · ${int(ct.all.cancellations)} cancellations · ${int(ct.exact_repeats_retained)} exact repeats retained`;
render();watchSections(['overview','segments','decision']);
"""


def main() -> None:
    data = load()
    html_text = page(
        title="Hotel Cancellation Review",
        description="Interactive review of hotel booking cancellations: counts versus rates by segment, lead time and arrival month.",
        rail_name="Hotel<br>Cancellations",
        nav=[("overview", "Overview"), ("segments", "Count vs rate"), ("decision", "Next check")],
        window_label="COMPLETE YEAR",
        window_value="<strong>2016 arrivals</strong>July 2015–Aug 2017 in source",
        credit="HISTORICAL REVIEW<br>Two hotels, Portugal<br>Zak Rademacher",
        identity="HOSPITALITY / CANCELLATION REVIEW",
        period="2016 <span>/</span> HISTORICAL PUBLIC DATA",
        body=BODY,
        data=data,
        script=SCRIPT,
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html_text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(html_text):,} bytes)")


if __name__ == "__main__":
    main()
