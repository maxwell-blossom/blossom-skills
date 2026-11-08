#!/usr/bin/env python3
"""Generates supabase/seed.sql from data.py. Safe to re-run: every statement upserts on its primary key.
Run once in Supabase → SQL Editor after schema.sql, or re-run after editing data.py."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data
from hidden import HIDDEN
data.SKILLS = [s for s in data.SKILLS if s['id'] not in HIDDEN]

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
# JSON twin for the seed function (netlify/functions/seed.mjs): same rows, loaded through supabase-js.
rows = {'creators': [], 'skills': [], 'skill_updates': []}
for handle, c in creators:
    rows['creators'].append({'handle': handle, 'name': c['name'], 'badge': c.get('badge'), 'bio': c.get('bio'), 'followers': c.get('followers', 0),
                             'photo_url': f"{SITE}/profiles/{c['photo']}" if c.get('photo') else None})
for s in data.SKILLS:
    rows['skills'].append({'id': s['id'], 'creator': s['creator'], 'name': s['name'], 'emoji': s.get('emoji'), 'cat': s.get('cat'), 'pitch': s.get('pitch'),
                           'highlights': s.get('highlights') or [], 'requires': s.get('requires') or [], 'optional': s.get('optional') or [],
                           'trades': bool(s.get('trades')), 'price': s.get('price') or {'free': True}, 'cadence': s.get('cadence'), 'prompts': s.get('prompts') or [],
                           'sample': s.get('sample'), 'shots': [list(x) for x in (s.get('shots') or [])], 'skill_md': s['skill'], 'status': s.get('status') or 'live',
                           'downloads': s.get('downloads', 0), 'rating': s.get('rating', 0), 'ratings': s.get('ratings', 0), 'version': s.get('version', '1.0.0'),
                           'updated_at': s.get('updated')})
    for ver, date, note in (s.get('log') or []):
        rows['skill_updates'].append({'skill_id': s['id'], 'version': ver, 'note': note, 'created_at': date})
jpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'netlify', 'functions', 'seed-data.json')
os.makedirs(os.path.dirname(jpath), exist_ok=True)
json.dump(rows, open(jpath, 'w', encoding='utf-8'), ensure_ascii=False)
print(f"wrote {path} and {jpath} ({len(data.SKILLS)} skills, {len(rows['creators'])} creators, {len(rows['skill_updates'])} updates)")
