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
  const anyOf=(s.requires||[]).length===1&&s.requires[0]==='blossom-connector'&&(s.optional||[]).some(r=>mcp(r)?.compat);
  const slug=s.id, tok=tokens()[s.id], url = s.price.free ? (s.remote ? `${SITE}/api/download?skill=${slug}` : `${SITE}/skills/${slug}/SKILL.md`) : tok ? `${SITE}/api/download?skill=${slug}&token=${encodeURIComponent(tok)}` : null;
  if(!url){ const note=`<p class="small">Subscribe first — your personal install command (a link only you can use) appears here right after checkout.</p>`; return `<div class="itabs">${['Claude','Claude Code','Cursor','ChatGPT','Grok'].map((v,i)=>`<button class="${i===0?'on':''}" disabled>${v}</button>`).join('')}</div><div id="ibody">${note}</div>`; }
  const tabs = {claude:'Claude', code:'Claude Code', cursor:'Cursor', chatgpt:'ChatGPT', grok:'Grok'};
  const content = {
    claude: `<ol class="steps"><li><b>Download</b> the skill with the button above. Put <code>SKILL.md</code> in a folder named <code>${slug}</code> and zip it.</li><li>In Claude: <b>Settings → Capabilities → Skills → Upload skill</b> and choose the zip <span class="small">(Pro, Max, Team or Enterprise, with code execution on)</span>. In the Claude desktop app or Claude Code you can also drop the file into a chat and say <i>“Save this as a skill.”</i></li><li>Then just ask: <i>“${esc(s.prompts[0])}”</i>. Claude will ask to connect ${(s.requires||[]).map(r=>mcp(r)?.name).filter(Boolean).join(' and ')||'nothing extra'}${anyOf?' (or your broker MCP)':''} the first time.</li></ol>`,
    code: `<div class="code"><button class="cp" data-copy="mkdir -p ~/.claude/skills/${slug} && curl -fsSL ${url} -o ~/.claude/skills/${slug}/SKILL.md">Copy</button>mkdir -p ~/.claude/skills/${slug} \\
  && curl -fsSL ${url} \\
     -o ~/.claude/skills/${slug}/SKILL.md</div><p class="small" style="margin:10px 0 0">Then <code>/${slug}</code> in any session, or just ask in plain words.</p>`,
    cursor: `<div class="code"><button class="cp" data-copy="mkdir -p ~/.cursor/skills/${slug} && curl -fsSL ${url} -o ~/.cursor/skills/${slug}/SKILL.md">Copy</button>mkdir -p ~/.cursor/skills/${slug} \\
  && curl -fsSL ${url} -o ~/.cursor/skills/${slug}/SKILL.md</div><p class="small" style="margin:10px 0 0">Cursor reads skills from <code>~/.cursor/skills</code> (all projects) or <code>.cursor/skills</code> (this project). Add the MCPs it needs under <b>Cursor Settings → MCP → Add new MCP server</b> (snippets on each MCP page).</p>`,
    chatgpt: `<ol class="steps"><li>Open <b>ChatGPT → Projects → New project</b> and paste the skill file into the project’s <b>Instructions</b> (download it above and copy the contents).</li><li>Add the MCPs this skill needs: <b>Plugins → + → Add custom MCP server</b>, paste the URL from each MCP page and sign in when asked <span class="small">(Business, Enterprise or Pro; on Business an admin creates it)</span>.</li><li>Ask: <i>“${esc(s.prompts[0])}”</i></li></ol>`,
    grok: `<ol class="steps"><li>Add the MCPs this skill needs at <b>grok.com/connectors → New Connector → Custom</b> (the URL is on each MCP page; sign in when asked).</li><li>Grok has no skill files yet, so start a chat by pasting the SKILL.md (download it above) as your first message, then ask: <i>“${esc(s.prompts[0])}”</i>.</li><li>Pin that chat — or save the skill text as a Grok Project’s instructions if your plan has Projects.</li></ol>`
  };
  return `<div class="itabs">${Object.entries(tabs).map(([k,v])=>`<button class="${state.itab===k?'on':''}" data-itab="${k}">${v}</button>`).join('')}</div><div id="ibody">${content[state.itab]}</div>`;
}
// Rating box on the Reviews tab. Buyers (and anyone signed in, for free skills) can rate; one rating per person, re-posting replaces it.
// Skills posted without "What it does" lines: fall back to the SKILL.md description (sentences), so the section is never empty.
const first = t => (String(t||'').match(/^[\s\S]*?\.(?=\s|$)/)||[String(t||'')])[0];   // first sentence; a dot inside a domain doesn't count
function hlFallback(s){ const m=(s.skill||'').match(/^---\n([\s\S]*?)\n---/); const d=(m?(m[1].match(/^description:\s*(.*)$/m)||[])[1]||'':'').trim().replace(/^["']|["']$/g,'');
  const sents=d.split(/(?<=\.)\s+(?=[A-Z“"])/).map(x=>x.trim()).filter(x=>x&&!/^Use (when|whenever|if|for|this)\b/i.test(x));   // the "Use whenever…" sentence is routing for the AI, not for the reader
  return sents.length?sents.slice(0,3):[s.pitch]; }
function composeBox(s, have){
  const mineRev = ME && (s.reviews||[]).find(r=>r[0]===ME.username);
  const can = !!ME && have && !ownsSkill(s);
  const why = !ME ? 'Sign in to Blossom to rate it.' : ownsSkill(s) ? 'Creators can’t rate their own skill.' : !have ? (s.price.free?'Download the skill to rate it.':'Only people who bought this skill can rate it.') : (mineRev ? 'You’ve rated this — post again to change it.' : 'Your Blossom name shows with your rating.');
  const pick = state.stars || (mineRev?mineRev[1]:0);
  const words = ['','Not for me','Meh','Useful','Really good','Essential'];
  // Star first; the note and Post button appear once a star is picked (the note is optional).
  return `<div class="compose">${avatar(ME?.username,36)}<div style="flex:1"><div class="pick" ${can?'':'style="opacity:.45;pointer-events:none"'}>${[1,2,3,4,5].map(n=>`<button type="button" data-star="${n}" class="${n<=pick?'on':''}" aria-label="${n} star${n>1?'s':''}">★</button>`).join('')}<span class="pw">${pick?words[pick]:(can?'Tap a star to rate it':'')}</span></div>
    ${pick?`<textarea id="revtxt" placeholder="Add a note (optional) — what did it do for you?" ${can?'':'disabled'}>${esc(mineRev?mineRev[2]:'')}</textarea>
    <div class="prow"><button class="pill pri sm" id="revgo" ${can?'':'disabled'}>${mineRev?'Update rating':'Post rating'}</button><span class="note" style="margin:0">${esc(why)}</span></div>`:`<div class="note" style="margin:6px 0 0">${esc(why)}</div>`}</div></div>`;
}
function detail(id){
  const s=skill(id); if(!s) return `<div class="wrap"><div class="empty">${D.loaded?'That skill doesn’t exist (yet). <a href="'+BASE+'">Back to the library</a>':'Loading…'}</div></div>`;
  const c=creator(s.creator); const plans=planOptions(s); if(!state.plan||!plans.find(p=>p.k===state.plan)) state.plan=plans.find(p=>p.k==='yearly')?.k||plans[0].k;
  const have = s.price.free || !!tokens()[s.id];
  const sel = plans.find(p=>p.k===state.plan);
  const cta = s.price.free ? `<button class="pill pri lg" id="get">Get it free</button>` : have ? `<button class="pill teal lg" id="get">${owned()[s.id]==='once'?'Download · it’s yours':'Download · you’re subscribed'}</button>` : `<button class="pill pri lg" id="buy">${sel.k==='once'?`Buy for ${money(sel.price)}`:`Subscribe · ${money(sel.price)}/${sel.k==='monthly'?'mo':'yr'}`}</button>`;
  const amt = s.price.free ? `<div class="amt">Free</div><div class="sub">Free. Needs the Blossom Connector (included with <b>Blossom PRO+</b>).</div>` : `<div class="amt">${money(sel.price)}<small> ${sel.k==='monthly'?'/ month':sel.k==='yearly'?'/ year':'one-time'}</small></div><div class="sub">${sel.k==='once'?'Pay once. Updates included for 12 months.':'Every update while you’re subscribed. Cancel anytime.'}</div>`;
  const planSel = plans.length>1 ? `<div class="plans">${plans.map(p=>`<label class="plan ${state.plan===p.k?'on':''}"><input type="radio" name="plan" value="${p.k}" ${state.plan===p.k?'checked':''}><div><b>${p.label}</b>${p.sub?(p.k==='yearly'&&/Save/.test(p.sub)?` <span class="save">${p.sub}</span>`:`<div class="small">${p.sub}</div>`):''}</div><span class="pr">${money(p.price)}${p.k==='monthly'?'/mo':p.k==='yearly'?'/yr':''}</span></label>`).join('')}</div>` : '';
  // Star breakdown: real counts only. Until ratings exist the bars stay empty — no invented distribution.
  const dist = [5,4,3,2,1].map(n=>[n, (s.reviews||[]).filter(r=>r[1]===n).length]);
  const tot = dist.reduce((a,[,v])=>a+v,0) || 1;
  const reviews = (s.reviews||[]).map(([h,r,t,d])=>`<div class="rev">${avatar(h,36)}<div style="flex:1"><div class="who"><b>@${esc(h)}</b> ${badge(creator(h))} · ${stars(r)}${d?` · <span style="color:var(--ter)">${ago(d)}</span>`:''}</div>${t?`<p>${esc(t)}</p>`:''}</div></div>`).join('');
  const tabsHtml = `<div class="dtabs"><button class="${state.dtab==='overview'?'on':''}" data-dtab="overview">Overview</button><button class="${state.dtab==='updates'?'on':''}" data-dtab="updates">Updates <span class="small">(${s.log.length})</span></button><button class="${state.dtab==='reviews'?'on':''}" data-dtab="reviews">Reviews <span class="small">(${s.ratings})</span></button></div>`;
  // Skills that need the Connector and list broker MCPs as alternatives: either source of portfolio data will do, so both are shown under "What it needs" — Max, Nov 25.
  const opt=(s.optional||[]).filter(r=>mcp(r)), brokerOpt=opt.filter(r=>mcp(r).compat), otherOpt=opt.filter(r=>!mcp(r).compat);
  const anyOf=(s.requires||[]).length===1&&s.requires[0]==='blossom-connector'&&brokerOpt.length>0;
  let body='';
  if(state.dtab==='overview') body = `
    <div class="blk"><h3>${IC.check}What it does</h3><div class="what">${((s.highlights||[]).length?s.highlights:hlFallback(s)).map(h=>`<p>${esc(h)}</p>`).join('')}</div></div>
    <div class="blk"><h3>${IC.chat}Try these prompts</h3><div class="prompts">${s.prompts.map(p=>`<div class="prompt"><span>“${esc(p)}”</span><button class="cp" data-copy="${esc(p)}">Copy</button></div>`).join('')}</div></div>
    <div class="blk"><h3>${IC.sparkle}What you get${(s.shots||[]).length?` <span class="small" style="font-weight:600">· ${s.shots.length} screenshot${s.shots.length===1?'':'s'} from real runs</span>`:''}</h3>${(s.shots||[]).length?`<div class="gal ${s.shots.length===1?'one':''}">${s.shots.map(([f,c])=>`<figure data-lb="${shotUrl(f)}"><img src="${shotUrl(f)}" alt="${esc(c)}" loading="lazy"><figcaption>${esc(c)}</figcaption></figure>`).join('')}</div><details style="margin-top:12px"><summary class="small" style="cursor:pointer;font-weight:700">Sample reply as text</summary><div class="sample" style="margin-top:8px"><div class="md">${md(s.sample)}</div></div></details>`:`<div class="sample"><span class="lbl">Sample output · what your AI replies</span><div class="md">${md(s.sample)}</div></div>`}</div>
    <div class="blk"><h3>${IC.plug}What it needs</h3>${anyOf?`<p class="small" style="margin:0 0 10px">Your portfolio — from the <b>Blossom Connector</b> or a <b>broker MCP</b>. Either one works.</p>`:''}${(s.requires||[]).map(r=>{const m=mcp(r); return m?`<div class="reqrow"><div class="em">${mIcon(m,true)}</div><div><b>${esc(m.name)}</b><span>${esc(first(m.pitch))}</span></div><a class="pill sec sm" href="${BASE}/mcp/${m.id}">Connect</a></div>`:''}).join('')||'<p class="small">Nothing beyond your AI assistant.</p>'}${(s.requires||[]).includes('blossom-connector')?brokerStrip('<b style="color:var(--ink)">Works with your brokerage.</b> The Connector reads whatever you\'ve linked to Blossom, so this skill runs the same on Wealthsimple, Questrade, Robinhood, Public, IBKR, TD and the rest.'+(anyOf?'':' Broker MCPs are optional extras.')):''}${anyOf?`<div class="orline"><span>or connect your brokerage directly</span></div>${brokerOpt.map(r=>{const m=mcp(r); return `<div class="reqrow" style="border-style:dashed"><div class="em" style="background:var(--bg)">${mIcon(m,true)}</div><div><b>${esc(m.name)}</b><span>${esc(first(m.pitch))}</span></div><a class="pill sec sm" href="${BASE}/mcp/${m.id}">Details</a></div>`}).join('')}`:''}</div>
    ${otherOpt.length?`<div class="blk"><h3>${IC.plus}Also works with</h3><p class="small" style="margin:0 0 10px">Not required. If you have these connected, the skill uses them too.</p>${otherOpt.map(r=>{const m=mcp(r); return `<div class="reqrow" style="border-style:dashed"><div class="em" style="background:var(--bg)">${mIcon(m,true)}</div><div><b>${esc(m.name)} <span class="badge" style="background:var(--lav2);color:var(--p600)">supported</span></b><span>${esc(first(m.pitch))}</span></div><a class="pill sec sm" href="${BASE}/mcp/${m.id}">Details</a></div>`}).join('')}</div>`:''}
    <div class="blk"><h3>${IC.gear}How to install</h3>${installBlock(s)}</div>
    <div class="blk"><details class="skillmd"><summary>${IC.file}SKILL.md <span class="small" style="font-weight:600">· what your AI actually reads</span></summary><pre>${esc(s.skill)}</pre></details></div>`;
  else if(state.dtab==='updates') body = `
    <div class="promise"><span class="em">🔁</span><div><b style="color:var(--ink)">Updated ${esc(s.cadence.toLowerCase())}.</b> <span class="small">${s.price.free?'Free skills are updated at the creator’s pace.':'Subscribers get an email update when the new update ships.'}</span></div></div>
    <div class="tl">${s.log.map(([v,d,n],i)=>`<div class="tli"><span class="v">v${v}</span><span class="d">${new Date(d).toLocaleDateString('en-CA',{month:'short',day:'numeric',year:'numeric'})}</span>${i===0?'<span class="tag">Latest</span>':''}<p>${esc(n)}</p></div>`).join('')}</div>`;
  else body = `
    <div class="rsum"><div><div class="big">${s.rating.toFixed(1)}</div><div>${stars(s.rating)}</div><div class="small">${s.ratings} ratings · ${fmtN(s.downloads)} downloads</div></div><div class="bars">${dist.map(([n,v])=>`<div><span>${n} ★</span><i><b style="width:${Math.round(v/tot*100)}%"></b></i><span>${Math.round(v/tot*100)}%</span></div>`).join('')}</div></div>
    ${composeBox(s, have)}
    <div style="margin-top:14px">${reviews||`<div class="small" style="padding:14px 0;border-top:1px solid var(--border)">No ratings yet — be the first.</div>`}</div>`;
  const cc = creatorCard(s.creator);
  const reqs = '' && (s.requires||[]).length ? `<div class="card" style="padding:14px 16px"><b style="color:var(--ink);font-size:13.5px">Needs</b>${(s.requires||[]).map(r=>{const m=mcp(r);return m?`<div style="display:flex;gap:8px;align-items:center;margin-top:8px;font-size:13.5px"><span>${m.emoji}</span><a href="${BASE}/mcp/${m.id}">${esc(m.name)}</a><span class="small" style="margin-left:auto">${/^Free/.test(m.price)?'free':'from free'}</span></div>`:''}).join('')}</div>`:'';
  return `<div class="wrap">${pageHead('Skills', '/')}
  <div class="detail"><div>
    <div class="card"><div class="dhead"><div class="em">${sIcon(s)}</div><div style="flex:1;min-width:0"><h1>${esc(s.name)}${s.trades?' <span class="badge warn">⚠️ can place orders</span>':''}</h1><div class="pitch">${esc(s.pitch)}</div><div class="by">${avatar(s.creator,24)} <b>${esc(c?.name||s.creator)}</b> @${esc(s.creator)} ${badge(c)}</div>
      <div class="stats"><div><b>${fmtN(s.downloads)}</b>downloads</div><div><b>${stars(s.rating)} ${s.rating.toFixed(1)}</b>${s.ratings} ratings</div><div><b>v${s.version}</b>updated ${ago(s.updated)}</div><div><b>${esc(s.cadence.split(',')[0].slice(0,16))}</b>update cadence</div></div></div></div>
      ${tabsHtml}<div class="dbody">${body}</div></div>
  </div>
  <div class="side">
    <div class="card buy">${amt}${planSel}${cta}${s.price.free?'':`<div class="stripe">Secure checkout by <b>Stripe</b> · 80% goes to the creator</div>`}
      <ul class="incl"><li>Works in Claude, Claude Code, Cursor, ChatGPT, Grok</li><li>${s.price.free?'Updates at the creator’s pace':'Every update while subscribed'}</li><li>${s.trades?'⚠️ Can place orders through your broker MCP':'Read-only: never places trades'}</li>${s.price.free?'':'<li>Cancel anytime from My skills</li>'}</ul>
</div>
    ${cc}${reqs}
  </div></div></div>`;
}
// The Blossom app's profile card without its live parts: followers, the portfolio donut and Follow all read Blossom data
// this site can't reach, so it keeps the avatar, name and handle, and links to the profile on Blossom when there is one.
function creatorCard(h){
  const c=creator(h); if(!c) return '';
  const profile=c.url?`<div class="ppanel" style="margin-top:14px"><a class="pfollow" href="${esc(c.url)}" target="_blank" rel="noopener">View profile on Blossom</a></div>`:'';
  return `<div class="card pcard2"><div class="pava">${avatar(h,72)}<span class="pbolt"><svg viewBox="0 0 24 24"><path d="M13 2L4 14h6l-1 8 9-12h-6z"/></svg></span></div><div class="pname">${esc(c.name||h)} ${badge(c)}</div><div class="phandle">@${esc(h)}</div>
    ${profile}</div>`;
}
function bindDetail(id){
  const s=skill(id); if(!s) return;
  document.querySelectorAll('[data-dtab]').forEach(b=>b.onclick=()=>{ state.dtab=b.dataset.dtab; route(); });
  const starBtns=[...document.querySelectorAll('[data-star]')];
  starBtns.forEach(b=>{ b.onclick=()=>{ state.stars=+b.dataset.star; const txt=$('#revtxt')?.value; route(); if($('#revtxt')) $('#revtxt').value=txt||''; };
    b.onmouseenter=()=>{ const n=+b.dataset.star; starBtns.forEach(x=>x.classList.toggle('hov',+x.dataset.star<=n)); };
    b.onmouseleave=()=>starBtns.forEach(x=>x.classList.remove('hov')); });
  const rg=$('#revgo'); if(rg) rg.onclick=async()=>{ const n=state.stars||((s.reviews||[]).find(r=>ME&&r[0]===ME.username)||[])[1]; if(!n){ toast('Pick a star rating first'); return; }
    rg.disabled=true; rg.textContent='Saving…';
    try{ const j=await post('review',{identity:await idToken(), skill:s.id, stars:n, body:($('#revtxt')?.value||'').trim()}); s.rating=j.rating; s.ratings=j.ratings; const me=ME.username; s.reviews=[[me,n,($('#revtxt')?.value||'').trim(),new Date().toISOString().slice(0,10)],...(s.reviews||[]).filter(r=>r[0]!==me)]; state.stars=0; toast('Thanks — your rating is live'); route(); }
    catch(err){ rg.disabled=false; rg.textContent='Post rating'; toast(err.message, 5000); } };
  document.querySelectorAll('[data-itab]').forEach(b=>b.onclick=()=>{ state.itab=b.dataset.itab; $('#ibody').innerHTML = installBlock(s).replace(/^[\s\S]*?<div id="ibody">/,'').replace(/<\/div>$/,''); document.querySelectorAll('[data-itab]').forEach(x=>x.classList.toggle('on',x.dataset.itab===state.itab)); bindCopy(); });
  document.querySelectorAll('input[name=plan]').forEach(r=>r.onchange=()=>{ state.plan=r.value; route(); });
  bindCopy();
  const g=$('#get'); if(g) g.onclick=()=>downloadSkill(s);
  const rs=$('#restore'); if(rs) rs.onclick=e=>{ e.preventDefault(); restoreAccess(); };
  const b=$('#buy'); if(b) b.onclick=()=>{ const t=b.textContent; b.disabled=true; b.textContent='Opening secure checkout…'; checkout(s, state.plan).catch(()=>{}).finally(()=>{ if(document.body.contains(b)){ b.disabled=false; b.textContent=t; } }); };
  // Share = the public link (with its own preview image via og.mjs); the native share sheet where there is one, else copy it for a Blossom post.
  const sh=$('#share'); if(sh) sh.onclick=async()=>{ const url=SITE+'/skill/'+s.id; if(navigator.share){ try{ await navigator.share({title:s.name, text:s.pitch, url}); return; }catch(e){ if(e.name==='AbortError') return; } } copy(url,'Link copied — paste it in a Blossom post'); };
  document.querySelectorAll('[data-lb]').forEach(f=>f.onclick=()=>{ const m=document.createElement('div'); m.className='lb'; m.innerHTML=`<img src="${f.dataset.lb}" alt="">`; m.onclick=()=>m.remove(); document.body.appendChild(m); });
  document.querySelectorAll('[data-go]').forEach(el=>el.addEventListener('click',e=>{ if(e.target.closest('a,button')) return; go(el.dataset.go); }));
}
function bindCopy(){ document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=e=>{ e.stopPropagation(); copy(b.dataset.copy); }); }
