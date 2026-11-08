#!/usr/bin/env python3
"""Renders sample-output screenshots (Blossom-styled widgets) for the seed skills → assets/shots/<skill>_<n>.jpg"""
import os, asyncio
from playwright.async_api import async_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'shots'); os.makedirs(OUT, exist_ok=True)
BASE = """<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet"><style>
:root{--purple:#7361F7;--lav:#EDE9FF;--teal:#35C7B2;--tealt:#E1F4F1;--green:#12BD57;--red:#E70037;--orange:#FF7733;--yellow:#F6C000;--ink:#171717;--text:#3F3F46;--muted:#72777F;--border:#E3E3E3;--bg:#F1F5F7}
body{margin:0;background:var(--bg);font-family:Nunito,sans-serif;color:var(--text);font-size:14px;-webkit-font-smoothing:antialiased}
.frame{width:900px;padding:22px;box-sizing:border-box}
.card{background:#fff;border-radius:14px;box-shadow:0 2px 4px 2px rgba(0,0,0,.04);padding:18px 22px;margin-bottom:14px}
h2{margin:0 0 4px;font-size:18px;color:var(--ink)}.sub{color:var(--muted);font-size:12.5px;margin-bottom:14px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}.kpi{background:#fff;border-radius:12px;padding:14px 16px;box-shadow:0 2px 4px 2px rgba(0,0,0,.04)}.kpi span{font-size:12px;color:var(--muted);display:block}.kpi b{font-size:22px;color:var(--ink)}
table{width:100%;border-collapse:collapse;font-size:13.5px}th{text-align:left;color:var(--muted);font-weight:600;font-size:12px;padding:6px 8px;border-bottom:1px solid var(--border)}td{padding:9px 8px;border-bottom:1px solid #F0F0F0;color:var(--text)}td b{color:var(--ink)}
.up{color:var(--green);font-weight:700}.dn{color:var(--red);font-weight:700}
.chip{display:inline-block;border-radius:999px;padding:2px 9px;font-size:11.5px;font-weight:700}.chip.p{background:var(--lav);color:#4D35EB}.chip.t{background:var(--tealt);color:#409082}.chip.o{background:#FFE4D6;color:#C2410C}.chip.r{background:#FCD9E1;color:#B1002B}
.bars{display:flex;align-items:flex-end;gap:10px;height:170px;padding:8px 0 0}.bar{flex:1;display:flex;flex-direction:column-reverse;gap:1px}.bar i{display:block;border-radius:3px 3px 0 0}.bar .l{position:absolute}
.axis{display:flex;gap:10px;margin-top:6px}.axis span{flex:1;text-align:center;font-size:11px;color:var(--muted)}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-top:10px}.legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.meter{height:10px;background:var(--bg);border-radius:999px;overflow:hidden}.meter b{display:block;height:100%;border-radius:999px}
.hbar{display:grid;grid-template-columns:120px 1fr 90px;gap:10px;align-items:center;padding:6px 0;font-size:13px}
.ava{display:inline-block;width:22px;height:22px;border-radius:50%;background:#C7C2F5;vertical-align:middle;margin-right:6px}
.beevis{display:flex;gap:12px;align-items:flex-start}.beevis .b{width:34px;height:34px;border-radius:50%;background:#2323B3;flex:none}.bubble{background:#F6F6FB;border-radius:14px;padding:12px 14px;font-size:13.5px;line-height:1.5}
</style></head><body><div class="frame">__BODY__</div></body></html>"""

COLORS = ['#7361F7','#35C7B2','#FF7733','#F6C000','#12BD57','#2323B3','#E70037','#A8AEBB']

def dividend_1():
    months = ['Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov']
    stacks = [[180,120,0,90,60],[210,0,140,0,70],[160,110,0,95,0],[190,130,150,0,80],[205,0,0,100,60],[170,125,145,0,0],[185,0,0,95,75],[220,130,150,0,0],[175,0,0,100,65],[200,120,140,0,0],[190,0,0,95,70],[230,135,160,0,80]]
    mx = 620
    bars = ''.join('<div class="bar">' + ''.join(f'<i style="height:{round(v/mx*170)}px;background:{COLORS[i]}"></i>' for i,v in enumerate(st) if v) + '</div>' for st in stacks)
    return f"""<div class="kpis"><div class="kpi"><span>Next 12 months</span><b>$6,284</b></div><div class="kpi"><span>Monthly average</span><b>$524</b></div><div class="kpi"><span>Yield on cost</span><b>4.1%</b></div><div class="kpi"><span>Next payment</span><b>Dec 1 · $412</b></div></div>
<div class="card"><h2>💸 Monthly income timeline</h2><div class="sub">Projected from current holdings and declared dividends · CAD · ex-div dates from Blossom</div><div class="bars">{bars}</div><div class="axis">{''.join(f'<span>{m}</span>' for m in months)}</div>
<div class="legend"><span><i style="background:{COLORS[0]}"></i>ENB</span><span><i style="background:{COLORS[1]}"></i>RY</span><span><i style="background:{COLORS[2]}"></i>SCHD</span><span><i style="background:{COLORS[3]}"></i>TD</span><span><i style="background:{COLORS[4]}"></i>XEI</span></div></div>
<div class="card"><h2>Annual income by holding</h2><table><tr><th>Ticker</th><th>Shares</th><th>Yield</th><th>Annual</th><th>Share of income</th></tr>
<tr><td><b>ENB</b></td><td>120</td><td>6.4%</td><td><b>$2,318</b></td><td><div class="meter"><b style="width:37%;background:{COLORS[0]}"></b></div></td></tr>
<tr><td><b>RY</b></td><td>40</td><td>3.6%</td><td><b>$1,490</b></td><td><div class="meter"><b style="width:24%;background:{COLORS[1]}"></b></div></td></tr>
<tr><td><b>SCHD</b></td><td>110</td><td>3.5%</td><td><b>$1,206</b></td><td><div class="meter"><b style="width:19%;background:{COLORS[2]}"></b></div></td></tr>
<tr><td><b>TD</b></td><td>35</td><td>4.9%</td><td><b>$770</b></td><td><div class="meter"><b style="width:12%;background:{COLORS[3]}"></b></div></td></tr>
<tr><td><b>XEI</b></td><td>60</td><td>4.6%</td><td><b>$500</b></td><td><div class="meter"><b style="width:8%;background:{COLORS[4]}"></b></div></td></tr></table></div>"""

def dividend_2():
    return """<div class="card"><h2>📅 Ex-dividend calendar · next 30 days</h2><div class="sub">Hold through the ex-date to get paid. Pay dates are Blossom's, not estimates.</div>
<table><tr><th>Ex-date</th><th>Ticker</th><th>Per share</th><th>Your shares</th><th>You get</th><th>Pay date</th><th>Change vs last</th></tr>
<tr><td>Nov 14</td><td><b>ENB</b></td><td>$0.9425</td><td>120</td><td><b>$113.10</b></td><td>Dec 1</td><td class="up">▲ 3.0%</td></tr>
<tr><td>Nov 20</td><td><b>SCHD</b></td><td>US$0.2645</td><td>110</td><td><b>$40.57</b></td><td>Dec 8</td><td class="dn">▼ 1.2%</td></tr>
<tr><td>Nov 25</td><td><b>XEI</b></td><td>$0.0695</td><td>60</td><td><b>$4.17</b></td><td>Nov 28</td><td>—</td></tr>
<tr><td>Dec 2</td><td><b>TD</b></td><td>$1.05</td><td>35</td><td><b>$36.75</b></td><td>Jan 31</td><td class="up">▲ 3.8%</td></tr></table></div>
<div class="card"><div class="beevis"><div class="b"></div><div class="bubble"><b>Two things worth knowing.</b> SCHD trimmed its payout for the second quarter in a row — still 3.5% on your cost, but the trend is down. And 37% of your income is one name (ENB); a 10% cut there is $230 a year.</div></div></div>"""

def crowd_1():
    rows = [('NVDA','$4.2M','1,842','3.1×','🔥 spike','up'),('ENB','$1.8M','920','2.4×','first-time buyers ↑','up'),('TSLA','−$2.1M','1,310','2.0×','net selling','dn'),('SHOP','$960K','610','1.8×','',''),('XEQT','$1.4M','2,205','1.2×','steady',''),('AAPL','−$640K','780','1.5×','dormant sellers','dn')]
    trs = ''.join(f'<tr><td><b>{t}</b></td><td class="{c}">{n}</td><td>{h}</td><td><b>{x}</b></td><td><div class="meter" style="width:140px"><b style="width:{int(float(x[:-1])/3.1*100)}%;background:{"#E70037" if c=="dn" else "#7361F7"}"></b></div></td><td>{"<span class=\"chip o\">"+f+"</span>" if f else ""}</td></tr>' for t,n,h,x,f,c in rows)
    return f"""<div class="kpis"><div class="kpi"><span>Scanned</span><b>1,214 tickers</b></div><div class="kpi"><span>Unusual this week</span><b>6</b></div><div class="kpi"><span>Biggest net buy</span><b>NVDA · $4.2M</b></div><div class="kpi"><span>Biggest net sell</span><b>TSLA · −$2.1M</b></div></div>
<div class="card"><h2>🔎 Crowd flow scanner · week of Nov 3</h2><div class="sub">Each ticker vs its own 12-week history · net $ and headcount from the Aggregate Trade Data MCP · every row ≥ 20 accounts</div>
<table><tr><th>Ticker</th><th>Net $ this week</th><th>Investors</th><th>vs 12-wk avg</th><th></th><th>Signal</th></tr>{trs}</table></div>"""

def crowd_2():
    pts = [12,14,11,15,13,16,18,15,19,22,24,41]
    w,h = 820,150; mx=max(pts)
    poly = ' '.join(f'{round(i*(w/11))},{round(h-p/mx*h)}' for i,p in enumerate(pts))
    return f"""<div class="card"><h2>NVDA · 12 weeks of crowd flow</h2><div class="sub">Investors buying per week · this week is 3.1× the average · 38% of buyers had never held it</div>
<svg width="{w}" height="{h+20}" style="display:block;margin-top:8px"><polyline points="{poly}" fill="none" stroke="#7361F7" stroke-width="3" stroke-linejoin="round"/><circle cx="{w}" cy="{round(h-41/mx*h)}" r="6" fill="#7361F7"/><text x="{w-120}" y="{round(h-41/mx*h)-14}" font-family="Nunito" font-weight="800" font-size="13" fill="#171717">1,842 this week</text></svg>
<div class="legend"><span><i style="background:#7361F7"></i>Investors buying</span><span>First-time buyers 38% (avg 14%)</span><span>Dormant sellers 4%</span></div></div>
<div class="card"><div class="beevis"><div class="b"></div><div class="bubble"><b>What's behind it:</b> earnings on Nov 19 plus the Blackwell delivery headlines. The last two spikes like this (Aug 28, May 22) faded to average within 3 weeks. Nothing here is a recommendation — it's what 1,842 Blossom investors did.</div></div></div>"""

def risk_1():
    segs = [('Technology',38,'#7361F7'),('Financials',22,'#35C7B2'),('Energy',14,'#FF7733'),('Health',9,'#F6C000'),('Other',17,'#A8AEBB')]
    r=70; c=2*3.14159*r; off=0; arcs=''
    for n,v,col in segs:
        arcs += f'<circle r="{r}" cx="110" cy="110" fill="none" stroke="{col}" stroke-width="28" stroke-dasharray="{c*v/100} {c}" stroke-dashoffset="{-off}" transform="rotate(-90 110 110)"/>'; off += c*v/100
    return f"""<div class="card" style="display:grid;grid-template-columns:240px 1fr;gap:18px;align-items:center"><svg width="220" height="220">{arcs}<text x="110" y="104" text-anchor="middle" font-family="Nunito" font-weight="800" font-size="26" fill="#171717">38%</text><text x="110" y="124" text-anchor="middle" font-family="Nunito" font-size="12" fill="#72777F">in Technology</text></svg>
<div><h2>🛡️ Look-through concentration</h2><div class="sub">Direct holdings + what's inside your ETFs</div>
{''.join(f'<div class="hbar"><span><i style="display:inline-block;width:10px;height:10px;border-radius:3px;background:{col};margin-right:6px"></i>{n}</span><div class="meter"><b style="width:{v*2}%;background:{col}"></b></div><b style="text-align:right">{v}%</b></div>' for n,v,col in segs)}</div></div>
<div class="card"><h2>Top single-name exposure</h2><div class="sub">You own more NVDA than you think: 4.2% direct + 5.6% through XEQT, VFV and QQC</div>
<table><tr><th>Name</th><th>Direct</th><th>Via ETFs</th><th>Total</th><th>Rule of thumb</th></tr>
<tr><td><b>NVDA</b></td><td>4.2%</td><td>5.6%</td><td><b>9.8%</b></td><td><span class="chip r">over 7.5%</span></td></tr>
<tr><td><b>RY</b></td><td>6.1%</td><td>2.0%</td><td><b>8.1%</b></td><td><span class="chip r">over 7.5%</span></td></tr>
<tr><td><b>AAPL</b></td><td>0%</td><td>4.9%</td><td><b>4.9%</b></td><td><span class="chip t">ok</span></td></tr>
<tr><td><b>ENB</b></td><td>4.4%</td><td>0.3%</td><td><b>4.7%</b></td><td><span class="chip t">ok</span></td></tr></table></div>"""

def earnings_1():
    days = ['Mon 10','Tue 11','Wed 12','Thu 13','Fri 14','Mon 17','Tue 18','Wed 19','Thu 20','Fri 21']
    on = {'Wed 12':['SHOP'],'Thu 13':['CSU'],'Wed 19':['NVDA','TD'],'Thu 20':['WMT'],'Fri 21':['BMO']}
    cells = ''.join(f'<div style="background:{"#EDE9FF" if d in on else "#fff"};border:1px solid var(--border);border-radius:10px;padding:8px 6px;min-height:64px"><div style="font-size:11px;color:var(--muted)">{d}</div>{"".join(f"<div style=\"font-weight:800;color:#4D35EB;font-size:13px\">{t}</div>" for t in on.get(d,[]))}</div>' for d in days)
    return f"""<div class="card"><h2>📅 Next 14 days · 6 of your 23 holdings report</h2><div class="sub">After-close unless marked · consensus from Fiscal.ai · "last time" = move the day after</div>
<div style="display:grid;grid-template-columns:repeat(10,1fr);gap:6px;margin:10px 0 16px">{cells}</div>
<table><tr><th>Date</th><th>Ticker</th><th>Weight</th><th>EPS est.</th><th>Rev est.</th><th>Last time</th><th>Holders on Blossom did</th></tr>
<tr><td>Nov 12</td><td><b>SHOP</b></td><td>3.1%</td><td>US$0.41</td><td>US$2.9B</td><td class="up">+9.4%</td><td><span class="chip t">62% held</span> <span class="chip p">21% added</span></td></tr>
<tr><td>Nov 13</td><td><b>CSU</b></td><td>2.4%</td><td>$28.10</td><td>$2.8B</td><td class="dn">−3.1%</td><td><span class="chip t">88% held</span></td></tr>
<tr><td>Nov 19</td><td><b>NVDA</b></td><td>9.8%*</td><td>US$1.42</td><td>US$57B</td><td class="dn">−2.6%</td><td><span class="chip p">34% added</span> <span class="chip o">11% trimmed</span></td></tr>
<tr><td>Nov 19</td><td><b>TD</b></td><td>4.0%</td><td>$2.05</td><td>$14.1B</td><td class="up">+1.8%</td><td><span class="chip t">79% held</span></td></tr></table>
<div class="sub" style="margin:10px 0 0">* look-through: 4.2% direct + 5.6% via ETFs</div></div>"""

def rebalance_1():
    rows = [('Canadian equity',30,34,'#7361F7'),('US equity',40,44,'#35C7B2'),('International',15,11,'#FF7733'),('Bonds',10,7,'#F6C000'),('Cash',5,4,'#A8AEBB')]
    return f"""<div class="card"><h2>🎯 Target vs reality</h2><div class="sub">All accounts · drift since your last rebalance (Jul 2)</div>
{''.join(f'<div class="hbar" style="grid-template-columns:140px 1fr 110px"><span>{n}</span><div style="position:relative;height:16px;background:var(--bg);border-radius:999px"><b style="position:absolute;left:0;top:0;height:100%;width:{a*2}%;background:{c};border-radius:999px;opacity:.9"></b><i style="position:absolute;left:{t*2}%;top:-4px;width:2px;height:24px;background:#171717"></i></div><b style="text-align:right;color:{"#E70037" if abs(a-t)>=4 else "#12BD57"}">{a}% <span style="color:var(--muted);font-weight:600">/ {t}%</span></b></div>' for n,t,a,c in rows)}
<div class="legend" style="margin-top:14px"><span>bar = actual · line = target · red = drifted 4+ points</span></div></div>
<div class="card"><h2>Fix it with the next $3,000, not with sells</h2><div class="sub">Uses new contributions first so nothing is taxable · TFSA room $11,400 left</div>
<table><tr><th>Buy</th><th>Account</th><th>Amount</th><th>After</th><th>Why</th></tr>
<tr><td><b>XEF</b></td><td>TFSA</td><td><b>$1,800</b></td><td>International 11% → 14%</td><td>biggest gap, cheapest MER</td></tr>
<tr><td><b>ZAG</b></td><td>RRSP</td><td><b>$1,200</b></td><td>Bonds 7% → 9%</td><td>interest sheltered in RRSP</td></tr>
<tr><td colspan="5" style="color:var(--muted)">US and Canadian equity drift back under 2 points without selling anything.</td></tr></table></div>"""

def tfsa_1():
    return """<div class="kpis"><div class="kpi"><span>TFSA room</span><b>$11,400</b></div><div class="kpi"><span>RRSP room</span><b>$23,850</b></div><div class="kpi"><span>FHSA room</span><b>$8,000</b></div><div class="kpi"><span>Est. tax drag today</span><b class="dn">$410 / yr</b></div></div>
<div class="card"><h2>🍁 Where each holding belongs</h2><div class="sub">By what it pays and how it's taxed · based on your accounts, not generic rules</div>
<table><tr><th>Holding</th><th>Now in</th><th>Belongs in</th><th>Why</th><th>$ / yr</th></tr>
<tr><td><b>SCHD</b></td><td>Personal</td><td><span class="chip p">RRSP</span></td><td>US dividends: 15% withholding waived in RRSP, not TFSA</td><td class="dn">−$180</td></tr>
<tr><td><b>ZAG</b></td><td>TFSA</td><td><span class="chip p">RRSP</span></td><td>interest is fully taxable — shelter it where room is cheapest</td><td class="dn">−$95</td></tr>
<tr><td><b>ENB</b></td><td>RRSP</td><td><span class="chip t">Personal</span></td><td>eligible Canadian dividend — tax credit is wasted inside RRSP</td><td class="dn">−$135</td></tr>
<tr><td><b>XEQT</b></td><td>TFSA</td><td><span class="chip t">TFSA ✓</span></td><td>growth, keep it sheltered</td><td>—</td></tr>
<tr><td><b>BTC</b></td><td>Crypto</td><td><span class="chip t">Crypto ✓</span></td><td>no registered option</td><td>—</td></tr></table></div>
<div class="card"><h2>Next $5,000: FHSA first</h2><div class="sub">You're a first-time buyer with $8,000 of FHSA room — deductible like an RRSP, tax-free out like a TFSA.</div><div class="meter" style="height:18px"><b style="width:62%;background:#35C7B2"></b></div><div class="legend"><span>$5,000 → FHSA (XEQT)</span><span>then TFSA</span><span>RRSP at tax time</span></div></div>"""


def reply(title, body, prompt):
    """A chat-reply frame: the user's prompt, then the skill's verdict."""
    return f"""<div class="card" style="background:var(--bg);box-shadow:none;padding:0"><div style="display:flex;justify-content:flex-end;margin-bottom:12px"><div style="background:#7361F7;color:#fff;border-radius:16px 16px 4px 16px;padding:10px 14px;font-size:14px;max-width:70%">{prompt}</div></div>
<div class="card" style="margin:0;border-radius:16px 16px 16px 4px"><div class="sub" style="margin-bottom:8px">✨ {title}</div>{body}</div></div>"""

def space_1():
    rows=[('LUNR','2.2×','$1.76B <span class="sub" style="display:inline">(was $213M)</span>','+$367M','−80%','business up, price down','r'),('MDA','3.4×','$3.9B','+$1.3B','−31%','priced like a contractor, growing like a platform','t'),('PL','6.1×','$0.7B','+$0.2B','−12%','fair; watch margins','t'),('RKLB','~50×','$1.1B','+$0.5B','−18%','priced for Neutron working first time','o'),('ASTS','~135×','pre-revenue','+$0.9B','−22%','a story, not a multiple','o')]
    trs=''.join(f'<tr><td><b>{n}</b></td><td><b>{ps}</b></td><td>{bl}</td><td>{c}</td><td class="dn">{dd}</td><td><span class="chip {cls}">{v}</span></td></tr>' for n,ps,bl,c,dd,v,cls in rows)
    body=f"""<h2>🚀 Space lens · your names: LUNR, MDA, PL · watch: RKLB, ASTS, KRMN</h2>
<table><tr><th>Name</th><th>Fwd P/S</th><th>Backlog</th><th>Net cash</th><th>Since 52-wk high</th><th>Verdict</th></tr>{trs}</table>
<p style="margin:14px 0 6px;font-size:13.5px;line-height:1.55"><b>LUNR</b> — the widest gap between business and price in the sector. Since the May 28 high: 6th CLPS mission ($148M) · 18 spacecraft for L3Harris · $600M+ comms program · Lanteris closed (revenue 4×) · two NASA Earth-science wins · SXM-11 delivered. Management still guides positive adj. EBITDA. The −80% is macro and the SPCX IPO pulling money from the sector, not the company.</p>
<div class="beevis" style="margin-top:10px"><div class="b" style="background:#2323B3;border-radius:50%;width:30px;height:30px"></div><div class="bubble" style="font-size:13px"><b>@anthony.invests, Nov 5:</b> “$LUNR that once was at the same valuation a year ago did not have Lanteris… yet its share price has fallen more than 80%.” <span style="color:#7361F7">→ post</span></div></div>
<p class="sub" style="margin:12px 0 0">🇨🇦 CDRs: RKLB has a CIBC CDR (CAD-hedged). LUNR and ASTS don’t. · Anthony’s framework, your holdings; he holds LUNR and MDA. Not a recommendation.</p>"""
    return reply('Space Stock Lens by Anthony', body, 'Run the space lens on my portfolio')

def piiverse_1():
    rows=[('1','Income first: every holding pays monthly or weekly','21 of 23 do — <b>CNQ</b> and <b>ENB</b> pay quarterly','⚠️'),('2','No single fund over 10% of the income sleeve','<b>HHIS</b> is 12.4%','⚠️'),('3','Keep a 5% cash reserve; let distributions rebuild it','2.1% — you spent it on the dip','⚠️'),('4','Know the yield <i>and</i> the NAV trend of every CC fund','4 you can’t explain: MSTY, CONY, YBIT, USOY','⚠️'),('5','NAV indifference: judge by income paid, not price','you sold <b>BANK</b> on a −6% day; it had paid every month','❌'),('6','Growth sleeve separate from income sleeve','CVE and HWX sit beside the income funds','⚠️'),('7','Write the rule down before you break it','—','✅')]
    trs=''.join(f'<tr><td class="sub" style="display:table-cell">{n}</td><td>{r}</td><td>{y}</td><td style="font-size:16px">{g}</td></tr>' for n,r,y,g in rows)
    body=f"""<h2>💰 PIIverse rules check · 23 holdings · income sleeve $412K</h2>
<table><tr><th>#</th><th>Perry’s rule</th><th>You</th><th></th></tr>{trs}</table>
<div class="kpis" style="margin:14px 0 0;grid-template-columns:repeat(4,1fr)"><div class="kpi"><span>This month pays</span><b>$2,870</b></div><div class="kpi"><span>Week 2 (alignment day)</span><b>$1,230</b></div><div class="kpi"><span>Cash reserve</span><b class="dn">2.1% / 5%</b></div><div class="kpi"><span>Back to 5% by</span><b>week 2</b></div></div>
<p style="margin:14px 0 6px;font-size:13.5px;line-height:1.55"><b>The honest line (rule 5):</b> three of your last five trades were sells on red days in funds that kept paying. Perry’s test is simple — did the income stop? It didn’t.</p>
<div class="beevis"><div class="b" style="background:#12BD57;border-radius:50%;width:30px;height:30px"></div><div class="bubble" style="font-size:13px"><b>@piiverse, Nov 6:</b> “even when bloodbaths on the markets… INCOME KEEPS PAYING OUT… I haven’t realized ANY LOSS.” <span style="color:#7361F7">→ post</span></div></div>
<p class="sub" style="margin:12px 0 0">Perry’s rules, your portfolio. He runs ~$1.7M this way and holds MSTY, HHIS, BANK and ENCL. Not a recommendation.</p>"""
    return reply('PIIverse Income Rules Check', body, 'Run my portfolio through Perry’s income rules')

SHOTS = {
  'space-stock-lens': [('space_1', space_1, 'The verdict: Anthony’s forward-P/S ladder on your space names, with what each company shipped since its high')],
  'piiverse-income-rules': [('piiverse_1', piiverse_1, 'The verdict: your income portfolio graded rule by rule, this month’s pay calendar, and the honest line')],
  'dividend-income-planner': [('dividend_1', dividend_1, 'Monthly income timeline and income by holding'), ('dividend_2', dividend_2, 'Ex-dividend calendar with what you get, and Beevis’s two flags')],
  'crowd-flow-scanner': [('crowd_1', crowd_1, 'This week’s unusual tickers vs their own 12-week history'), ('crowd_2', crowd_2, '12 weeks of crowd flow for one ticker, with first-time buyers')],
  'risk-concentration-check': [('risk_1', risk_1, 'Look-through sector mix and single-name exposure')],
  'earnings-season-checklist': [('earnings_1', earnings_1, 'The next 14 days, with consensus and what holders on Blossom did')],
  'rebalance-planner': [('rebalance_1', rebalance_1, 'Target vs reality, and the fix using new contributions only')],
  'tfsa-rrsp-optimizer': [('tfsa_1', tfsa_1, 'Which account each holding belongs in, with the $ reason')],
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':900,'height':600}, device_scale_factor=1.5)
        for sid, lst in SHOTS.items():
            for name, fn, cap in lst:
                await pg.set_content(BASE.replace('__BODY__', fn())); await pg.wait_for_timeout(500)
                el = await pg.query_selector('.frame'); path = os.path.join(OUT, f'{name}.jpg')
                await el.screenshot(path=path, type='jpeg', quality=82)
                print(sid, name, os.path.getsize(path)//1024, 'KB')
        await b.close()
asyncio.run(main())
