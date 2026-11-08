#!/usr/bin/env python3
"""Builds Blossom Skills V1: index.html (single page app) + skills/<slug>/SKILL.md files for the curl install."""
import json, base64, os, re
from data import CREATORS, MCPS, SKILLS
from hidden import HIDDEN
SKILLS = [s for s in SKILLS if s['id'] not in HIDDEN]

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
  f'<a href="/" class="on">{NAV["skills"]}Skills &amp; MCPs<span class="new">New</span></a><hr>'
  f'<a href="#" data-app>{NAV["save"]}Saved posts</a><hr>'
  f'<div class="sec"><span style="display:flex;align-items:center;gap:12px">{NAV["topics"]}Topics</span><svg class="chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></div>'
  + ''.join(f'<div class="topic"><img src="data:image/png;base64,{TOPIC_B64[k]}" alt="">{n}</div>' for n,k in TOPICS)
  + f'<div class="sub">See All Topics</div><hr><a href="#" data-app>{NAV["buzz"]}The Weekly Buzz</a><hr>'
  f'<a href="#" data-app>{NAV["resources"]}Resources</a><div class="sub">Get Help</div>'
  f'<a href="#" data-app class="bottom" style="color:var(--muted)">{NAV["settings"]}Settings</a></aside>')
for m in MCPS:
    if m.get('creator') == 'blossom' and not m.get('logo'): m['logo'] = 'logo_blossom_flower_256.jpg'   # Blossom MCPs get the flower, like the partner logos
    if m.get('logo'): m['logo_b64'] = base64.b64encode(open(os.path.join(OUT, 'assets', m['logo']), 'rb').read()).decode()

# write SKILL.md files for the curl install
# Free skills are served statically; paid SKILL.md lives only in Supabase and comes through /.netlify/functions/download with a purchase token.
def preview(md):
    head, _, rest = md.partition('\n---\n')
    body = rest.strip().split('\n')
    keep = '\n'.join(body[:8])
    return head + '\n---\n' + keep + '\n\n… the full SKILL.md (' + str(len(md.splitlines())) + ' lines) unlocks after purchase.'
SKILLS_OUT = []
os.makedirs(os.path.join(OUT, 'skills'), exist_ok=True)
for s in SKILLS:
    if s['price'].get('free'):
        d = os.path.join(OUT, 'skills', s['id']); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'SKILL.md'), 'w').write(s['skill'] + '\n')
        SKILLS_OUT.append(s)
    else:
        SKILLS_OUT.append(dict(s, skill=preview(s['skill']), paid_preview=True))

BASE = os.environ.get('BASE_PATH', '')   # '' on Netlify; '/skillsandmcps' when it moves under blossomsocial.com
DATA = json.dumps(dict(creators=CREATORS, mcps=MCPS, skills=SKILLS_OUT, site=SITE, base=BASE), ensure_ascii=False)

SRC = os.path.join(OUT, "src")
CSS = open(os.path.join(SRC, 'style.css'), encoding='utf-8').read()
CSS += '\n/* grid rhythm (v14): cards in a row share a height, screenshots are a fixed-height strip */\n.grid{align-items:stretch}.sk .shot{height:132px;aspect-ratio:auto;object-position:top}.sk>p{min-height:0}\n.sk .bot{display:grid;grid-template-columns:1fr auto;align-items:center;row-gap:4px}.sk .bot .l{display:flex;gap:14px;flex-wrap:wrap;min-width:0}.sk .bot .upd{grid-column:1/-1;display:inline}.g2 .sk .bot .upd{display:inline}.chip img{vertical-align:-2px;margin-right:2px}.chip.on img{filter:none}\n@media (max-width:720px){.tabs{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;gap:0}.tabs::-webkit-scrollbar{display:none}.tabs button{white-space:nowrap;margin-right:14px;font-size:15px;flex:none}.tabs button .n{display:none}.tabs .pill{flex:none;padding:6px 12px;font-size:13px}.sk .bot .l{gap:10px}}\n@media (max-width:980px){.detail .side{order:-1}.detail .side .card.buy{margin-bottom:0}}\n'
CSS += '\n/* learn / SEO section (home route only) */\n' + '.learn{display:none;margin-top:-10px}body.on-learn .learn{display:block}.learn-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.learn-steps div{background:#fff;border:1px solid var(--border);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;gap:6px}.learn-steps i{width:28px;height:28px;border-radius:50%;background:var(--purple);color:#fff;font-style:normal;font-weight:800;display:inline-flex;align-items:center;justify-content:center;font-size:13px}.learn-steps b{color:var(--ink);font-size:15.5px}.learn-steps span{font-size:14px;color:var(--text);line-height:1.5}@media (max-width:720px){.learn-steps{grid-template-columns:1fr}}.learn h2{font-size:22px;margin-bottom:8px}.learn .lead{font-size:15.5px;color:var(--text);margin:0 0 18px;max-width:820px}.learn-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.learn-grid article{background:#fff;border:1px solid var(--border);border-radius:12px;padding:16px 18px}.learn-grid h3{font-size:15.5px;margin-bottom:6px}.learn-grid p{margin:0;font-size:14px;color:var(--text);line-height:1.55}.learn-list{margin:0;padding-left:20px;font-size:14px;color:var(--text)}.learn-list li{margin:4px 0}@media (max-width:720px){.learn-grid{grid-template-columns:1fr}}'
JS = '\n'.join(open(os.path.join(SRC, 'js', f), encoding='utf-8').read() for f in sorted(os.listdir(os.path.join(SRC, 'js'))) if f.endswith('.js'))

FAQ = [
  ("What is a skill?", "A skill is a small text file (SKILL.md) that teaches an AI assistant how to do one job well — for example, grade your income portfolio against a creator’s written rules, or read space stocks the way one investor does. You download it once, add it to Claude, ChatGPT, Grok or Cursor, and from then on you can ask for it in plain words. Skills on Blossom are written by investors, so they carry that investor’s judgment, not generic advice."),
  ("What is an MCP?", "MCP (Model Context Protocol) is the open standard that lets an AI assistant connect to outside data and tools. An MCP server is what gives a skill its data: the Blossom Connector MCP gives your assistant read access to your portfolio, trades and the posts you follow; the Blossom Aggregate Trade Data MCP shows what 500,000+ investors are buying and selling; brokerage MCPs from Public, Questrade, Robinhood, Webull, moomoo, IBKR and Alpaca connect your account directly. You connect an MCP once and every skill that needs it just works."),
  ("Which AI assistants do these work with?", "Claude (desktop, web and Claude Code), ChatGPT, Grok and Cursor. Each skill page has install steps for all of them, and each MCP page has the connector URL or command for all of them."),
  ("Is it free?", "Many skills are free. Creators can also charge one-time, monthly or yearly; there are no free trials. The Blossom Connector MCP is included with Blossom PRO+. Blossom keeps 20% of each paid sale and pays creators the rest monthly."),
  ("Can I publish my own skill?", "Yes — anyone with a Blossom account can post a skill. Upload your SKILL.md, add a pitch, a sample output and screenshots, pick a price, and it goes live in the library."),
  ("Do skills place trades?", "Only if the creator turns on “This skill can place orders”, and then the listing says so. Everything else reads your data and explains, screens or alerts; the Blossom Connector itself never places trades."),
]
jsonld = [
  {"@context": "https://schema.org", "@type": "WebSite", "name": "Blossom Skills & MCPs", "alternateName": "Blossom skills marketplace", "url": SITE + "/", "publisher": {"@type": "Organization", "name": "Blossom Social", "url": "https://www.blossomsocial.com/"}},
  {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
  {"@context": "https://schema.org", "@type": "ItemList", "name": "Skills for investors", "itemListElement": [
      {"@type": "ListItem", "position": i + 1, "item": {"@type": "SoftwareApplication", "name": s_['name'], "description": s_['pitch'], "url": f"{SITE}/skill/{s_['id']}", "applicationCategory": "FinanceApplication", "operatingSystem": "Claude, ChatGPT, Grok, Cursor",
          "author": {"@type": "Person", "name": CREATORS[s_['creator']]['name']},
          "offers": {"@type": "Offer", "price": "0" if s_['price'].get('free') else str(s_['price'].get('monthly') or s_['price'].get('yearly') or s_['price'].get('once')), "priceCurrency": "CAD"}}}
      for i, s_ in enumerate(SKILLS)]},
]
JSONLD = ''.join('<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>' for j in jsonld)
import html as _html
def _p(t): return _html.escape(t)
LEARN = ('<section class="learn" id="learn"><div class="wrap">'
  '<h2>How it works</h2>'
  '<p class="lead">Blossom Skills &amp; MCPs is a skills marketplace for investors. Skills are instructions your AI assistant follows; MCPs are the connections that give it your data. Together they turn Claude, ChatGPT, Grok or Cursor into an investing assistant that knows your portfolio and thinks like the investors you follow on Blossom.</p>'
  '<div class="learn-steps">'
  '<div><i>1</i><b>Connect an MCP</b><span>Add the Blossom Connector (or a brokerage MCP) to your AI assistant once. OAuth, no keys to paste.</span></div>'
  '<div><i>2</i><b>Download a skill</b><span>Pick a skill from an investor you trust. Free, or a subscription that pays them to keep it current.</span></div>'
  '<div><i>3</i><b>Ask in plain words</b><span>“Run my portfolio through Perry’s income rules.” Your assistant reads your real holdings and answers the way that investor would.</span></div>'
  '</div>'
  '<h2 style="margin-top:28px">Questions</h2>'
  '<div class="learn-grid">' + ''.join(f'<article><h3>{_p(q)}</h3><p>{_p(a)}</p></article>' for q, a in FAQ) + '</div>'
  '<p class="small" style="margin-top:22px">Want to publish? <a href="/post">Post a skill</a> · <a href="/terms">Creator terms</a> · Built an MCP investors would use? <a href="mailto:partnerships@blossomsocial.com?subject=MCP%20listing%20on%20Blossom%20Skills">Tell us</a>.</p>'
  '</div></section>')
# llms.txt: the plain-text version of the catalogue for AI assistants and crawlers
llms = ['# Blossom Skills & MCPs', '', '> A skills marketplace for investors: investing skills (SKILL.md files) and MCP servers for Claude, ChatGPT, Grok and Cursor, built by verified investors on Blossom Social. ' + SITE + '/', '', '## What they are', '']
llms += [f'- {q} {a}' for q, a in FAQ]
llms += ['', '## Skills', ''] + [f'- [{s_["name"]}]({SITE}/skill/{s_["id"]}) by {CREATORS[s_["creator"]]["name"]} (@{s_["creator"]}): {s_["pitch"]} Price: {"free" if s_["price"].get("free") else ", ".join(f"{k} ${v}" for k, v in s_["price"].items())}.' for s_ in SKILLS]
llms += ['', '## MCPs', ''] + [f'- [{m["name"]}]({SITE}/mcp/{m["id"]}): {m["pitch"]}' for m in MCPS if not m.get('compat')]
llms += ['', '## Publish', '', f'- Post a skill: {SITE}/post', f'- Creator terms: {SITE}/terms', '']
open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(llms))


def page(title, desc, url, extra_ld='', app=''):
    """One HTML document. `app` is server-rendered content for crawlers; the SPA replaces it on load."""
    t = _p(title); d = _p(desc)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="keywords" content="skills marketplace, MCP marketplace, investing skills, Claude skills, ChatGPT investing, MCP for investors, Model Context Protocol, agent skills, Blossom Social, portfolio MCP, agentic trading">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:type" content="website"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.jpg"><meta property="og:image:secure_url" content="{SITE}/og.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:alt" content="Blossom Skills &amp; MCPs"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:site_name" content="Blossom Skills">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{SITE}/og.jpg">
{JSONLD}{extra_ld}
<link rel="icon" href="/favicon.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS.replace('__WALL__', wall_b64)}</style></head>
<body>
<div class="appbar"><a class="logo" href="/"><img src="data:image/png;base64,{logo_b64}" alt="Blossom"></a><span class="sp"></span>
<a class="pill sec" href="https://www.blossomsocial.com/" target="_blank" rel="noopener" style="background:var(--bg);display:inline-flex;align-items:center;gap:8px"><svg viewBox="0 0 16 16" style="width:15px;height:15px;fill:currentColor"><rect x="2" y="2" width="5" height="5" rx="1.2"/><rect x="9" y="2" width="5" height="5" rx="1.2"/><rect x="2" y="9" width="5" height="5" rx="1.2"/><rect x="9" y="9" width="5" height="5" rx="1.2"/></svg>Get App</a>
<a class="pill pri" href="https://www.blossomsocial.com/" target="_blank" rel="noopener" style="margin-left:12px">Sign up</a></div>
<div class="shell">{SIDEBAR}
<div class="main"><div id="app">{app}</div>
{LEARN}
<footer>Blossom Skills · V1 preview · <a href="/post">Post a skill</a> · <a href="/mcps">MCPs</a> · <a href="/learn">How it works</a> · <a href="https://www.blossomsocial.com/" target="_blank" rel="noopener">blossomsocial.com</a></footer></div></div>
<script>{JS.replace('__DATA__', DATA).replace('__BROKERS__', BROKERS_JS).replace('__BEEVIS__', beevis_b64).replace('__FLOWER__', flower_b64).replace('__BADGE__', badge_b64)}</script>
</body></html>"""

def ssr_skill(s_):
    """Crawler-visible summary of a skill (the SPA re-renders the full page)."""
    c = CREATORS[s_['creator']]
    price = 'Free' if s_['price'].get('free') else ' · '.join(f"${v} {k}" for k, v in s_['price'].items())
    reqs = ', '.join(next((m['name'] for m in MCPS if m['id'] == r), r) for r in (s_.get('requires') or []))
    return (f'<div class="wrap"><h1>{_p(s_["name"])}</h1><p>{_p(s_["pitch"])}</p><p>By {_p(c["name"])} (@{_p(s_["creator"])}) on Blossom · {_p(price)} · v{_p(s_["version"])} · updated {_p(s_["updated"])}</p>'
            + '<ul>' + ''.join(f'<li>{_p(h)}</li>' for h in (s_.get('highlights') or [])) + '</ul>'
            + (f'<p>Needs: {_p(reqs)}.</p>' if reqs else '') + '<p>Try: ' + ' · '.join(f'“{_p(x)}”' for x in s_['prompts']) + '</p>'
            + '<p>Works in Claude, ChatGPT, Grok and Cursor. <a href="/">All skills</a></p></div>')

def ssr_mcp(m):
    return (f'<div class="wrap"><h1>{_p(m["name"])}</h1><p>{_p(m["pitch"])}</p><p>{_p(m.get("about",""))}</p>'
            + '<ul>' + ''.join(f'<li><b>{_p(t)}</b> — {_p(d)}</li>' for t, d in m['tools']) + '</ul>'
            + '<p>Connects to Claude, ChatGPT, Grok and Cursor. <a href="/mcps">All MCPs</a></p></div>')

HOME_T = 'Blossom Skills & MCPs — the skills marketplace for investors (Claude, ChatGPT, Grok, Cursor)'
HOME_D = 'Blossom Skills & MCPs is a skills marketplace for investors: download investing skills and connect MCPs that give Claude, ChatGPT, Grok and Cursor access to your portfolio, trades and what 500,000+ Blossom investors are doing. Built by verified investors on Blossom.'
open(os.path.join(OUT, 'index.html'), 'w').write(page(HOME_T, HOME_D, SITE + '/'))
# one static page per seeded skill and per MCP, so each tile is its own indexable URL (skills posted later are rendered by netlify/functions/page.mjs)
PAGES = os.path.join(OUT, 'pages'); import shutil; shutil.rmtree(PAGES, ignore_errors=True)
urls = [SITE + '/', SITE + '/mcps', SITE + '/learn', SITE + '/post', SITE + '/terms']
for s_ in SKILLS:
    c = CREATORS[s_['creator']]
    ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "SoftwareApplication", "name": s_['name'], "description": s_['pitch'], "url": f"{SITE}/skill/{s_['id']}", "applicationCategory": "FinanceApplication", "operatingSystem": "Claude, ChatGPT, Grok, Cursor", "author": {"@type": "Person", "name": c['name']}, "softwareVersion": s_['version'], "dateModified": s_['updated'], "offers": {"@type": "Offer", "price": "0" if s_['price'].get('free') else str(s_['price'].get('monthly') or s_['price'].get('yearly') or s_['price'].get('once')), "priceCurrency": "CAD"}}, ensure_ascii=False) + '</script>'
    d = os.path.join(PAGES, 'skill', s_['id']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(page(f"{s_['name']} by {c['name']} — a skill for Claude, ChatGPT, Grok and Cursor | Blossom Skills", s_['pitch'], f"{SITE}/skill/{s_['id']}", ld, ssr_skill(s_)))
    urls.append(f"{SITE}/skill/{s_['id']}")
for m in MCPS:
    if m.get('compat'): continue
    d = os.path.join(PAGES, 'mcp', m['id']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(page(f"{m['name']} MCP — connect it to Claude, ChatGPT, Grok and Cursor | Blossom Skills", m['pitch'], f"{SITE}/mcp/{m['id']}", '', ssr_mcp(m)))
    urls.append(f"{SITE}/mcp/{m['id']}")
for route_ in ('mcps', 'learn', 'post', 'terms'):
    d = os.path.join(PAGES, route_); os.makedirs(d, exist_ok=True)
    titles = {'mcps': ('MCPs for investors — Blossom Connector, Aggregate Trade Data, Fiscal.ai and brokerage MCPs | Blossom Skills', 'MCP servers that connect Claude, ChatGPT, Grok and Cursor to your portfolio, trades, the Blossom community and your brokerage.'),
              'learn': ('What are skills and MCPs? How Blossom Skills works', 'Skills are instructions your AI assistant follows; MCPs are the connections that give it your data. How to connect an MCP, download a skill and ask in plain words.'),
              'post': ('Post a skill — publish your investing skill on Blossom', 'Upload a SKILL.md, add a pitch, sample output and screenshots, set a price, and it goes live in the Blossom Skills library.'),
              'terms': ('Creator terms — Blossom Skills', 'Terms for publishing and selling skills on Blossom Skills: ownership, the 20% platform fee, monthly payouts, updates, refunds and removal.')}
    open(os.path.join(d, 'index.html'), 'w').write(page(titles[route_][0], titles[route_][1], f"{SITE}/{route_}"))
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{u}</loc></url>' for u in urls) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\nSitemap: {SITE}/.netlify/functions/sitemap\n')
# Netlify: static pages win; skills published later (no static page) are rendered by the page function; everything else is the SPA shell.
open(os.path.join(OUT, '_redirects'), 'w').write('/skill/*  /.netlify/functions/page  200\n/mcp/*  /index.html  200\n/u/*  /index.html  200\n/manage/*  /index.html  200\n/success/*  /index.html  200\n/*  /index.html  200\n')
print('index.html', round(len(open(os.path.join(OUT, 'index.html')).read())/1024), 'KB;', len(SKILLS), 'skills,', len(MCPS), 'mcps;', len(urls), 'urls in sitemap')
