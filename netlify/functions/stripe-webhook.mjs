// Stripe → us. Records purchases and subscription changes. Set STRIPE_WEBHOOK_SECRET from the Stripe dashboard.
import { db, stripe, json, bad, sign, SITE, HOST } from './_lib.mjs';
import { sendMail } from './_mail.mjs';
import { receiptEmail } from './_receipt.mjs';
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
        skill_id: skill, plan, buyer_email: (cs.customer_details?.email || cs.customer_email || '').toLowerCase(), buyer_user_id: cs.metadata?.user_id || null,
        stripe_session_id: cs.id, stripe_customer_id: cs.customer || null, stripe_subscription_id: cs.subscription || null,
        amount_cents: cs.amount_total, currency: cs.currency, status: 'active',
      }, { onConflict: 'stripe_session_id' });
      // Receipt + download link from us (Stripe's own receipt only goes out in live mode, and only if it's switched on in Stripe → Settings → Emails).
      const email = (cs.customer_details?.email || cs.customer_email || '').toLowerCase();
      const { data: s } = await sb.from('skills').select('id,name,creator,prompts').eq('id', skill).single();
      if (email && s) {
        const { data: c } = await sb.from('creators').select('name').eq('handle', s.creator).maybeSingle();
        const amount = ((cs.amount_total || 0) / 100).toFixed(2) + ' ' + String(cs.currency || 'cad').toUpperCase();
        const mail = receiptEmail({
          skill: { ...s, creatorName: c?.name || '' }, plan, amount, sessionId: cs.id, when: new Date(),
          download: `${SITE}/api/download?skill=${encodeURIComponent(s.id)}&token=${encodeURIComponent(sign(s.id, email))}`,
          page: `${SITE}/skill/${s.id}`, mySkills: `${SITE}/purchases`, logo: `${HOST}/skills/og-logo.png`,   // the wordmark is served from this host; the public host proxies only /skills pages
        });
        await sendMail({ to: email, ...mail }).catch(e => console.warn('mail', e.message));
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
