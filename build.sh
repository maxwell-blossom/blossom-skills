#!/usr/bin/env bash
# Netlify build: unpack binary assets, build the page, assemble the publish dir.
set -euo pipefail
[ -d assets ] || base64 -d assets.tgz.b64 | tar xz
python3 build.py
rm -rf dist && mkdir -p dist
cp index.html dist/ && cp -r skills dist/skills && cp -r assets/shots dist/shots && cp assets/og.jpg dist/og.jpg && cp assets/logo_blossom_flower_256.jpg dist/favicon.jpg
mkdir -p dist/profiles && cp assets/profiles/*.jpg dist/profiles/
# TEMP: expose the seed for the one-off Supabase load (remove after seeding)
cp supabase/seed.sql dist/seed.sql && printf '/seed.sql\n  Access-Control-Allow-Origin: *\n  Cache-Control: no-store\n' > dist/_headers
