// GET ?session_id=cs_… → confirms the Stripe session is paid, records the purchase if the webhook hasn't yet, returns a download token.
import { db, stripe, json, bad, sign } from './_lib.mjs';
export default async (req) => {
  const sid = new URL(req.url).searchParams.get('session_id');
  if (!sid) return bad('session_id required');
  const cs = await stripe().checkout.sessions.retrieve(sid).catch(() => null);
  if (!cs) return bad('Unknown session', 404);
  if (cs.payment_status !== 'paid') return bad('Not paid yet', 402);
  const [skill, plan] = (cs.client_reference_id || '').split(':');
  const email = (cs.customer_details?.email || cs.customer_email || '').toLowerCase();
  if (!skill || !email) return bad('Session has no skill or email');
  const sb = db();
  await sb.from('purchases').upsert({ skill_id: skill, plan, buyer_email: email, stripe_session_id: cs.id, stripe_customer_id: cs.customer || null, stripe_subscription_id: cs.subscription || null, amount_cents: cs.amount_total, currency: cs.currency, status: 'active' }, { onConflict: 'stripe_session_id' });
  const { data: s } = await sb.from('skills').select('id,name').eq('id', skill).single();
  return json({ skill, plan, email, name: s?.name, token: sign(skill, email) });
};
