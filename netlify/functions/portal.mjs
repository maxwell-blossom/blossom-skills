// POST {identity} → a Stripe Customer Portal URL for the signed-in buyer, where they can cancel or change a subscription.
// Needs the Customer Portal switched on once in the Stripe dashboard (Settings → Billing → Customer portal). Returns 404 when the user has no Stripe customer.
import { db, stripe, json, bad, identity, SITE } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const { identity: token } = await req.json().catch(() => ({}));
  const me = identity(token);
  if (!me) return bad('Sign in to Blossom first', 401);
  const { data } = await db().from('purchases').select('stripe_customer_id,created_at').eq('buyer_user_id', me.userId).not('stripe_customer_id', 'is', null).order('created_at', { ascending: false }).limit(1);
  const customer = data?.[0]?.stripe_customer_id;
  if (!customer) return bad('No subscription found for your account', 404);
  let st; try { st = stripe(); } catch (e) { return bad('Billing is not set up yet', 503); }
  try {
    const session = await st.billingPortal.sessions.create({ customer, return_url: `${SITE}/purchases` });
    return json({ url: session.url });
  } catch (e) {
    return bad(/portal/i.test(e.message) ? 'The billing portal isn’t switched on in Stripe yet' : e.message, 502);
  }
};
