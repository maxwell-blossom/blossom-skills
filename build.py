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
# Free skills are served statically; paid SKILL.md lives only in Supabase and comes through /.netlify/functions/download with a purchase token.
def preview(md):
    head, _, rest = md.partition('\n---\n')
    body = rest.strip().split('\n')
    keep = '\n'.join(body[:8])
    return head + '\n---\n' + keep + '\n\n… the full SKILL.md (' + str(len(md.splitlines())) + ' lines) unlocks after purchase.'
SKILLS_OUT = []
for s in SKILLS:
    if s['price'].get('free'):
        d = os.path.join(OUT, 'skills', s['id']); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'SKILL.md'), 'w').write(s['skill'] + '\n')
        SKILLS_OUT.append(s)
    else:
        SKILLS_OUT.append(dict(s, skill=preview(s['skill']), paid_preview=True))

DATA = json.dumps(dict(creators=CREATORS, mcps=MCPS, skills=SKILLS_OUT, site=SITE), ensure_ascii=False)

SRC = os.path.join(OUT, "src")
CSS = open(os.path.join(SRC, 'style.css'), encoding='utf-8').read()
JS = '\n'.join(open(os.path.join(SRC, 'js', f), encoding='utf-8').read() for f in sorted(os.listdir(os.path.join(SRC, 'js'))) if f.endswith('.js'))

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
