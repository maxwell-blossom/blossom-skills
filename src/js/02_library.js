// ---------- library
function skillCard(s){
  const c=creator(s.creator); const p=priceLabel(s.price);
  return `<div class="card sk" data-go="/skill/${s.id}">
    <div class="top"><div class="em">${sIcon(s)}</div><div style="min-width:0"><h3>${esc(s.name)}${s.trades?' <span class="badge warn">⚠️ can place orders</span>':''}</h3><div class="by">${avatar(s.creator,20)} <b>@${esc(s.creator)}</b> ${badge(c)}</div></div></div>
    <p>${esc(s.pitch)}</p>
    ${(s.shots||[]).length?`<img class="shot" src="${shotUrl(s.shots[0][0])}" alt="" loading="lazy">`:''}
    ${(s.highlights||[]).length?`<ul class="hl">${s.highlights.slice(0,3).map(h=>`<li>${esc(h)}</li>`).join('')}</ul>`:''}
    <div class="req">${reqChips(s)}</div>
    <div class="bot"><span class="l"><span>${fmtN(s.downloads)} downloads</span><span>${s.ratings?`${stars(s.rating)} <b style="color:var(--ink)">${s.rating.toFixed(1)}</b> <span style="color:var(--muted)">(${s.ratings})</span>`:'No ratings yet'}</span></span><span class="price ${p.cls}">${p.t}</span><span class="upd">v${s.version} · updated ${ago(s.updated)}</span></div>
  </div>`;
}
function mcpCard(m){
  const by = `<span class="small">by <b style="color:var(--ink)">${esc(m.creator ? creator(m.creator).name : m.creator_name)}</b></span>`;
  return `<div class="card sk" data-go="/mcp/${m.id}">
    <div class="top"><div class="em mcp">${mIcon(m,true)}</div><div style="min-width:0"><h3>${esc(m.name)} ${m.trades?' <span class="badge warn">⚠️ can place orders</span>':''}</h3><div class="by">${by}</div></div></div>
    <p>${esc(m.pitch)}</p>
    <ul class="hl">${m.tools.slice(0,3).map(([t,d])=>`<li><b style="font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:var(--purple);font-weight:600">${esc(t)}</b> <span>${esc(d.split('.')[0])}</span></li>`).join('')}</ul><div class="req"><span class="chip rq">${m.tools.length} tools</span><span class="chip rq">${m.auth.split('·')[0].trim()}</span></div>
    <div class="bot"><span class="l"><span>${fmtN(m.installs)} connected</span><span>${stars(m.rating)} <b style="color:var(--ink)">${m.rating.toFixed(1)}</b></span></span><span class="price ${/^Free/.test(m.price)?'free':/PRO\+/.test(m.price)?'pro':''}">${esc(m.price.split('·')[0].trim())}</span></div>
  </div>`;
}
function library(){
  const uses = (s,id)=>(s.requires||[]).includes(id)||(s.optional||[]).includes(id);
  let list = allSkills().filter(s=>state.cat==='All'||uses(s,state.cat)).filter(s=>!state.q||(s.name+' '+s.pitch+' '+s.creator+' '+s.cat).toLowerCase().includes(state.q.toLowerCase()));
  const mo = s => s.price.free?0:(s.price.monthly||(s.price.yearly||0)/12||(s.price.once||0)/12);   // monthly-equivalent price for sorting
  const sorters = {top:(a,b)=>b.rating*Math.log(b.ratings+1)-a.rating*Math.log(a.ratings+1), dl:(a,b)=>b.downloads-a.downloads, new:(a,b)=>b.updated.localeCompare(a.updated), price:(a,b)=>mo(a)-mo(b), pricehi:(a,b)=>mo(b)-mo(a)};
  list.sort(sorters[state.sort]);
  const totalDl = D.skills.reduce((a,s)=>a+s.downloads,0);
  const hero = `<div class="hero"><div>
      <h1>🤖 The Best Skills and MCPs for&nbsp;Investors</h1>
      <p>Discover and download skills built by Blossom investors for Claude, ChatGPT, Grok and Cursor to supercharge your investing.</p>
      <div class="search"><span style="color:var(--muted)">🔍</span><input id="q" placeholder="Search skills, creators, tickers… try “dividends”" value="${esc(state.q)}"><button class="pill pri sm" id="qgo">Search</button></div>
    </div>
    <div class="side">
      <div class="stack">${['maxstocks','dividendsdan','tfsa_tina','northofthe49','quantqueen','earningsedge'].map(h=>avatar(h,48)).join('')}</div>
      <div class="t">Built by verified investors on Blossom</div>
    </div></div>`;
  const tabs = `<div class="tabs"><button class="${state.tab==='skills'?'on':''}" data-tab="skills">Skills<span class="n">${allSkills().length}</span></button><button class="${state.tab==='mcps'?'on':''}" data-tab="mcps">MCPs<span class="n">${listedMcps().length}</span></button><button class="${state.tab==='learn'?'on':''}" data-tab="learn">How it works</button><span class="sp" style="flex:1"></span><a class="pill pri sm" href="/post" style="align-self:center">+ Post a skill</a></div>`;
  let body='';
  if(state.tab==='skills'){
    body = `<div class="filters"><button class="chip ${state.cat==='All'?'on':''}" data-cat="All">All</button>${D.mcps.map(m=>`<button class="chip ${state.cat===m.id?'on':''}" data-cat="${m.id}" title="Skills that use ${esc(m.name)}">${mIcon(m)} ${SHORT[m.id]||esc(m.name)}</button>`).join('')}<span class="sp"></span><select id="sort"><option value="top" ${state.sort==='top'?'selected':''}>Top rated</option><option value="dl" ${state.sort==='dl'?'selected':''}>Most downloaded</option><option value="new" ${state.sort==='new'?'selected':''}>Recently updated</option><option value="price" ${state.sort==='price'?'selected':''}>Price: low to high</option><option value="pricehi" ${state.sort==='pricehi'?'selected':''}>Price: high to low</option></select></div>
      <div class="grid">${list.map(skillCard).join('')||'<div class="empty">Nothing matches that yet. <a href="/post">Post the first one →</a></div>'}</div>`;
  } else if(state.tab==='learn'){
    body = '';   // the How-it-works section is static HTML below #app (see build.py LEARN) so crawlers get it without JS
  } else {
    body = `<p class="small" style="margin:0 0 16px">An MCP is what gives a skill its data. Connect one once and every skill that needs it just works.</p><div class="grid">${listedMcps().map(mcpCard).join('')}</div>
      <div class="card" style="margin-top:18px;padding:18px 22px;display:flex;gap:16px;align-items:center;background:linear-gradient(100deg,#fff,#F1F5F7)"><div style="font-size:30px">🧩</div><div><b style="color:var(--ink)">MCPs are listed by Blossom and its partners.</b><div class="small">Built an MCP investors would use? Tell us what it does and who it’s for and we'll consider adding it to the library!</div></div><a class="pill out sm" style="margin-left:auto" href="mailto:partnerships@blossomsocial.com?subject=MCP%20listing%20on%20Blossom%20Skills">Get in touch</a></div>`;
  }
  return `<div class="wrap">${hero}${tabs}${body}</div>`;
}
function bindLibrary(){
  document.querySelectorAll('[data-go]').forEach(el=>el.addEventListener('click',e=>{ if(e.target.closest('a,button')) return; go(el.dataset.go); }));
  document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{ go(b.dataset.tab==='mcps'?'/mcps':b.dataset.tab==='learn'?'/learn':'/'); });
  document.querySelectorAll('[data-cat]').forEach(b=>b.onclick=()=>{ state.cat=b.dataset.cat; route(); });
  const so=$('#sort'); if(so) so.onchange=()=>{ state.sort=so.value; route(); };
  const q=$('#q'); if(q){ const doSearch=()=>{ state.q=q.value; route(); const nq=$('#q'); if(nq){nq.focus(); nq.setSelectionRange(nq.value.length,nq.value.length);} }; q.addEventListener('keydown',e=>{ if(e.key==='Enter') doSearch(); }); $('#qgo').onclick=doSearch; }
}

