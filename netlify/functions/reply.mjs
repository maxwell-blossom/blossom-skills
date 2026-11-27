// POST {identity, skill, handle, body} → the creator's reply to one review (empty body removes it). Only the skill's creator can reply.
import { db, json, bad, identity } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { identity: token, skill, handle, body } = await req.json().catch(() => ({}));
  const me = identity(token);
  if (!me) return bad('Sign in to Blossom to reply', 401);
  if (!skill || !handle) return bad('skill and handle are required');
  const text = String(body || '').trim().slice(0, 1000);
  const sb = db();
  const { data: s } = await sb.from('skills').select('id,creator').eq('id', skill).single();
  const { data: c } = s ? await sb.from('creators').select('user_id').eq('handle', s.creator).maybeSingle() : { data: null };
  if (!c?.user_id || c.user_id !== me.userId) return bad('Only the creator can reply to reviews of this skill', 403);
  const patch = text ? { reply: text, replied_at: new Date().toISOString() } : { reply: null, replied_at: null };
  const { data, error } = await sb.from('reviews').update(patch).eq('skill_id', skill).eq('handle', handle).select('user_id');
  if (error) return bad(/column .* does not exist/i.test(error.message) ? 'Replies aren’t switched on yet (run the review_replies migration)' : error.message, 500);
  if (!data?.length) return bad('That review isn’t there any more', 404);
  return json({ ok: true, reply: text, replied_at: patch.replied_at });
};
