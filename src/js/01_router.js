// ---------- router
function route(){
  state.itab='claude'; document.querySelectorAll('.modal,.lb').forEach(m=>m.remove());
  if(/^#\//.test(location.hash)){ history.replaceState(null,'', BASE + location.hash.slice(1)); }   // old #/… links still work
  const path = location.pathname.startsWith(BASE) ? location.pathname.slice(BASE.length) : location.pathname;
  const h = '#' + (path === '' || path === '/' ? '/' : path.replace(/\/$/, ''));
  const q = new URLSearchParams(location.search);
  if(q.get('checkout')==='success'){ const id=q.get('skill'), plan=q.get('plan')||'monthly', sid=q.get('session_id'); history.replaceState(null,'', BASE + '/success/'+id+'/'+plan);
    if(sid && !tokens()[id]) api('unlock?session_id='+encodeURIComponent(sid)).then(j=>{ const t=tokens(); t[id]=j.token; LS.set('tokens',t); if(j.email) LS.set('email',j.email); const o=owned(); o[id]=j.plan||plan; LS.set('owned',o); route(); }).catch(e=>toast('Could not confirm the payment: '+e.message));
    return route(); }
  const parts = h.slice(2).split('/');
  document.body.classList.toggle('on-learn', parts[0]==='learn');
  window.scrollTo(0,0);
  const app = $('#app');
  if(parts[0]==='' ){ state.tab='skills'; app.innerHTML=library(); bindLibrary(); }
  else if(parts[0]==='terms'){ app.innerHTML=terms(); }
  else if(parts[0]==='examples'){ state.tab='examples'; app.innerHTML=library(); bindLibrary(); }
  else if(parts[0]==='mcps'){ state.tab='mcps'; app.innerHTML=library(); bindLibrary(); }
  else if(parts[0]==='learn'){ state.tab='learn'; app.innerHTML=library(); bindLibrary(); }
  else if(parts[0]==='skill'){ app.innerHTML=detail(parts[1]); bindDetail(parts[1]); }
  else if(parts[0]==='mcp'){ app.innerHTML=mcpDetail(parts[1]); bindMcp(parts[1]); }
  else if(parts[0]==='u'){ app.innerHTML=creatorPage(parts[1]); bindLibrary(); }
  else if(parts[0]==='post'){ if(!state.wiz) state.wiz=newWiz(); app.innerHTML=wizard(); bindWizard(); }
  else if(parts[0]==='manage'){ app.innerHTML=manage(parts[1]); bindManage(parts[1]); }
  else if(parts[0]==='success'){ app.innerHTML=success(parts[1], parts[2]); bindDetail(parts[1]); }
  else { app.innerHTML=library(); bindLibrary(); }
}
window.addEventListener('popstate', route);
document.addEventListener('click', e => { const b = e.target.closest('a.pback'); if(!b) return; e.preventDefault(); if(window.__navd && history.length > 1) history.back(); else go(b.getAttribute('href')); });
// Same-origin links navigate in-app (no reload); new-tab/modified clicks and external links are left alone.
document.addEventListener('click', e => { const a = e.target.closest('a[href]'); if(!a || a.target || a.hasAttribute('download') || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return; const u = new URL(a.href, location.href); if(u.origin !== location.origin || !u.pathname.startsWith(BASE + '/')) return; if(a.getAttribute('href') === '#') { e.preventDefault(); return; } e.preventDefault(); go(u.pathname.slice(BASE.length) + u.search); });

