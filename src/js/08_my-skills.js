// ---------- my skills: what the signed-in Blossom user has bought (from the restore function, so it works on any device) and posted
const MY = { owned: null, err: null };   // owned: [{skill, plan, token}] · null = not loaded yet
async function loadMySkills(){
  try { const j=await post('restore',{identity:await idToken()}); const t=tokens(), o=owned(); (j.owned||[]).forEach(x=>{ t[x.skill]=x.token; o[x.skill]=x.plan; }); LS.set('tokens',t); LS.set('owned',o); MY.owned=j.owned||[]; MY.err=null; }
  catch(err){ MY.owned=[]; MY.err=err.message; }
  if(state.prev==='purchases') route();
}
function mySkills(){
  if(MY.owned===null){ loadMySkills(); return `<div class="wrap">${pageHead('Skills','/')}<div class="grid">${skeletons(2)}</div></div>`; }
  const planTxt = p => p==='once'?'One-time purchase':p==='monthly'?'Monthly subscription':p==='yearly'?'Yearly subscription':esc(p);
  const bought = MY.owned.map(x=>{ const s=skill(x.skill);
    return `<div class="card sk" ${s?`data-go="/skill/${s.id}"`:''}><div class="top"><div class="em">${s?sIcon(s):'🧾'}</div><div style="min-width:0"><h3>${esc(s?s.name:x.skill)}</h3><div class="by">${s?`${avatar(s.creator,20)} <b>@${esc(s.creator)}</b> ${badge(creator(s.creator))}`:'No longer listed'}</div></div></div>
      ${s?`<p>${esc(s.pitch)}</p>`:''}<div class="bot"><span class="l"><span>${planTxt(x.plan)}</span></span>${s?`<button class="pill teal sm" data-dl="${s.id}">Download SKILL.md</button>`:''}</div></div>`; }).join('');
  const posted = allSkills().filter(ownsSkill).map(s=>`<div class="card sk" data-go="/manage/${s.id}"><div class="top"><div class="em">${sIcon(s)}</div><div style="min-width:0"><h3>${esc(s.name)}</h3><div class="by">v${esc(s.version)} · ${esc(priceLabel(s.price).t)}</div></div></div><p>${esc(s.pitch)}</p><div class="bot"><span class="l"><span>${fmtN(s.downloads)} downloads</span></span><a class="pill sec sm" href="${BASE}/manage/${s.id}">Manage</a></div></div>`).join('');
  return `<div class="wrap">${pageHead('Skills','/')}
    <h2 style="font-size:22px;margin-bottom:4px">My skills</h2><p class="small" style="margin:0 0 18px">Signed in as <b>@${esc(ME?.username||'')}</b>. Purchases are tied to your Blossom account, so they're here on any device.</p>
    ${MY.err?`<div class="empty">Couldn’t load your purchases: ${esc(MY.err)}</div>`:''}
    <h3 style="font-size:16px;margin:0 0 10px">Purchased</h3>
    <div class="grid">${bought||`<div class="empty" style="grid-column:1/-1">Nothing bought yet. <a href="${BASE}">Browse skills</a></div>`}</div>
    <h3 style="font-size:16px;margin:26px 0 10px">Posted by you</h3>
    <div class="grid">${posted||`<div class="empty" style="grid-column:1/-1">You haven’t posted a skill yet. <a href="${BASE}/post">Post one →</a></div>`}</div></div>`;
}
function bindMySkills(){
  document.querySelectorAll('[data-go]').forEach(el=>el.addEventListener('click',e=>{ if(e.target.closest('a,button')) return; go(el.dataset.go); }));
  document.querySelectorAll('[data-dl]').forEach(b=>b.onclick=e=>{ e.stopPropagation(); const s=skill(b.dataset.dl); if(s) downloadSkill(s); });
}
