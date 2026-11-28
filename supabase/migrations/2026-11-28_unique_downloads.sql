-- Nov 28: from here on the download count is distinct people, not hits (Max: creators must not be able to buff their stats).
-- downloads.viewer identifies who downloaded: e:<email> for buyers, u:<blossom user id> when signed in, d:<salted device hash> otherwise.
alter table downloads add column if not exists viewer text;
-- Rows logged before this keep counting one each, so no creator sees their number drop (Max, Nov 28); only new downloads dedupe.
update downloads set viewer = 'legacy:' || id::text where viewer is null;
create index if not exists downloads_skill_viewer on downloads (skill_id, viewer);
create or replace function download_count(sid text) returns integer language sql stable as $$
  select count(distinct viewer)::int from downloads where skill_id = sid
$$;
