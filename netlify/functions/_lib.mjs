// Shared helpers for the Blossom Skills functions.
import { createClient } from '@supabase/supabase-js';
import Stripe from 'stripe';
import { createHmac, timingSafeEqual } from 'node:crypto';

export const SITE = process.env.SITE_URL || 'https://blossom-skills.netlify.app';
export const TAKE = 0.20;

export function db() {
  const url = process.env.SUPABASE_DATABASE_URL || process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;
  if (!url || !key) throw new Error('Supabase is not configured (SUPABASE_DATABASE_URL / SUPABASE_SERVICE_ROLE_KEY)');
  return createClient(url, key, { auth: { persistSession: false } });
}
export function stripe() {
  if (!process.env.STRIPE_SECRET_KEY) throw new Error('STRIPE_SECRET_KEY is not set');
  return new Stripe(process.env.STRIPE_SECRET_KEY);
}
export const json = (body, status = 200, extra = {}) =>
  new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store', ...extra } });
export const bad = (msg, status = 400) => json({ error: msg }, status);

// Download tokens: HMAC of "<skill>:<email>:<exp>" with the site's secret. No DB round-trip to verify.
function secret() { return process.env.DOWNLOAD_SECRET || process.env.SUPABASE_JWT_SECRET || process.env.STRIPE_SECRET_KEY; }
export function sign(skill, email, days = 365) {
  const exp = Math.floor(Date.now() / 1000) + days * 86400;
  const payload = `${skill}:${email.toLowerCase()}:${exp}`;
  const mac = createHmac('sha256', secret()).update(payload).digest('base64url');
  return Buffer.from(payload).toString('base64url') + '.' + mac;
}
export function verify(token) {
  try {
    const [p, mac] = token.split('.');
    const payload = Buffer.from(p, 'base64url').toString();
    const expect = createHmac('sha256', secret()).update(payload).digest('base64url');
    if (!timingSafeEqual(Buffer.from(mac), Buffer.from(expect))) return null;
    const [skill, email, exp] = payload.split(':');
    if (Number(exp) < Date.now() / 1000) return null;
    return { skill, email };
  } catch { return null; }
}
export const money = (p) => Math.round(Number(p) * 100);
export function planPrice(price, plan) {
  if (plan === 'once' && price.once) return money(price.once);
  if (plan === 'monthly' && price.monthly) return money(price.monthly);
  if (plan === 'yearly' && price.yearly) return money(price.yearly);
  return null;
}
