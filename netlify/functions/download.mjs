// GET ?skill=<id>&token=<t> → SKILL.md for a paid skill (free skills are served statically from /skills/<id>/SKILL.md).
import { db, verify } from './_lib.mjs';
export default async (req) => {
  const u = new URL(req.url); const id = u.searchParams.get('skill'); const token = u.searchParams.get('token') || '';
  const sb = db();
  const { data: s } = await sb.from('skills').select('id,price,skill_md,status').eq('id', id).single();
  if (!s || s.status === 'removed') return new Response('Not found', { status: 404 });
  if (!s.price?.free) {
    const v = verify(token);
    if (!v || v.skill !== id) return new Response('This skill needs a purchase. Open it on Blossom Skills to buy or restore access.', { status: 403 });
    const { data: p } = await sb.from('purchases').select('status').eq('skill_id', id).eq('buyer_email', v.email).in('status', ['active']).limit(1);
    if (!p?.length) return new Response('Your subscription is not active. Renew it on Blossom Skills.', { status: 403 });
    await sb.from('downloads').insert({ skill_id: id, buyer_email: v.email });
  } else {
    await sb.from('downloads').insert({ skill_id: id });
  }
  return new Response(s.skill_md + '\n', { headers: { 'content-type': 'text/markdown; charset=utf-8', 'content-disposition': 'attachment; filename="SKILL.md"', 'cache-control': 'no-store' } });
};
