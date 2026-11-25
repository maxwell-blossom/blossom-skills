// POST {identity, skill, stars, body} → saves the signed-in user's rating of a skill (one per person; posting again replaces it).
// Paid skills: only people with a purchase row can rate. Free skills: anyone signed in. Creators can't rate their own.
// Recomputes skills.rating / skills.ratings from the reviews table so the catalogue stays consistent.
import { db, json, bad, identity } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { identity: token, skill, stars, body } = await req.json().catch(() => ({}));
  const me = identity(token);
  if (!me) return bad('Sign in to Blossom to rate', 401);
  const n = Math.round(Number(stars));
  if (!skill || !(n >= 1 && n <= 5)) return bad('skill and stars (1–5) are required');
  const text = String(body || '').trim().slice(0, 1000);
  const sb = db();
  const { data: s } = await sb.from('skills').select('id,price,status,creator').eq('id', skill).single();
  if (!s || s.status !== 'live') return bad('Unknown skill', 404);
  const { data: c } = await sb.from('creators').select('user_id').eq('handle', s.creator).maybeSingle();
  if (c?.user_id && c.user_id === me.userId) return bad('You can’t rate your own skill', 403);
  if (!s.price?.free) {
    const { data: p } = await sb.from('purchases').select('id').eq('skill_id', skill).eq('buyer_user_id', me.userId).in('status', ['active', 'canceled']).limit(1);
    if (!p?.length) return bad('Only people who bought this skill can rate it', 403);
  }
  const row = { skill_id: skill, user_id: me.userId, handle: me.username || null, stars: n, body: text, updated_at: new Date().toISOString() };
  const { error } = await sb.from('reviews').upsert(row, { onConflict: 'skill_id,user_id' });
  if (error) return bad(/relation .* does not exist/i.test(error.message) ? 'Ratings aren’t switched on yet (reviews table missing)' : error.message, 500);
  const { data: all } = await sb.from('reviews').select('stars').eq('skill_id', skill);
  const ratings = (all || []).length, rating = ratings ? +((all.reduce((a, r) => a + r.stars, 0) / ratings).toFixed(2)) : 0;
  await sb.from('skills').update({ rating, ratings }).eq('id', skill);
  return json({ ok: true, rating, ratings });
};
