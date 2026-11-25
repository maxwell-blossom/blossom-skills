-- Nov 24: ratings. One review per person per skill; skills.rating / skills.ratings are recomputed from here by netlify/functions/review.mjs.
-- Run once in Supabase → SQL Editor (dev and prod).
create table if not exists reviews (
  id         uuid primary key default gen_random_uuid(),
  skill_id   text not null references skills(id) on delete cascade,
  user_id    text not null,
  handle     text,
  stars      int not null check (stars between 1 and 5),
  body       text default '',
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  unique (skill_id, user_id)
);
alter table reviews enable row level security;
