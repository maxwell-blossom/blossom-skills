// POST {email, mcp} — waitlist for the Blossom MCPs (Connector, Aggregate Trade Data) while they're "coming soon".
import { db, json, bad } from './_lib.mjs';
export default async (req) => {
  if (req.method !== 'POST') return bad('POST only', 405);
  const b = await req.json().catch(() => ({}));
  const email = String(b.email || '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return bad('A valid email is required');
  const mcp = String(b.mcp || '').replace(/[^a-z0-9-]/g, '').slice(0, 64) || 'unknown';
  const { error } = await db().from('waitlist').upsert({ email, mcp }, { onConflict: 'email,mcp', ignoreDuplicates: true });
  if (error) return bad(error.message, 500);
  return json({ ok: true });
};
