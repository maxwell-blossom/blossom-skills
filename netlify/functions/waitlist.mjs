// POST {email, identity, mcp} — waitlist for the Blossom MCPs (Connector, Aggregate Trade Data) while they're "coming soon".
import { db, json, bad, identity } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const b = await req.json().catch(() => ({}));
  const mcp = String(b.mcp || '').replace(/[^a-z0-9-]/g, '').slice(0, 64) || 'unknown';
  const me = identity(b.identity);
  // {check:true}: is the signed-in person already on this list (by account, or by the email on their account)? The page uses it to show "On the waitlist" instead of the join button.
  if (b.check) {
    if (!me) return json({ on: false });
    const em = String(me.email || '').trim().toLowerCase();
    let q = db().from('waitlist').select('email').eq('mcp', mcp);
    q = em ? q.or(`user_id.eq.${me.userId},email.eq.${em}`) : q.eq('user_id', me.userId);
    const { data, error } = await q.limit(1);
    if (error) return bad(error.message, 500);
    return json({ on: !!(data && data.length) });
  }
  const email = String(b.email || '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return bad('A valid email is required');
  const { error } = await db().from('waitlist').upsert({ email, user_id: me?.userId ?? null, mcp }, { onConflict: 'email,mcp', ignoreDuplicates: true });
  if (error) return bad(error.message, 500);
  return json({ ok: true, on: true });
};
