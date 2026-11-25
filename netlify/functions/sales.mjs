// POST {identity, skill?} → sales for the signed-in creator's skills (all of them, or one): every purchase row, plus totals.
// Creator share = 80% of what buyers paid; Blossom's 20% covers card processing, refunds and payouts (creator terms, §4).
import { db, json, bad, identity, TAKE } from './_lib.mjs';
const mask = (e) => String(e || '').replace(/^(.).*(@.*)$/, '$1…$2');
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { identity: token, skill } = await req.json().catch(() => ({}));
  const me = identity(token);
  if (!me) return bad('Sign in to Blossom first', 401);
  const sb = db();
  const { data: cs } = await sb.from('creators').select('handle,payout_method,payout_email').eq('user_id', me.userId);
  const payout = cs?.[0]?.payout_email ? { method: cs[0].payout_method, email: cs[0].payout_email } : null;   // the creator's own details, for the manage page only
  const handles = (cs || []).map(c => c.handle);
  if (!handles.length) return json({ skills: [], sales: [], totals: { sales: 0, gross_cents: 0, creator_cents: 0, active_subs: 0 } });
  let q = sb.from('skills').select('id,name,price').in('creator', handles);
  if (skill) q = q.eq('id', skill);
  const { data: skills } = await q;
  const ids = (skills || []).map(s => s.id);
  if (!ids.length) return skill ? bad('Not your skill', 403) : json({ skills: [], sales: [], totals: { sales: 0, gross_cents: 0, creator_cents: 0, active_subs: 0 } });
  const { data: rows } = await sb.from('purchases').select('skill_id,plan,amount_cents,currency,status,buyer_email,created_at,current_period_end').in('skill_id', ids).order('created_at', { ascending: false });
  const sales = (rows || []).map(r => ({ skill: r.skill_id, plan: r.plan, cents: r.amount_cents || 0, currency: r.currency || 'cad', status: r.status, buyer: mask(r.buyer_email), at: r.created_at, until: r.current_period_end }));
  const paid = sales.filter(s => s.status !== 'refunded');
  const gross = paid.reduce((a, s) => a + s.cents, 0);
  const totals = { sales: paid.length, gross_cents: gross, creator_cents: Math.round(gross * (1 - TAKE)), active_subs: sales.filter(s => s.status === 'active' && s.plan !== 'once').length };
  const per = {}; for (const s of sales) { const p = per[s.skill] = per[s.skill] || { sales: 0, gross_cents: 0, active_subs: 0 }; if (s.status !== 'refunded') { p.sales++; p.gross_cents += s.cents; } if (s.status === 'active' && s.plan !== 'once') p.active_subs++; }
  return json({ skills: (skills || []).map(s => ({ id: s.id, name: s.name, ...(per[s.id] || { sales: 0, gross_cents: 0, active_subs: 0 }) })), sales, totals, payout });
};
