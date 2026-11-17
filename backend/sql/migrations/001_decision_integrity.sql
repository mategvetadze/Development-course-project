-- Run once BEFORE deploying the updated API, with database-owner approval.
-- Additive: no rows deleted or rewritten; historical timings remain NULL.
-- lock_timeout aborts the whole migration rather than blocking active writers.
begin;
set local lock_timeout = '5s';
alter table cards add constraint cards_set_id_id_key unique (set_id, id);
alter table decisions add column ms_total bigint check (ms_total >= 0);
alter table decisions add constraint decisions_card_set_fkey
  foreign key (set_id, card_id) references cards(set_id, id) on delete cascade
  not valid;
commit;

-- NOT VALID protects new writes while preserving any existing invalid rows.
-- Review this query before a separately approved repair/constraint validation:
-- select d.id, d.set_id, d.card_id from decisions d join cards c on c.id=d.card_id
-- where d.set_id <> c.set_id;
-- After resolving those rows: ALTER TABLE decisions VALIDATE CONSTRAINT decisions_card_set_fkey;
-- Updated completion/summary queries exclude mismatched historical rows.
