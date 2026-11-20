// Transactional email through SendGrid (Blossom's existing account; blossomsocial.com is domain-authenticated there).
// Set SENDGRID_API_KEY (Mail Send permission) in Netlify. RECEIPT_FROM defaults to "Blossom Skills <skills@blossomsocial.com>".
// Without a key this is a no-op, so nothing else breaks.
export async function sendMail({ to, subject, html, text }) {
  const key = process.env.SENDGRID_API_KEY;
  if (!key || !to) return { skipped: true };
  const m = (process.env.RECEIPT_FROM || 'Blossom Skills <skills@blossomsocial.com>').match(/^\s*(.*?)\s*<([^>]+)>\s*$/);
  const from = m ? { email: m[2], name: m[1] || undefined } : { email: process.env.RECEIPT_FROM };
  const body = {
    personalizations: [{ to: [{ email: to }] }],
    from, reply_to: from, subject,
    content: [{ type: 'text/plain', value: text || ' ' }, { type: 'text/html', value: html || ' ' }],   // SendGrid requires text/plain before text/html
  };
  const r = await fetch('https://api.sendgrid.com/v3/mail/send', { method: 'POST', headers: { authorization: 'Bearer ' + key, 'content-type': 'application/json' }, body: JSON.stringify(body) });
  if (!r.ok) { console.warn('sendgrid', r.status, await r.text().catch(() => '')); return { error: r.status }; }
  return { ok: true, id: r.headers.get('x-message-id') || null };   // 202 Accepted with an empty body
}
export const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
