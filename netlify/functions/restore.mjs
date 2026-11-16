// POST {user_id} → the Blossom user's active purchases, with fresh download tokens (V1: the user id is not verified).
import { db, json, bad, sign, userId } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { user_id } = await req.json().catch(() => ({}));
  const buyer = userId(user_id);
  if (!buyer) return bad('user_id required');
  const { data } = await db().from('purchases').select('skill_id,plan,status,buyer_email').eq('buyer_user_id', buyer).eq('status', 'active');
  return json({ owned: (data || []).map(p => ({ skill: p.skill_id, plan: p.plan, token: sign(p.skill_id, p.buyer_email) })) });
};
