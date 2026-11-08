#!/usr/bin/env python3
"""Renders the 1200x630 share-card image (og.jpg) for blossom-skills.netlify.app"""
import os, base64, asyncio
from playwright.async_api import async_playwright
OUT=os.path.dirname(os.path.abspath(__file__))
b64=lambda p: base64.b64encode(open(os.path.join(OUT,'assets',p),'rb').read()).decode()
logo=b64('_blossom_logo_t.png'); wall=b64('wall_tile.jpg')
avs=''.join(f'<img src="data:image/jpeg;base64,{b64("profiles/avatar_%02d.jpg"%n)}">' for n in (1,9,8,4,10,5))
HTML=f"""<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap" rel="stylesheet"><style>
body{{margin:0;width:1200px;height:630px;font-family:Nunito,sans-serif;color:#171717;-webkit-font-smoothing:antialiased}}
.c{{position:relative;width:1200px;height:630px;background:linear-gradient(105deg,#EDE9FF,#F6E9FA 48%,#E1F4F1);overflow:hidden}}
.c:before{{content:"";position:absolute;inset:0;background:url(data:image/jpeg;base64,{wall}) repeat;background-size:211px;opacity:.13;mix-blend-mode:multiply}}
.in{{position:relative;padding:64px 72px;height:100%;box-sizing:border-box;display:flex;flex-direction:column}}
.logo{{height:52px;width:auto;align-self:flex-start}}
h1{{font-size:68px;line-height:1.08;margin:54px 0 18px;font-weight:900;letter-spacing:-.5px;max-width:980px}}
p{{font-size:28px;color:#3F3F46;margin:0;max-width:900px;line-height:1.35;font-weight:600}}
.foot{{margin-top:auto;display:flex;align-items:center;gap:18px}}
.stack{{display:flex}}.stack img{{width:64px;height:64px;border-radius:50%;border:3px solid #fff;margin-right:-16px;object-fit:cover;box-shadow:0 2px 6px rgba(0,0,0,.1)}}
.t{{font-size:23px;font-weight:800;margin-left:28px;flex:1;white-space:nowrap}}.t span{{display:block;font-size:18px;color:#72777F;font-weight:600}}
.pill{{white-space:nowrap;margin-left:auto;background:#7361F7;color:#fff;border-radius:999px;padding:16px 30px;font-size:24px;font-weight:800}}
</style></head><body><div class="c"><div class="in">
<img class="logo" src="data:image/png;base64,{logo}">
<h1>🤖 The Best Skills and MCPs for Investors</h1>
<p>Discover and download skills built by Blossom investors for Claude, ChatGPT, Grok and Cursor.</p>
<div class="foot"><div class="stack">{avs}</div><div class="t">Built by verified investors on Blossom<span>Free, or subscribe to a creator · blossom-skills.netlify.app</span></div><div class="pill">Browse skills →</div></div>
</div></div></body></html>"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1200,'height':630}, device_scale_factor=1)
        await pg.set_content(HTML); await pg.wait_for_timeout(800)
        await pg.screenshot(path=os.path.join(OUT,'assets','og.jpg'), type='jpeg', quality=88); await b.close()
    print('og.jpg', os.path.getsize(os.path.join(OUT,'assets','og.jpg'))//1024, 'KB')
asyncio.run(main())
