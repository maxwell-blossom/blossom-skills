// GET /.netlify/functions/sitemap → every live skill in the database (the static sitemap.xml covers the seeded pages and MCPs).
import { db, SITE } from './_lib.mjs';
export default async () => {
  const { data } = await db().from('skills').select('id,updated_at').eq('status', 'live');
  const body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
    (data || []).map((s) => `<url><loc>${SITE}/skill/${s.id}</loc>${s.updated_at ? `<lastmod>${s.updated_at.slice(0, 10)}</lastmod>` : ''}</url>`).join('') + '</urlset>\n';
  return new Response(body, { headers: { 'content-type': 'application/xml; charset=utf-8', 'cache-control': 'public, max-age=600' } });
};
