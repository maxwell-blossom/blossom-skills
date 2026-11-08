// POST {creator:{handle,name,email,payout_method,payout_email}, skill:{…}} → creates the creator if needed and the skill, live immediately (no review queue for now — Max, Nov 8).
import { db, json, bad } from './_lib.mjs';
const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 48);
const handleSlug = (s) => s.toLowerCase().replace(/^@/, '').replace(/[^a-z0-9._-]/g, '').slice(0, 32);   // Blossom handles keep dots and underscores (anthony.invests, tfsa_tina)
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const body = await req.json().catch(() => ({}));
  const c = body.creator || {}, k = body.skill || {};
  if (!c.handle || !k.name || !k.skill_md) return bad('creator.handle, skill.name and skill.skill_md are required');
  if (/sk_live|sk_test|api[_-]?key\s*[:=]\s*\S{12,}|ghp_[A-Za-z0-9]{20,}/i.test(k.skill_md)) return bad('The SKILL.md looks like it contains a secret. Remove it and try again.');
  const sb = db();
  const handle = handleSlug(c.handle);
  if (!handle) return bad('A Blossom handle is required');
  const row = { handle, name: c.name || c.handle };
  if (typeof c.url === 'string' && /^https:\/\/(www\.)?blossomsocial\.com\/\S+$/.test(c.url.trim())) row.url = c.url.trim().slice(0, 200);
  if (c.email) row.email = c.email;
  if (c.payout_method && c.payout_email) { row.payout_method = c.payout_method; row.payout_email = c.payout_email; }
  await sb.from('creators').upsert(row, { onConflict: 'handle', ignoreDuplicates: false });
  let id = slug(k.name) || 'skill';
  const { data: clash } = await sb.from('skills').select('id').eq('id', id).maybeSingle();
  if (clash) id = `${id}-${Math.random().toString(36).slice(2, 6)}`;
  const price = k.price && typeof k.price === 'object' ? k.price : { free: true };
  const { error } = await sb.from('skills').insert({
    id, creator: handle, name: k.name, emoji: k.emoji || '🧾', icon_url: k.icon_url || null, cat: k.cat || 'Portfolio', pitch: k.pitch || '',
    highlights: k.highlights || [], requires: k.requires || [], optional: k.optional || [], trades: !!k.trades, price, cadence: k.cadence || 'Monthly',
    prompts: k.prompts || [], sample: k.sample || '', shots: k.shots || [], skill_md: k.skill_md, status: 'live', version: '1.0.0',
  });
  if (error) return bad(error.message, 500);
  await sb.from('skill_updates').insert({ skill_id: id, version: '1.0.0', note: k.first || 'Initial release' });
  return json({ id, status: 'live' });
};
