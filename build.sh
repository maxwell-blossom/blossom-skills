#!/usr/bin/env bash
# Netlify build: unpack binary assets, build the page, assemble the publish dir.
# Functions read STRIPE_SECRET_KEY / STRIPE_WEBHOOK_SECRET from Netlify env (set Nov 8, Stripe sandbox).
set -euo pipefail
[ -d assets ] || base64 -d assets.tgz.b64 | tar xz
python3 build.py
python3 gen_seed.py
# Everything lives under /skills (the path the Blossom web app proxies); the shell is skills.html so /skills
# itself is served without a trailing-slash redirect. _redirects and robots.txt stay at the publish root.
rm -rf dist && mkdir -p dist/skills
cp index.html dist/skills.html && cp -r skills dist/skills/skills && cp -r assets/shots dist/skills/shots && cp assets/og.jpg dist/skills/og.jpg && cp assets/logo_blossom_flower_256.jpg dist/skills/favicon.jpg
mkdir -p dist/skills/profiles && cp assets/profiles/*.jpg dist/skills/profiles/
# Creator rows seeded before the move point at /profiles on this host.
mkdir -p dist/profiles && cp assets/profiles/*.jpg dist/profiles/
cp llms.txt dist/skills/llms.txt
cp -r pages/. dist/skills/ && cp sitemap.xml dist/skills/ && cp robots.txt _redirects dist/
