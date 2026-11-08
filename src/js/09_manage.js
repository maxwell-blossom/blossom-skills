// ---------- manage (creator view)
function manage(id){
  const s=skill(id); if(!s) return library();
  const subs = s.mine? 0 : Math.round(s.downloads*(s.price.free?0:0.18));
  const mrr = s.price.free?0: subs*(s.price.monthly||((s.price.yearly||s.price.once||0)/12));
  return `<div class="wrap">${pageHead('Skills','/')}
    <div class="card" style="padding:22px 26px;display:flex;gap:16px;align-items:center;margin-bottom:16px"><div class="em" style="width:56px;height:56px;border-radius:14px;background:var(--lav2);display:flex;align-items:center;justify-content:center;font-size:28px">${s.emoji}</div><div style="flex:1"><h1 style="font-size:22px">${esc(s.name)} ${s.status==='In review'?'<span class="badge beta">In review</span>':'<span class="badge partner">Live</span>'}</h1><div class="small">${s.status==='In review'?'Submitted today · most listings are live within 24 hours · you’ll get a DM':'Live since '+ago(s.updated)} · <a href="/skill/${s.id}">View listing</a> · <a href="#" data-copy="${SITE}/skill/${s.id}">Copy link</a></div></div><a class="pill sec" href="/skill/${s.id}">Preview</a></div>
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
  $('#pub').onclick=()=>{ const v=$('#ver').value.trim(), n=$('#note').value.trim(); if(!n){ toast('Say what changed'); return; }
    const local=()=>{ const m=mine(); const i=m.findIndex(x=>x.id===id); const today=new Date().toISOString().slice(0,10); if(i>=0){ m[i].log.unshift([v,today,n]); m[i].version=v; LS.set('mine',m); } else { s.log.unshift([v,today,n]); s.version=v; } toast('Update published · '+(s.price.free?'followers':'subscribers')+' notified'); route(); };
    if(s.mine) post('update',{skill:id, creator:s.creator, version:v, note:n}).then(local).catch(err=>toast('Could not publish the update: '+err.message)); else local(); };
}

document.querySelectorAll('[data-app]').forEach(a=>a.addEventListener('click',e=>{ e.preventDefault(); toast('That’s the Blossom web app — this preview only has Skills & MCPs'); }));
route();
loadCatalogue();
