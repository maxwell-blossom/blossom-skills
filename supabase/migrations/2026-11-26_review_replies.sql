-- Nov 26: creators can reply to a review (one reply per review, editable). Run once in Supabase → SQL Editor (dev and prod).
-- Until this runs, the catalogue falls back to reading reviews without the reply columns, so nothing breaks — replies just can't be saved.
alter table reviews add column if not exists reply text;
alter table reviews add column if not exists replied_at timestamptz;
