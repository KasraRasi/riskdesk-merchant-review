"""Generate self-contained offline HTML with all synthetic data embedded."""
import csv, json
from pathlib import Path
from core import assess, metrics
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'

def generate():
    with (ROOT/'data'/'synthetic_merchants.csv').open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    cases=[]
    for r in rows:
        a=assess(r)
        cases.append({k:v for k,v in r.items() if k!='ground_truth_fraud'} | {
            'score':a.score,'priority':a.priority,'reasons':a.reasons,
            'counterevidence':a.counterevidence,'next_steps':a.next_steps})
    result=json.loads((OUT/'evaluation.json').read_text())
    json_cases=json.dumps(cases,ensure_ascii=True).replace('</','<\\/')
    json_metrics=json.dumps(result['threshold_results']).replace('</','<\\/')
    html = r'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>RiskDesk | Merchant Review Lab</title>
<style>
:root{--bg:#f3f6fa;--ink:#172338;--muted:#64738a;--navy:#101e34;--blue:#2b66b9;--teal:#0e7f78;--red:#ad3e40;--amber:#a96517;--line:#dfe6ee;--white:#fff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Arial}
header{background:var(--navy);color:white;padding:28px max(24px,calc((100vw - 1300px)/2)) 30px}
.header-top{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}h1{font-size:28px;letter-spacing:-.8px;margin:4px 0 4px;font-weight:760}.tag{display:inline-block;background:#213650;border:1px solid #415a79;border-radius:20px;font-size:11px;letter-spacing:1.4px;padding:4px 10px;font-weight:800;color:#dcecff}
header p{color:#bac9db;max-width:720px;margin:5px 0 0}.important{color:#f4cb80!important;font-size:12px}
.layout{max-width:1350px;margin:22px auto;padding:0 18px 30px}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}.metric{background:white;padding:17px 20px;border-radius:10px;border:1px solid var(--line);box-shadow:0 2px 10px #16273908}.metric .label{font-size:11px;letter-spacing:.7px;text-transform:uppercase;color:var(--muted);font-weight:750}.metric strong{display:block;font-size:26px;letter-spacing:-.8px;margin:1px 0;color:var(--ink)}.metric small{color:var(--muted);font-size:12px}
.main{display:grid;grid-template-columns:minmax(350px,.95fr) minmax(400px,1.2fr);gap:16px;align-items:start}.panel{border-radius:12px;background:var(--white);border:1px solid var(--line);box-shadow:0 2px 10px #13233808;min-width:0}
.panelheader{padding:19px 21px;border-bottom:1px solid var(--line)}h2{font-size:17px;margin:0 0 5px;letter-spacing:-.3px}h3{font-size:12px;text-transform:uppercase;letter-spacing:.7px;margin:20px 0 8px;color:#344761}.meta{font-size:12px;color:var(--muted)}
.controls{padding:13px 19px;display:flex;flex-direction:column;gap:10px;border-bottom:1px solid var(--line)}input,select{font:inherit;border:1px solid #d5e0eb;border-radius:7px;padding:9px 11px;outline:none;background:#fbfdff;color:#223049;width:100%}input:focus,select:focus{border-color:#4485cf;box-shadow:0 0 0 2px #4485cf20}.filters{display:flex;gap:7px}.filters button{flex:1;font-size:12px;padding:7px 6px;border:1px solid #dfe6ee;background:#fff;color:#4a5e77;border-radius:7px;cursor:pointer;font-weight:700}.filters button.active{background:#eaf1fb;border-color:#8eafe1;color:#1d4f97}
.queuelist{max-height:710px;overflow-y:auto}.item{padding:13px 19px;border-bottom:1px solid #eaf0f6;cursor:pointer;display:grid;grid-template-columns:1fr auto;gap:7px}.item:hover{background:#f8fbff}.item.active{background:#eef5ff;border-left:3px solid #3c78c6;padding-left:16px}.itemtop{font-weight:800}.itemsub{font-size:12px;color:var(--muted);margin-top:1px}.score{font-weight:800;font-variant-numeric:tabular-nums;font-size:17px}.pill{display:inline-block;padding:3px 8px;border-radius:30px;font-size:11px;font-weight:800}.high{background:#fcebec;color:#a33f48}.medium{background:#fff0de;color:#9b5a13}.low{background:#e6f5ef;color:#187155}.dot{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:6px;background:currentColor}
.detail{padding:21px}.detailtitle{font-size:25px;font-weight:800;letter-spacing:-.8px}.desccards{display:grid;grid-template-columns:repeat(2,1fr);gap:9px;margin:17px 0}.dcard{border:1px solid #e3eaf2;border-radius:8px;padding:10px 13px;background:#fafcff}.dcard .small{font-size:11px;color:var(--muted);text-transform:uppercase;font-weight:760;letter-spacing:.45px}.dcard b{display:block;font-size:15px;margin-top:2px}.signals{padding-left:20px;margin:4px 0 8px}.signals li{padding:4px 0}.callout{background:#edf6f8;border-left:3px solid #0b7d83;padding:13px 15px;margin-top:15px;border-radius:4px;font-size:13px}.callout strong{color:#0b6170}.muted{color:var(--muted)}
.footerpanel{margin-top:16px;padding:19px 21px}.thresholds{width:100%;border-collapse:collapse;font-size:13px}.thresholds th{text-align:right;color:#57657a;font-size:11px;text-transform:uppercase;letter-spacing:.3px;padding:9px 4px;border-bottom:1px solid var(--line)}.thresholds td{text-align:right;padding:9px 4px;border-bottom:1px solid #edf1f6;font-variant-numeric:tabular-nums}.thresholds tr.current{background:#edf4ff}.thresholds th:first-child,.thresholds td:first-child{text-align:left}.fine{font-size:11.5px;color:#6b798c;margin:11px 0 0}

.empty{padding:18px;color:#6b7e94;text-align:center}
.analystreview{background:#f7faff;border:1px solid #dce7f7;padding:17px;border-radius:9px;margin-top:19px}
.analystreview h3{margin:0 0 4px}.analystreview p{margin:5px 0 10px;font-size:12px;color:var(--muted)}
.analystreview textarea{width:100%;padding:10px 11px;border:1px solid #cedbed;border-radius:7px;min-height:96px;resize:vertical;font:inherit;background:white}
.analystreview textarea:focus{outline:2px solid #7fa9db;outline-offset:1px}
.actionrow{display:flex;gap:8px;align-items:center;margin-top:8px;flex-wrap:wrap}
.actionrow button{border:0;border-radius:7px;background:#1c5eaa;color:#fff;padding:9px 12px;font:inherit;font-weight:700;cursor:pointer}
.actionrow button.secondary{background:#fff;color:#24578c;border:1px solid #8dadcf}
.actionrow button:hover{filter:brightness(.94)}.savedstate{font-size:12px;color:#267960}
.queuehint{font-size:10px;color:#52718a}

@media(max-width:950px){.metrics{grid-template-columns:repeat(2,1fr)}.main{grid-template-columns:1fr}.queuelist{max-height:360px}}
@media(max-width:500px){.metrics{gap:8px}.metric{padding:12px}.metric strong{font-size:23px}h1{font-size:23px}.desccards{grid-template-columns:1fr}}
</style></head>
<body><header><div class="header-top"><div><span class="tag">INDEPENDENT PORTFOLIO DEMO</span><h1>RiskDesk <span style="color:#5ac4bb">/</span> Merchant Review Lab</h1><p>Investigate evidence, triage conflicting signals and document proportionate next steps - without equating unusual activity with fraud.</p></div><div style="text-align:right"><div style="font-size:12px;color:#bfd4e6">Evidence-led merchant risk review</div><div style="font-size:13px;font-weight:650">Risk operations + explainable analytics</div></div></div><p class="important">SYNTHETIC MERCHANTS ONLY · Review scores do not authorize account holds, rejections or payout changes · Not affiliated with CPOS</p></header>
<main class="layout"><section class="metrics" id="metrics"></section><section class="main"><div class="panel"><div class="panelheader"><h2>Merchant investigation queue</h2><div class="meta">Score = review priority points, not probability of fraud. Select any case for evidence.</div></div><div class="controls"><input id="search" placeholder="Search merchant ID or sector" aria-label="Search merchant queue"><div class="filters"><button data-filter="all" class="active">All</button><button data-filter="high">High</button><button data-filter="medium">Medium</button><button data-filter="low">Low</button></div><select id="order" aria-label="Queue order"><option value="score">Highest priority first</option><option value="id">Merchant ID</option><option value="sector">Business type</option></select><div class="meta" id="count"></div></div><div class="queuelist" id="list"></div></div><div class="panel"><div class="panelheader"><h2>Evidence-based case review</h2><div class="meta">Demonstrates analyst reasoning, verification requests and proportional response.</div></div><div class="detail" id="detail"></div></div></section>
<section class="panel footerpanel"><h2>Review-threshold trade-offs <span style="font-weight:400;font-size:12px;color:#6b7a90">(offline evaluation against synthetic outcomes)</span></h2><p class="meta">Lower thresholds catch more simulated fraud but require more reviews and create more friction for legitimate merchants. These figures are not real-world performance claims.</p><div style="overflow:auto"><table class="thresholds" id="thresholds"><thead><tr><th>Review score ≥</th><th>Precision</th><th>Recall</th><th>Legitimate cases flagged</th><th>Fraud cases missed</th><th>Review queue</th></tr></thead><tbody></tbody></table></div><p class="fine">Metrics are based on intentionally simulated labels and relationships. The production decision needs independent evidence, an authorized analyst and company-approved policy. Ground-truth labels are never displayed in case review.</p></section><div style="margin:16px 3px;color:#66768a;font-size:12px">Designed to spark discussion about KYB verification, documentation, merchant communication, audit trails, rule calibration and human oversight. This demo uses no real merchants or platform integration.</div></main>
<script>
const CASES=__CASE_JSON__;
const METRICS=__METRIC_JSON__;
const $=id=>document.getElementById(id);
let filter='all',selected='M-0001';
const REVIEW_KEY='riskdesk_review_notes_v1';
let reviewNotes={};
try{reviewNotes=JSON.parse(localStorage.getItem(REVIEW_KEY)||'{}')||{}}catch(e){reviewNotes={}}
function persistReviews(){try{localStorage.setItem(REVIEW_KEY,JSON.stringify(reviewNotes));return true}catch(e){return false}}
function reviewStatus(id){return reviewNotes[id]?.status||''}
function csvVal(s){return '"'+String(s??'').replace(/"/g,'""')+'"'}
function exportReviews(){const rows=[['merchant_id','analyst_status','review_notes','saved_at'],...Object.entries(reviewNotes).sort().map(([id,r])=>[id,r.status,r.notes,r.updatedAt])];const csv=rows.map(r=>r.map(csvVal).join(',')).join('\r\n');const blob=new Blob([csv],{type:'text/csv;charset=utf-8;'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='riskdesk_analyst_review_log.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
function saveReview(id){const status=$('reviewstatus').value;const notes=$('reviewmemo').value.trim();reviewNotes[id]={status,notes,updatedAt:new Date().toISOString()};const persisted=persistReviews();renderList();const m=$('savefeedback');if(m)m.textContent=persisted?'Saved in this browser (demo only).':'Saved for this page session; browser storage unavailable.'}

const sorted=CASES.slice().sort((a,b)=>b.score-a.score);
const esc=s=>String(s??'').replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function level(a){return a.score>=70?'high':a.score>=35?'medium':'low'}
function renderMetrics(){const m=METRICS.find(x=>x.threshold===35);const chunks=[['Synthetic merchants',String(m.n),'For repeatable offline evaluation'],['Cases queued',String(m.review_queue),'At illustrative score ≥ 35'],['Precision',Math.round(m.precision*100)+'%','Among synthetic cases sent to review'],['Recall',Math.round(m.recall*100)+'%','Of synthetic fraud labels identified']];$('metrics').innerHTML=chunks.map(x=>`<div class="metric"><div class="label">${x[0]}</div><strong>${x[1]}</strong><small>${x[2]}</small></div>`).join('')}
function renderList(){const q=$('search').value.trim().toLowerCase(),order=$('order').value;let rows=CASES.filter(c=>(filter==='all'||level(c)===filter)&&(!q||c.merchant_id.toLowerCase().includes(q)||c.sector.toLowerCase().includes(q)));rows.sort(order==='score'?(a,b)=>b.score-a.score:order==='sector'?(a,b)=>a.sector.localeCompare(b.sector): (a,b)=>a.merchant_id.localeCompare(b.merchant_id));$('count').textContent=`${rows.length} merchant cases shown · ${CASES.length} total`;const set=rows.slice(0,90);$('list').innerHTML=set.map(c=>`<div class="item ${c.merchant_id===selected?'active':''}" role="button" tabindex="0" data-id="${c.merchant_id}"><div><div class="itemtop">${c.merchant_id} <span style="font-weight:500;color:#64738a">· ${esc(c.sector)}</span></div><div class="itemsub"><span class="pill ${level(c)}"><span class="dot"></span>${level(c).toUpperCase()}</span> &nbsp; ${c.reasons.length} risk signals ${reviewStatus(c.merchant_id)?`<span class="queuehint">· Memo saved</span>`:''}</div></div><div class="score">${c.score}<span style="font-size:10px;font-weight:500"> pts</span></div></div>`).join('')+(rows.length>90?`<div class="empty">Showing first 90; refine search to find others</div>`:'');if(!rows.length)$('list').innerHTML='<div class="empty">No matching cases</div>';document.querySelectorAll('.item').forEach(e=>{function choose(){selected=e.dataset.id;renderList();renderDetail()}e.addEventListener('click',choose);e.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();choose()}})})}
function renderDetail(){const c=CASES.find(x=>x.merchant_id===selected)||CASES[0];const levelName=level(c);let detail=`<div style="display:flex;justify-content:space-between;align-items:center;gap:6px;flex-wrap:wrap"><div class="detailtitle">${esc(c.merchant_id)}</div><span class="pill ${levelName}">${levelName.toUpperCase()} REVIEW PRIORITY</span></div><div class="meta">${esc(c.sector)} · ${esc(c.merchant_age_days)} days in business · score ${c.score} points</div><div class="desccards">`;
const fields=[['KYC status',c.kyc_status],['Business registration',c.registration_status],['Payout bank name',c.bank_name_match==='1'?'Matches':'Mismatch'],['Invoice evidence',c.invoice_evidence],['7-day activity vs expected',Number(c.volume_spike_ratio).toFixed(2)+'×'],['Disputes (30d)',`${c.disputes_30d} / ${c.tx_count_30d}`]];
detail+=fields.map(([t,v])=>`<div class="dcard"><div class="small">${esc(t)}</div><b>${esc(v)}</b></div>`).join('')+'</div>';
for(const [title,items] of [['Potential concerns',c.reasons],['Counterevidence / benign explanations',c.counterevidence],['Proportionate next steps',c.next_steps]]){detail+=`<h3>${title}</h3><ul class="signals">${(items.length?items:['No concerns recorded at this stage.']).map(s=>`<li>${esc(s)}</li>`).join('')}</ul>`}
detail+=`<div class="callout"><strong>Analyst judgment, not an automated hold:</strong> ${esc(c.evidence_note)} An analyst should verify the facts, request only necessary documents, explain the next steps to the merchant, and record the final decision and reasoning.</div>`;
const prior=reviewNotes[c.merchant_id]||{};
const choices=['Needs verification','Request additional documents','Escalate for specialist review','Routine monitoring','Review complete'];
detail+=`<section class="analystreview"><h3>Analyst decision log · interactive demonstration</h3><p>Practice a defensible human review. Notes are stored only in this browser; nothing is sent to a server and no merchant account is changed.</p><label for="reviewstatus">Review status</label><select id="reviewstatus" aria-label="Review status">${choices.map(x=>`<option value="${esc(x)}" ${prior.status===x?'selected':''}>${esc(x)}</option>`).join('')}</select><label for="reviewmemo" style="display:block;margin-top:10px">Rationale, evidence gaps and next step</label><textarea id="reviewmemo" placeholder="Write what you would verify, what evidence supports the decision, and when to follow up.">${esc(prior.notes||'')}</textarea><div class="actionrow"><button type="button" id="savereview">Save review note</button><button type="button" class="secondary" id="exportreviews">Export review log (CSV)</button><span class="savedstate" id="savefeedback">${prior.updatedAt?'Previous review loaded.':''}</span></div></section>`;$('detail').innerHTML=detail;$('savereview').addEventListener('click',()=>saveReview(c.merchant_id));$('exportreviews').addEventListener('click',exportReviews)}
function renderThresholds(){const target=$('thresholds').querySelector('tbody');target.innerHTML=METRICS.map(m=>`<tr class="${m.threshold===35?'current':''}"><td><b>${m.threshold}${m.threshold===35?' · illustrative default':''}</b></td><td>${Math.round(m.precision*100)}%</td><td>${Math.round(m.recall*100)}%</td><td>${m.fp}</td><td>${m.fn}</td><td>${m.review_queue}</td></tr>`).join('')}
$('search').addEventListener('input',renderList);$('order').addEventListener('change',renderList);document.querySelectorAll('.filters button').forEach(b=>b.addEventListener('click',()=>{filter=b.dataset.filter;document.querySelectorAll('.filters button').forEach(n=>n.classList.remove('active'));b.classList.add('active');renderList()}));renderMetrics();renderList();renderDetail();renderThresholds();
</script></body></html>'''
    html=html.replace('__CASE_JSON__',json_cases).replace('__METRIC_JSON__',json_metrics)
    p=OUT/'riskdesk_demo.html'
    p.write_text(html,encoding='utf-8')
    print('Created',p,p.stat().st_size,'bytes')

if __name__=='__main__':generate()
