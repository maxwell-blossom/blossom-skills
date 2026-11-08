const D = __DATA__;
const BASE = D.base || '';   // '' on blossom-skills.netlify.app; '/skillsandmcps' once it lives on blossomsocial.com
function go(path){ history.pushState(null, '', BASE + path); window.__navd=true; route(); }
D.remote = [];   // skills published through the site and approved (status=live in Supabase); loaded by loadCatalogue()
const shotUrl = f => /^https?:|^data:/.test(f) ? f : 'shots/' + f;
async function loadCatalogue(){
  try {
    const j = await api('catalogue');
    const have = new Set(D.skills.map(s=>s.id));
    (j.creators||[]).forEach(c=>{ if(!D.creators[c.handle]) D.creators[c.handle] = {handle:c.handle, name:c.name, badge:c.badge, bio:c.bio||'', followers:c.followers||0, photo_url:c.photo_url, url:c.url||null, following:c.following||0, stocks:c.stocks||0, portfolio:Array.isArray(c.portfolio)?c.portfolio:null, color:'#7361F7', initials:(c.name||c.handle).slice(0,1).toUpperCase()}; });
    const logs = {}; (j.updates||[]).forEach(u=>{ (logs[u.skill_id]=logs[u.skill_id]||[]).push([u.version, (u.created_at||'').slice(0,10), u.note]); });
    D.remote = (j.skills||[]).filter(s=>!have.has(s.id)).map(s=>({ id:s.id, creator:s.creator, name:s.name, emoji:s.emoji||'🧾', icon:s.icon_url||null, cat:s.cat||'Portfolio', pitch:s.pitch||'', highlights:s.highlights||[], requires:s.requires||[], optional:s.optional||[], trades:!!s.trades, price:s.price||{free:true}, cadence:s.cadence||'Monthly', prompts:(s.prompts||[]).length?s.prompts:['Run '+s.name], sample:s.sample||'', shots:s.shots||[], skill:s.skill_md||'', status:'live', downloads:s.downloads||0, rating:+s.rating||0, ratings:s.ratings||0, version:s.version||'1.0.0', updated:(s.updated_at||'').slice(0,10), log:logs[s.id]||[['1.0.0',(s.updated_at||'').slice(0,10),'Initial release']], reviews:[], remote:true }));
    D.loaded = true; route();
  } catch(e) { D.loaded = true; console.warn('catalogue', e.message); }
}
const BROKERS = __BROKERS__;
function brokerStrip(note){ return `<div class="brokers"><div class="bl">${BROKERS.map(([n,b])=>`<img src="data:image/png;base64,${b}" alt="${n}" title="${n}">`).join('')}<span class="more">+ 14 more</span></div><div class="small">${note}</div></div>`; }
const SITE = D.site;
const I = (d)=>`<svg viewBox="0 0 24 24" aria-hidden="true">${d}</svg>`;
const IC = {
  check: I('<path d="M20 6L9 17l-5-5"/>'), chat: I('<path d="M21 12a8 8 0 0 1-8 8H6l-3 3V12a8 8 0 0 1 8-8h2a8 8 0 0 1 8 8z"/>'), sparkle: I('<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.8 2.2L22 20l-2.2.8L19 23l-.8-2.2L16 20l2.2-.8z"/>'),
  plug: I('<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0zM12 18v4"/>'), plus: I('<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>'), gear: I('<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>'),
  file: I('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>'), wrench: I('<path d="M14.7 6.3a4 4 0 0 0 5 5l-9.4 9.4a2.1 2.1 0 0 1-3-3l9.4-9.4z"/><path d="M14.7 6.3L17 4l3 3-2.3 2.3"/>'), lock: I('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'),
  back: I('<path d="M15 18l-6-6 6-6"/>'),
  puzzle: I('<path d="M10 3h4v3a2 2 0 1 0 4 0h3v4h-3a2 2 0 1 0 0 4h3v4h-3a2 2 0 1 0-4 0v3h-4v-3a2 2 0 1 0-4 0H3v-4h3a2 2 0 1 0 0-4H3V6h3a2 2 0 1 0 4 0z"/>'), refresh: I('<path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/>'), x: I('<path d="M18 6L6 18M6 6l12 12"/>'), circle: I('<circle cx="12" cy="12" r="8"/>'),
};
// ---- Backend: Netlify functions in front of Supabase + Stripe Checkout (see netlify/functions/).
const API = '/.netlify/functions/';
async function api(name, opts){ const r = await fetch(API+name, opts); let j; try{ j = await r.json(); }catch(e){ j = {error: await r.text().catch(()=>'')||('HTTP '+r.status)}; } if(!r.ok) throw new Error(j.error || j.errorMessage || ('HTTP '+r.status)); return j; }
const post = (name, body) => api(name, {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
const tokens = () => LS.get('tokens', {});
const emailOk = e => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e||'');
// Small email prompt used by checkout and restore.
function askEmail(title, cta, onGo, hint){
  const m=document.createElement('div'); m.className='modal'; m.innerHTML=`<div class="mbox"><div class="mh"><span style="font-size:18px">✉️</span><b>${esc(title)}</b><button class="x" id="mx">×</button></div><div class="mb">
    <div class="f"><label>Your email</label><input type="email" id="em" placeholder="you@example.com" value="${esc(LS.get('email',''))}" autocomplete="email"><div class="hint">${esc(hint||"Only for your receipt. The download unlocks right here as soon as you’ve paid.")}</div></div>
    <button class="pill pri lg" id="go" style="margin-top:4px">${esc(cta)}</button></div></div>`;
  document.body.appendChild(m); const inp=$('#em',m); inp.focus();
  $('#mx',m).onclick=()=>m.remove(); m.addEventListener('click',e=>{ if(e.target===m) m.remove(); });
  const go=async()=>{ const e=inp.value.trim(); if(!emailOk(e)){ toast('Enter a valid email'); return; } LS.set('email',e); const b=$('#go',m); b.disabled=true; b.textContent='One moment…'; try{ await onGo(e); m.remove(); }catch(err){ b.disabled=false; b.textContent=cta; toast(err.message); } };
  $('#go',m).onclick=go; inp.onkeydown=e=>{ if(e.key==='Enter') go(); };
}
// Download: free skills come from the page, paid ones from the download function with the buyer's token.
async function downloadSkill(s){
  let text;
  if(s.price.free && s.skill && !s.remote){ text=s.skill+'\n'; }
  else if(s.price.free){ const r=await fetch(API+'download?skill='+encodeURIComponent(s.id)); if(!r.ok){ toast(await r.text()); return; } text=await r.text(); }
  else { const t=tokens()[s.id]; if(!t){ toast('Buy the skill or restore access first'); return; }
    const r=await fetch(API+'download?skill='+encodeURIComponent(s.id)+'&token='+encodeURIComponent(t)); if(!r.ok){ toast(await r.text()); return; } text=await r.text(); }
  const blob=new Blob([text],{type:'text/markdown'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='SKILL.md'; a.click();
  const d=LS.get('dl',{}); d[s.id]=(d[s.id]||0)+1; LS.set('dl',d); toast('Downloaded SKILL.md — put it in a folder named '+s.id);
}
function restoreAccess(){
  askEmail('Restore access', 'Find my purchases', async(e)=>{ const j=await post('restore',{email:e}); if(!j.owned.length) throw new Error('No active purchases for '+e); const t=tokens(), o=owned(); j.owned.forEach(x=>{ t[x.skill]=x.token; o[x.skill]=x.plan; }); LS.set('tokens',t); LS.set('owned',o); toast('Restored '+j.owned.length+' skill'+(j.owned.length===1?'':'s')); route(); });
}
const TAKE = 0.20, STRIPE_PCT = 0.029, STRIPE_FIX = 0.30;
const ME = 'maxstocks';
const $ = (s, el=document) => el.querySelector(s);
const esc = s => String(s??'').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmtN = n => n >= 1000 ? (n/1000).toFixed(n>=10000?0:1).replace(/\.0$/,'')+'K' : String(n);
const money = v => '$' + (Number.isInteger(v) ? v : v.toFixed(2));
const ago = d => { const days = Math.floor((new Date() - new Date(d))/86400000); return days<=0?'today':days===1?'1 day ago':days<30?days+' days ago':Math.round(days/30)+' mo ago'; };
const LS = { get:(k,d)=>{try{return JSON.parse(localStorage.getItem('bs_'+k))??d}catch(e){return d}}, set:(k,v)=>{try{localStorage.setItem('bs_'+k,JSON.stringify(v))}catch(e){}} };
let state = { tab:'skills', cat:'All', sort:'top', q:'', dtab:'overview', itab:'claude', plan:null, wiz:null };
const mine = () => LS.get('mine', []);
const allSkills = () => { const r=D.remote||[]; const ids=new Set(r.map(s=>s.id)); return D.skills.concat(r).concat(mine().filter(s=>!ids.has(s.id))); };
const skill = id => allSkills().find(s=>s.id===id);
const mcp = id => D.mcps.find(m=>m.id===id);
const listedMcps = () => D.mcps.filter(m=>!m.compat);   // broker MCPs (compat:true) aren't listed; skills can still say they're compatible with them
const creator = h => D.creators[h];
const owned = () => LS.get('owned', {});

// Page header in the Blossom app style: round back button on the left, title (and a line under it) centred.
function pageHead(title, sub, back){ return `<div class="phead"><a class="pback" href="${back}" aria-label="Back">${IC.back}</a><div class="pt"><b>${title}</b>${sub?`<span>${sub}</span>`:''}</div><span class="pback" style="visibility:hidden"></span></div>`; }
const isReal = s => !!(s.remote || s.mine);   // published through the site, as opposed to the seeded examples
function toast(t){ document.querySelectorAll('.toast').forEach(x=>x.remove()); const el=document.createElement('div'); el.className='toast'; el.textContent=t; document.body.appendChild(el); setTimeout(()=>el.remove(),2200); }
function copy(t, msg='Copied'){ navigator.clipboard?.writeText(t).then(()=>toast(msg),()=>toast(msg)); }
function avatar(h, size=28){
  const c = creator(h); if(!c) return `<span class="ava" style="width:${size}px;height:${size}px;background:#ddd"></span>`;
  if (c.beevis) return `<span class="ava" style="width:${size}px;height:${size}px"><img src="data:image/svg+xml;base64,__BEEVIS__" alt=""></span>`;
  if (c.photo_url) return `<span class="ava" style="width:${size}px;height:${size}px;border:1px solid var(--border);background:#fff"><img src="${esc(c.photo_url)}" alt=""></span>`;
  if (c.photo_b64) return `<span class="ava" style="width:${size}px;height:${size}px;border:1px solid var(--border);background:#fff"><img src="data:image/jpeg;base64,${c.photo_b64}" alt=""></span>`;
  if (c.logo) return `<span class="ava" style="width:${size}px;height:${size}px;background:#fff;border:1px solid var(--border)"><img src="data:image/jpeg;base64,__FLOWER__" alt="" style="width:70%;height:70%"></span>`;
  return `<span class="ava" style="width:${size}px;height:${size}px;background:${c.color};font-size:${Math.round(size*.38)}px">${c.initials}</span>`;
}
const VB = `<img class="vb" src="data:image/svg+xml;base64,__BADGE__" alt="verified">`;
function badge(c){ if(!c) return ''; return ['verified','official','ambassador'].includes(c.badge) ? VB : ''; }   // text tags (Blossom / Ambassador / PRO) dropped — Max, Nov 8
function stars(r){ const full=Math.round(r); return '<span class="star">'+'★'.repeat(full)+'</span><span style="color:#ddd">'+'★'.repeat(5-full)+'</span>'; }
function priceLabel(p){ if(p.free) return {t:'Free',cls:'free'}; if(p.monthly) return {t:money(p.monthly)+'/mo',cls:''}; if(p.yearly) return {t:money(p.yearly)+'/yr',cls:''}; if(p.once) return {t:money(p.once)+' once',cls:''}; return {t:'Free',cls:'free'}; }
function sIcon(s){ return s.icon?`<img src="${s.icon}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">`:s.emoji; }
// MCP icon: a partner logo when one is set, else the emoji. `tile` = the big square on cards/detail; otherwise inline.
function mIcon(m, tile){ if(!m.logo_b64) return m.emoji; return tile ? `<img src="data:image/png;base64,${m.logo_b64}" alt="${esc(m.name)}" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">` : `<img src="data:image/png;base64,${m.logo_b64}" alt="" style="width:1em;height:1em;border-radius:3px;vertical-align:-2px">`; }
const SHORT={'blossom-connector':'Connector','blossom-trade-data':'Trade Data','fiscal-ai':'Fiscal.ai','public-mcp':'Public.com','questrade-mcp':'Questrade','robinhood-mcp':'Robinhood','webull-mcp':'Webull','moomoo-mcp':'moomoo','ibkr-mcp':'IBKR','alpaca-mcp':'Alpaca','schwab-mcp':'Schwab','tradier-mcp':'Tradier'};
function reqChips(s){ const opt=(s.optional||[]).filter(r=>mcp(r)); const shown=opt.slice(0,3), more=opt.length-shown.length;
  return (s.requires||[]).map(r=>{const m=mcp(r); return m?`<span class="chip rq" title="${esc(m.name)}">${mIcon(m)} ${SHORT[r]||esc(m.name)}</span>`:''}).join('')
    + shown.map(r=>{const m=mcp(r); return `<span class="chip rq opt" title="Supported: ${esc(m.name)}">${mIcon(m)} ${SHORT[r]||esc(m.name)} <i>supported</i></span>`}).join('')
    + (more>0?`<span class="chip rq opt" title="${esc(opt.slice(3).map(r=>mcp(r).name).join(', '))}">+${more} more</span>`:''); }

// tiny markdown: bold, inline code, tables, code blocks, lists, links
function md(src){
  const lines = src.split('\n'); let out=[], i=0;
  const inl = t => esc(t).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/\*(.+?)\*/g,'<i>$1</i>').replace(/`(.+?)`/g,'<code>$1</code>').replace(/\[(.+?)\]\((.+?)\)/g,'<a href="$2">$1</a>').replace(/\[(.+?)\]/g,'<a href="#">$1</a>');
  while(i<lines.length){
    const l=lines[i];
    if(l.startsWith('```')){ let j=i+1, buf=[]; while(j<lines.length && !lines[j].startsWith('```')){buf.push(lines[j]);j++;} out.push('<pre>'+esc(buf.join('\n'))+'</pre>'); i=j+1; continue; }
    if(/^#{1,4} /.test(l)){ const n=l.match(/^#+/)[0].length; out.push(`<h${n+1}>`+inl(l.replace(/^#+ /,''))+`</h${n+1}>`); i++; continue; }
    if(l.startsWith('|')){ let rows=[]; while(i<lines.length && lines[i].startsWith('|')){ rows.push(lines[i]); i++; } rows=rows.filter(r=>!/^\|\s*-/.test(r)); const cells=r=>r.split('|').slice(1,-1).map(c=>c.trim());
      // Cells get the same treatment Claude's own chat output gets: numbers right-aligned, gains green / losses red, verdict words as chips.
      const td=c=>{ const t=c.replace(/\*\*/g,''); const num=/^[~≈]?[+\-−$]?\$?\d[\d,.]*%?$|^[+\-−]\d/.test(t)||/^\d+(\.\d+)?%$/.test(t)||t==='n/a'||t==='—'; const cls=/^[+]\d|^\+/.test(t)?' up':/^[\-−]\d/.test(t)?' down':''; const v=/^(healthy|strong|good|pass|ok|buy|hold|keep)\b/i.test(t)?'ok':/^(watch|caution|monitor|neutral|too young|new)\b/i.test(t)?'warn':/^(eroding|weak|bad|fail|avoid|sell|cut|risk)\b/i.test(t)?'bad':''; return `<td class="${num?'num':''}${cls}">`+(v?`<span class="verdict ${v}">${inl(c)}</span>`:inl(c))+'</td>'; };
      out.push('<table><tr>'+cells(rows[0]).map(c=>'<th>'+inl(c)+'</th>').join('')+'</tr>'+rows.slice(1).map(r=>'<tr>'+cells(r).map(td).join('')+'</tr>').join('')+'</table>'); continue; }
    if(/^\d+\. /.test(l)){ let items=[]; while(i<lines.length && /^\d+\. /.test(lines[i])){ items.push(lines[i].replace(/^\d+\. /,'')); i++; } out.push('<ol>'+items.map(x=>'<li>'+inl(x)+'</li>').join('')+'</ol>'); continue; }
    if(/^[-•] /.test(l)){ let items=[]; while(i<lines.length && /^[-•] /.test(lines[i])){ items.push(lines[i].slice(2)); i++; } out.push('<ul>'+items.map(x=>'<li>'+inl(x)+'</li>').join('')+'</ul>'); continue; }
    if(l.trim()===''){ i++; continue; }
    out.push('<p>'+inl(l)+'</p>'); i++;
  }
  return out.join('');
}

