// ---------- creator page
function creatorPage(h){
  const c=creator(h); if(!c) return library();
  const mine_=allSkills().filter(s=>s.creator===h);
  const dl=mine_.reduce((a,s)=>a+s.downloads,0);
  return `<div class="wrap"><div class="card chead">${avatar(h,76)}<div style="flex:1"><h1>${esc(c.name)} ${badge(c)}</h1><div class="h">@${h}</div><p>${esc(c.bio)}</p><div class="nums"><span><b>${fmtN(c.followers)}</b> followers</span><span><b>${mine_.length}</b> skills</span><span><b>${fmtN(dl)}</b> downloads</span><span><b>${(mine_.reduce((a,s)=>a+s.rating,0)/Math.max(1,mine_.length)).toFixed(1)} ★</b> avg rating</span></div></div><button class="pill teal" id="follow">Follow</button></div>
  <div class="sec-h"><h2>Skills by @${h}</h2></div><div class="grid">${mine_.map(skillCard).join('')||'<div class="empty">No skills yet.</div>'}</div></div>`;
}

