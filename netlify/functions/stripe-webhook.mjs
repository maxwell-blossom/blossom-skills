// Stripe → us. Records purchases and subscription changes. Set STRIPE_WEBHOOK_SECRET from the Stripe dashboard.
import { db, stripe, json, bad, sign, SITE } from './_lib.mjs';
import { sendMail, esc } from './_mail.mjs';
export const config = { path: '/api/stripe-webhook' };
export default async (req) => {
  const sig = req.headers.get('stripe-signature');
  const raw = await req.text();
  let event;
  try { event = stripe().webhooks.constructEvent(raw, sig, process.env.STRIPE_WEBHOOK_SECRET); }
  catch (e) { return bad('Bad signature: ' + e.message); }
  const sb = db();
  if (event.type === 'checkout.session.completed') {
    const cs = event.data.object;
    const [skill, plan] = (cs.client_reference_id || '').split(':');
    if (skill && plan && cs.payment_status === 'paid') {
      await sb.from('purchases').upsert({
        skill_id: skill, plan, buyer_email: (cs.customer_details?.email || cs.customer_email || '').toLowerCase(),
        stripe_session_id: cs.id, stripe_customer_id: cs.customer || null, stripe_subscription_id: cs.subscription || null,
        amount_cents: cs.amount_total, currency: cs.currency, status: 'active',
      }, { onConflict: 'stripe_session_id' });
      // Receipt + download link from us (Stripe's own receipt only goes out in live mode, and only if it's switched on in Stripe → Settings → Emails).
      const email = (cs.customer_details?.email || cs.customer_email || '').toLowerCase();
      const { data: s } = await sb.from('skills').select('id,name,creator,prompts').eq('id', skill).single();
      if (email && s) {
        const amt = ((cs.amount_total || 0) / 100).toFixed(2) + ' ' + String(cs.currency || 'cad').toUpperCase();
        const planTxt = plan === 'once' ? 'One-time purchase' : plan === 'monthly' ? 'Monthly subscription' : 'Yearly subscription';
        const dl = `${SITE}/.netlify/functions/download?skill=${encodeURIComponent(s.id)}&token=${encodeURIComponent(sign(s.id, email))}`;
        const page = `${SITE}/skill/${s.id}`;
        const prompt = (s.prompts || [])[0] || 'Run ' + s.name;
        const html = `<div style="font-family:Nunito,Helvetica,Arial,sans-serif;max-width:560px;margin:0 auto;color:#171717;line-height:1.5">
<h1 style="font-size:22px;margin:24px 0 6px">You're in. ${esc(s.name)} is yours.</h1>
<p style="color:#72777F;margin:0 0 18px">${planTxt} · ${esc(amt)} · by @${esc(s.creator)} on Blossom Skills</p>
<p><a href="${dl}" style="display:inline-block;background:#7361F7;color:#fff;text-decoration:none;font-weight:700;padding:12px 22px;border-radius:999px">Download SKILL.md</a></p>
<p style="margin-top:22px"><b>Install it in Claude</b><br>Open Claude, drop the file into a chat and say <i>"Save this as a skill."</i> Then ask: <i>"${esc(prompt)}"</i></p>
<p>It also works in Claude Code, Cursor, ChatGPT and Grok — the steps are on <a href="${page}" style="color:#7361F7">the skill page</a>.</p>
<p style="color:#72777F;font-size:13px;margin-top:26px">Keep this email: the download link is yours for 12 months${plan === 'once' ? '' : ' while you\'re subscribed'}. Receipt for your records — Stripe session ${esc(cs.id)}. Questions: <a href="mailto:skills@blossomsocial.com" style="color:#7361F7">skills@blossomsocial.com</a>.</p></div>`;
        const text = `You're in. ${s.name} is yours.\n${planTxt} · ${amt} · by @${s.creator} on Blossom Skills\n\nDownload: ${dl}\n\nInstall in Claude: open Claude, drop the file into a chat and say "Save this as a skill." Then ask: "${prompt}"\nOther assistants: ${page}\n\nReceipt · Stripe session ${cs.id}`;
        await sendMail({ to: email, subject: `Your receipt · ${s.name} on Blossom Skills`, html, text }).catch(e => console.warn('mail', e.message));
      }
    }
  }
  if (event.type === 'customer.subscription.deleted' || event.type === 'customer.subscription.updated') {
    const sub = event.data.object;
    const status = sub.status === 'active' || sub.status === 'trialing' ? 'active' : sub.status === 'past_due' ? 'past_due' : 'canceled';
    await sb.from('purchases').update({ status, current_period_end: sub.current_period_end ? new Date(sub.current_period_end * 1000).toISOString() : null }).eq('stripe_subscription_id', sub.id);
  }
  if (event.type === 'charge.refunded') {
    const ch = event.data.object;
    if (ch.payment_intent) {
      const sessions = await stripe().checkout.sessions.list({ payment_intent: ch.payment_intent, limit: 1 });
      const cs = sessions.data[0]; if (cs) await sb.from('purchases').update({ status: 'refunded' }).eq('stripe_session_id', cs.id);
    }
  }
  return json({ received: true });
};
