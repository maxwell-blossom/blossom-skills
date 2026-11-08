// Transactional email through Resend (https://resend.com). Set RESEND_API_KEY in Netlify; RECEIPT_FROM defaults to skills@blossomsocial.com
// (the domain has to be verified in Resend). Without a key this is a no-op, so nothing else breaks.
export async function sendMail({ to, subject, html, text }) {
  const key = process.env.RESEND_API_KEY;
  if (!key || !to) return { skipped: true };
  const from = process.env.RECEIPT_FROM || 'Blossom Skills <skills@blossomsocial.com>';
  const r = await fetch('https://api.resend.com/emails', { method: 'POST', headers: { authorization: 'Bearer ' + key, 'content-type': 'application/json' }, body: JSON.stringify({ from, to, subject, html, text }) });
  if (!r.ok) { console.warn('resend', r.status, await r.text().catch(() => '')); return { error: r.status }; }
  return await r.json();
}
export const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
