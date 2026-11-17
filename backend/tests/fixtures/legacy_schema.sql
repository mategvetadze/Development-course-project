-- Production schema shape at ffd24e4, used to exercise the upgrade path.
create table card_sets (
  id uuid primary key default gen_random_uuid(),
  published_at timestamptz not null default now()
);
create table cards (
  id uuid primary key default gen_random_uuid(),
  set_id uuid not null references card_sets(id) on delete cascade,
  position int not null check (position between 1 and 5),
  role text not null, company text not null, field text not null, source text not null,
  source_url text not null, students_ok boolean not null, experience text not null,
  hours text not null, pay text not null, deadline date not null,
  unique (set_id, position)
);
create table decisions (
  id uuid primary key default gen_random_uuid(),
  set_id uuid not null references card_sets(id) on delete cascade,
  card_id uuid not null references cards(id) on delete cascade,
  anonymous_id text not null,
  decision text not null check (decision in ('apply', 'skip')),
  skip_reason text check (skip_reason is null or skip_reason in
    ('not_my_field', 'not_eligible', 'hours', 'pay', 'not_interested', 'other')),
  ms_on_card int, created_at timestamptz not null default now(),
  unique (set_id, card_id, anonymous_id)
);
