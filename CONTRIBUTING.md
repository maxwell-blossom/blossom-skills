# Working on Blossom Skills

- `data.py` is the catalogue (skills, MCPs, creators). `build.py` is the page. `gen_shots.py` renders the sample-output screenshots (needs Playwright).
- Binary assets (logos, avatars, screenshots) live in `assets.tgz.b64`. `bash build.sh` unpacks them into `assets/` and builds `dist/`. After changing anything under `assets/`, repack: `tar czf - assets | base64 -w 0 > assets.tgz.b64`.
- Local preview: `bash build.sh && python3 -m http.server -d dist 8080`.
- Netlify builds from this repo (`netlify.toml`): every push to `main` deploys https://blossom-skills.netlify.app; branches get preview URLs.
