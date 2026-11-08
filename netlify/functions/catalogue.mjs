// GET /.netlify/functions/catalogue → live skills + creators (never the SKILL.md of paid skills)
import { db, json } from './_lib.mjs';
export default async () => {
  const sb = db();
  const [{ data: skills, error: e1 }, { data: creators, error: e2 }] = await Promise.all([
    sb.from('skills').select('id,creator,name,emoji,icon_url,cat,pitch,highlights,requires,optional,trades,price,cadence,prompts,sample,shots,status,downloads,rating,ratings,version,updated_at').eq('status', 'live').order('downloads', { ascending: false }),
    sb.from('creators').select('handle,name,badge,bio,followers,photo_url'),
  ]);
  if (e1 || e2) return json({ error: (e1 || e2).message }, 500);
  return json({ skills, creators }, 200, { 'cache-control': 'public, max-age=60' });
};
