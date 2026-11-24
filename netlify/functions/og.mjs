// GET /skills/api/og?skill=<id> → 1200×630 PNG for link previews (og:image) of one skill.
// Drawn as SVG and rasterised with resvg; Nunito is fetched once per cold start and kept in memory.
import { Resvg } from '@resvg/resvg-js';
import { db, SITE, HOST } from './_lib.mjs';
import { writeFileSync } from 'node:fs';
import { inflateSync } from 'node:zlib';
export const config = { path: '/skills/api/og' };

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
// Blossom wordmark: build.sh copies assets/_blossom_logo_t.png to dist/skills/og-logo.png; fetched once per cold start from this host.
const LOGO_URL = `${HOST}/skills/og-logo.png`;
// Fonts: Nunito 800 (headings) and 600 (body) from fontsource, as WOFF, converted to TTF because resvg reads sfnt only
// (and resvg-js 2.6 ignores fontBuffers, so they go through /tmp as files). The fontsource build names the families
// "Nunito ExtraLight ExtraBold" / "Nunito ExtraLight SemiBold" — the SVG below selects by those names. Pinned to 5.0.14.
const FONTS = { heading: ['Nunito ExtraLight ExtraBold', 'https://cdn.jsdelivr.net/npm/@fontsource/nunito@5.0.14/files/nunito-latin-800-normal.woff', '/tmp/nunito-800.ttf'],
                body: ['Nunito ExtraLight SemiBold', 'https://cdn.jsdelivr.net/npm/@fontsource/nunito@5.0.14/files/nunito-latin-600-normal.woff', '/tmp/nunito-600.ttf'] };
// WOFF 1.0 → sfnt: 44-byte header, 20-byte directory entries (tag, offset, compLength, origLength, origChecksum); tables are zlib-deflated when compLength < origLength.
function woffToSfnt(buf) {
  const flavor = buf.readUInt32BE(4), n = buf.readUInt16BE(12), tables = [];
  for (let i = 0; i < n; i++) { const o = 44 + i * 20, off = buf.readUInt32BE(o + 4), comp = buf.readUInt32BE(o + 8), orig = buf.readUInt32BE(o + 12); const raw = buf.subarray(off, off + comp); tables.push({ tag: buf.subarray(o, o + 4), sum: buf.readUInt32BE(o + 16), orig, data: comp === orig ? raw : inflateSync(raw) }); }
  const es = Math.floor(Math.log2(n)), sr = (1 << es) * 16;
  const head = Buffer.alloc(12 + n * 16); head.writeUInt32BE(flavor, 0); head.writeUInt16BE(n, 4); head.writeUInt16BE(sr, 6); head.writeUInt16BE(es, 8); head.writeUInt16BE(n * 16 - sr, 10);
  let off = head.length; const parts = [head];
  tables.forEach((t, i) => { const o = 12 + i * 16; t.tag.copy(head, o); head.writeUInt32BE(t.sum, o + 4); head.writeUInt32BE(off, o + 8); head.writeUInt32BE(t.orig, o + 12); const pad = (4 - (t.data.length % 4)) % 4; parts.push(t.data, Buffer.alloc(pad)); off += t.data.length + pad; });
  return Buffer.concat(parts);
}
let fontFiles = null, logo = null;
async function assets() {
  if (!fontFiles) {
    fontFiles = await Promise.all(Object.values(FONTS).map(async ([, url, path]) => { const r = await fetch(url); if (!r.ok) throw new Error('font ' + r.status); writeFileSync(path, woffToSfnt(Buffer.from(await r.arrayBuffer()))); return path; }));
  }
  if (logo === null) { try { const r = await fetch(LOGO_URL); logo = r.ok ? Buffer.from(await r.arrayBuffer()).toString('base64') : ''; } catch { logo = ''; } }
  return { fontFiles, logo };
}
// Greedy wrap by an average glyph width (Nunito ≈ 0.52em); good enough for two lines of a title.
function wrap(text, size, maxWidth, maxLines) {
  const perChar = size * 0.52, words = String(text || '').split(/\s+/).filter(Boolean), lines = []; let cur = '';
  for (const w of words) { const t = cur ? cur + ' ' + w : w; if (t.length * perChar <= maxWidth || !cur) cur = t; else { lines.push(cur); cur = w; } }
  if (cur) lines.push(cur);
  if (lines.length > maxLines) { lines.length = maxLines; lines[maxLines - 1] = lines[maxLines - 1].replace(/\s*\S*$/, '') + '…'; }
  return lines;
}
async function emojiPng(emoji) {
  try {
    const cps = [...emoji].map((c) => c.codePointAt(0).toString(16)).filter((h) => h !== 'fe0f').join('-');
    const r = await fetch(`https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.1.0/assets/72x72/${cps}.png`);
    if (!r.ok) return null;
    return Buffer.from(await r.arrayBuffer()).toString('base64');
  } catch { return null; }
}
export function svg({ name, pitch, creator, who, price, emojiB64, logoB64 }) {
  const title = wrap(name, 56, 1040, 2), sub = wrap(pitch, 28, 1040, 2);
  const titleY = 296, lineH = 66, subY = titleY + (title.length - 1) * lineH + 70;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#EDE9FF"/><stop offset=".5" stop-color="#F6E9FA"/><stop offset="1" stop-color="#E1F4F1"/></linearGradient></defs>
<rect width="1200" height="630" fill="url(#g)"/>
${logoB64 ? `<image x="72" y="58" width="206" height="62" href="data:image/png;base64,${logoB64}"/>` : `<text x="72" y="104" font-family="Nunito ExtraLight ExtraBold" font-size="44" fill="#171717">blossom</text>`}
<text x="296" y="100" font-family="Nunito ExtraLight ExtraBold" font-size="26" fill="#72777F">Skills &amp; MCPs</text>
<rect x="72" y="150" width="68" height="68" rx="16" fill="#EDE9FF"/>
${emojiB64 ? `<image x="88" y="166" width="36" height="36" href="data:image/png;base64,${emojiB64}"/>` : `<circle cx="106" cy="184" r="12" fill="#7361F7"/>`}
${title.map((l, i) => `<text x="72" y="${titleY + i * lineH}" font-family="Nunito ExtraLight ExtraBold" font-size="56" fill="#171717">${esc(l)}</text>`).join('')}
${sub.map((l, i) => `<text x="72" y="${subY + i * 40}" font-family="Nunito ExtraLight SemiBold" font-size="28" fill="#3F3F46">${esc(l)}</text>`).join('')}
<text x="72" y="548" font-family="Nunito ExtraLight ExtraBold" font-size="26" fill="#171717">by ${esc(who)} · @${esc(creator)}</text>
<text x="72" y="582" font-family="Nunito ExtraLight SemiBold" font-size="22" fill="#72777F">Works in Claude, ChatGPT, Grok and Cursor · Built by verified investors on Blossom</text>
<rect x="${1128 - Math.max(120, price.length * 16 + 48)}" y="516" width="${Math.max(120, price.length * 16 + 48)}" height="56" rx="28" fill="#7361F7"/>
<text x="${1128 - Math.max(120, price.length * 16 + 48) / 2}" y="553" text-anchor="middle" font-family="Nunito ExtraLight ExtraBold" font-size="26" fill="#ffffff">${esc(price)}</text>
</svg>`;
}
export async function render(s, who) {
  const { fontFiles, logo } = await assets();
  const price = s.price?.free ? 'Free' : s.price?.once ? `$${s.price.once} once` : s.price?.monthly ? `$${s.price.monthly}/mo` : s.price?.yearly ? `$${s.price.yearly}/yr` : 'Free';
  const emojiB64 = await emojiPng(s.emoji || '🧾');
  const r = new Resvg(svg({ name: s.name, pitch: s.pitch, creator: s.creator, who, price, emojiB64, logoB64: logo }), { font: { fontFiles, loadSystemFonts: false, defaultFontFamily: FONTS.body[0] }, fitTo: { mode: 'width', value: 1200 } });
  return r.render().asPng();
}
export default async (req) => {
  const id = new URL(req.url).searchParams.get('skill') || '';
  const sb = db();
  const { data: s } = await sb.from('skills').select('id,creator,name,pitch,emoji,price,status').eq('id', id).eq('status', 'live').maybeSingle();
  if (!s) return Response.redirect(`${SITE}/og.jpg`, 302);
  const { data: c } = await sb.from('creators').select('name').eq('handle', s.creator).maybeSingle();
  try {
    const png = await render(s, c?.name || s.creator);
    return new Response(png, { headers: { 'content-type': 'image/png', 'cache-control': 'public, max-age=3600, s-maxage=86400' } });
  } catch (e) { console.warn('og', e.message); return Response.redirect(`${SITE}/og.jpg`, 302); }
};
