// POST {skill, identity, version?, note?, skill_md?, price?, payout?} → the creator's edits to their own skill.
//   version + note       append to the update log (and replace the SKILL.md when skill_md is sent)
//   price                {free:true} | {once} | {monthly, yearly?} — applies to new buyers only (existing subscriptions keep their Stripe price)
//   payout               {method:'etransfer'|'paypal', email} — stored on the creator row
//   highlights           up to 3 short lines for "What it does" on the listing
//   pitch, prompts, sample, shots   the rest of the listing (shots: data URIs like publish; [] clears them)
//   name, emoji, icon_url, cat, requires, optional, trades, cadence   the rest of what the edit wizard can change
// Every branch checks the signed-in Blossom account owns the skill's creator handle.
import { db, json, bad, identity } from './_lib.mjs';
const num = (v) => { const n = Number(v); return Number.isFinite(n) && n >= 0 ? Math.round(n * 100) / 100 : null; };
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { skill, identity: token, version, note, skill_md, price, payout, highlights, pitch, prompts, sample, shots, name, emoji, icon_url, cat, requires, optional, trades, cadence } = await req.json().catch(() => ({}));
  const me = identity(token);
  if (!me) return bad('Sign in to Blossom to update a skill', 401);
  const owner = me.userId;
  if (!skill) return bad('skill is required');
  const sb = db();
  const { data: s } = await sb.from('skills').select('id,creator,price').eq('id', skill).single();
  const { data: c } = s ? await sb.from('creators').select('user_id').eq('handle', s.creator).maybeSingle() : { data: null };
  if (!c?.user_id || c.user_id !== owner) return bad('Not your skill', 403);
  const patch = {};
  if (version && note) {
    if (skill_md) {
      if (/sk_live|sk_test|api[_-]?key\s*[:=]\s*\S{12,}|ghp_[A-Za-z0-9]{20,}/i.test(skill_md)) return bad('The SKILL.md looks like it contains a secret. Remove it and try again.');
      patch.skill_md = String(skill_md).slice(0, 200000);
    }
    patch.version = String(version).slice(0, 20); patch.updated_at = new Date().toISOString();
  }
  if (price && typeof price === 'object') {
    const p = price.free ? { free: true } : {};
    if (!price.free) {
      const once = num(price.once), monthly = num(price.monthly), yearly = num(price.yearly);
      if (once) p.once = once; if (monthly) p.monthly = monthly; if (yearly) p.yearly = yearly;
      if (!Object.keys(p).length) return bad('Set a one-time, monthly or yearly price, or make it free');
    }
    patch.price = p;
  }
  if (Array.isArray(highlights)) patch.highlights = highlights.map(h => String(h || '').trim().slice(0, 110)).filter(Boolean).slice(0, 3);
  if (typeof pitch === 'string' && pitch.trim()) patch.pitch = pitch.trim().slice(0, 160);
  if (typeof name === 'string' && name.trim()) patch.name = name.trim().slice(0, 48);
  if (typeof emoji === 'string' && emoji.trim()) patch.emoji = emoji.trim().slice(0, 8);
  if (icon_url !== undefined) { const isImg = (d) => typeof d === 'string' && /^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+$/.test(d); if (icon_url === null) patch.icon_url = null; else if (isImg(icon_url) && icon_url.length <= 60 * 1024 * 1.4) patch.icon_url = icon_url; }
  if (typeof cat === 'string' && cat.trim()) patch.cat = cat.trim().slice(0, 24);
  const ids = (a) => Array.isArray(a) ? a.map(x => String(x || '').trim().slice(0, 40)).filter(Boolean).slice(0, 8) : null;
  if (ids(requires)) patch.requires = ids(requires); if (ids(optional)) patch.optional = ids(optional);
  if (typeof trades === 'boolean') patch.trades = trades;
  if (typeof cadence === 'string' && cadence.trim()) patch.cadence = cadence.trim().slice(0, 40);
  if (Array.isArray(prompts)) patch.prompts = prompts.map(p => String(p || '').trim().slice(0, 200)).filter(Boolean).slice(0, 6);
  if (typeof sample === 'string') patch.sample = sample.slice(0, 20000);
  if (Array.isArray(shots)) {
    const isImg = (d) => typeof d === 'string' && /^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+$/.test(d);
    patch.shots = shots.slice(0, 4).map(x => Array.isArray(x) ? x : [x, '']).filter(([d]) => isImg(d) && d.length <= 400 * 1024 * 1.4).map(([d, cap]) => [d, String(cap || '').slice(0, 120)]);
  }
  if (Object.keys(patch).length) { const { error } = await sb.from('skills').update(patch).eq('id', skill); if (error) return bad(error.message, 500); }
  if (version && note) await sb.from('skill_updates').insert({ skill_id: skill, version: patch.version, note: String(note).slice(0, 2000) });
  if (payout && typeof payout === 'object') {
    const method = payout.method === 'paypal' ? 'paypal' : payout.method === 'etransfer' ? 'etransfer' : null;
    const email = String(payout.email || '').trim();
    if (!method || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return bad('Payout needs a method (e-Transfer or PayPal) and a valid email');
    const { error } = await sb.from('creators').update({ payout_method: method, payout_email: email }).eq('handle', s.creator);
    if (error) return bad(error.message, 500);
  }
  return json({ ok: true, price: patch.price || s.price });
};
