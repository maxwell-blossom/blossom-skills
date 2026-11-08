#!/usr/bin/env python3
"""Builds Blossom Skills V1: index.html (single page app) + skills/<slug>/SKILL.md files for the curl install."""
import json, base64, os, re
from data import CREATORS, MCPS, SKILLS

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://blossom-skills.netlify.app'

logo_b64 = base64.b64encode(open(os.path.join(OUT, 'assets/_blossom_logo.png'), 'rb').read()).decode()
wall_b64 = base64.b64encode(open(os.path.join(OUT, 'assets/wall_tile.jpg'), 'rb').read()).decode()
BROKERS = [(n, base64.b64encode(open(os.path.join(OUT, 'assets/brokers', n + '.png'), 'rb').read()).decode()) for n in ('wealthsimple', 'questrade', 'robinhood', 'public', 'ibkr', 'td')]
BROKERS_JS = json.dumps(BROKERS)
flower_b64 = base64.b64encode(open(os.path.join(OUT, 'assets/logo_blossom_flower_256.jpg'), 'rb').read()).decode()
beevis_svg = open(os.path.join(OUT, 'assets/beevis_avatar.svg')).read()
beevis_b64 = base64.b64encode(beevis_svg.encode()).decode()
badge_svg = open(os.path.join(OUT, 'assets/badge_verified_teal.svg')).read()
badge_b64 = base64.b64encode(badge_svg.encode()).decode()
for c in CREATORS.values():
    if c.get('photo'): c['photo_b64'] = base64.b64encode(open(os.path.join(OUT, 'assets/profiles', c['photo']), 'rb').read()).decode()
NAV = {k: open(os.path.join(OUT, 'assets/nav', k + '.svg')).read().strip() for k in ('home','markets','learn','portfolio','insights','save','topics','buzz','settings')}
beevis_webp = base64.b64encode(open(os.path.join(OUT, 'assets/nav/beevis-sidebar-icon.webp'), 'rb').read()).decode()
NAV['beevis'] = f'<img src="data:image/webp;base64,{beevis_webp}" alt="" style="width:18px;height:18px">'
NAV['skills'] = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none"><path fill-rule="evenodd" d="M8 .9a.7.7 0 0 1 .7.7v1.1h2.3A2.5 2.5 0 0 1 13.5 5.2v6.1a2.5 2.5 0 0 1-2.5 2.5H5a2.5 2.5 0 0 1-2.5-2.5V5.2A2.5 2.5 0 0 1 5 2.7h2.3V1.6A.7.7 0 0 1 8 .9m-3 3.2a1.1 1.1 0 0 0-1.1 1.1v6.1a1.1 1.1 0 0 0 1.1 1.1h6a1.1 1.1 0 0 0 1.1-1.1V5.2A1.1 1.1 0 0 0 11 4.1zm1.2 2.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2m3.6 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2M5.6 9.6h4.8a.6.6 0 0 1 0 1.2H5.6a.6.6 0 0 1 0-1.2M.5 6.4a.7.7 0 0 1 .7.7v2.3a.7.7 0 0 1-1.4 0V7.1a.7.7 0 0 1 .7-.7m15 0a.7.7 0 0 1 .7.7v2.3a.7.7 0 0 1-1.4 0V7.1a.7.7 0 0 1 .7-.7" fill="currentColor"/></svg>'
TOPICS = [('ETFs','etfs'),('Passive Income','passive_income'),('Beginner Investors','beginnerinvestors'),('Dividends','dividends'),('Market News','marketnews')]
TOPIC_B64 = {k: base64.b64encode(open(os.path.join(OUT, 'assets/topics', k + '.png'), 'rb').read()).decode() for _, k in TOPICS}
NAV['about'] = open(os.path.join(OUT, 'assets/nav/about.svg')).read().strip()
NAV['resources'] = open(os.path.join(OUT, 'assets/nav/resources.svg')).read().strip()
SIDEBAR = ('<aside class="sidebar">'
  f'<a href="#" data-app>{NAV["about"]}About Blossom</a><hr>'
  f'<a href="#" data-app>{NAV["home"]}Home</a><a href="#" data-app>{NAV["markets"]}Markets</a><a href="#" data-app>{NAV["learn"]}Learn</a><a href="#" data-app>{NAV["portfolio"]}Portfolio</a><a href="#" data-app>{NAV["insights"]}Insights</a><hr>'
  f'<a href="#" data-app>{NAV["beevis"]}Chat with Beevis</a>'
  f'<a href="#/" class="on">{NAV["skills"]}Skills &amp; MCPs<span class="new">New</span></a><hr>'
  f'<a href="#" data-app>{NAV["save"]}Saved posts</a><hr>'
  f'<div class="sec"><span style="display:flex;align-items:center;gap:12px">{NAV["topics"]}Topics</span><svg class="chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></div>'
  + ''.join(f'<div class="topic"><img src="data:image/png;base64,{TOPIC_B64[k]}" alt="">{n}</div>' for n,k in TOPICS)
  + f'<div class="sub">See All Topics</div><hr><a href="#" data-app>{NAV["buzz"]}The Weekly Buzz</a><hr>'
  f'<a href="#" data-app>{NAV["resources"]}Resources</a><div class="sub">Get Help</div>'
  f'<a href="#" data-app class="bottom" style="color:var(--muted)">{NAV["settings"]}Settings</a></aside>')
for m in MCPS:
    if m.get('logo'): m['logo_b64'] = base64.b64encode(open(os.path.join(OUT, 'assets', m['logo']), 'rb').read()).decode()

# write SKILL.md files for the curl install
for s in SKILLS:
    d = os.path.join(OUT, 'skills', s['id']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'SKILL.md'), 'w').write(s['skill'] + '\n')

DATA = json.dumps(dict(creators=CREATORS, mcps=MCPS, skills=SKILLS, site=SITE), ensure_ascii=False)

CSS = r"""
:root{--purple:#7361F7;--p600:#4D35EB;--lav:#E6E2FD;--lav2:#EDE9FF;--teal:#35C7B2;--tealt:#E1F4F1;--tealx:#409082;--green:#12BD57;--greent:#D9F1E2;--red:#E70037;--redt:#FCD9E1;--orange:#FF7733;--oranget:#FFE4D6;--yellow:#F6C000;--yellowt:#FFF8DF;--ink:#171717;--text:#3F3F46;--muted:#72777F;--ter:#A8AEBB;--border:#E3E3E3;--bg:#F1F5F7;--beevis:#2323B3;--beevist:#EBEBFF;--card:#fff;--r:12px;--shadow:0 2px 4px 2px rgba(0,0,0,.04)}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font-family:Nunito,"SF Pro Rounded",-apple-system,"Segoe UI",sans-serif;font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:var(--purple);text-decoration:none}a:hover{text-decoration:underline}
button{font:inherit;cursor:pointer;border:0;background:none;color:inherit}
input,select,textarea{font:inherit;color:var(--ink)}
h1,h2,h3,h4{margin:0;color:var(--ink);font-weight:700;letter-spacing:-.01em}
.appbar{position:sticky;top:0;z-index:20;height:72px;background:#fff;border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 24px;gap:18px}
.shell{display:flex;align-items:flex-start}
.sidebar{width:236px;flex:none;position:sticky;top:72px;height:calc(100vh - 72px);overflow:auto;background:#fff;border-right:1px solid var(--border);padding:14px 12px 20px;display:flex;flex-direction:column;gap:2px}
.sidebar a{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:12px;color:var(--text);font-weight:600;font-size:15px;line-height:1.2;white-space:nowrap}
.sidebar a:hover{background:var(--bg);text-decoration:none}
.sidebar a.on{background:var(--tealt);color:var(--tealx)}
.sidebar a svg,.sidebar .sec svg{width:18px;height:18px;flex:none;color:var(--muted)}
.sidebar a.on svg{color:var(--teal)}
.sidebar .acct{display:flex;justify-content:space-between;padding:4px 12px 4px 42px;font-size:13.5px;color:var(--muted)}.sidebar .acct b{font-weight:600;color:var(--text)}
.sidebar hr{border:0;border-top:1px solid var(--border);margin:10px 4px}
.sidebar .sec{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;font-weight:600;color:var(--text);font-size:15px}
.sidebar .topic{display:flex;align-items:center;gap:10px;padding:5px 12px 5px 30px;font-size:14px;color:var(--text);font-weight:600}.sidebar .topic img{width:20px;height:20px;border-radius:50%;flex:none}
.sidebar .sub{padding:6px 12px 6px 30px;font-size:14px;color:var(--muted)}
.sidebar .new{margin-left:auto;background:var(--purple);color:#fff;font-size:9.5px;font-weight:800;letter-spacing:.3px;border-radius:999px;padding:2px 6px}
.sidebar .cnt{margin-left:auto;background:var(--beevis);color:#fff;font-size:11px;font-weight:800;border-radius:999px;min-width:20px;height:20px;display:flex;align-items:center;justify-content:center}
.sidebar .bottom{margin-top:auto}
.main{flex:1;min-width:0}
@media (max-width:980px){.sidebar{display:none}}
.appbar .logo{display:flex;align-items:center;gap:10px;height:72px}
.appbar .logo img{height:30px}
.appbar .logo .prod{font-weight:800;font-size:17px;color:var(--ink);padding-left:10px;border-left:1px solid var(--border);line-height:1}
.appbar nav{display:flex;gap:4px;margin-left:8px}
.appbar nav a{padding:8px 12px;border-radius:12px;color:var(--text);font-weight:600;font-size:14px}
.appbar nav a.on,.appbar nav a:hover{background:var(--bg);text-decoration:none;color:var(--ink)}
.appbar .sp{flex:1}
.pill{display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:999px;padding:9px 20px;font-weight:600;font-size:15px;line-height:1.2;white-space:nowrap;transition:background .15s,transform .05s}
.pill:active{transform:translateY(1px)}
.pill.pri{background:var(--purple);color:#fff}.pill.pri:hover{background:var(--p600);text-decoration:none}
.pill.sec{background:var(--bg);color:var(--text)}.pill.sec:hover{background:#e8edf0;text-decoration:none}
.pill.out{border:1px solid var(--purple);color:var(--purple);background:#fff}.pill.out:hover{background:var(--lav2);text-decoration:none}
.pill.teal{background:var(--teal);color:#fff}.pill.teal:hover{background:#2bb5a1;text-decoration:none}
.pill.dis{background:var(--lav);color:var(--purple);cursor:default}
.pill.sm{padding:6px 14px;font-size:13px}.pill.lg{padding:14px 24px;font-size:16px;width:100%}
.ava{display:inline-flex;align-items:center;justify-content:center;border-radius:50%;color:#fff;font-weight:800;font-size:12px;overflow:hidden;flex:none;letter-spacing:0}
.ava img{width:100%;height:100%;object-fit:cover}
.wrap{max-width:1180px;margin:0 auto;padding:24px}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);box-shadow:var(--shadow)}
.sec-h{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin:28px 0 12px}
.sec-h h2{font-size:20px}.sec-h a{font-weight:600;font-size:14px}
/* hero */
.hero{display:grid;grid-template-columns:1.35fr .65fr;gap:28px;align-items:center;padding:40px 44px;border-radius:24px;background:linear-gradient(105deg,#EDE9FF 0%,#F6E9FA 48%,#E1F4F1 100%);position:relative;overflow:hidden}
.hero:before{content:"";position:absolute;inset:0;background:url(data:image/jpeg;base64,__WALL__) repeat;background-size:211px 211px;opacity:.14;mix-blend-mode:multiply;pointer-events:none}
.hero>*{position:relative}
.hero h1{font-size:34px;line-height:1.15;font-weight:800;color:var(--ink);margin-bottom:10px;letter-spacing:-.02em}
.hero p{font-size:16px;color:var(--text);margin:0 0 18px;max-width:560px}
.hero .search{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--border);border-radius:999px;padding:6px 6px 6px 18px;max-width:560px;box-shadow:var(--shadow)}
.hero .search input{flex:1;border:0;outline:0;font-size:16px;background:transparent}
.hero .stats{display:flex;gap:26px;margin-top:18px;flex-wrap:wrap}
.hero .stats b{display:block;font-size:22px;color:var(--ink);font-weight:800}.hero .stats span{font-size:13px;color:var(--muted)}
.hero .side{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;text-align:center}
.hero .stack{display:flex;justify-content:center}.hero .stack .ava{border:3px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.08);margin-left:-12px}.hero .stack .ava:first-child{margin-left:0}
.hero .side .t{font-size:15px;font-weight:700;color:var(--ink)}.hero .side .t span{display:block;font-size:13px;color:var(--muted);font-weight:600;margin-top:2px}
.hero .side .ctas{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
/* tabs & filters */
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--border);margin:26px 0 14px}
.tabs button{padding:8px 4px 10px;margin-right:16px;font-size:17px;font-weight:600;color:var(--muted);border-bottom:2px solid transparent;margin-bottom:-1px}
.tabs button.on{color:var(--ink);border-color:var(--teal)}
.tabs button .n{font-size:12px;color:var(--ter);font-weight:700;margin-left:6px;background:var(--bg);border-radius:999px;padding:1px 7px}
.filters{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:0 0 18px}
.chip{border:1px solid var(--border);background:#fff;border-radius:999px;padding:6px 13px;font-size:13.5px;font-weight:600;color:var(--text)}
.chip.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.chip.rq{background:var(--bg);border-color:transparent;font-weight:600;color:var(--text);font-size:12.5px;padding:4px 10px}.chip.rq.opt{background:#fff;border:1px dashed var(--border);color:var(--muted)}.chip.rq.opt i{font-style:normal;font-size:10.5px;color:var(--ter);font-weight:800;text-transform:uppercase;letter-spacing:.04em}
.badge.broker{background:var(--greent);color:#0b7a3b}.badge.warn{background:var(--redt);color:#b4002b}
.filters .sp{flex:1}.filters select{border:1px solid var(--border);border-radius:999px;padding:7px 32px 7px 14px;background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%2372777F' stroke-width='1.6'/%3E%3C/svg%3E") no-repeat right 12px center;appearance:none;font-size:13.5px;font-weight:600}
/* grid cards */
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.grid.g2{grid-template-columns:repeat(2,minmax(0,1fr))}
.sk{padding:22px 22px 16px;display:flex;flex-direction:column;gap:12px;cursor:pointer;transition:box-shadow .15s,transform .15s;position:relative}
.sk:hover{box-shadow:0 6px 18px rgba(23,23,23,.08);transform:translateY(-1px)}
.sk .top{display:flex;gap:12px;align-items:flex-start}
.sk .em{width:56px;height:56px;border-radius:14px;background:var(--lav2);display:flex;align-items:center;justify-content:center;font-size:28px;flex:none}
.sk .em.mcp{background:var(--tealt)}
.sk .shot{display:block;width:100%;height:150px;object-fit:cover;object-position:top;border-radius:10px;border:1px solid var(--border);margin:12px 0 2px;background:var(--bg)}
.gal{display:grid;grid-template-columns:1fr 1fr;gap:12px}.gal.one{grid-template-columns:1fr}.gal figure{margin:0;cursor:zoom-in}.gal img{display:block;width:100%;border-radius:10px;border:1px solid var(--border);background:var(--bg)}.gal figcaption{font-size:12.5px;color:var(--muted);margin-top:6px}
.lb{position:fixed;inset:0;background:rgba(23,23,23,.82);z-index:60;display:flex;align-items:center;justify-content:center;padding:30px;cursor:zoom-out}.lb img{max-width:min(1100px,100%);max-height:100%;border-radius:12px;background:#fff}
@media (max-width:720px){.gal{grid-template-columns:1fr}}
.sk h3{font-size:18px;line-height:1.25}
.sk .by{display:flex;align-items:center;gap:6px;font-size:13px;color:var(--muted);margin-top:3px}
.sk .by b{color:var(--text);font-weight:600}
.sk p{margin:0;font-size:14.5px;color:var(--text);line-height:1.5;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.sk .hl{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:5px}.sk .hl li{font-size:13.5px;color:var(--muted);display:flex;gap:8px;line-height:1.4}.sk .hl li:before{content:"✓";color:var(--teal);font-weight:800;flex:none}
.sk .req{display:flex;gap:6px;flex-wrap:wrap}
.sk .bot{display:flex;align-items:center;gap:14px;font-size:13px;color:var(--muted);margin-top:auto;padding-top:8px;border-top:1px solid #f0f0f2}
.sk .bot .sp{flex:1}.sk .bot .upd{color:var(--ter)}
.star{color:var(--yellow)}
.price{border-radius:999px;padding:3px 10px;font-size:12.5px;font-weight:700;background:var(--lav2);color:var(--purple);white-space:nowrap}
.price.free{background:var(--tealt);color:var(--tealx)}
.badge{display:inline-flex;align-items:center;gap:3px;font-size:11px;font-weight:800;border-radius:999px;padding:1px 7px;line-height:1.5;vertical-align:middle}
.badge.official{background:var(--lav2);color:var(--purple)}.badge.ambassador{background:var(--oranget);color:#c94f12}.badge.pro{background:var(--lav);color:var(--purple)}.badge.partner{background:var(--tealt);color:var(--tealx)}.badge.beta{background:var(--yellowt);color:#8a6a00}
.vb{display:inline-block;width:14px;height:14px;vertical-align:-2px}
/* detail */
.detail{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:20px;align-items:start}.detail>*{min-width:0}
.dhead{padding:26px 28px;display:flex;gap:20px;align-items:flex-start}
.dhead .em{width:76px;height:76px;border-radius:18px;background:var(--lav2);display:flex;align-items:center;justify-content:center;font-size:40px;flex:none}
.dhead .em.mcp{background:var(--tealt)}
.dhead h1{font-size:28px;font-weight:800;line-height:1.15}
.dhead .pitch{font-size:16px;color:var(--text);margin:8px 0 12px}
.dhead .by{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--muted);flex-wrap:wrap}
.dhead .by b{color:var(--ink);font-weight:700}
.stats{display:flex;gap:0;margin-top:16px;border-top:1px solid var(--border);flex-wrap:wrap}
.stats div{padding:12px 18px 0 0;margin-right:18px;font-size:12.5px;color:var(--muted)}
.stats div b{display:block;font-size:17px;color:var(--ink);font-weight:800}
.dtabs{display:flex;gap:0;border-bottom:1px solid var(--border);margin-top:4px;padding:0 28px}
.dtabs button{padding:12px 2px 12px;margin-right:22px;font-size:15px;font-weight:600;color:var(--muted);border-bottom:2px solid transparent;margin-bottom:-1px}
.dtabs button.on{color:var(--ink);border-color:var(--teal)}
.dbody{padding:22px 28px}
.dbody h3{font-size:16px;margin:0 0 10px}
.dbody .blk{margin-bottom:26px}
.prompts{display:flex;flex-direction:column;gap:8px}
.prompt{display:flex;align-items:center;gap:10px;background:var(--bg);border-radius:12px;padding:10px 14px;font-size:14.5px;color:var(--ink)}
.prompt .cp{margin-left:auto;font-size:12px;color:var(--purple);font-weight:700;flex:none}
.sample{background:#fff;border:1px solid var(--border);border-radius:14px;padding:14px 18px 16px;font-size:14.5px}
.sample .lbl{display:block;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--ter);margin-bottom:10px}
.md{overflow-x:auto}.md p{margin:0 0 10px}.md table{border-collapse:collapse;width:100%;font-size:13.5px;margin:8px 0}.md th,.md td{border-bottom:1px solid var(--border);padding:6px 8px;text-align:left;vertical-align:top}.md th{color:var(--muted);font-weight:700;font-size:12px}
.md pre{background:var(--bg);border-radius:10px;padding:10px 12px;font-size:12.5px;overflow:auto;line-height:1.5}.md code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.md ol,.md ul{margin:0 0 10px;padding-left:22px}
.reqrow{display:flex;gap:12px;align-items:center;padding:12px 14px;border:1px solid var(--border);border-radius:12px;margin-bottom:8px}
.reqrow .em{width:36px;height:36px;border-radius:10px;background:var(--tealt);display:flex;align-items:center;justify-content:center;font-size:18px;flex:none}
.reqrow b{display:block;font-size:14px;color:var(--ink)}.reqrow span{font-size:12.5px;color:var(--muted)}
.reqrow .pill{margin-left:auto}
.brokers{border:1px solid var(--border);border-radius:12px;padding:12px 14px;margin-top:10px;background:#fff}.brokers .bl{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin-bottom:8px}.brokers img{height:18px;width:auto;opacity:.9}.brokers .more{font-size:12.5px;color:var(--ter);font-weight:700}
.itabs{display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap}
.itabs button{border:1px solid var(--border);border-radius:999px;padding:5px 12px;font-size:13px;font-weight:600;color:var(--text);background:#fff}
.itabs button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.code{background:#1f1f24;color:#e6e6ea;border-radius:12px;padding:14px 16px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;line-height:1.55;position:relative;overflow:auto;white-space:pre-wrap;word-break:break-word}
.code .cp{position:absolute;top:8px;right:8px;background:#34343c;color:#fff;border-radius:999px;padding:3px 10px;font-size:11px;font-weight:700;font-family:Nunito,sans-serif}
.steps{margin:10px 0 0;padding-left:20px;font-size:14px;color:var(--text)}.steps li{margin-bottom:5px}
.skillmd{border:1px solid var(--border);border-radius:12px;overflow:hidden}
.skillmd summary{padding:12px 16px;cursor:pointer;font-weight:700;font-size:14px;color:var(--ink);list-style:none;display:flex;align-items:center;gap:8px}
.skillmd summary:after{content:"▾";margin-left:auto;color:var(--muted)}
.skillmd pre{margin:0;padding:14px 16px;background:var(--bg);font-size:12.5px;line-height:1.5;overflow:auto;max-height:420px;white-space:pre-wrap;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
/* updates */
.tl{position:relative;padding-left:26px}
.tl:before{content:"";position:absolute;left:7px;top:6px;bottom:6px;width:2px;background:var(--lav)}
.tli{position:relative;margin-bottom:18px}
.tli:before{content:"";position:absolute;left:-23px;top:5px;width:10px;height:10px;border-radius:50%;background:var(--purple);border:2px solid #fff;box-shadow:0 0 0 2px var(--lav)}
.tli .v{font-weight:800;color:var(--ink);font-size:14px}.tli .d{font-size:12.5px;color:var(--muted);margin-left:8px}.tli p{margin:3px 0 0;font-size:14px}
.tli .tag{font-size:11px;font-weight:800;background:var(--tealt);color:var(--tealx);border-radius:999px;padding:1px 7px;margin-left:8px;vertical-align:1px}
.promise{display:flex;gap:12px;align-items:center;background:var(--lav2);border-radius:12px;padding:12px 14px;margin-bottom:18px;font-size:14px}
.promise .em{font-size:22px}
/* reviews */
.rsum{display:grid;grid-template-columns:140px 1fr;gap:22px;align-items:center;margin-bottom:22px}
.rsum .big{font-size:44px;font-weight:800;color:var(--ink);line-height:1}
.rsum .bars div{display:grid;grid-template-columns:34px 1fr 36px;gap:8px;align-items:center;font-size:12.5px;color:var(--muted);margin:3px 0}
.rsum .bars i{display:block;height:8px;border-radius:999px;background:var(--bg);overflow:hidden}.rsum .bars i b{display:block;height:100%;background:var(--yellow)}
.rev{display:flex;gap:12px;padding:14px 0;border-top:1px solid var(--border)}
.rev .who{font-size:13.5px;color:var(--muted)}.rev .who b{color:var(--ink);font-weight:700}
.rev p{margin:4px 0 6px;font-size:14.5px;color:var(--text)}
.rev .act{font-size:12.5px;color:var(--muted);display:flex;gap:14px}
.compose{display:flex;gap:12px;align-items:flex-start;background:var(--bg);border-radius:14px;padding:14px;margin-top:10px}
.compose>div{flex:1;min-width:0}.compose textarea{width:100%;border:1px solid var(--border);border-radius:12px;padding:10px 12px;min-height:64px;resize:vertical;background:#fff}
.compose .note{font-size:12px;color:var(--muted);margin-top:6px}
/* sidebar */
.side{position:sticky;top:92px;display:flex;flex-direction:column;gap:14px}
.buy{padding:20px}
.buy .amt{font-size:30px;font-weight:800;color:var(--ink);line-height:1}.buy .amt small{font-size:14px;color:var(--muted);font-weight:600}
.buy .sub{font-size:13px;color:var(--muted);margin:4px 0 14px}
.plans{display:flex;flex-direction:column;gap:8px;margin-bottom:14px}
.plan{display:flex;align-items:center;gap:10px;border:1.5px solid var(--border);border-radius:12px;padding:10px 12px;cursor:pointer;font-size:14px}
.plan.on{border-color:var(--purple);background:var(--lav2)}
.plan b{color:var(--ink)}.plan .save{margin-left:auto;font-size:11px;font-weight:800;background:var(--greent);color:#0b7a3b;border-radius:999px;padding:1px 7px}
.plan .pr{margin-left:auto;font-weight:800;color:var(--ink)}
.plan input{accent-color:var(--purple)}
.incl{list-style:none;margin:12px 0 0;padding:0;font-size:13.5px;color:var(--text)}.incl li{padding:4px 0;display:flex;gap:8px}.incl li:before{content:"✓";color:var(--teal);font-weight:800}
.stripe{display:block;text-align:center;font-size:12px;color:var(--ter);margin-top:10px;white-space:nowrap}
.ccard{padding:16px;display:flex;gap:12px;align-items:center}
.ccard b{display:block;color:var(--ink);font-size:15px}.ccard span{font-size:13px;color:var(--muted)}
.ccard .pill{margin-left:auto}
.small{font-size:13px;color:var(--muted)}
/* tool table */
.tools{width:100%;border-collapse:collapse;font-size:14px}.tools td{padding:9px 8px 9px 0;border-bottom:1px solid var(--border);vertical-align:top}.tools td:first-child{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;color:var(--purple);white-space:nowrap;width:220px}
/* creator page */
.chead{padding:26px 28px;display:flex;gap:20px;align-items:center}
.chead h1{font-size:26px;font-weight:800}.chead .h{color:var(--muted);font-size:14px}.chead p{margin:6px 0 0;font-size:15px}
.chead .nums{display:flex;gap:18px;margin-top:8px;font-size:13.5px;color:var(--muted)}.chead .nums b{color:var(--ink)}
/* wizard */
.wiz{display:grid;grid-template-columns:230px minmax(0,1fr);gap:20px;align-items:start}.wiz>*{min-width:0}
.wsteps{padding:14px;position:sticky;top:92px}
.wsteps div{display:flex;gap:10px;align-items:center;padding:10px 8px;border-radius:10px;font-size:14px;font-weight:600;color:var(--muted)}
.wsteps div.on{background:var(--lav2);color:var(--purple)}.wsteps div.done{color:var(--tealx)}
.wsteps i{width:24px;height:24px;border-radius:50%;background:var(--bg);display:inline-flex;align-items:center;justify-content:center;font-style:normal;font-size:12px;font-weight:800;flex:none}
.wsteps div.on i{background:var(--purple);color:#fff}.wsteps div.done i{background:var(--teal);color:#fff}
.wpanel{padding:26px 28px}
.wpanel h2{font-size:22px;font-weight:800;margin-bottom:4px}.wpanel .lead{color:var(--muted);margin:0 0 20px;font-size:14.5px}
.f{margin-bottom:18px}.f label{display:block;font-weight:700;font-size:13.5px;color:var(--ink);margin-bottom:6px}.f .hint{font-size:12.5px;color:var(--muted);margin-top:5px}
.f input[type=text],.f input[type=number],.f textarea,.f select{width:100%;border:1px solid var(--border);border-radius:12px;padding:10px 12px;background:#fff;outline:0;font:inherit;font-size:14.5px;color:var(--ink)}
.f select{appearance:none;-webkit-appearance:none;padding-right:38px;background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%2372777F' stroke-width='1.6'/%3E%3C/svg%3E") no-repeat right 14px center;cursor:pointer;font-weight:600}
.f select.msel{width:auto;min-width:132px;flex:none;margin-left:auto;border-radius:999px;padding:7px 36px 7px 14px;font-size:13.5px;line-height:1.2;background-position:right 13px center}
.price.pro{background:var(--lav);color:var(--p600)}
.btiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}.btile{display:flex;align-items:center;gap:10px;padding:8px 10px;border:1px solid var(--border);border-radius:12px;background:#fff;text-align:left;cursor:pointer}.btile:hover{background:var(--bg)}.btile.on{background:var(--tealt);border-color:var(--teal)}.btile .bl{width:32px;height:32px;border-radius:8px;overflow:hidden;flex:none;border:1px solid var(--border)}.btile .bl img{width:100%;height:100%;object-fit:cover;display:block}.btile .bn{font-weight:700;font-size:13.5px;color:var(--ink);line-height:1.15;min-width:0}.btile .bn small{display:block;font-weight:600;color:var(--muted);font-size:11.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.emojis .up{position:relative;overflow:hidden;font-size:11px;font-weight:700;color:var(--muted);line-height:1.1;background:#fff;border:1px dashed var(--border)}.emojis .up img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.emojis .up.on{outline:2px solid var(--purple)}
.f input:focus,.f textarea:focus,.f select:focus{border-color:var(--purple);box-shadow:0 0 0 3px var(--lav2)}
.f textarea{min-height:84px;resize:vertical}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.drop{border:2px dashed #cfc9f7;border-radius:14px;padding:26px;text-align:center;background:#faf9ff;cursor:pointer}
.drop b{display:block;color:var(--ink);font-size:15px}.drop span{font-size:13px;color:var(--muted)}
.drop.ok{border-style:solid;border-color:var(--teal);background:var(--tealt)}
.emojis{display:flex;gap:6px;flex-wrap:wrap}.emojis button{width:40px;height:40px;border-radius:10px;background:var(--bg);font-size:20px}.emojis button.on{background:var(--lav);outline:2px solid var(--purple)}
.checks{display:flex;flex-direction:column;gap:8px}
.check{display:flex;gap:10px;align-items:center;border:1px solid var(--border);border-radius:12px;padding:10px 12px;font-size:14px}
.check.ok{border-color:var(--teal);background:var(--tealt)}.check.bad{border-color:#f3b8c6;background:var(--redt)}
.pcards{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.pcard{border:1.5px solid var(--border);border-radius:14px;padding:14px;cursor:pointer}
.pcard.on{border-color:var(--purple);background:var(--lav2)}
.pcard b{display:block;color:var(--ink);font-size:15px}.pcard span{font-size:12.5px;color:var(--muted)}
.payout{background:var(--bg);border-radius:14px;padding:14px 16px;font-size:14px}
.payout div{display:flex;justify-content:space-between;padding:4px 0}.payout div.tot{border-top:1px solid var(--border);margin-top:6px;padding-top:8px;font-weight:800;color:var(--ink)}
.sug{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}.sug button{border:1px solid var(--border);border-radius:999px;padding:4px 11px;font-size:12.5px;font-weight:700;background:#fff}
.tog{display:flex;gap:10px;align-items:center;font-size:14px;color:var(--ink);font-weight:600}
.tog input{width:40px;height:22px;appearance:none;background:#d7d9df;border-radius:999px;position:relative;cursor:pointer;flex:none}.tog input:checked{background:var(--purple)}.tog input:after{content:"";position:absolute;top:3px;left:3px;width:16px;height:16px;border-radius:50%;background:#fff;transition:left .15s}.tog input:checked:after{left:21px}
.wnav{display:flex;justify-content:space-between;align-items:center;margin-top:26px;padding-top:18px;border-top:1px solid var(--border)}
.preview{border:1px solid var(--border);border-radius:14px;padding:14px;background:var(--bg)}
.review-ok{display:flex;gap:12px;align-items:center;background:var(--yellowt);border-radius:12px;padding:12px 14px;font-size:14px;margin-bottom:18px}
/* manage */
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}
.kpi{padding:14px 16px}.kpi span{font-size:12.5px;color:var(--muted);display:block}.kpi b{font-size:22px;font-weight:800;color:var(--ink)}
/* modal */
.modal{position:fixed;inset:0;background:rgba(23,23,23,.45);display:flex;align-items:center;justify-content:center;z-index:50;padding:20px}
.mbox{background:#fff;border-radius:20px;width:100%;max-width:520px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.25)}
.mbox .mh{padding:18px 22px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px}
.mbox .mh b{font-size:16px;color:var(--ink)}.mbox .mh .x{margin-left:auto;font-size:20px;color:var(--muted)}
.mbox .mb{padding:20px 22px}
.sline{display:flex;justify-content:space-between;font-size:14px;padding:6px 0}
.sline.tot{border-top:1px solid var(--border);margin-top:6px;padding-top:10px;font-weight:800;color:var(--ink)}
.fake{border:1px solid var(--border);border-radius:12px;padding:10px 12px;font-size:14px;color:var(--ter);background:#fafafa;margin:6px 0}
.success{text-align:center;padding:40px 24px}
.success .big{font-size:56px}.success h1{font-size:26px;margin:10px 0 6px}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--ink);color:#fff;border-radius:999px;padding:10px 18px;font-size:14px;font-weight:600;z-index:60;box-shadow:0 8px 24px rgba(0,0,0,.2)}
footer{margin:40px 0 20px;text-align:center;font-size:12.5px;color:var(--ter)}
footer a{color:var(--muted)}
.empty{padding:40px;text-align:center;color:var(--muted)}
@media (max-width:980px){.grid,.grid.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.sk .bot .upd{display:none}.detail{grid-template-columns:1fr}.side{position:static}.wiz{grid-template-columns:1fr}.wsteps{position:static;display:flex;overflow:auto;gap:4px}.wsteps div{white-space:nowrap}.pcards{grid-template-columns:repeat(2,1fr)}.kpis{grid-template-columns:repeat(2,1fr)}}
@media (max-width:720px){.wrap{padding:16px}.appbar{padding:0 16px}.hero .side{display:flex}.hero .stack .ava{width:40px!important;height:40px!important}.grid,.grid.g2{grid-template-columns:minmax(0,1fr)}.chead{flex-direction:column;align-items:flex-start}.chead .nums{flex-wrap:wrap;gap:10px}.tools td:first-child{white-space:normal;width:auto;min-width:96px;overflow-wrap:anywhere;word-break:normal}.stats div{margin-right:10px;padding-right:8px}.hero .stats{gap:18px}.dhead .by{font-size:13px}.grid{grid-template-columns:1fr}.hero{grid-template-columns:1fr;padding:22px 18px}.hero h1{font-size:26px}.hero .side{display:none}.appbar{padding:0 16px;gap:10px}.appbar nav{display:none}.appbar .logo .prod{display:none}.dhead{padding:18px;flex-direction:column}.dbody,.dtabs{padding-left:18px;padding-right:18px}.dtabs button{margin-right:14px;font-size:14px}.rsum{grid-template-columns:1fr}.row2{grid-template-columns:1fr}.wpanel{padding:18px}.pcards{grid-template-columns:1fr 1fr}}
/* ---- design pass (v11) ---- */
h1,h2,h3,h4{letter-spacing:0}.hero h1{letter-spacing:0}
:focus-visible{outline:2px solid var(--purple);outline-offset:2px}
.chip:hover,.itabs button:hover,.sug button:hover{background:var(--bg)}.pcard:hover,.plan:hover{border-color:var(--purple)}
.chip.on{background:var(--tealt);color:var(--tealx);border-color:var(--tealt)}.itabs button.on{background:var(--tealt);color:var(--tealx);border-color:var(--tealt)}
.tabs button .n{color:var(--muted)}.dtabs button{font-size:16px}
.grid{align-items:start}
.sk .bot{border-top-color:var(--border);flex-wrap:wrap;row-gap:4px}.sk .bot>span{white-space:nowrap}.sk .bot .upd{color:var(--muted)}.g2 .sk .bot .upd{display:none}
.sk .em{border-radius:12px}.dhead .em{border-radius:16px}
.sk .shot{height:auto;aspect-ratio:16/9}
.gal img{aspect-ratio:3/2;object-fit:cover;object-position:top}
.hl2{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;list-style:none;margin:0;padding:0}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.stats div{padding:12px 0 0;margin:0}
.hero .stats{display:flex;border-top:0;margin-top:18px}.hero .stats div{padding:0;margin:0}
.ccard{flex-wrap:wrap}.ccard>div{flex:1;min-width:0}.ccard .pill{flex-basis:100%;margin-left:0}
.hint{font-size:12.5px;color:var(--muted);margin-top:5px}
footer{padding:0 16px;color:var(--muted)}
.brokers .bl{gap:14px}.brokers img{height:16px}.brokers .more{color:var(--muted)}
.sample,.compose,.drop,.pcard,.payout,.preview{border-radius:12px}
.sample .lbl{color:var(--muted)}.stripe{color:var(--muted)}
.tog input{background:#CCCBD0}.badge.beta{color:#AC8600}.drop{border-color:var(--lav);background:#FAF9FF}.check.bad{border-color:#F3B8C6}
.plan,.pcard{border-width:1px}.plan.on,.pcard.on{box-shadow:0 0 0 1px var(--purple)}
.plan input,.check input{width:18px;height:18px;accent-color:var(--purple)}
.f input:disabled,.compose textarea:disabled{background:var(--bg);color:var(--muted)}
.code{background:var(--bg);color:var(--ink)}.code .cp{background:#fff;color:var(--text);border:1px solid var(--border)}
.prompt .cp{border:1px solid var(--border);border-radius:999px;padding:3px 10px;background:#fff;color:var(--text);font-size:11.5px}
.dhead+.dbody{border-top:1px solid var(--border)}
.dbody h3{display:flex;align-items:center;gap:8px;font-size:17px}.dbody h3 svg,.skillmd summary svg{width:17px;height:17px;stroke:var(--muted);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
.check .st{width:20px;height:20px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;flex:none;background:var(--bg);color:var(--muted)}.check .st svg{width:12px;height:12px;stroke:currentColor;fill:none;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}.check .st.ok{background:var(--teal);color:#fff}.check .st.bad{background:var(--red);color:#fff}.check .st.soft{background:var(--lav);color:var(--p600)}
.reqrow .em svg{width:18px;height:18px;stroke:var(--p600);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.check .mt{width:32px;height:32px;border-radius:8px;overflow:hidden;background:var(--tealt);display:inline-flex;align-items:center;justify-content:center;font-size:17px;flex:none}
.f label.tog{display:flex;margin-bottom:0}
.wpanel h2{font-size:24px}.chead h1{font-size:28px}
.tools td:first-child{width:auto;padding-right:18px}
.sidebar{width:256px;padding-bottom:0}.sidebar a{padding:13px 12px;font-size:16px}.sidebar a svg,.sidebar .sec svg{width:16px;height:16px}.sidebar a.on{color:var(--teal)}.sidebar hr{margin:12px 4px}.sidebar .sec{font-size:16px;padding:10px 12px}.sidebar .sub{padding:8px 12px 8px 58px;font-weight:600}.sidebar .topic{padding:7px 12px 7px 30px}
.sidebar .new{background:var(--beevis);font-size:10px;letter-spacing:0;padding:2px 8px}
.sidebar .bottom{position:sticky;bottom:0;background:#fff;padding-bottom:18px;margin-top:auto}
.sidebar .sec .chev{width:16px;height:16px;stroke:var(--muted);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.price{font-size:12.5px}
@media (max-width:980px){.sk .bot .upd{display:inline}}
@media (max-width:720px){.stats{grid-template-columns:1fr 1fr}.hl2{grid-template-columns:1fr}.md table{min-width:520px}.wsteps{display:none}.filters{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;padding-bottom:4px}.filters::-webkit-scrollbar{display:none}.filters .sp{display:none}.filters select{flex:none}.filters .chip{flex:none}.modal{align-items:flex-end;padding:0}.mbox{border-radius:20px 20px 0 0;max-width:none}.sk .shot{display:none}.g2 .sk .bot .upd,.sk .bot .upd{display:none}.tools td:first-child{white-space:normal}}
"""

JS = r"""
const D = __DATA__;
const BROKERS = __BROKERS__;
function brokerStrip(note){ return `<div class="brokers"><div class="bl">${BROKERS.map(([n,b])=>`<img src="data:image/png;base64,${b}" alt="${n}" title="${n}">`).join('')}<span class="more">+ 14 more</span></div><div class="small">${note}</div></div>`; }
const SITE = D.site;
const I = (d)=>`<svg viewBox="0 0 24 24" aria-hidden="true">${d}</svg>`;
const IC = {
  check: I('<path d="M20 6L9 17l-5-5"/>'), chat: I('<path d="M21 12a8 8 0 0 1-8 8H6l-3 3V12a8 8 0 0 1 8-8h2a8 8 0 0 1 8 8z"/>'), sparkle: I('<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.8 2.2L22 20l-2.2.8L19 23l-.8-2.2L16 20l2.2-.8z"/>'),
  plug: I('<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0zM12 18v4"/>'), plus: I('<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>'), gear: I('<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>'),
  file: I('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>'), wrench: I('<path d="M14.7 6.3a4 4 0 0 0 5 5l-9.4 9.4a2.1 2.1 0 0 1-3-3l9.4-9.4z"/><path d="M14.7 6.3L17 4l3 3-2.3 2.3"/>'), lock: I('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'),
  puzzle: I('<path d="M10 3h4v3a2 2 0 1 0 4 0h3v4h-3a2 2 0 1 0 0 4h3v4h-3a2 2 0 1 0-4 0v3h-4v-3a2 2 0 1 0-4 0H3v-4h3a2 2 0 1 0 0-4H3V6h3a2 2 0 1 0 4 0z"/>'), refresh: I('<path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/>'), x: I('<path d="M18 6L6 18M6 6l12 12"/>'), circle: I('<circle cx="12" cy="12" r="8"/>'),
};
// ---- Stripe Payment Links (test mode). Paste the link for each paid plan; null = not wired yet (mock checkout opens).
const PAYLINKS = {
  'dividend-income-planner': {monthly:'https://buy.stripe.com/test_8x2aEZaUOazn4nR0fd8so00', yearly:null},
  'tfsa-rrsp-optimizer': {once:null},
  'crowd-flow-scanner': {monthly:null, yearly:null},
  'canadian-bank-earnings-prep': {monthly:null},
  'risk-concentration-check': {yearly:null},
  'fundamentals-deep-dive': {monthly:null, yearly:null},
  'crypto-allocation-guardrails': {yearly:null},
  'rebalance-planner': {monthly:null, yearly:null},
};
const TAKE = 0.20, STRIPE_PCT = 0.029, STRIPE_FIX = 0.30;
const ME = 'maxstocks';
const $ = (s, el=document) => el.querySelector(s);
const esc = s => String(s??'').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmtN = n => n >= 1000 ? (n/1000).toFixed(n>=10000?0:1).replace(/\.0$/,'')+'K' : String(n);
const money = v => '$' + (Number.isInteger(v) ? v : v.toFixed(2));
const ago = d => { const days = Math.round((new Date('2026-11-07') - new Date(d))/86400000); return days<=0?'today':days===1?'1 day ago':days<30?days+' days ago':Math.round(days/30)+' mo ago'; };
const LS = { get:(k,d)=>{try{return JSON.parse(localStorage.getItem('bs_'+k))??d}catch(e){return d}}, set:(k,v)=>{try{localStorage.setItem('bs_'+k,JSON.stringify(v))}catch(e){}} };
let state = { tab:'skills', cat:'All', sort:'top', q:'', dtab:'overview', itab:'claude', plan:null, wiz:null };
const mine = () => LS.get('mine', []);
const allSkills = () => D.skills.concat(mine());
const skill = id => allSkills().find(s=>s.id===id);
const mcp = id => D.mcps.find(m=>m.id===id);
const listedMcps = () => D.mcps.filter(m=>!m.compat);   // broker MCPs (compat:true) aren't listed; skills can still say they're compatible with them
const creator = h => D.creators[h];
const owned = () => LS.get('owned', {});

function toast(t){ document.querySelectorAll('.toast').forEach(x=>x.remove()); const el=document.createElement('div'); el.className='toast'; el.textContent=t; document.body.appendChild(el); setTimeout(()=>el.remove(),2200); }
function copy(t, msg='Copied'){ navigator.clipboard?.writeText(t).then(()=>toast(msg),()=>toast(msg)); }
function avatar(h, size=28){
  const c = creator(h); if(!c) return `<span class="ava" style="width:${size}px;height:${size}px;background:#ddd"></span>`;
  if (c.beevis) return `<span class="ava" style="width:${size}px;height:${size}px"><img src="data:image/svg+xml;base64,__BEEVIS__" alt=""></span>`;
  if (c.photo_b64) return `<span class="ava" style="width:${size}px;height:${size}px;border:1px solid var(--border);background:#fff"><img src="data:image/jpeg;base64,${c.photo_b64}" alt=""></span>`;
  if (c.logo) return `<span class="ava" style="width:${size}px;height:${size}px;background:#fff;border:1px solid var(--border)"><img src="data:image/jpeg;base64,__FLOWER__" alt="" style="width:70%;height:70%"></span>`;
  return `<span class="ava" style="width:${size}px;height:${size}px;background:${c.color};font-size:${Math.round(size*.38)}px">${c.initials}</span>`;
}
const VB = `<img class="vb" src="data:image/svg+xml;base64,__BADGE__" alt="verified">`;
function badge(c){ if(!c) return ''; if(c.badge==='verified') return VB; if(c.badge==='official') return VB+` <span class="badge official">Blossom</span>`; if(c.badge==='ambassador') return VB+` <span class="badge ambassador">Ambassador</span>`; if(c.badge==='pro') return `<span class="badge pro">PRO</span>`; return ''; }
function stars(r){ const full=Math.round(r); return '<span class="star">'+'★'.repeat(full)+'</span><span style="color:#ddd">'+'★'.repeat(5-full)+'</span>'; }
function priceLabel(p){ if(p.free) return {t:'Free',cls:'free'}; if(p.monthly) return {t:money(p.monthly)+'/mo',cls:''}; if(p.yearly) return {t:money(p.yearly)+'/yr',cls:''}; if(p.once) return {t:money(p.once)+' once',cls:''}; return {t:'Free',cls:'free'}; }
function sIcon(s){ return s.icon?`<img src="${s.icon}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">`:s.emoji; }
// MCP icon: a partner logo when one is set, else the emoji. `tile` = the big square on cards/detail; otherwise inline.
function mIcon(m, tile){ if(!m.logo_b64) return m.emoji; return tile ? `<img src="data:image/png;base64,${m.logo_b64}" alt="${esc(m.name)}" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">` : `<img src="data:image/png;base64,${m.logo_b64}" alt="" style="width:1em;height:1em;border-radius:3px;vertical-align:-2px">`; }
const SHORT={'blossom-connector':'Connector','blossom-trade-data':'Trade Data','fiscal-ai':'Fiscal.ai','public-mcp':'Public.com','questrade-mcp':'Questrade','robinhood-mcp':'Robinhood','webull-mcp':'Webull','moomoo-mcp':'moomoo','ibkr-mcp':'IBKR','alpaca-mcp':'Alpaca','schwab-mcp':'Schwab','tradier-mcp':'Tradier'};
function reqChips(s){ return (s.requires||[]).map(r=>{const m=mcp(r); return m?`<span class="chip rq" title="${esc(m.name)}">${mIcon(m)} ${SHORT[r]||esc(m.name)}</span>`:''}).join('') + (s.optional||[]).map(r=>{const m=mcp(r); return m?`<span class="chip rq opt" title="Optional: ${esc(m.name)}">${mIcon(m)} ${SHORT[r]||esc(m.name)} <i>optional</i></span>`:''}).join(''); }

// tiny markdown: bold, inline code, tables, code blocks, lists, links
function md(src){
  const lines = src.split('\n'); let out=[], i=0;
  const inl = t => esc(t).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/\*(.+?)\*/g,'<i>$1</i>').replace(/`(.+?)`/g,'<code>$1</code>').replace(/\[(.+?)\]\((.+?)\)/g,'<a href="$2">$1</a>').replace(/\[(.+?)\]/g,'<a href="#">$1</a>');
  while(i<lines.length){
    const l=lines[i];
    if(l.startsWith('```')){ let j=i+1, buf=[]; while(j<lines.length && !lines[j].startsWith('```')){buf.push(lines[j]);j++;} out.push('<pre>'+esc(buf.join('\n'))+'</pre>'); i=j+1; continue; }
    if(l.startsWith('|')){ let rows=[]; while(i<lines.length && lines[i].startsWith('|')){ rows.push(lines[i]); i++; } rows=rows.filter(r=>!/^\|\s*-/.test(r)); const cells=r=>r.split('|').slice(1,-1).map(c=>c.trim()); out.push('<table><tr>'+cells(rows[0]).map(c=>'<th>'+inl(c)+'</th>').join('')+'</tr>'+rows.slice(1).map(r=>'<tr>'+cells(r).map(c=>'<td>'+inl(c)+'</td>').join('')+'</tr>').join('')+'</table>'); continue; }
    if(/^\d+\. /.test(l)){ let items=[]; while(i<lines.length && /^\d+\. /.test(lines[i])){ items.push(lines[i].replace(/^\d+\. /,'')); i++; } out.push('<ol>'+items.map(x=>'<li>'+inl(x)+'</li>').join('')+'</ol>'); continue; }
    if(/^[-•] /.test(l)){ let items=[]; while(i<lines.length && /^[-•] /.test(lines[i])){ items.push(lines[i].slice(2)); i++; } out.push('<ul>'+items.map(x=>'<li>'+inl(x)+'</li>').join('')+'</ul>'); continue; }
    if(l.trim()===''){ i++; continue; }
    out.push('<p>'+inl(l)+'</p>'); i++;
  }
  return out.join('');
}

// ---------- router
function route(){
  state.itab='claude'; document.querySelectorAll('.modal,.lb').forEach(m=>m.remove());
  const h = location.hash || '#/';
  const q = new URLSearchParams(location.search);
  if(q.get('checkout')==='success'){ const id=q.get('skill'), plan=q.get('plan')||'monthly'; const o=owned(); o[id]=plan; LS.set('owned',o); history.replaceState(null,'','?'+'#/success/'+id+'/'+plan); return route(); }
  const parts = h.slice(2).split('/');
  window.scrollTo(0,0);
  const app = $('#app');
  if(parts[0]==='' ){ state.tab='skills'; app.innerHTML=library(); bindLibrary(); }
  else if(parts[0]==='terms'){ app.innerHTML=terms(); }
  else if(parts[0]==='mcps'){ state.tab='mcps'; app.innerHTML=library(); bindLibrary(); }
  else if(parts[0]==='skill'){ app.innerHTML=detail(parts[1]); bindDetail(parts[1]); }
  else if(parts[0]==='mcp'){ app.innerHTML=mcpDetail(parts[1]); bindMcp(parts[1]); }
  else if(parts[0]==='u'){ app.innerHTML=creatorPage(parts[1]); bindLibrary(); }
  else if(parts[0]==='post'){ if(!state.wiz) state.wiz=newWiz(); app.innerHTML=wizard(); bindWizard(); }
  else if(parts[0]==='manage'){ app.innerHTML=manage(parts[1]); bindManage(parts[1]); }
  else if(parts[0]==='success'){ app.innerHTML=success(parts[1], parts[2]); bindDetail(parts[1]); }
  else { app.innerHTML=library(); bindLibrary(); }
}
window.addEventListener('hashchange', route);

// ---------- library
function skillCard(s){
  const c=creator(s.creator); const p=priceLabel(s.price);
  return `<div class="card sk" data-go="#/skill/${s.id}">
    <div class="top"><div class="em">${sIcon(s)}</div><div style="min-width:0"><h3>${esc(s.name)}${s.trades?' <span class="badge warn">⚠️ can place orders</span>':''}</h3><div class="by">${avatar(s.creator,20)} <b>@${esc(s.creator)}</b> ${badge(c)}</div></div></div>
    <p>${esc(s.pitch)}</p>
    ${(s.shots||[]).length?`<img class="shot" src="shots/${s.shots[0][0]}" alt="" loading="lazy">`:''}
    ${(s.highlights||[]).length?`<ul class="hl">${s.highlights.slice(0,3).map(h=>`<li>${esc(h)}</li>`).join('')}</ul>`:''}
    <div class="req">${reqChips(s)}</div>
    <div class="bot"><span>${fmtN(s.downloads)} downloads</span><span>${s.ratings?`${stars(s.rating)} <b style="color:var(--ink)">${s.rating.toFixed(1)}</b> <span style="color:var(--muted)">(${s.ratings})</span>`:'No ratings yet'}</span><span class="upd">v${s.version} · updated ${ago(s.updated)}${(s.shots||[]).length?` · ${s.shots.length} screenshot${s.shots.length===1?'':'s'}`:''}</span><span class="sp"></span><span class="price ${p.cls}">${p.t}</span></div>
  </div>`;
}
function mcpCard(m){
  const by = m.creator ? `${avatar(m.creator,20)} <b>@${m.creator}</b> ${badge(creator(m.creator))}` : `<span class="small">by <b style="color:var(--ink)">${esc(m.creator_name)}</b></span>`;
  return `<div class="card sk" data-go="#/mcp/${m.id}">
    <div class="top"><div class="em mcp">${mIcon(m,true)}</div><div style="min-width:0"><h3>${esc(m.name)} ${m.status?`<span class="badge ${m.status==='Broker'?'broker':m.status==='Partner'?'partner':'beta'}">${m.status}</span>`:''}${m.trades?' <span class="badge warn">⚠️ can place orders</span>':''}</h3><div class="by">${by}</div></div></div>
    <p>${esc(m.pitch)}</p>
    <ul class="hl">${m.tools.slice(0,3).map(([t,d])=>`<li><b style="font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:var(--purple);font-weight:600">${esc(t)}</b> <span>${esc(d.split('.')[0])}</span></li>`).join('')}</ul><div class="req"><span class="chip rq">${m.tools.length} tools</span><span class="chip rq">${m.auth.split('·')[0].trim()}</span></div>
    <div class="bot"><span>${fmtN(m.installs)} connected</span><span>${stars(m.rating)} <b style="color:var(--ink)">${m.rating.toFixed(1)}</b></span><span class="sp"></span><span class="price ${/^Free/.test(m.price)?'free':/PRO\+/.test(m.price)?'pro':''}">${esc(m.price.split('·')[0].trim().replace('Requires Blossom PRO+','PRO+'))}</span></div>
  </div>`;
}
function library(){
  const cats = ['All','Portfolio','Earnings','Dividends','Screens','Social','Research','Canada','Crypto','News'];
  let list = allSkills().filter(s=>state.cat==='All'||s.cat===state.cat).filter(s=>!state.q||(s.name+' '+s.pitch+' '+s.creator+' '+s.cat).toLowerCase().includes(state.q.toLowerCase()));
  const mo = s => s.price.free?0:(s.price.monthly||(s.price.yearly||0)/12||(s.price.once||0)/12);   // monthly-equivalent price for sorting
  const sorters = {top:(a,b)=>b.rating*Math.log(b.ratings+1)-a.rating*Math.log(a.ratings+1), dl:(a,b)=>b.downloads-a.downloads, new:(a,b)=>b.updated.localeCompare(a.updated), price:(a,b)=>mo(a)-mo(b), pricehi:(a,b)=>mo(b)-mo(a)};
  list.sort(sorters[state.sort]);
  const totalDl = D.skills.reduce((a,s)=>a+s.downloads,0);
  const hero = `<div class="hero"><div>
      <h1>🤖 The Best Skills and MCPs for&nbsp;Investors</h1>
      <p>Discover and download skills built by Blossom investors for Claude, ChatGPT, Grok and Cursor to supercharge your investing.</p>
      <div class="search"><span style="color:var(--muted)">🔍</span><input id="q" placeholder="Search skills, creators, tickers… try “dividends”" value="${esc(state.q)}"><button class="pill pri sm" id="qgo">Search</button></div>
      <div class="stats"><div><b>${allSkills().length}</b><span>skills</span></div><div><b>${listedMcps().length}</b><span>MCPs</span></div><div><b>${fmtN(totalDl)}</b><span>downloads</span></div><div><b>${Object.keys(D.creators).length}</b><span>creators</span></div></div>
    </div>
    <div class="side">
      <div class="stack">${['maxstocks','dividendsdan','tfsa_tina','northofthe49','quantqueen','earningsedge'].map(h=>avatar(h,48)).join('')}</div>
      <div class="t">Built by verified investors on Blossom<span>${Object.keys(D.creators).length} creators · ${fmtN(totalDl)} downloads</span></div>
    </div></div>`;
  const tabs = `<div class="tabs"><button class="${state.tab==='skills'?'on':''}" data-tab="skills">Skills<span class="n">${allSkills().length}</span></button><button class="${state.tab==='mcps'?'on':''}" data-tab="mcps">MCPs<span class="n">${listedMcps().length}</span></button><span class="sp" style="flex:1"></span><a class="pill pri sm" href="#/post" style="align-self:center">+ Post a skill</a></div>`;
  let body='';
  if(state.tab==='skills'){
    body = `<div class="filters">${cats.map(c=>`<button class="chip ${state.cat===c?'on':''}" data-cat="${c}">${c}</button>`).join('')}<span class="sp"></span><select id="sort"><option value="top" ${state.sort==='top'?'selected':''}>Top rated</option><option value="dl" ${state.sort==='dl'?'selected':''}>Most downloaded</option><option value="new" ${state.sort==='new'?'selected':''}>Recently updated</option><option value="price" ${state.sort==='price'?'selected':''}>Price: low to high</option><option value="pricehi" ${state.sort==='pricehi'?'selected':''}>Price: high to low</option></select></div>
      <div class="grid">${list.map(skillCard).join('')||'<div class="empty">Nothing matches that yet. <a href="#/post">Post the first one →</a></div>'}</div>`;
  } else {
    body = `<p class="small" style="margin:0 0 16px">An MCP is what gives a skill its data. Connect one once and every skill that needs it just works.</p><div class="grid">${listedMcps().map(mcpCard).join('')}</div>
      <div class="card" style="margin-top:18px;padding:18px 22px;display:flex;gap:16px;align-items:center;background:linear-gradient(100deg,#fff,#F1F5F7)"><div style="font-size:30px">🧩</div><div><b style="color:var(--ink)">MCPs are listed by Blossom and its partners.</b><div class="small">Built an MCP investors would use? Tell us what it does and who it’s for and we'll consider adding it to the library!</div></div><a class="pill out sm" style="margin-left:auto" href="mailto:partnerships@blossomsocial.com?subject=MCP%20listing%20on%20Blossom%20Skills">Get in touch</a></div>`;
  }
  return `<div class="wrap">${hero}${tabs}${body}</div>`;
}
function bindLibrary(){
  document.querySelectorAll('[data-go]').forEach(el=>el.addEventListener('click',e=>{ if(e.target.closest('a,button')) return; location.hash=el.dataset.go; }));
  document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{ location.hash = b.dataset.tab==='mcps'?'#/mcps':'#/'; });
  document.querySelectorAll('[data-cat]').forEach(b=>b.onclick=()=>{ state.cat=b.dataset.cat; route(); });
  const so=$('#sort'); if(so) so.onchange=()=>{ state.sort=so.value; route(); };
  const q=$('#q'); if(q){ const go=()=>{ state.q=q.value; route(); const nq=$('#q'); if(nq){nq.focus(); nq.setSelectionRange(nq.value.length,nq.value.length);} }; q.addEventListener('keydown',e=>{ if(e.key==='Enter') go(); }); $('#qgo').onclick=go; }
}

// ---------- skill detail
function planOptions(s){
  const p=s.price, o=[];
  if(p.free) return [{k:'free',label:'Free',price:0}];
  if(p.once) o.push({k:'once',label:'One-time',price:p.once,sub:'Yours forever · includes updates for 12 months'});
  if(p.monthly) o.push({k:'monthly',label:'Monthly',price:p.monthly,sub:'Cancel anytime'});
  if(p.yearly) o.push({k:'yearly',label:'Yearly',price:p.yearly,sub:p.monthly?`Save ${Math.round((1-p.yearly/(p.monthly*12))*100)}%`:'Billed once a year'});
  return o;
}
function installBlock(s){
  const slug=s.id, url=`${SITE}/skills/${slug}/SKILL.md`;
  const tabs = {claude:'Claude', code:'Claude Code', cursor:'Cursor', chatgpt:'ChatGPT', grok:'Grok'};
  const content = {
    claude: `<ol class="steps"><li><b>Download</b> the skill with the button above (you get <code>${slug}/SKILL.md</code>).</li><li>In Claude: <b>Settings → Capabilities → Skills → Add skill</b>, and upload the folder.</li><li>Open a chat and type <i>“${esc(s.prompts[0])}”</i>. Claude will ask to connect ${(s.requires||[]).map(r=>mcp(r)?.name).filter(Boolean).join(' and ')||'nothing extra'} the first time.</li></ol>`,
    code: `<div class="code"><button class="cp" data-copy="mkdir -p ~/.claude/skills/${slug} && curl -fsSL ${url} -o ~/.claude/skills/${slug}/SKILL.md">Copy</button>mkdir -p ~/.claude/skills/${slug} \\
  && curl -fsSL ${url} \\
     -o ~/.claude/skills/${slug}/SKILL.md</div><p class="small" style="margin:10px 0 0">Then <code>/${slug}</code> in any session, or just ask in plain words.</p>`,
    cursor: `<div class="code"><button class="cp" data-copy="mkdir -p .cursor/rules && curl -fsSL ${url} -o .cursor/rules/${slug}.mdc">Copy</button>mkdir -p .cursor/rules \\
  && curl -fsSL ${url} -o .cursor/rules/${slug}.mdc</div><p class="small" style="margin:10px 0 0">Add the Blossom MCPs under <b>Cursor Settings → MCP</b> (snippets on each MCP page).</p>`,
    chatgpt: `<ol class="steps"><li>Open <b>ChatGPT → Projects → New project</b> and paste the skill file into the project instructions (download it above and copy the contents).</li><li>Enable <b>Developer mode</b> and add the MCPs this skill needs (connector URLs are on each MCP page).</li><li>Ask: <i>“${esc(s.prompts[0])}”</i></li></ol>`,
    grok: `<ol class="steps"><li>Add the MCPs this skill needs at <b>grok.com/connectors → New Connector → Custom</b> (the URL is on each MCP page; sign in when asked).</li><li>Grok has no skill files yet, so start a chat by pasting the SKILL.md (download it above) as your first message, then ask: <i>“${esc(s.prompts[0])}”</i>.</li><li>Pin that chat — or save the skill text as a Grok Project’s instructions if your plan has Projects.</li></ol>`
  };
  return `<div class="itabs">${Object.entries(tabs).map(([k,v])=>`<button class="${state.itab===k?'on':''}" data-itab="${k}">${v}</button>`).join('')}</div><div id="ibody">${content[state.itab]}</div>`;
}
function detail(id){
  const s=skill(id); if(!s) return `<div class="wrap"><div class="empty">That skill doesn’t exist (yet). <a href="#/">Back to the library</a></div></div>`;
  const c=creator(s.creator); const plans=planOptions(s); if(!state.plan||!plans.find(p=>p.k===state.plan)) state.plan=plans.find(p=>p.k==='yearly')?.k||plans[0].k;
  const have = owned()[s.id] || s.price.free;
  const sel = plans.find(p=>p.k===state.plan);
  const cta = s.price.free ? `<button class="pill pri lg" id="get">Get it free</button>` : have ? `<button class="pill teal lg" id="get">Download · you’re subscribed</button>` : `<button class="pill pri lg" id="buy">${sel.k==='once'?`Buy for ${money(sel.price)}`:`Subscribe · ${money(sel.price)}/${sel.k==='monthly'?'mo':'yr'}`}</button>`;
  const amt = s.price.free ? `<div class="amt">Free</div><div class="sub">Free. Needs the Blossom Connector (included with <b>Blossom PRO+</b>).</div>` : `<div class="amt">${money(sel.price)}<small> ${sel.k==='monthly'?'/ month':sel.k==='yearly'?'/ year':'one-time'}</small></div><div class="sub">${sel.k==='once'?'Pay once. Updates included for 12 months.':'Every update while you’re subscribed. Cancel anytime.'}</div>`;
  const planSel = plans.length>1 ? `<div class="plans">${plans.map(p=>`<label class="plan ${state.plan===p.k?'on':''}"><input type="radio" name="plan" value="${p.k}" ${state.plan===p.k?'checked':''}><div><b>${p.label}</b>${p.sub?(p.k==='yearly'&&/Save/.test(p.sub)?` <span class="save">${p.sub}</span>`:`<div class="small">${p.sub}</div>`):''}</div><span class="pr">${money(p.price)}${p.k==='monthly'?'/mo':p.k==='yearly'?'/yr':''}</span></label>`).join('')}</div>` : '';
  const dist = [5,4,3,2,1].map(n=>{ const share = n===5?Math.round((s.rating-4)*100): n===4?Math.round((5-s.rating)*80): n===3?Math.max(2,Math.round((5-s.rating)*18)):n===2?2:1; return [n,Math.max(0,Math.min(100,share))]; });
  const tot = dist.reduce((a,[,v])=>a+v,0);
  const reviews = (s.reviews||[]).map(([h,r,t],ri)=>`<div class="rev">${avatar(h,36)}<div style="flex:1"><div class="who"><b>@${h}</b> ${badge(creator(h))} · ${stars(r)} · <span style="color:var(--ter)">${['3 days','1 week','2 weeks','3 weeks'][h.length%4]} ago</span></div><p>${esc(t)}</p><div class="act"><span>Helpful (${(h.length*7+r*3)%37+3})</span><span>Reply</span><span>Report</span></div></div></div>`).join('');
  const tabsHtml = `<div class="dtabs"><button class="${state.dtab==='overview'?'on':''}" data-dtab="overview">Overview</button><button class="${state.dtab==='updates'?'on':''}" data-dtab="updates">Updates <span class="small">(${s.log.length})</span></button><button class="${state.dtab==='reviews'?'on':''}" data-dtab="reviews">Reviews <span class="small">(${s.ratings})</span></button></div>`;
  let body='';
  if(state.dtab==='overview') body = `
    <div class="blk"><h3>${IC.check}What it does</h3><ul class="hl hl2">${(s.highlights||[]).map(h=>`<li style="display:flex;gap:8px;font-size:14.5px"><span style="color:var(--teal);font-weight:800">✓</span>${esc(h)}</li>`).join('')}</ul></div>
    <div class="blk"><h3>${IC.chat}Try these prompts</h3><div class="prompts">${s.prompts.map(p=>`<div class="prompt"><span>“${esc(p)}”</span><button class="cp" data-copy="${esc(p)}">Copy</button></div>`).join('')}</div></div>
    <div class="blk"><h3>${IC.sparkle}What you get${(s.shots||[]).length?` <span class="small" style="font-weight:600">· ${s.shots.length} screenshot${s.shots.length===1?'':'s'} from real runs</span>`:''}</h3>${(s.shots||[]).length?`<div class="gal ${s.shots.length===1?'one':''}">${s.shots.map(([f,c])=>`<figure data-lb="shots/${f}"><img src="shots/${f}" alt="${esc(c)}" loading="lazy"><figcaption>${esc(c)}</figcaption></figure>`).join('')}</div><details style="margin-top:12px"><summary class="small" style="cursor:pointer;font-weight:700">Sample reply as text</summary><div class="sample" style="margin-top:8px"><div class="md">${md(s.sample)}</div></div></details>`:`<div class="sample"><span class="lbl">Sample output · what your AI replies</span><div class="md">${md(s.sample)}</div></div>`}</div>
    <div class="blk"><h3>${IC.plug}What it needs</h3>${(s.requires||[]).map(r=>{const m=mcp(r); return m?`<div class="reqrow"><div class="em">${mIcon(m,true)}</div><div><b>${esc(m.name)}</b><span>${esc(m.pitch.split('.')[0])}.</span></div><a class="pill sec sm" href="#/mcp/${m.id}">Connect</a></div>`:''}).join('')||'<p class="small">Nothing beyond your AI assistant.</p>'}${(s.requires||[]).includes('blossom-connector')?brokerStrip('<b style="color:var(--ink)">Works with your brokerage.</b> The Connector reads whatever you\'ve linked to Blossom, so this skill runs the same on Wealthsimple, Questrade, Robinhood, Public, IBKR, TD and the rest. Broker MCPs are optional extras.'):''}</div>
    ${(s.optional||[]).length?`<div class="blk"><h3>${IC.plus}Optional MCPs</h3><p class="small" style="margin:0 0 10px">Not required. If you have these connected, the skill uses them too.</p>${(s.optional||[]).map(r=>{const m=mcp(r); return m?`<div class="reqrow" style="border-style:dashed"><div class="em" style="background:var(--bg)">${mIcon(m,true)}</div><div><b>${esc(m.name)} <span class="badge" style="background:var(--tealt);color:var(--tealx)">optional</span></b><span>${esc(m.pitch.split('.')[0])}.</span></div><a class="pill sec sm" href="#/mcp/${m.id}">Details</a></div>`:''}).join('')}</div>`:''}
    <div class="blk"><h3>${IC.gear}How to install</h3>${installBlock(s)}</div>
    <div class="blk"><details class="skillmd"><summary>${IC.file}SKILL.md <span class="small" style="font-weight:600">· what your AI actually reads</span></summary><pre>${esc(s.skill)}</pre></details></div>`;
  else if(state.dtab==='updates') body = `
    <div class="promise"><span class="em">🔁</span><div><b style="color:var(--ink)">Updated ${esc(s.cadence.toLowerCase())}.</b> <span class="small">${s.price.free?'Free skills are updated at the creator’s pace.':'Subscribers get every update automatically and a DM when one ships — that’s what the subscription pays for.'}</span></div></div>
    <div class="tl">${s.log.map(([v,d,n],i)=>`<div class="tli"><span class="v">v${v}</span><span class="d">${new Date(d).toLocaleDateString('en-CA',{month:'short',day:'numeric',year:'numeric'})}</span>${i===0?'<span class="tag">Latest</span>':''}<p>${esc(n)}</p></div>`).join('')}</div>`;
  else body = `
    <div class="rsum"><div><div class="big">${s.rating.toFixed(1)}</div><div>${stars(s.rating)}</div><div class="small">${s.ratings} ratings · ${fmtN(s.downloads)} downloads</div></div><div class="bars">${dist.map(([n,v])=>`<div><span>${n} ★</span><i><b style="width:${Math.round(v/tot*100)}%"></b></i><span>${Math.round(v/tot*100)}%</span></div>`).join('')}</div></div>
    <div class="compose">${avatar(ME,36)}<div style="flex:1"><textarea placeholder="Ran it? Say what it did for you…" disabled></textarea><div class="note">Ratings and comments open when V1 goes live. Only people who downloaded the skill can rate it.</div></div></div>
    <div style="margin-top:14px">${reviews}</div>`;
  const cc = `<div class="card ccard">${avatar(s.creator,44)}<div><b>${esc(c?.name||s.creator)} ${badge(c)}</b><span>@${esc(s.creator)} · ${fmtN(c?.followers||0)} followers</span></div><a class="pill sec sm" href="#/u/${s.creator}">Blossom profile</a></div>`;
  const reqs = '' && (s.requires||[]).length ? `<div class="card" style="padding:14px 16px"><b style="color:var(--ink);font-size:13.5px">Needs</b>${(s.requires||[]).map(r=>{const m=mcp(r);return m?`<div style="display:flex;gap:8px;align-items:center;margin-top:8px;font-size:13.5px"><span>${m.emoji}</span><a href="#/mcp/${m.id}">${esc(m.name)}</a><span class="small" style="margin-left:auto">${/^Free/.test(m.price)?'free':'from free'}</span></div>`:''}).join('')}</div>`:'';
  return `<div class="wrap"><div class="small" style="margin-bottom:12px"><a href="#/">Skills</a> › ${esc(s.cat)} › ${esc(s.name)}</div>
  <div class="detail"><div>
    <div class="card"><div class="dhead"><div class="em">${sIcon(s)}</div><div style="flex:1;min-width:0"><h1>${esc(s.name)}${s.trades?' <span class="badge warn">⚠️ can place orders</span>':''}</h1><div class="pitch">${esc(s.pitch)}</div><div class="by">${avatar(s.creator,24)} <b>${esc(c?.name||s.creator)}</b> @${esc(s.creator)} ${badge(c)}<button class="pill teal sm" id="follow" style="margin-left:6px">Follow</button></div>
      <div class="stats"><div><b>${fmtN(s.downloads)}</b>downloads</div><div><b>${stars(s.rating)} ${s.rating.toFixed(1)}</b>${s.ratings} ratings</div><div><b>v${s.version}</b>updated ${ago(s.updated)}</div><div><b>${esc(s.cadence.split(',')[0].slice(0,16))}</b>update cadence</div></div></div></div>
      ${tabsHtml}<div class="dbody">${body}</div></div>
  </div>
  <div class="side">
    <div class="card buy">${amt}${planSel}${cta}${s.price.free?'':`<div class="stripe">Secure checkout by <b>Stripe</b> · 80% goes to the creator</div>`}
      <ul class="incl"><li>Works in Claude, Claude Code, Cursor, ChatGPT, Grok</li><li>${s.price.free?'Updates at the creator’s pace':'Every update while subscribed'}</li><li>${s.trades?'⚠️ Can place orders through your broker MCP':'Read-only: never places trades'}</li>${s.price.free?'':'<li>Cancel anytime from Settings → Subscriptions</li>'}</ul>
      <button class="pill sec" id="share" style="width:100%;margin-top:12px">Share</button></div>
    ${cc}${reqs}
  </div></div></div>`;
}
function bindDetail(id){
  const s=skill(id); if(!s) return;
  document.querySelectorAll('[data-dtab]').forEach(b=>b.onclick=()=>{ state.dtab=b.dataset.dtab; route(); });
  document.querySelectorAll('[data-itab]').forEach(b=>b.onclick=()=>{ state.itab=b.dataset.itab; $('#ibody').innerHTML = installBlock(s).replace(/^[\s\S]*?<div id="ibody">/,'').replace(/<\/div>$/,''); document.querySelectorAll('[data-itab]').forEach(x=>x.classList.toggle('on',x.dataset.itab===state.itab)); bindCopy(); });
  document.querySelectorAll('input[name=plan]').forEach(r=>r.onchange=()=>{ state.plan=r.value; route(); });
  bindCopy();
  const dl=()=>{ const blob=new Blob([s.skill+'\n'],{type:'text/markdown'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='SKILL.md'; a.click(); const d=LS.get('dl',{}); d[s.id]=(d[s.id]||0)+1; LS.set('dl',d); toast('Downloaded SKILL.md — put it in a folder named '+s.id); };
  const g=$('#get'); if(g) g.onclick=dl;
  const b=$('#buy'); if(b) b.onclick=()=>checkout(s, state.plan);
  const f=$('#follow'); if(f) f.onclick=()=>{ f.textContent='Following'; f.className='pill sec sm'; toast('Following @'+s.creator); };
  const sh=$('#share'); if(sh) sh.onclick=()=>copy(SITE+'/#/skill/'+s.id,'Link copied');
  document.querySelectorAll('[data-lb]').forEach(f=>f.onclick=()=>{ const m=document.createElement('div'); m.className='lb'; m.innerHTML=`<img src="${f.dataset.lb}" alt="">`; m.onclick=()=>m.remove(); document.body.appendChild(m); });
  document.querySelectorAll('[data-go]').forEach(el=>el.addEventListener('click',e=>{ if(e.target.closest('a,button')) return; location.hash=el.dataset.go; }));
}
function bindCopy(){ document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=e=>{ e.stopPropagation(); copy(b.dataset.copy); }); }

// ---------- checkout (Stripe Payment Links, test mode)
function checkout(s, plan){
  const link = (PAYLINKS[s.id]||{})[plan];
  const price = s.price[plan];
  if(link){ const u=new URL(link); u.searchParams.set('client_reference_id', ME+':'+s.id+':'+plan); location.href=u.toString(); return; }
  const take=price*TAKE, cr=price-take;
  const m=document.createElement('div'); m.className='modal'; m.innerHTML=`<div class="mbox"><div class="mh"><span style="font-size:18px">🔒</span><b>Checkout · ${esc(s.name)}</b><button class="x" id="mx">×</button></div><div class="mb">
    <div class="small" style="background:var(--yellowt);border-radius:10px;padding:8px 10px;margin-bottom:12px">Test mode · no Stripe Payment Link is set for this plan yet. When it is, this button opens real Stripe Checkout.</div>
    <div class="sline"><span>${esc(s.name)} · ${plan==='once'?'one-time':plan}</span><b>${money(price)}</b></div>
    <div class="sline tot"><span>Due today</span><span>${money(price)}</span></div>
    <div style="margin:14px 0 6px;font-size:12.5px;font-weight:700;color:var(--muted)">CARD</div><div class="fake">4242 4242 4242 4242</div><div style="display:flex;gap:8px"><div class="fake" style="flex:1">MM / YY</div><div class="fake" style="flex:1">CVC</div></div>
    <button class="pill pri lg" id="pay" style="margin-top:14px">Pay ${money(price)}</button>
    <div class="small" style="margin-top:12px">Of ${money(price)}: Blossom 20% ≈ ${money(+take.toFixed(2))} · creator ≈ <b>${money(+cr.toFixed(2))}</b></div>
  </div></div>`;
  document.body.appendChild(m);
  $('#mx',m).onclick=()=>m.remove(); m.addEventListener('click',e=>{ if(e.target===m) m.remove(); });
  $('#pay',m).onclick=()=>{ m.remove(); const o=owned(); o[s.id]=plan; LS.set('owned',o); location.hash='#/success/'+s.id+'/'+plan; };
}
function success(id, plan){
  const s=skill(id); if(!s) return library();
  return `<div class="wrap" style="max-width:720px"><div class="card success"><div class="big">🎉</div><h1>You’re in. ${esc(s.name)} is yours.</h1><p class="small">${plan==='once'?'One-time purchase':'Subscribed · '+plan} · receipt sent by Stripe · manage it under Settings → Subscriptions</p>
    <button class="pill pri lg" id="get" style="max-width:360px;margin:16px auto 0">Download SKILL.md</button>
    <div style="text-align:left;margin-top:26px"><h3 style="font-size:15px;margin-bottom:8px">Install it</h3>${installBlock(s)}</div>
    <div style="margin-top:22px"><a href="#/skill/${s.id}">Back to the skill</a> · <a href="#/">Browse more</a></div></div></div>`;
}

// ---------- MCP detail
function mcpDetail(id){
  const m=mcp(id); if(!m) return library();
  const by = m.creator ? `${avatar(m.creator,24)} <b>${esc(creator(m.creator).name)}</b> @${m.creator} ${badge(creator(m.creator))}` : `<span class="small">by <b style="color:var(--ink)">${esc(m.creator_name)}</b>${m.id==='fiscal-ai'?' · <a href="https://docs.fiscal.ai/docs/guides/mcp-integration" target="_blank" rel="noopener">docs ↗</a>':''}</span>`;
  const local = !/^https?:/.test(m.url);
  const snippets = local ? {
    claude: `<ol class="steps"><li>This MCP runs on your computer. Install it: <code>${esc(m.url.split('  ')[0])}</code>.</li><li>Set the credentials it needs (${esc(m.auth.split(';')[0])}).</li><li>Add it to Claude Desktop under <b>Settings → Developer → Edit config</b> as a stdio server, or run it with HTTP transport and add the local URL as a custom connector.</li></ol>`,
    code: `<div class="code"><button class="cp" data-copy="claude mcp add ${m.id} -- ${m.url.split('  ')[0]}">Copy</button>claude mcp add ${m.id} -- ${esc(m.url.split('  ')[0])}</div>`,
    cursor: `<div class="code"><button class="cp" data-copy='{"mcpServers":{"${m.id}":{"command":"${m.url.split(' ')[0]}","args":${JSON.stringify(m.url.split('  ')[0].split(' ').slice(1))}}}}'>Copy</button>{\n  "mcpServers": {\n    "${m.id}": { "command": "${m.url.split(' ')[0]}", "args": ${JSON.stringify(m.url.split('  ')[0].split(' ').slice(1))} }\n  }\n}</div>`,
    chatgpt: `<p class="small">ChatGPT only connects to remote MCPs. Run this server with its HTTP transport behind a tunnel, or use it from Claude or Cursor.</p>`,
    grok: `<p class="small">Grok only connects to MCPs reachable on the public internet. Run this server with its HTTP transport behind a tunnel (xAI documents the tunnel setup), or use it from Claude or Cursor.</p>`
  } : {
    claude: `<ol class="steps"><li>In Claude: <b>Settings → Connectors → Add custom connector</b>.</li><li>Paste <code>${m.url}</code> and click Add.</li><li>Sign in${m.creator?' with your Blossom account':''} when the browser opens. Done — every skill that needs ${esc(m.name)} now works.</li></ol>`,
    code: `<div class="code"><button class="cp" data-copy="claude mcp add --transport http ${m.id} ${m.url}">Copy</button>claude mcp add --transport http ${m.id} ${m.url}</div>`,
    cursor: `<div class="code"><button class="cp" data-copy='{"mcpServers":{"${m.id}":{"url":"${m.url}"}}}'>Copy</button>{\n  "mcpServers": {\n    "${m.id}": { "url": "${m.url}" }\n  }\n}</div><p class="small" style="margin:10px 0 0">Cursor Settings → MCP → Add. OAuth opens on first use.</p>`,
    chatgpt: `<ol class="steps"><li>ChatGPT → Settings → Connectors → <b>Developer mode</b> → Create.</li><li>URL <code>${m.url}</code>, auth OAuth.</li><li>Enable it in a chat under Tools.</li></ol>`,
    grok: `<ol class="steps"><li>Go to <b>grok.com/connectors → New Connector → Custom</b>.</li><li>Paste <code>${m.url}</code> and complete the sign-in it asks for.</li><li>Turn the connector on in a chat. On Grok Business or Enterprise an admin provisions it first in the cloud console.</li></ol>`
  };
  const using = allSkills().filter(s=>(s.requires||[]).includes(m.id));
  return `<div class="wrap"><div class="small" style="margin-bottom:12px"><a href="#/mcps">MCPs</a> › ${esc(m.name)}</div>
  <div class="detail"><div>
    <div class="card"><div class="dhead"><div class="em mcp">${mIcon(m,true)}</div><div style="flex:1;min-width:0"><h1>${esc(m.name)} ${m.status?`<span class="badge ${m.status==='Broker'?'broker':m.status==='Partner'?'partner':'beta'}">${m.status}</span>`:''}${m.trades?' <span class="badge warn">⚠️ can place orders</span>':''}</h1><div class="pitch">${esc(m.pitch)}</div><div class="by">${by}</div>
      <div class="stats"><div><b>${fmtN(m.installs)}</b>connected</div><div><b>${stars(m.rating)} ${m.rating.toFixed(1)}</b>${m.ratings} ratings</div><div><b>${m.tools.length}</b>tools</div><div><b>${m.version==='—'?ago(m.updated):'v'+m.version}</b>${m.version==='—'?'last update':'updated '+ago(m.updated)}</div></div></div></div>
      <div class="dbody">
        <div class="blk"><h3>${IC.wrench}Tools</h3><table class="tools">${m.tools.map(([t,d])=>`<tr><td>${esc(t)}</td><td>${esc(d)}</td></tr>`).join('')}</table></div>
        <div class="blk"><h3>${IC.lock}About</h3><p style="margin:0">${esc(m.about)}</p>${m.id==='blossom-connector'?brokerStrip('<b style="color:var(--ink)">One connector, every brokerage.</b> Blossom already normalises 20+ brokerages through its linking partner, so a skill written against these tools works for any of them — and a Robinhood or Public user doesn\'t need that broker\'s own MCP.'):''}<p class="small" style="margin:8px 0 0">Sign-in: ${esc(m.auth)}</p>${m.trades?`<div class="review-ok" style="margin-top:12px"><span>⚠️</span><div><b>This MCP can place real orders.</b> Skills that use its trading tools carry a “⚠️ can place orders” badge; every other skill only reads positions, quotes and options data from it. Use a scoped key where the broker offers one.</div></div>`:''}</div>
        <div class="blk"><h3>${IC.gear}Connect it</h3><div class="itabs">${Object.entries({claude:'Claude',code:'Claude Code',cursor:'Cursor',chatgpt:'ChatGPT',grok:'Grok'}).map(([k,v])=>`<button class="${state.itab===k?'on':''}" data-mtab="${k}">${v}</button>`).join('')}</div><div id="mbody">${snippets[state.itab]}</div></div>
        <div class="blk"><h3>${IC.puzzle}Skills that use it (${using.length})</h3><div class="grid g2">${using.slice(0,6).map(skillCard).join('')}</div></div>
        <div class="blk"><h3>${IC.refresh}Updates</h3><div class="tl">${m.log.map(([v,d,n],i)=>`<div class="tli"><span class="v">${v==='—'?'':'v'+v}</span><span class="d">${new Date(d).toLocaleDateString('en-CA',{month:'short',day:'numeric',year:'numeric'})}</span>${i===0?'<span class="tag">Latest</span>':''}<p>${esc(n)}</p></div>`).join('')}</div></div>
      </div></div>
  </div>
  <div class="side"><div class="card buy"><div class="amt" style="font-size:22px">${esc(m.price.split('·')[0].trim())}</div><div class="sub">${esc(m.price.split('·').slice(1).join('·').trim()||(m.creator?'Read-only access to your own data':'Billed by Fiscal.ai'))}</div>
    <button class="pill pri lg" id="connect">${m.creator?'Connect to Claude':(m.id==='fiscal-ai'?'Open on fiscal.ai':'Copy install command')}</button>
    <ul class="incl"><li>OAuth — no keys to paste</li><li>Revoke any time</li><li>${m.creator?'Never places trades, never sees your broker login':'Partner MCP · support via Fiscal.ai'}</li></ul></div></div></div></div>`;
}
function bindMcp(id){
  const m=mcp(id);
  document.querySelectorAll('[data-mtab]').forEach(b=>b.onclick=()=>{ state.itab=b.dataset.mtab; route(); });
  bindCopy();
  $('#connect').onclick=()=>{ if(m.id==='fiscal-ai'){ window.open('https://docs.fiscal.ai/docs/guides/mcp-integration','_blank'); return; } if(!m.creator){ copy(m.url.split('  ')[0], 'Install command copied'); return; } copy(m.url, 'Connector URL copied — paste it in Claude → Settings → Connectors'); };
  document.querySelectorAll('[data-go]').forEach(el=>el.addEventListener('click',e=>{ if(e.target.closest('a,button')) return; location.hash=el.dataset.go; }));
}

// ---------- creator page
function creatorPage(h){
  const c=creator(h); if(!c) return library();
  const mine_=allSkills().filter(s=>s.creator===h);
  const dl=mine_.reduce((a,s)=>a+s.downloads,0);
  return `<div class="wrap"><div class="card chead">${avatar(h,76)}<div style="flex:1"><h1>${esc(c.name)} ${badge(c)}</h1><div class="h">@${h}</div><p>${esc(c.bio)}</p><div class="nums"><span><b>${fmtN(c.followers)}</b> followers</span><span><b>${mine_.length}</b> skills</span><span><b>${fmtN(dl)}</b> downloads</span><span><b>${(mine_.reduce((a,s)=>a+s.rating,0)/Math.max(1,mine_.length)).toFixed(1)} ★</b> avg rating</span></div></div><button class="pill teal" id="follow">Follow</button></div>
  <div class="sec-h"><h2>Skills by @${h}</h2></div><div class="grid">${mine_.map(skillCard).join('')||'<div class="empty">No skills yet.</div>'}</div></div>`;
}

// ---------- post a skill (wizard)
const EMOJIS=['🧾','💸','🍁','📈','🔥','🏦','🛡️','🔎','📰','🪙','🎯','💎','🐝','🤑','📉','🧠','⚡','🧮','🏠','🌱'];
function pitchFrom(desc){ let t=desc.split(/(?<=\.)\s/)[0].trim(); if(t.length>160){ t=t.slice(0,160); t=t.slice(0,t.lastIndexOf(' '))+'…'; } return t; }
function newWiz(){ return {step:1, type:'skill', file:null, text:'', files:[], shots:[], optional:[], trades:false, icon:null, payMethod:'etransfer', payEmail:'', name:'', emoji:'🧾', pitch:'', cat:'Portfolio', prompts:['','',''], sample:'', requires:['blossom-connector'], model:'free', once:29, monthly:4.99, yearly:39, stripe:false, cadence:'Monthly', first:'Initial release', agree:false, tested:false, nosecret:false}; }
function parseFront(t){ const m=t.match(/^---\n([\s\S]*?)\n---/); const o={}; if(m){ m[1].split('\n').forEach(l=>{const i=l.indexOf(':'); if(i>0) o[l.slice(0,i).trim()]=l.slice(i+1).trim();}); } return o; }
function payout(price){ const take=price*TAKE; return {fee:0, take, you:price-take}; }   // Blossom covers card processing out of its 20%
function wizard(){
  const w=state.wiz; const steps=['Your skill','Listing','Pricing','Updates','Review & publish']; w.type='skill';
  const nav = `<div class="card wsteps">${steps.map((t,i)=>`<div class="${w.step===i+1?'on':w.step>i+1?'done':''}"><i>${w.step>i+1?'✓':i+1}</i>${t}</div>`).join('')}</div>`;
  let p='';
  if(w.step===1){
    const fm=parseFront(w.text); const ok=!!w.text; const checks=[[fm.name&&fm.description?`Found the name and description: <b>${esc(fm.name)}</b> — ${esc(fm.description.split('.')[0].slice(0,90))}…`:'No name or description yet — add them on the next step, or tell your AI to put a <code>name</code> and <code>description</code> at the top of the file', !!(fm.name&&fm.description), 'soft'],['A reasonable size (under 20 KB)', ok&&w.text.length<20000],['No API keys or secrets inside', ok&&!/sk_live|sk_test|api[_-]?key\s*[:=]\s*\S{12,}|ghp_[A-Za-z0-9]{20,}/i.test(w.text)]];
    p=`<h2>Your skill</h2><p class="lead">A skill is a SKILL.md your AI reads — instructions, what it needs, what to output. Runs in Claude, ChatGPT, Grok and Cursor.</p>
      ${true?`<div class="f"><label>Your SKILL.md</label><div class="drop ${ok?'ok':''}" id="drop">${ok?`<b>✓ ${esc(fm.name||'SKILL.md')} loaded</b><span>${(w.text.length/1024).toFixed(1)} KB · click to replace</span>`:`<b>Drop your SKILL.md here, or click to choose</b><span>We read the name and description from the block between the --- lines at the top.</span>`}<input type="file" id="file" accept=".md,.txt" style="display:none"></div><div class="hint">Don’t have one? <a href="#" id="tpl">Start from the Blossom template</a> — a checklist skill wired to the Connector MCP.</div></div>
      <div class="f"><label>Or paste it</label><textarea id="text" placeholder="---&#10;name: my-skill&#10;description: What it does and when your AI should use it&#10;---&#10;# My skill&#10;…">${esc(w.text)}</textarea></div>
      <div class="f"><label>Supporting files <span class="small" style="font-weight:600">(optional)</span></label><div class="drop" id="fdrop" style="padding:16px"><b>${w.files.length?`✓ ${w.files.length} file${w.files.length>1?'s':''}: ${w.files.join(', ')}`:'Add reference files, scripts or templates'}</b><span>Anything your SKILL.md refers to — a sectors map, an ETF look-through CSV, a Python helper. Shipped alongside it as a folder.</span><input type="file" id="ffile" multiple style="display:none"></div></div>
      <div class="f"><label>Checks</label><div class="checks">${checks.map(([t,v,soft])=>`<div class="check ${ok?(v?'ok':(soft?'':'bad')):''}"><span class="st ${ok?(v?'ok':(soft?'soft':'bad')):''}">${ok?(v?IC.check:(soft?IC.chat:IC.x)):IC.circle}</span><span>${t}</span></div>`).join('')}</div></div>`
      :``}`;
  } else if(w.step===2){
    const cats=['Portfolio','Earnings','Dividends','Screens','Social','Research','Canada','Crypto','News'];
    p=`<h2>How it shows up</h2><p class="lead">This is what people see in the library. Lead with the outcome, not the mechanism.</p>
      <div class="f"><label>Icon</label><div class="emojis">${EMOJIS.map(e=>`<button class="${!w.icon&&w.emoji===e?'on':''}" data-emoji="${e}">${e}</button>`).join('')}<button class="up ${w.icon?'on':''}" id="iconup" title="Upload your own (square PNG or JPG)">${w.icon?`<img src="${w.icon}" alt="">`:'⬆ Your<br>own'}</button><input type="file" id="iconfile" accept="image/*" style="display:none"></div><div class="hint">Pick an emoji or upload a square image — it’s shown at 56px on the card, so keep it simple.</div></div>
      <div class="row2"><div class="f"><label>Name</label><input type="text" id="name" value="${esc(w.name)}" placeholder="Earnings Season Checklist" maxlength="48"><div class="hint">Up to 48 characters.</div></div><div class="f"><label>Category</label><select id="cat">${cats.map(c=>`<option ${w.cat===c?'selected':''}>${c}</option>`).join('')}</select></div></div>
      <div class="f"><label>One-line pitch</label><textarea id="pitch" rows="2" style="min-height:0;resize:none" placeholder="Every holding reporting in the next 14 days, what the Street expects, and what investors who hold it did last quarter." maxlength="160">${esc(w.pitch)}</textarea><div class="hint">${160-w.pitch.length} characters left. Say what the user gets, in their words.</div></div>
      <div class="f"><label>Three prompts that trigger it</label>${[0,1,2].map(i=>`<input type="text" data-prompt="${i}" value="${esc(w.prompts[i])}" placeholder="${['Run my earnings checklist','Which of my holdings report this week?','What did investors do with NVDA after earnings?'][i]}" style="margin-bottom:8px">`).join('')}</div>
      <div class="f"><label>Sample output</label><textarea id="sample" placeholder="Paste a real run. Markdown is fine — tables, bold, code.">${esc(w.sample)}</textarea></div>
      <div class="f"><label>Screenshots <span class="small" style="font-weight:600">(up to 4 — the most persuasive thing on your listing)</span></label><div class="drop" id="sdrop" style="padding:16px"><b>${w.shots.length?`✓ ${w.shots.join(', ')}`:'Add screenshots of a real run'}</b><span>Charts, tables, the widget your skill builds. The first one shows on your card in the library; all of them show under “What you get”. PNG or JPG.</span><input type="file" id="sfile" accept="image/*" multiple style="display:none"></div></div>
      <div class="f"><label>MCPs it uses</label><div class="checks">${D.mcps.map(m=>{const st=w.requires.includes(m.id)?'req':w.optional.includes(m.id)?'opt':'';return `<div class="check ${st==='req'?'ok':''}" style="gap:12px"><span class="mt">${mIcon(m,true)}</span><span style="flex:1;min-width:0"><b style="color:var(--ink)">${esc(m.name)}</b> <span class="small">· ${m.creator?'Blossom':(m.status==='Broker'?('brokerage · '+esc(m.country||'')):'partner')}</span></span><select class="msel" data-mcp="${m.id}"><option value="" ${st===''?'selected':''}>Not used</option><option value="req" ${st==='req'?'selected':''}>Required</option><option value="opt" ${st==='opt'?'selected':''}>Optional</option></select></div>`}).join('')}</div><div class="hint">Detected from your SKILL.md — fix it if we got it wrong. Required MCPs show on the card; optional ones show under “Optional MCPs” on the listing. Through the Blossom Connector a skill already works with any brokerage you’ve linked, so pick a broker’s own MCP only if the skill calls it directly (to trade, or for data Blossom doesn’t have).</div></div>
      <div class="f"><label class="tog"><input type="checkbox" id="trades" ${w.trades?'checked':''}> This skill can place orders</label><div class="hint">Turn it on if the skill calls a broker MCP’s trading tools. Buyers see a “can place orders” badge on the card and the listing. Detected from your SKILL.md — change it if we got it wrong.</div></div>`;
  } else if(w.step===3){
    const price = w.model==='once'?w.once:w.model==='monthly'?w.monthly:w.model==='yearly'?w.yearly:0;
    const po=payout(price);
    const subs=w.model==='monthly'||w.model==='yearly';
    p=`<h2>Set your price</h2><p class="lead">Free gets you reach. Subscriptions pay you to keep it current — people pay for the updates, not the file.</p>
      <div class="pcards">${[['free','Free','Reach and followers. Updates when you feel like it.'],['once','One-time','Pay once. Buyers get updates for 12 months.'],['monthly','Monthly','Recurring. Cancel anytime. Promise an update cadence.'],['yearly','Yearly','Recurring, billed once a year. Cancel anytime.']].map(([k,t,d])=>`<div class="pcard ${w.model===k?'on':''}" data-model="${k}"><b>${t}</b><span>${d}</span></div>`).join('')}</div>
      ${w.model==='free'?'':`<div class="row2" style="margin-top:18px"><div class="f"><label>${w.model==='once'?'Price':w.model==='monthly'?'Price per month':'Price per year'} (CAD)</label><input type="number" id="price" min="1" max="499" step="0.01" value="${price}"><div class="sug">${(w.model==='once'?[9,19,29,49]:w.model==='monthly'?[2.99,4.99,9.99,19.99]:[19,39,79,149]).map(v=>`<button data-sug="${v}">${money(v)}</button>`).join('')}</div></div>
        <div class="f"><label>What you keep per sale</label><div class="payout"><div><span>Price</span><span>${money(price)}</span></div><div><span>Blossom (20%)</span><span>−${money(+po.take.toFixed(2))}</span></div><div class="tot"><span>You keep</span><span>${money(+po.you.toFixed(2))}${subs?(w.model==='monthly'?' / mo':' / yr'):''}</span></div></div><div class="hint">Blossom’s 20% covers card processing, refunds and payouts.</div></div></div>
        ${w.model==='monthly'?`<div class="f"><label class="tog"><input type="checkbox" id="addyear" ${w.addyear?'checked':''}> Also offer yearly at ${money(+(w.monthly*10).toFixed(2))} (2 months free)</label></div>`:''}
        ${subs?`<div class="hint" style="margin:-6px 0 14px">No free trials on Blossom Skills — the first charge happens at checkout. Win people over with the sample output and the update log instead.</div>`:''}
        <div class="f"><label>Getting paid</label><div class="reqrow" style="margin:0 0 10px"><div class="em" style="background:var(--lav2)">${IC.lock}</div><div><b>Blossom handles the payment and pays you out</b><span>Buyers pay Blossom by card. You get 80% of every sale, paid monthly on the 1st by Interac e-Transfer or PayPal. No Stripe account, no tax forms to chase.</span></div></div>
        <div class="row2"><div class="f" style="margin:0"><label>Pay me by</label><div class="pcards" style="grid-template-columns:1fr 1fr"><div class="pcard ${w.payMethod==='etransfer'?'on':''}" data-pay="etransfer"><b>Interac e-Transfer</b><span>Canada · to your email</span></div><div class="pcard ${w.payMethod==='paypal'?'on':''}" data-pay="paypal"><b>PayPal</b><span>Anywhere · to your PayPal email</span></div></div></div>
        <div class="f" style="margin:0"><label>${w.payMethod==='etransfer'?'e-Transfer email':'PayPal email'}</label><input type="text" id="payemail" value="${esc(w.payEmail)}" placeholder="you@example.com" inputmode="email" autocomplete="email"><div class="hint">${w.payMethod==='etransfer'?'Must be registered for Interac e-Transfer with your bank. Set up autodeposit so you don’t need a security question.':'The email on your PayPal account. PayPal’s own fees apply on receipt.'} You can change this later under Manage → Payouts.</div></div></div>`}`;
  } else if(w.step===4){
    p=`<h2>Keep it current</h2><p class="lead">Your update cadence is shown on the listing, and ${w.model==='monthly'||w.model==='yearly'?'it’s what subscribers are paying for. ':''}Every update goes in the log and DMs everyone who has it.</p>
      <div class="f"><label>How often will you update it?</label><select id="cadence">${['Weekly','Monthly','Quarterly','When something changes'].map(c=>`<option ${w.cadence===c?'selected':''}>${c}</option>`).join('')}</select><div class="hint">Miss two in a row and the listing shows “update overdue”. Be honest here.</div></div>
      <div class="f"><label>First entry in the update log</label><div class="row2"><input type="text" value="v1.0.0" disabled><input type="text" id="first" value="${esc(w.first)}"></div></div>
      <div class="f"><label>Preview</label><div class="preview"><div class="promise" style="margin-bottom:10px"><span class="em">🔁</span><div><b style="color:var(--ink)">Updated ${esc(w.cadence.toLowerCase())}.</b> <span class="small">Subscribers get every update automatically and a DM when one ships.</span></div></div><div class="tl"><div class="tli"><span class="v">v1.0.0</span><span class="d">Nov 7, 2026</span><span class="tag">Latest</span><p>${esc(w.first)}</p></div></div></div></div>`;
  } else {
    const fake = {id:'preview', version:'1.0.0', updated:'2026-11-08', emoji:w.emoji, icon:w.icon, name:w.name||'Untitled skill', creator:ME, cat:w.cat, pitch:w.pitch||'Your one-line pitch shows here.', downloads:0, rating:0, ratings:0, optional:w.optional, trades:w.trades, price: w.model==='free'?{free:true}:w.model==='once'?{once:+w.once}:w.model==='monthly'?{monthly:+w.monthly, yearly:w.addyear?+(w.monthly*10).toFixed(2):undefined}:{yearly:+w.yearly}, requires:w.requires};
    p=`<h2>Review & publish</h2><p class="lead">This is the card people will see. Publish puts it in review; most listings are live within a day.</p>
      <div class="f"><label>Preview</label><div class="preview"><div class="grid" style="grid-template-columns:1fr"><div style="max-width:520px">${skillCard(fake).replace('data-go','data-x')}</div></div>${w.files.length||w.shots.length?`<div class="small" style="margin-top:8px">Ships with ${w.files.length} supporting file${w.files.length===1?'':'s'}${w.shots.length?` · ${w.shots.length} screenshot${w.shots.length===1?'':'s'}`:''}.</div>`:''}</div></div>
      <div class="f"><label>Before you publish</label><div class="checks">
        <label class="check ${w.tested?'ok':''}"><input type="checkbox" id="tested" ${w.tested?'checked':''}> I ran it in Claude or ChatGPT this week and the sample output is real</label>
        <label class="check ${w.nosecret?'ok':''}"><input type="checkbox" id="nosecret" ${w.nosecret?'checked':''}> No API keys, account numbers or personal data in the file</label>
        <label class="check ${w.agree?'ok':''}"><input type="checkbox" id="agree" ${w.agree?'checked':''}> I own this content and agree to the <a href="#/terms" target="_blank">Creator terms</a> (20% platform fee${w.model!=='free'?', paid out monthly by Blossom':''})</label>
      </div></div>
      <div class="review-ok"><span>🕵️</span><div><b>Review:</b> we run every new skill once against a test portfolio, check it does what the listing says (a skill that places orders must say so), and look for anything that would get a creator in trouble. You’ll get a DM when it’s live.</div></div>`;
  }
  const canNext = w.step===1 ? (w.type==='mcp' || !!w.text) : w.step===2 ? (w.name && w.pitch) : w.step===3 ? (w.model==='free' || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(w.payEmail)) : true;
  const last = w.step===5;
  return `<div class="wrap"><div class="small" style="margin-bottom:12px"><a href="#/">Skills</a> › Post a skill</div><div class="wiz">${nav}<div class="card wpanel">${p}
    <div class="wnav"><button class="pill sec" id="back" ${w.step===1?'style="visibility:hidden"':''}>← Back</button><div class="small">Step ${w.step} of 5</div><button class="pill ${canNext?'pri':'dis'}" id="next" ${canNext?'':'disabled'}>${last?'Publish':'Continue →'}</button></div></div></div></div>`;
}
const TEMPLATE = `---\nname: my-checklist\ndescription: A short checklist run against the user's Blossom portfolio. Use when the user asks to "run my checklist".\n---\n\n# My checklist\n\n## Needs\n- Blossom Connector MCP: get_portfolio\n\n## Steps\n1. Call get_portfolio. Keep holdings with weight >= 1%.\n2. For each holding, check: (your rule here).\n3. Output a table: Ticker | Weight | Check | Note.\n\n## Rules\n- Only describe what the user holds. No buy/sell recommendations.\n`;
function bindWizard(){
  const w=state.wiz; const re=()=>{ $('#app').innerHTML=wizard(); bindWizard(); };
  document.querySelectorAll('[data-type]').forEach(b=>b.onclick=()=>{ w.type=b.dataset.type; re(); });
  const drop=$('#drop'), file=$('#file'); if(drop){ drop.onclick=()=>file.click(); file.onchange=()=>{ const f=file.files[0]; if(!f) return; f.text().then(t=>{ w.text=t; const fm=parseFront(t); if(fm.name&&!w.name) w.name=fm.name.replace(/[-_]/g,' ').replace(/\b\w/g,c=>c.toUpperCase()); if(fm.description&&!w.pitch) w.pitch=pitchFrom(fm.description); w.trades=/place[_ ]order|submit[_ ]order|execute[_ ]trade/i.test(t); w.requires=[...new Set([...(/connector|get_portfolio|get_holdings/i.test(t)?['blossom-connector']:[]),...(/trade.?data|crowd_flows|anomalies|ticker_history/i.test(t)?['blossom-trade-data']:[]),...(/fiscal/i.test(t)?['fiscal-ai']:[])])]; re(); }); };
    drop.ondragover=e=>{e.preventDefault(); drop.classList.add('ok');}; drop.ondrop=e=>{ e.preventDefault(); const f=e.dataTransfer.files[0]; if(f) f.text().then(t=>{ w.text=t; re(); }); }; }
  const tpl=$('#tpl'); if(tpl) tpl.onclick=e=>{ e.preventDefault(); w.text=TEMPLATE; w.name=w.name||'My Checklist'; re(); };
  const text=$('#text'); if(text) text.onchange=()=>{ w.text=text.value; re(); };
  document.querySelectorAll('[data-emoji]').forEach(b=>b.onclick=()=>{ w.emoji=b.dataset.emoji; w.icon=null; re(); });
  const iu=$('#iconup'), ifl=$('#iconfile'); if(iu){ iu.onclick=()=>ifl.click(); ifl.onchange=()=>{ const f=ifl.files[0]; if(!f) return; const img=new Image(); img.onload=()=>{ const c=document.createElement('canvas'); c.width=c.height=128; const x=c.getContext('2d'); const m=Math.min(img.width,img.height); x.drawImage(img,(img.width-m)/2,(img.height-m)/2,m,m,0,0,128,128); w.icon=c.toDataURL('image/png'); re(); }; img.src=URL.createObjectURL(f); }; }
  const bindVal=(id,key,cb)=>{ const el=$(id); if(el) el.oninput=()=>{ w[key]=el.type==='number'?+el.value:el.value; if(cb) cb(); }; };
  bindVal('#name','name'); bindVal('#cat','cat'); bindVal('#sample','sample'); bindVal('#first','first'); bindVal('#cadence','cadence');
  const pitch=$('#pitch'); if(pitch) pitch.oninput=()=>{ w.pitch=pitch.value.replace(/\n/g,' '); pitch.nextElementSibling.textContent=(160-w.pitch.length)+' characters left. Say what the user gets, in their words.'; };
  document.querySelectorAll('[data-prompt]').forEach(i=>i.oninput=()=>{ w.prompts[+i.dataset.prompt]=i.value; });
  document.querySelectorAll('[data-mcp]').forEach(sel=>sel.onchange=()=>{ const id=sel.dataset.mcp; w.requires=w.requires.filter(x=>x!==id); w.optional=w.optional.filter(x=>x!==id); if(sel.value==='req') w.requires.push(id); if(sel.value==='opt') w.optional.push(id); re(); });
  const fd=$('#fdrop'), ff=$('#ffile'); if(fd){ fd.onclick=()=>ff.click(); ff.onchange=()=>{ w.files=[...ff.files].map(f=>f.name).slice(0,20); re(); }; }
  const sd=$('#sdrop'), sf=$('#sfile'); if(sd){ sd.onclick=()=>sf.click(); sf.onchange=()=>{ w.shots=[...sf.files].map(f=>f.name).slice(0,4); re(); }; }
  document.querySelectorAll('[data-model]').forEach(b=>b.onclick=()=>{ w.model=b.dataset.model; re(); });
  const price=$('#price'); if(price) price.onchange=()=>{ const v=Math.max(1,+price.value||1); w[w.model]=v; re(); };
  document.querySelectorAll('[data-sug]').forEach(b=>b.onclick=()=>{ w[w.model]=+b.dataset.sug; re(); });
  const ay=$('#addyear'); if(ay) ay.onchange=()=>{ w.addyear=ay.checked; re(); };
  document.querySelectorAll('[data-pay]').forEach(b=>b.onclick=()=>{ w.payMethod=b.dataset.pay; re(); });
  const pe=$('#payemail'); if(pe) pe.oninput=()=>{ const was=/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(w.payEmail); w.payEmail=pe.value.trim(); const now=/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(w.payEmail); if(was!==now){ const n=$('#next'); n.className='pill '+(now||w.model==='free'?'pri':'dis'); n.disabled=!(now||w.model==='free'); } };
  const tdx=$('#trades'); if(tdx) tdx.onchange=()=>{ w.trades=tdx.checked; re(); };
  ['tested','nosecret','agree'].forEach(k=>{ const el=$('#'+k); if(el) el.onchange=()=>{ w[k]=el.checked; re(); }; });
  $('#back').onclick=()=>{ w.step=Math.max(1,w.step-1); re(); };
  $('#next').onclick=()=>{ if(w.step<5){ if(w.step===1 && w.type==='skill'){ const fm=parseFront(w.text); if(!w.name && fm.name) w.name=fm.name.replace(/[-_]/g,' ').replace(/\b\w/g,c=>c.toUpperCase()); if(!w.pitch && fm.description) w.pitch=pitchFrom(fm.description); } w.step++; re(); return; }
    if(!(w.tested&&w.nosecret&&w.agree)){ toast('Tick the three checks first'); return; }
    const id=(w.name||'skill').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')+'-'+Math.random().toString(36).slice(2,6);
    const s={id, emoji:w.emoji, icon:w.icon, payout:{method:w.payMethod, email:w.payEmail}, name:w.name, creator:ME, cat:w.cat, pitch:w.pitch, downloads:0, rating:0, ratings:0, updated:'2026-11-07', version:'1.0.0', requires:w.requires, optional:w.optional, trades:w.trades, files:w.files, shots:w.shots, price: w.model==='free'?{free:true}:w.model==='once'?{once:+w.once}:w.model==='monthly'?{monthly:+w.monthly, yearly:w.addyear?+(w.monthly*10).toFixed(2):undefined}:{yearly:+w.yearly}, cadence:w.cadence, prompts:w.prompts.filter(Boolean).length?w.prompts.filter(Boolean):['Run '+w.name], sample:w.sample||'_Sample output will appear here once you add one._', log:[['1.0.0','2026-11-07',w.first]], reviews:[], skill:w.text||TEMPLATE, status:'In review', mine:true};
    const m=mine(); m.unshift(s); LS.set('mine',m); state.wiz=null; location.hash='#/manage/'+id; };
}

// ---------- creator terms (draft)
function terms(){
  const S=(h,b)=>`<h3 style="margin:22px 0 6px;font-size:16px">${h}</h3><p style="margin:0;font-size:14.5px;line-height:1.6">${b}</p>`;
  return `<div class="wrap" style="max-width:820px"><div class="small" style="margin-bottom:12px"><a href="#/">Skills</a> › Creator terms</div>
  <div class="card" style="padding:28px 32px"><h1 style="font-size:26px;margin:0 0 4px">Blossom Skills — Creator Terms</h1><div class="small">Draft v0.1 · November 2026 · for review by Blossom before launch. Plain-language summary first, the terms follow.</div>
  <div class="review-ok" style="margin:16px 0 4px"><span>🌼</span><div><b>In short:</b> you own your skill, Blossom gets a licence to host and sell it, you keep 80% of what it earns, you keep it updated if people subscribe, you never put secrets or personal data in it, and nothing on Blossom Skills is investment advice.</div></div>
  ${S('1. Who can publish','Anyone with a Blossom account in good standing. You must be 18 or older and legally able to receive payments where you live. Blossom may ask you to verify your identity before the first payout.')}
  ${S('2. What you’re publishing','A skill is a text file (SKILL.md) plus optional supporting files and screenshots. You confirm that you wrote it or have the right to publish it, that it does what the listing says, that the sample output comes from a real run, and that it contains no API keys, passwords, account numbers or personal data — yours or anyone else’s.')}
  ${S('3. Ownership and licence','You keep ownership of your skill. You grant Blossom a worldwide, non-exclusive licence to host, display, distribute and sell it on Blossom Skills, to show excerpts and screenshots in marketing for the marketplace, and to keep delivering it to people who already bought or subscribed, for as long as their purchase or subscription lasts, even after you unlist it.')}
  ${S('4. Pricing and fees','You set the price: free, one-time, monthly or yearly. Blossom keeps 20% of each sale and covers payment processing out of that share; you receive 80% of what the buyer pays. The split applies to the amount the buyer pays after any Blossom-funded promotion. There are no free trials on Blossom Skills; the first charge happens at checkout. Price changes apply to new buyers only.')}
  ${S('5. Payouts','Blossom collects every payment and pays you your share. Payouts run monthly, on the 1st, for sales that cleared at least 14 days earlier, by Interac e-Transfer (Canada) or PayPal to the email you give us when you publish, in CAD or USD. PayPal’s receiving fees are yours. Blossom issues the tax statements your country requires at year end; you are responsible for your own taxes. Blossom may hold or reverse a payout to cover refunds, chargebacks or fraud.')}
  ${S('6. Subscriptions and updates','A subscription is a promise to keep the skill current. If you set a cadence, keep it; miss two updates in a row and the listing shows “update overdue”, and after 90 days without an update Blossom may pause new subscriptions. Existing subscribers keep access. You can change the cadence at any time; tell subscribers in the update log.')}
  ${S('7. Refunds','Buyers can request a refund within 14 days of a one-time purchase, or of the first charge of a subscription, if the skill does not do what the listing says. Blossom decides refunds and may deduct them from your next payout. Subscriptions can be cancelled anytime and end at the period’s end.')}
  ${S('8. What you can’t publish','Anything that places orders without clearly declaring it (use the “can place orders” setting); anything that gives personalised investment advice or presents itself as a licensed adviser; pump-and-dump, front-running or market-manipulation content; copies of other creators’ skills; skills that scrape or store other users’ data; anything illegal where you or your buyers are. Skills that call a broker MCP’s trading tools must say so and must leave the final decision with the user.')}
  ${S('9. Review and removal','Blossom reviews every new skill and update before it goes live and may reject or remove a listing at any time, with a reason where it can give one. Blossom may also remove a skill on a valid rights complaint. Removal does not affect payouts already earned, unless the removal is for fraud.')}
  ${S('10. Not investment advice','Blossom Skills is a marketplace for software. Nothing published on it is investment, tax or legal advice from Blossom or from the creator, and Blossom does not check that any skill’s output is accurate. Buyers use skills at their own risk; creators must include that disclosure in their output where it’s reasonable to do so.')}
  ${S('11. Liability','To the extent the law allows, neither Blossom nor the creator is liable for trading losses or any indirect loss from using a skill. Blossom’s total liability to a creator is limited to the fees it has kept from that creator’s sales in the previous 12 months.')}
  ${S('12. Ending this','You can unlist a skill at any time; current buyers and subscribers keep it. Blossom can close a creator account for breaking these terms or Blossom’s Community Guidelines. Either side can end the relationship on 30 days’ notice; sections 3 (for existing buyers), 5, 10 and 11 survive.')}
  ${S('13. Changes','Blossom may update these terms with 30 days’ notice by email and in the creator dashboard. Publishing or updating a skill after that date means you accept the new terms.')}
  <p class="small" style="margin-top:22px">Questions: <a href="mailto:creators@blossomsocial.com">creators@blossomsocial.com</a>. These terms sit alongside Blossom’s Terms of Service and Community Guidelines.</p>
  </div></div>`;
}

// ---------- manage (creator view)
function manage(id){
  const s=skill(id); if(!s) return library();
  const subs = s.mine? 0 : Math.round(s.downloads*(s.price.free?0:0.18));
  const mrr = s.price.free?0: subs*(s.price.monthly||((s.price.yearly||s.price.once||0)/12));
  return `<div class="wrap"><div class="small" style="margin-bottom:12px"><a href="#/">Skills</a> › Manage › ${esc(s.name)}</div>
    <div class="card" style="padding:22px 26px;display:flex;gap:16px;align-items:center;margin-bottom:16px"><div class="em" style="width:56px;height:56px;border-radius:14px;background:var(--lav2);display:flex;align-items:center;justify-content:center;font-size:28px">${s.emoji}</div><div style="flex:1"><h1 style="font-size:22px">${esc(s.name)} ${s.status==='In review'?'<span class="badge beta">In review</span>':'<span class="badge partner">Live</span>'}</h1><div class="small">${s.status==='In review'?'Submitted today · most listings are live within 24 hours · you’ll get a DM':'Live since '+ago(s.updated)} · <a href="#/skill/${s.id}">View listing</a> · <a href="#" data-copy="${SITE}/#/skill/${s.id}">Copy link</a></div></div><a class="pill sec" href="#/skill/${s.id}">Preview</a></div>
    <div class="kpis"><div class="card kpi"><span>Downloads</span><b>${fmtN(s.downloads)}</b></div><div class="card kpi"><span>${s.price.free?'Followers from this skill':'Active subscribers'}</span><b>${s.price.free?fmtN(Math.round(s.downloads*0.12)):fmtN(subs)}</b></div><div class="card kpi"><span>Est. monthly payout</span><b>${money(+(mrr*(1-STRIPE_PCT)*(1-TAKE)).toFixed(0))}</b></div><div class="card kpi"><span>Rating</span><b>${s.ratings?s.rating.toFixed(1)+' ★':'—'}</b></div></div>
    <div class="detail"><div class="card" style="padding:22px 26px"><h3 style="font-size:16px;margin-bottom:4px">🔁 Publish an update</h3><p class="small" style="margin:0 0 14px">Bumps the version, adds to the log, DMs everyone who has it${s.price.free?'':' — this is what subscribers pay for'}.</p>
      <div class="row2"><div class="f"><label>New SKILL.md</label><div class="drop" style="padding:16px"><b>Drop the updated file</b><span>or keep the current one and just log the change</span></div></div><div class="f"><label>Version</label><input type="text" id="ver" value="${s.version.replace(/(\d+)$/,(m)=>+m+1)}"><div class="hint">Was v${s.version}</div></div></div>
      <div class="f"><label>What changed</label><textarea id="note" placeholder="Adds the ‘what investors who hold it did’ column…"></textarea></div>
      <button class="pill pri" id="pub">Publish update</button>
      <h3 style="font-size:16px;margin:26px 0 10px">Update log</h3><div class="tl">${s.log.map(([v,d,n],i)=>`<div class="tli"><span class="v">v${v}</span><span class="d">${new Date(d).toLocaleDateString('en-CA',{month:'short',day:'numeric',year:'numeric'})}</span>${i===0?'<span class="tag">Latest</span>':''}<p>${esc(n)}</p></div>`).join('')}</div></div>
    <div class="side"><div class="card buy"><b style="color:var(--ink)">Pricing</b><div class="small" style="margin:6px 0 10px">${s.price.free?'Free':[s.price.once&&money(s.price.once)+' one-time',s.price.monthly&&money(s.price.monthly)+'/mo',s.price.yearly&&money(s.price.yearly)+'/yr'].filter(Boolean).join(' · ')}</div><button class="pill sec sm" style="width:100%">Change pricing</button><div class="small" style="margin-top:10px">Price changes apply to new subscribers only. Existing ones keep their price.</div></div>
      <div class="card buy"><b style="color:var(--ink)">Payouts</b><div class="small" style="margin:6px 0 10px">Paid by Blossom · monthly, on the 1st · ${s.payout?.email?`${s.payout.method==='paypal'?'PayPal':'e-Transfer'} to ${esc(s.payout.email.replace(/^(.).+(@.+)$/,'$1…$2'))}`:'no payout details yet'}</div><button class="pill sec sm" style="width:100%">${s.payout?.email?'Change payout details':'Add payout details'}</button></div></div></div></div>`;
}
function bindManage(id){
  const s=skill(id); if(!s) return; bindCopy();
  $('#pub').onclick=()=>{ const v=$('#ver').value.trim(), n=$('#note').value.trim(); if(!n){ toast('Say what changed'); return; } const m=mine(); const i=m.findIndex(x=>x.id===id); if(i>=0){ m[i].log.unshift([v,'2026-11-07',n]); m[i].version=v; LS.set('mine',m); } else { s.log.unshift([v,'2026-11-07',n]); s.version=v; } toast('Update published · '+(s.price.free?'followers':'subscribers')+' notified'); route(); };
}

document.querySelectorAll('[data-app]').forEach(a=>a.addEventListener('click',e=>{ e.preventDefault(); toast('That’s the Blossom web app — this preview only has Skills & MCPs'); }));
route();
"""

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Best Skills and MCPs for Investors — Blossom Skills</title>
<meta property="og:title" content="The Best Skills and MCPs for Investors — Blossom Skills">
<meta property="og:description" content="Skills and MCPs built by verified investors on Blossom, for Claude, ChatGPT, Grok and Cursor. Connect your portfolio once, then run the skills — free, or subscribe to a creator.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://blossom-skills.netlify.app/">
<meta property="og:image" content="https://blossom-skills.netlify.app/og.jpg"><meta property="og:image:secure_url" content="https://blossom-skills.netlify.app/og.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:alt" content="The Best Skills and MCPs for Investors — Blossom Skills"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:site_name" content="Blossom Skills">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="The Best Skills and MCPs for Investors — Blossom Skills"><meta name="twitter:image" content="https://blossom-skills.netlify.app/og.jpg">
<link rel="canonical" href="https://blossom-skills.netlify.app/">
<meta name="description" content="Skills and MCPs built by verified investors on Blossom, for Claude, ChatGPT, Grok and Cursor. Connect your portfolio once, then run the skills — free, or subscribe to a creator.">
<link rel="icon" href="/favicon.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS.replace('__WALL__', wall_b64)}</style></head>
<body>
<div class="appbar"><a class="logo" href="#/"><img src="data:image/png;base64,{logo_b64}" alt="Blossom"></a><span class="sp"></span>
<a class="pill sec" href="https://www.blossomsocial.com/" target="_blank" rel="noopener" style="background:var(--bg);display:inline-flex;align-items:center;gap:8px"><svg viewBox="0 0 16 16" style="width:15px;height:15px;fill:currentColor"><rect x="2" y="2" width="5" height="5" rx="1.2"/><rect x="9" y="2" width="5" height="5" rx="1.2"/><rect x="2" y="9" width="5" height="5" rx="1.2"/><rect x="9" y="9" width="5" height="5" rx="1.2"/></svg>Get App</a>
<a class="pill pri" href="https://www.blossomsocial.com/" target="_blank" rel="noopener" style="margin-left:12px">Sign up</a></div>
<div class="shell">{SIDEBAR}
<div class="main"><div id="app"></div>
<footer>Blossom Skills · V1 preview · <a href="#/post">Post a skill</a> · <a href="#/mcps">MCPs</a> · <a href="https://www.blossomsocial.com/" target="_blank" rel="noopener">blossomsocial.com</a></footer></div></div>
<script>{JS.replace('__DATA__', DATA).replace('__BROKERS__', BROKERS_JS).replace('__BEEVIS__', beevis_b64).replace('__FLOWER__', flower_b64).replace('__BADGE__', badge_b64)}</script>
</body></html>"""

open(os.path.join(OUT, 'index.html'), 'w').write(HTML)
print('index.html', round(len(HTML)/1024), 'KB;', len(SKILLS), 'skills,', len(MCPS), 'mcps')
