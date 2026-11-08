// POST /.netlify/functions/seed — loads the catalogue from data.py (via gen_seed.py → seed-data.json) into Supabase.
// Runs only while the skills table is empty, unless ADMIN_KEY is set in Netlify and sent as the x-admin-key header.
// Upserts on primary keys, so re-running with the key refreshes catalogue rows without touching purchases.
import { db, json, bad } from './_lib.mjs';
import seed from './seed-data.json';

export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const sb = db();
  const { count, error: cErr } = await sb.from('skills').select('id', { count: 'exact', head: true });
  if (cErr) return bad('DB error: ' + cErr.message, 500);
  const key = process.env.ADMIN_KEY;
  const authed = key && req.headers.get('x-admin-key') === key;
  if (count > 0 && !authed) return bad('Catalogue already seeded (' + count + ' skills). Set ADMIN_KEY in Netlify and send x-admin-key to re-seed.', 409);

  const r1 = await sb.from('creators').upsert(seed.creators, { onConflict: 'handle' });
  if (r1.error) return bad('creators: ' + r1.error.message, 500);
  const r2 = await sb.from('skills').upsert(seed.skills, { onConflict: 'id' });
  if (r2.error) return bad('skills: ' + r2.error.message, 500);

  // skill_updates has no unique (skill_id, version) key; insert only the ones missing.
  const { data: existing, error: eErr } = await sb.from('skill_updates').select('skill_id,version');
  if (eErr) return bad('skill_updates: ' + eErr.message, 500);
  const have = new Set((existing || []).map((u) => u.skill_id + '@' + u.version));
  const missing = seed.skill_updates.filter((u) => !have.has(u.skill_id + '@' + u.version));
  if (missing.length) {
    const r3 = await sb.from('skill_updates').insert(missing);
    if (r3.error) return bad('skill_updates insert: ' + r3.error.message, 500);
  }
  return json({ ok: true, creators: seed.creators.length, skills: seed.skills.length, updates_added: missing.length });
};
