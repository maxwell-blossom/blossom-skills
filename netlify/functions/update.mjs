// POST {skill, user_id, version, note, skill_md?} → appends to the update log (and replaces the SKILL.md when provided).
import { db, json, bad, userId } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { skill, user_id, version, note, skill_md } = await req.json().catch(() => ({}));
  const owner = userId(user_id);
  if (!skill || !owner || !version || !note) return bad('skill, user_id, version and note are required');
  const sb = db();
  const { data: s } = await sb.from('skills').select('id,creator').eq('id', skill).single();
  const { data: c } = s ? await sb.from('creators').select('user_id').eq('handle', s.creator).maybeSingle() : { data: null };
  if (!c?.user_id || c.user_id !== owner) return bad('Not your skill', 403);
  const patch = { version, updated_at: new Date().toISOString() }; if (skill_md) patch.skill_md = skill_md;
  await sb.from('skills').update(patch).eq('id', skill);
  await sb.from('skill_updates').insert({ skill_id: skill, version, note });
  return json({ ok: true });
};
