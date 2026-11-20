// POST {identity} → the signed-in Blossom user's active purchases, with fresh download tokens.
import { db, json, bad, sign, identity } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { identity: token } = await req.json().catch(() => ({}));
  const me = identity(token);
  if (!me) return bad('Sign in to Blossom to restore purchases', 401);
  const buyer = me.userId;
  const { data } = await db().from('purchases').select('skill_id,plan,status,buyer_email').eq('buyer_user_id', buyer).eq('status', 'active');
  return json({ owned: (data || []).map(p => ({ skill: p.skill_id, plan: p.plan, token: sign(p.skill_id, p.buyer_email) })) });
};
