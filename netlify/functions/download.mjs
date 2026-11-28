// GET ?skill=<id>&token=<t>[&identity=<jwt>] → SKILL.md for a paid skill (free skills are served statically from /skills/<id>/SKILL.md).
// The download count is distinct people, not hits: a buyer counts once per email, a signed-in Blossom user once per account,
// anyone else once per device (a salted hash of IP + browser, never stored raw). The creator's own downloads don't count.
import { createHash } from 'node:crypto';
import { db, verify, identity } from './_lib.mjs';
export default async (req, context) => {
  const u = new URL(req.url); const id = u.searchParams.get('skill'); const token = u.searchParams.get('token') || '';
  const me = identity(u.searchParams.get('identity') || '');
  const sb = db();
  const { data: s } = await sb.from('skills').select('id,creator,price,skill_md,status').eq('id', id).single();
  if (!s || s.status === 'removed') return new Response('Not found', { status: 404 });
  const ip = context?.ip || req.headers.get('x-nf-client-connection-ip') || (req.headers.get('x-forwarded-for') || '').split(',')[0].trim();
  const device = 'd:' + createHash('sha256').update(`${ip}|${req.headers.get('user-agent') || ''}|${process.env.SKILLS_IDENTITY_SECRET || ''}`).digest('base64url').slice(0, 24);
  let row;
  if (!s.price?.free) {
    const v = verify(token);
    if (!v || v.skill !== id) return new Response('This skill needs a purchase. Open it on Blossom Skills to buy or restore access.', { status: 403 });
    const { data: p } = await sb.from('purchases').select('status').eq('skill_id', id).eq('buyer_email', v.email).in('status', ['active']).limit(1);
    if (!p?.length) return new Response('Your subscription is not active. Renew it on Blossom Skills.', { status: 403 });
    row = { skill_id: id, buyer_email: v.email, viewer: 'e:' + v.email.toLowerCase() };
  } else {
    row = { skill_id: id, viewer: me ? 'u:' + me.userId : device };
  }
  const { data: c } = await sb.from('creators').select('user_id').eq('handle', s.creator).maybeSingle();
  const own = !!(me && c?.user_id && me.userId === c.user_id);
  if (!own) await sb.from('downloads').insert(row);
  // The listing shows skills.downloads: distinct viewers in the log (download_count(), from the Nov 28 migration).
  const { data: n } = await sb.rpc('download_count', { sid: id });
  if (typeof n === 'number') await sb.from('skills').update({ downloads: n }).eq('id', id);
  return new Response(s.skill_md + '\n', { headers: { 'content-type': 'text/markdown; charset=utf-8', 'content-disposition': 'attachment; filename="SKILL.md"', 'cache-control': 'no-store', ...(typeof n === 'number' ? { 'x-downloads': String(n) } : {}) } });
};
