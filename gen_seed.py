#!/usr/bin/env python3
"""Generates supabase/seed.sql from data.py. Safe to re-run: every statement upserts on its primary key.
Run once in Supabase → SQL Editor after schema.sql, or re-run after editing data.py."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data

SITE = os.environ.get('SITE_URL', 'https://blossom-skills.netlify.app')

def q(v):
    if v is None: return 'null'
    if isinstance(v, bool): return 'true' if v else 'false'
    if isinstance(v, (int, float)): return str(v)
    return "'" + str(v).replace("'", "''") + "'"

def j(v):
    return q(json.dumps(v if v is not None else [], ensure_ascii=False)) + '::jsonb'

out = ['-- Blossom Skills — seed (generated from data.py). Safe to re-run: upserts on primary keys.', 'begin;']

creators = data.CREATORS.items() if isinstance(data.CREATORS, dict) else [(c['handle'], c) for c in data.CREATORS]
for handle, c in creators:
    photo = f"{SITE}/profiles/{c['photo']}" if c.get('photo') else None
    out.append(
        f"insert into creators (handle,name,badge,bio,followers,photo_url) values ({q(handle)},{q(c['name'])},{q(c.get('badge'))},{q(c.get('bio'))},{c.get('followers', 0)},{q(photo)}) "
        "on conflict (handle) do update set name=excluded.name,badge=excluded.badge,bio=excluded.bio,followers=excluded.followers,photo_url=excluded.photo_url;")

for s in data.SKILLS:
    shots = [list(x) for x in (s.get('shots') or [])]
    out.append(
        "insert into skills (id,creator,name,emoji,cat,pitch,highlights,requires,optional,trades,price,cadence,prompts,sample,shots,skill_md,status,downloads,rating,ratings,version,updated_at) values ("
        f"{q(s['id'])},{q(s['creator'])},{q(s['name'])},{q(s.get('emoji'))},{q(s.get('cat'))},{q(s.get('pitch'))},{j(s.get('highlights'))},{j(s.get('requires'))},{j(s.get('optional'))},"
        f"{q(bool(s.get('trades')))},{j(s.get('price') or {'free': True})},{q(s.get('cadence'))},{j(s.get('prompts'))},{q(s.get('sample'))},{j(shots)},{q(s['skill'])},"
        f"{q(s.get('status') or 'live')},{s.get('downloads', 0)},{s.get('rating', 0)},{s.get('ratings', 0)},{q(s.get('version', '1.0.0'))},{q(s.get('updated'))}) "
        "on conflict (id) do update set creator=excluded.creator,name=excluded.name,emoji=excluded.emoji,cat=excluded.cat,pitch=excluded.pitch,highlights=excluded.highlights,"
        "requires=excluded.requires,optional=excluded.optional,trades=excluded.trades,price=excluded.price,cadence=excluded.cadence,prompts=excluded.prompts,sample=excluded.sample,"
        "shots=excluded.shots,skill_md=excluded.skill_md,status=excluded.status,version=excluded.version,updated_at=excluded.updated_at;")
    for ver, date, note in (s.get('log') or []):
        out.append(
            f"insert into skill_updates (skill_id,version,note,created_at) select {q(s['id'])},{q(ver)},{q(note)},{q(date)} "
            f"where not exists (select 1 from skill_updates where skill_id={q(s['id'])} and version={q(ver)});")

out.append('commit;')
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'supabase'), exist_ok=True)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'supabase', 'seed.sql')
open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(f"wrote {path} ({len(data.SKILLS)} skills, {len(list(creators))} creators)")
