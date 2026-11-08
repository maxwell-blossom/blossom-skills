// ---------- checkout (Stripe Checkout via /.netlify/functions/checkout; prices come from the database)
function checkout(s, plan){
  askEmail('Checkout · '+s.name, (plan==='once'?'Buy for ':'Subscribe · ')+money(s.price[plan])+(plan==='monthly'?'/mo':plan==='yearly'?'/yr':''), async(email)=>{
    const j=await post('checkout',{skill:s.id, plan, email}); if(!j.url) throw new Error('No checkout URL returned'); location.href=j.url; await new Promise(()=>{}); });
}
function success(id, plan){
  const s=skill(id); if(!s) return library();
  return `<div class="wrap" style="max-width:720px"><div class="card success"><div class="big">🎉</div><h1>You’re in. ${esc(s.name)} is yours.</h1><p class="small">${plan==='once'?'One-time purchase':'Subscribed · '+plan} · receipt sent by Stripe${tokens()[s.id]?'':' · confirming your payment…'}</p>
    <button class="pill pri lg" id="get" style="max-width:360px;margin:16px auto 0">Download SKILL.md</button>
    <div style="text-align:left;margin-top:26px"><h3 style="font-size:15px;margin-bottom:8px">Install it</h3>${installBlock(s)}</div>
    <div style="margin-top:22px"><a href="#/skill/${s.id}">Back to the skill</a> · <a href="#/">Browse more</a></div></div></div>`;
}

