// POST {skill, creator, version, note, skill_md?} → appends to the update log (and replaces the SKILL.md when provided).
import { db, json, bad } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { skill, creator, version, note, skill_md } = await req.json().catch(() => ({}));
  if (!skill || !creator || !version || !note) return bad('skill, creator, version and note are required');
  const sb = db();
  const { data: s } = await sb.from('skills').select('id,creator').eq('id', skill).single();
  if (!s || s.creator !== creator) return bad('Not your skill', 403);
  const patch = { version, updated_at: new Date().toISOString() }; if (skill_md) patch.skill_md = skill_md;
  await sb.from('skills').update(patch).eq('id', skill);
  await sb.from('skill_updates').insert({ skill_id: skill, version, note });
  return json({ ok: true });
};
