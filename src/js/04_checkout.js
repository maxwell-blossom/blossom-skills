// ---------- checkout (Stripe Checkout via /.netlify/functions/checkout; prices come from the database)
function checkout(s, plan){
  askEmail('Checkout · '+s.name, (plan==='once'?'Buy for ':'Subscribe · ')+money(s.price[plan])+(plan==='monthly'?'/mo':plan==='yearly'?'/yr':''), async(email)=>{
    const j=await post('checkout',{skill:s.id, plan, email}); if(!j.url) throw new Error('No checkout URL returned'); location.href=j.url; await new Promise(()=>{}); });
}
function success(id, plan){
  const s=skill(id); if(!s) return library();
  return `<div class="wrap" style="max-width:720px"><div class="card success"><div class="big">🎉</div><h1>You’re in. ${esc(s.name)} is yours.</h1><p class="small">${plan==='once'?'One-time purchase':'Subscribed · '+plan} · receipt on its way to ${esc(LS.get('email','your email'))}${tokens()[s.id]?'':' · confirming your payment…'}</p>
    <button class="pill pri lg" id="get" style="max-width:360px;margin:16px auto 0">Download SKILL.md</button>
    <div style="text-align:left;margin-top:26px"><h3 style="font-size:15px;margin-bottom:8px">Install it</h3>${installBlock(s)}</div>
    <div style="margin-top:22px"><a href="/skill/${s.id}">Back to the skill</a> · <a href="/">Browse more</a></div></div></div>`;
}


// Confetti burst on the success page (canvas, no library). Fires once per purchase.
function confetti(key){
  if(window.__confetti===key) return; window.__confetti=key;
  const c=document.createElement('canvas'); c.className='confetti'; c.width=innerWidth; c.height=innerHeight; document.body.appendChild(c);
  const x=c.getContext('2d'); const COL=['#7361F7','#35C7B2','#FF7733','#F6C000','#E70037','#4D35EB'];
  const P=Array.from({length:160},()=>({x:innerWidth/2+(Math.random()-.5)*160, y:innerHeight*0.35, vx:(Math.random()-.5)*14, vy:-Math.random()*14-4, r:4+Math.random()*5, c:COL[Math.random()*COL.length|0], a:Math.random()*Math.PI, s:(Math.random()-.5)*.3, t:Math.random()<.5}));
  const t0=performance.now();
  (function f(now){ const dt=(now-t0)/1000; x.clearRect(0,0,c.width,c.height);
    P.forEach(p=>{ p.vy+=0.35; p.vx*=0.99; p.x+=p.vx; p.y+=p.vy; p.a+=p.s; x.save(); x.translate(p.x,p.y); x.rotate(p.a); x.fillStyle=p.c; x.globalAlpha=Math.max(0,1-Math.max(0,dt-1.8)/1.2); if(p.t) x.fillRect(-p.r/2,-p.r/4,p.r,p.r/2); else { x.beginPath(); x.arc(0,0,p.r/2,0,7); x.fill(); } x.restore(); });
    if(dt<3.2) requestAnimationFrame(f); else c.remove(); })(t0);
}
