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

