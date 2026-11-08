// GET /.netlify/functions/catalogue → live skills + creators + update log. Paid skills get a SKILL.md preview, never the full file.
import { db, json } from './_lib.mjs';
const preview = (md) => { const [head, , rest] = splitFront(md); const lines = (rest || '').trim().split('\n'); return head + '\n---\n' + lines.slice(0, 8).join('\n') + '\n\n… the full SKILL.md (' + md.split('\n').length + ' lines) unlocks after purchase.'; };
function splitFront(md) { const i = md.indexOf('\n---\n'); return i < 0 ? [md, '', ''] : [md.slice(0, i), '', md.slice(i + 5)]; }
export default async () => {
  const sb = db();
  const [{ data: skills, error: e1 }, { data: creators, error: e2 }, { data: updates, error: e3 }] = await Promise.all([
    sb.from('skills').select('id,creator,name,emoji,icon_url,cat,pitch,highlights,requires,optional,trades,price,cadence,prompts,sample,shots,skill_md,status,downloads,rating,ratings,version,updated_at').eq('status', 'live').order('downloads', { ascending: false }),
    sb.from('creators').select('handle,name,badge,bio,followers,photo_url,url'),
    sb.from('skill_updates').select('skill_id,version,note,created_at').order('created_at', { ascending: false }),
  ]);
  if (e1 || e2 || e3) return json({ error: (e1 || e2 || e3).message }, 500);
  for (const s of skills) { if (!s.price?.free) s.skill_md = preview(s.skill_md || ''); }
  return json({ skills, creators, updates }, 200, { 'cache-control': 'no-store' });
};
