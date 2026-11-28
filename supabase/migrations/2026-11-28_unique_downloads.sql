-- Nov 28: the download count is distinct people, not hits (Max: creators must not be able to buff their stats).
-- downloads.viewer identifies who downloaded: e:<email> for buyers, u:<blossom user id> when signed in, d:<salted device hash> otherwise.
alter table downloads add column if not exists viewer text;
-- Rows logged before this kept no identity for free downloads, so repeat hits within the same 10 minutes count as one person.
update downloads set viewer = coalesce('e:' || lower(buyer_email), 'legacy:' || floor(extract(epoch from created_at) / 600)::text) where viewer is null;
create index if not exists downloads_skill_viewer on downloads (skill_id, viewer);
create or replace function download_count(sid text) returns integer language sql stable as $$
  select count(distinct viewer)::int from downloads where skill_id = sid
$$;
-- Recount every live listing from the log (unlisted demo rows keep their seeded numbers).
update skills s set downloads = (select count(distinct d.viewer) from downloads d where d.skill_id = s.id) where s.status = 'live';
