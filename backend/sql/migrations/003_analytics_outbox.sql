-- Apply after 002. Outbox messages commit atomically with application rows.
begin;
set local lock_timeout = '5s';
create table analytics_outbox (
  id uuid primary key default gen_random_uuid(),
  distinct_id text not null,
  event text not null check (event in
    ('curator_publishes_card_set','student_decides_card','student_completes_card_set')),
  properties jsonb not null,
  occurred_at timestamptz not null default clock_timestamp(),
  delivered_at timestamptz,
  attempts int not null default 0 check (attempts >= 0),
  last_error text,
  next_attempt_at timestamptz not null default clock_timestamp()
);
create index analytics_outbox_pending_idx on analytics_outbox(next_attempt_at, occurred_at) where delivered_at is null;
commit;
