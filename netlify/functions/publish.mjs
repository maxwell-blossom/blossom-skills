// POST {identity, creator:{name,url,email,payout_method,payout_email}, skill:{…}} → creates the creator if needed and the skill, live immediately (no review queue for now — Max, Nov 8).
import { db, json, bad, identity } from './_lib.mjs';
const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 48);
const handleSlug = (s) => s.toLowerCase().replace(/^@/, '').replace(/[^a-z0-9._-]/g, '').slice(0, 32);   // Blossom handles keep dots and underscores (anthony.invests, tfsa_tina)
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const body = await req.json().catch(() => ({}));
  const c = body.creator || {}, k = body.skill || {};
  const me = identity(body.identity);
  if (!me) return bad('Sign in to Blossom to publish', 401);
  const owner = me.userId;
  if (!k.name || !k.skill_md) return bad('skill.name and skill.skill_md are required');
  if (/sk_live|sk_test|api[_-]?key\s*[:=]\s*\S{12,}|ghp_[A-Za-z0-9]{20,}/i.test(k.skill_md)) return bad('The SKILL.md looks like it contains a secret. Remove it and try again.');
  const sb = db();
  // The signed-in account's handle, never one the page names: an unclaimed handle would go to whoever posts first.
  const handle = handleSlug(me.username || '');
  if (!handle) return bad('Your Blossom account has no handle', 403);
  // A handle already claimed by another Blossom user stays theirs.
  const { data: existing } = await sb.from('creators').select('user_id').eq('handle', handle).maybeSingle();
  if (existing?.user_id && existing.user_id !== owner) return bad('That handle belongs to another Blossom account', 403);
  const row = { handle, user_id: owner, name: c.name || handle };
  if (typeof c.url === 'string' && /^https:\/\/(www\.)?blossomsocial\.com\/\S+$/.test(c.url.trim())) row.url = c.url.trim().slice(0, 200);
  if (c.email) row.email = c.email;
  if (c.payout_method && c.payout_email) { row.payout_method = c.payout_method; row.payout_email = c.payout_email; }
  await sb.from('creators').upsert(row, { onConflict: 'handle', ignoreDuplicates: false });
  let id = slug(k.name) || 'skill';
  const { data: clash } = await sb.from('skills').select('id').eq('id', id).maybeSingle();
  if (clash) id = `${id}-${Math.random().toString(36).slice(2, 6)}`;
  const price = k.price && typeof k.price === 'object' ? k.price : { free: true };
  // Screenshots and icon arrive as data URIs from the wizard. Keep them bounded: ≤4 shots, JPEG/PNG only, ≤400KB each; icon ≤60KB.
  const isImg = (d) => typeof d === 'string' && /^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+$/.test(d);
  const shots = (Array.isArray(k.shots) ? k.shots : []).slice(0, 4).map(x => Array.isArray(x) ? x : [x, '']).filter(([d]) => isImg(d) && d.length <= 400 * 1024 * 1.4).map(([d, cap]) => [d, String(cap || '').slice(0, 120)]);
  const icon_url = isImg(k.icon_url) && k.icon_url.length <= 60 * 1024 * 1.4 ? k.icon_url : null;
  const highlights = (Array.isArray(k.highlights) ? k.highlights : []).map(h => String(h || '').trim().slice(0, 110)).filter(Boolean).slice(0, 3);
  const { error } = await sb.from('skills').insert({
    id, creator: handle, name: k.name, emoji: k.emoji || '🧾', icon_url, cat: k.cat || 'Portfolio', pitch: k.pitch || '',
    highlights, requires: k.requires || [], optional: k.optional || [], trades: !!k.trades, price, cadence: k.cadence || 'Monthly',
    prompts: k.prompts || [], sample: k.sample || '', shots, skill_md: k.skill_md, status: 'live', version: '1.0.0',
  });
  if (error) return bad(error.message, 500);
  await sb.from('skill_updates').insert({ skill_id: id, version: '1.0.0', note: k.first || 'Initial release' });
  return json({ id, status: 'live' });
};
