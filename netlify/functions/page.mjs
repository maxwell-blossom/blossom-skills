// GET /skill/<id> for skills that have no static page (posted through the site after the last build).
// Takes the built index.html, swaps in the skill's title/description/canonical/JSON-LD and a crawler-visible summary; the SPA then renders the full page.
import { db, SITE } from './_lib.mjs';
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
let shell = null, shellAt = 0;
async function getShell() {
  if (shell && Date.now() - shellAt < 300000) return shell;
  const r = await fetch(`${SITE}/index.html`); shell = await r.text(); shellAt = Date.now(); return shell;
}
export default async (req) => {
  const u = new URL(req.url);
  const id = decodeURIComponent(u.pathname.replace(/^\/skill\//, '').replace(/\/$/, ''));
  const html = await getShell();
  const spa = () => new Response(html, { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } });
  if (!id) return spa();
  const sb = db();
  const { data: s } = await sb.from('skills').select('id,creator,name,pitch,highlights,requires,prompts,price,version,updated_at,status').eq('id', id).eq('status', 'live').maybeSingle();
  if (!s) return spa();
  const { data: c } = await sb.from('creators').select('name').eq('handle', s.creator).maybeSingle();
  const who = c?.name || s.creator;
  const title = `${s.name} by ${who} — a skill for Claude, ChatGPT, Grok and Cursor | Blossom Skills`;
  const url = `${SITE}/skill/${s.id}`;
  const price = s.price?.free ? 'Free' : Object.entries(s.price || {}).map(([k, v]) => `$${v} ${k}`).join(' · ');
  const ld = { '@context': 'https://schema.org', '@type': 'SoftwareApplication', name: s.name, description: s.pitch, url, applicationCategory: 'FinanceApplication', operatingSystem: 'Claude, ChatGPT, Grok, Cursor', author: { '@type': 'Person', name: who }, softwareVersion: s.version, dateModified: (s.updated_at || '').slice(0, 10), offers: { '@type': 'Offer', price: s.price?.free ? '0' : String(s.price?.monthly || s.price?.yearly || s.price?.once || 0), priceCurrency: 'CAD' } };
  const app = `<div class="wrap"><h1>${esc(s.name)}</h1><p>${esc(s.pitch)}</p><p>By ${esc(who)} (@${esc(s.creator)}) on Blossom · ${esc(price)} · v${esc(s.version)}</p><ul>${(s.highlights || []).map((h) => `<li>${esc(h)}</li>`).join('')}</ul><p>Try: ${(s.prompts || []).map((p) => `“${esc(p)}”`).join(' · ')}</p><p>Works in Claude, ChatGPT, Grok and Cursor. <a href="/">All skills</a></p></div>`;
  let out = html
    .replace(/<title>[^<]*<\/title>/, `<title>${esc(title)}</title>`)
    .replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${esc(s.pitch)}">`)
    .replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="${url}">`)
    .replace(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${esc(title)}">`)
    .replace(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${esc(s.pitch)}">`)
    .replace(/<meta property="og:url" content="[^"]*">/, `<meta property="og:url" content="${url}">`)
    .replace(/<meta name="twitter:title" content="[^"]*">/, `<meta name="twitter:title" content="${esc(title)}">`)
    .replace('<link rel="icon"', `<script type="application/ld+json">${JSON.stringify(ld)}</script>\n<link rel="icon"`)
    .replace('<div id="app"></div>', `<div id="app">${app}</div>`);
  return new Response(out, { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'public, max-age=300' } });
};
