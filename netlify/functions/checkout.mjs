// POST {skill, plan, email} → Stripe Checkout URL. Prices come from the skills table, not the client.
import { db, stripe, json, bad, planPrice, SITE } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { skill: id, plan, email } = await req.json().catch(() => ({}));
  if (!id || !plan || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email || '')) return bad('skill, plan and a valid email are required');
  const { data: s, error } = await db().from('skills').select('id,name,creator,price,status').eq('id', id).single();
  if (error || !s || s.status !== 'live') return bad('Unknown skill', 404);
  const cents = planPrice(s.price, plan);
  if (!cents) return bad('That plan is not offered for this skill');
  const recurring = plan === 'monthly' ? { interval: 'month' } : plan === 'yearly' ? { interval: 'year' } : null;
  const session = await stripe().checkout.sessions.create({
    mode: recurring ? 'subscription' : 'payment',
    customer_email: email,
    client_reference_id: `${s.id}:${plan}`,
    metadata: { skill: s.id, plan, creator: s.creator },
    line_items: [{ quantity: 1, price_data: { currency: 'cad', unit_amount: cents, product_data: { name: `${s.name} — ${plan === 'once' ? 'one-time' : plan}`, description: `Blossom Skills · by @${s.creator}` }, ...(recurring ? { recurring } : {}) } }],
    success_url: `${SITE}/?checkout=success&skill=${encodeURIComponent(s.id)}&plan=${plan}&session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${SITE}/#/skill/${encodeURIComponent(s.id)}`,
    allow_promotion_codes: false,
  });
  return json({ url: session.url });
};
