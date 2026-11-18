-- Apply after 001, before deploying the API. No historical timing is invented.
begin;
set local lock_timeout = '5s';

create table student_set_sessions (
  set_id uuid not null references card_sets(id) on delete cascade,
  anonymous_id text not null,
  started_at timestamptz,
  environment text not null check (environment in ('development','test','preview','production')),
  is_internal boolean not null,
  primary key (set_id, anonymous_id)
);

create table card_set_completions (
  id uuid primary key default gen_random_uuid(),
  set_id uuid not null,
  anonymous_id text not null,
  started_at timestamptz,
  completed_at timestamptz not null,
  ms_total bigint generated always as
    (ceil(extract(epoch from (completed_at - started_at)) * 1000)::bigint) stored,
  qualifies boolean generated always as
    (started_at is not null and completed_at - started_at <= interval '5 minutes') stored,
  apply_count int not null check (apply_count between 0 and 5),
  skip_count int not null check (skip_count between 0 and 5),
  environment text not null check (environment in ('development','test','preview','production')),
  is_internal boolean not null,
  check (apply_count + skip_count = 5),
  check (started_at is null or completed_at >= started_at),
  unique (set_id, anonymous_id),
  foreign key (set_id, anonymous_id) references student_set_sessions(set_id, anonymous_id) on delete cascade
);
create index card_set_completions_window_idx on card_set_completions(environment, completed_at);
commit;

-- Existing decisions/NULL client timings are left untouched. Only new, timed
-- journeys can qualify; do not replay/backfill historical success events.
