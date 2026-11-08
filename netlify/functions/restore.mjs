// POST {email} → emails nothing yet (V1): returns the list of skills this email has active purchases for, with fresh tokens.
// Real version: send a magic link instead of returning tokens to whoever types the email.
import { db, json, bad, sign } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { email } = await req.json().catch(() => ({}));
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email || '')) return bad('valid email required');
  const { data } = await db().from('purchases').select('skill_id,plan,status').eq('buyer_email', email.toLowerCase()).eq('status', 'active');
  return json({ owned: (data || []).map(p => ({ skill: p.skill_id, plan: p.plan, token: sign(p.skill_id, email) })) });
};
