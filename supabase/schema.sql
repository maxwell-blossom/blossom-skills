-- Blossom Skills — schema v1 (run once in Supabase → SQL Editor)
create extension if not exists pgcrypto;

create table if not exists creators (
  handle        text primary key,
  name          text not null,
  email         text,
  badge         text check (badge in ('official','verified','ambassador','pro')) ,
  bio           text,
  followers     int default 0,
  photo_url     text,
  url           text,          -- the creator's profile on blossomsocial.com
  following     int default 0,
  stocks        int default 0,
  portfolio     jsonb,         -- [{"t":"ZEQT","w":97.3}, …]
  payout_method text check (payout_method in ('etransfer','paypal')),
  payout_email  text,
  created_at    timestamptz default now()
);

create table if not exists skills (
  id          text primary key,                      -- slug
  creator     text not null references creators(handle),
  name        text not null,
  emoji       text,
  icon_url    text,
  cat         text,
  pitch       text,
  highlights  jsonb default '[]',
  requires    jsonb default '[]',                    -- mcp ids
  optional    jsonb default '[]',
  trades      boolean default false,
  price       jsonb not null default '{"free":true}',-- {free} | {once} | {monthly,yearly?} | {yearly}
  cadence     text,
  prompts     jsonb default '[]',
  sample      text,
  shots       jsonb default '[]',                    -- [[file, caption]]
  skill_md    text not null,                         -- the SKILL.md; never served publicly for paid skills
  status      text not null default 'review' check (status in ('review','live','unlisted','removed')),
  downloads   int default 0,
  rating      numeric(3,2) default 0,
  ratings     int default 0,
  version     text default '1.0.0',
  updated_at  timestamptz default now(),
  created_at  timestamptz default now()
);

create table if not exists skill_updates (
  id         uuid primary key default gen_random_uuid(),
  skill_id   text not null references skills(id) on delete cascade,
  version    text not null,
  note       text not null,
  created_at timestamptz default now()
);

create table if not exists purchases (
  id                     uuid primary key default gen_random_uuid(),
  skill_id               text not null references skills(id),
  buyer_email            text not null,
  plan                   text not null check (plan in ('once','monthly','yearly')),
  stripe_session_id      text unique,
  stripe_customer_id     text,
  stripe_subscription_id text,
  amount_cents           int,
  currency               text default 'cad',
  status                 text not null default 'active' check (status in ('active','canceled','refunded','past_due')),
  current_period_end     timestamptz,
  created_at             timestamptz default now()
);
create index if not exists purchases_buyer on purchases (lower(buyer_email), skill_id);

create table if not exists downloads (
  id          uuid primary key default gen_random_uuid(),
  skill_id    text not null references skills(id),
  buyer_email text,
  created_at  timestamptz default now()
);

create table if not exists payouts (
  id          uuid primary key default gen_random_uuid(),
  creator     text not null references creators(handle),
  period      text not null,                          -- '2026-11'
  gross_cents int not null,
  fee_cents   int not null,
  net_cents   int not null,
  method      text,
  sent_to     text,
  status      text not null default 'pending' check (status in ('pending','sent','failed')),
  created_at  timestamptz default now(),
  sent_at     timestamptz
);

-- Lock everything down: only the service role (Netlify functions) reads or writes.
alter table creators      enable row level security;
alter table skills        enable row level security;
alter table skill_updates enable row level security;
alter table purchases     enable row level security;
alter table downloads     enable row level security;
alter table payouts       enable row level security;

-- Monthly payout statement per creator (80% of cleared sales).
create or replace view v_creator_month as
select s.creator, to_char(p.created_at, 'YYYY-MM') as period,
       sum(p.amount_cents) as gross_cents,
       round(sum(p.amount_cents) * 0.20) as fee_cents,
       round(sum(p.amount_cents) * 0.80) as net_cents,
       count(*) as sales
from purchases p join skills s on s.id = p.skill_id
where p.status in ('active','canceled') and p.created_at < now() - interval '14 days'
group by 1, 2;

-- Nov 8: profile link on creators + MCP waitlist
alter table creators add column if not exists url text;
alter table creators add column if not exists following int default 0;
alter table creators add column if not exists stocks int default 0;
alter table creators add column if not exists portfolio jsonb;   -- [{"t":"ZEQT","w":97.3}, …] allocation weights shown on the creator card
create table if not exists waitlist (
  id         bigserial primary key,
  email      text not null,
  mcp        text not null,
  created_at timestamptz default now(),
  unique (email, mcp)
);
alter table waitlist enable row level security;
