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
  const slug=s.id, tok=tokens()[s.id], url = s.price.free ? `${SITE}/skills/${slug}/SKILL.md` : tok ? `${SITE}/.netlify/functions/download?skill=${slug}&token=${encodeURIComponent(tok)}` : null;
  if(!url){ const note=`<p class="small">Subscribe first — your personal install command (a link only you can use) appears here right after checkout.</p>`; return `<div class="itabs">${['Claude','Claude Code','Cursor','ChatGPT','Grok'].map((v,i)=>`<button class="${i===0?'on':''}" disabled>${v}</button>`).join('')}</div><div id="ibody">${note}</div>`; }
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
  const have = s.price.free || !!tokens()[s.id];
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
      <button class="pill sec" id="share" style="width:100%;margin-top:12px">Share</button>${s.price.free||have?'':'<div class="small" style="text-align:center;margin-top:10px"><a href="#" id="restore">Already bought it? Restore access</a></div>'}</div>
    ${cc}${reqs}
  </div></div></div>`;
}
function bindDetail(id){
  const s=skill(id); if(!s) return;
  document.querySelectorAll('[data-dtab]').forEach(b=>b.onclick=()=>{ state.dtab=b.dataset.dtab; route(); });
  document.querySelectorAll('[data-itab]').forEach(b=>b.onclick=()=>{ state.itab=b.dataset.itab; $('#ibody').innerHTML = installBlock(s).replace(/^[\s\S]*?<div id="ibody">/,'').replace(/<\/div>$/,''); document.querySelectorAll('[data-itab]').forEach(x=>x.classList.toggle('on',x.dataset.itab===state.itab)); bindCopy(); });
  document.querySelectorAll('input[name=plan]').forEach(r=>r.onchange=()=>{ state.plan=r.value; route(); });
  bindCopy();
  const g=$('#get'); if(g) g.onclick=()=>downloadSkill(s);
  const rs=$('#restore'); if(rs) rs.onclick=e=>{ e.preventDefault(); restoreAccess(); };
  const b=$('#buy'); if(b) b.onclick=()=>checkout(s, state.plan);
  const f=$('#follow'); if(f) f.onclick=()=>{ f.textContent='Following'; f.className='pill sec sm'; toast('Following @'+s.creator); };
  const sh=$('#share'); if(sh) sh.onclick=()=>copy(SITE+'/#/skill/'+s.id,'Link copied');
  document.querySelectorAll('[data-lb]').forEach(f=>f.onclick=()=>{ const m=document.createElement('div'); m.className='lb'; m.innerHTML=`<img src="${f.dataset.lb}" alt="">`; m.onclick=()=>m.remove(); document.body.appendChild(m); });
  document.querySelectorAll('[data-go]').forEach(el=>el.addEventListener('click',e=>{ if(e.target.closest('a,button')) return; location.hash=el.dataset.go; }));
}
function bindCopy(){ document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=e=>{ e.stopPropagation(); copy(b.dataset.copy); }); }

