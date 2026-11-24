"""Environment-dependent URLs for the build scripts. Mirrors netlify/functions/_lib.mjs.

BLOSSOM_ENV takes web-app's NEXT_PUBLIC_ENV values, DEV, STAGING or PROD (default), and picks the web app host
that proxies this site under /skills. Any single value can be overridden:
  APP_ORIGIN  the Blossom web app          (DEV https://dev.blossomsocial.com, STAGING https://staging.blossomsocial.com,
                                            PROD https://www.blossomsocial.com)
  BASE_PATH   where this site is served     (/skills)
  SITE_URL    public base URL of this site  (APP_ORIGIN + BASE_PATH)
"""
import os

APP_ORIGINS = {
    'DEV': 'https://dev.blossomsocial.com',
    'STAGING': 'https://staging.blossomsocial.com',
    'PROD': 'https://www.blossomsocial.com',
}

ENV = os.environ.get('BLOSSOM_ENV', 'PROD').strip().upper()
if ENV not in APP_ORIGINS:
    raise SystemExit(f"BLOSSOM_ENV must be one of {', '.join(APP_ORIGINS)}, got {ENV!r}")

APP = os.environ.get('APP_ORIGIN', APP_ORIGINS[ENV]).rstrip('/')
BASE = os.environ.get('BASE_PATH', '/skills')
SITE = (os.environ.get('SITE_URL') or (os.environ.get('SITE_ORIGIN', APP).rstrip('/') + BASE)).rstrip('/')
