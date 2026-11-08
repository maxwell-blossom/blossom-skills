// Stripe → us. Records purchases and subscription changes. Set STRIPE_WEBHOOK_SECRET from the Stripe dashboard.
import { db, stripe, json, bad } from './_lib.mjs';
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
