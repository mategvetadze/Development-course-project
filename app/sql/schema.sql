-- Paste into Neon SQL Editor (Sprint 1)

create table if not exists card_sets (
  id uuid primary key default gen_random_uuid(),
  published_at timestamptz not null default now()
);

create table if not exists cards (
  id uuid primary key default gen_random_uuid(),
  set_id uuid not null references card_sets(id) on delete cascade,
  position int not null check (position between 1 and 5),
  role text not null,
  company text not null,
  field text not null,
  source text not null,
  source_url text not null,
  students_ok boolean not null,
  experience text not null,
  hours text not null,
  pay text not null,
  deadline date not null,
  unique (set_id, position),
  unique (set_id, id)
);

create table if not exists decisions (
  id uuid primary key default gen_random_uuid(),
  set_id uuid not null references card_sets(id) on delete cascade,
  card_id uuid not null references cards(id) on delete cascade,
  anonymous_id text not null,
  decision text not null check (decision in ('apply', 'skip')),
  skip_reason text check (
    skip_reason is null
    or skip_reason in ('not_my_field', 'not_eligible', 'hours', 'pay', 'not_interested', 'other')
  ),
  ms_on_card int,
  ms_total bigint check (ms_total >= 0),
  created_at timestamptz not null default now(),
  unique (set_id, card_id, anonymous_id),
  constraint decisions_card_set_fkey foreign key (set_id, card_id)
    references cards(set_id, id) on delete cascade
);

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
