# MVP Boundary — Prometheus / CareerCards

**Value hypothesis under test:** A Georgian university student searching for an internship or entry-level job can make an apply-or-skip decision on five curated openings in under five minutes when eligibility, experience, hours, pay and deadlines are visible together, rather than checking scattered full posts. Evidence: `01-discovery/problem-statement.md` (interview logs 01, 04, 06, 07, 08, 09) and `02-design/prototype-plan.md`.

**The one person walking this journey:** **Nino**, the third-year university student looking for her first internship or entry-level role, in `00-foundation/icp.md`.

**Team initials:** MG = Mate Gvetadze; AP = Ani Purtskhvanidze; AS = Archil Sanikidze; ST = Saba Tabukashvili (`00-foundation/team-contract.md`).

## The journey

1. **Curator (AS for content; MG for publishing feature)** selects five real student-eligible openings, checks source links and key facts, removes duplicates, and publishes one card set.
2. **Nino** opens a shared link on her phone and sees five cards together.
3. **Nino** reads each card's role, employer, field, student eligibility, experience, hours, pay, source and deadline without opening the original listing.
4. **Nino** selects **Apply** (opens the source listing) or **Skip** (records a reason) once for each card.
5. **Nino** completes all five choices and sees an apply list with source links and deadlines, or an explicit message if she skipped everything.

**Why this is complete:** Nino has decided what to pursue, can open the selected original listings to apply, and can see the deadlines; the MVP does **not** claim to submit applications for her.

**Why this is smallest:** Removing manual curation from step 1 risks unclear eligibility and duplicate posts, the friction reported in logs 01, 06, 07 and 08. Removing the completion summary from step 5 also removes the observable all-five-decisions north star.

## Cut list

| Feature | Reason tied to evidence/value hypothesis | Comes back when |
|---|---|---|
| Automatic job scraping and deduplication | Five hand-curated cards are sufficient to test whether clear facts drive decisions; log 08 reported duplicates | Curating five current cards becomes a bottleneck |
| Field-specific feeds / field picker | ICP v2 spans several study fields; the `not_my_field` skip reason provides a demand signal | Skips for `not_my_field` show the mixed set is ineffective |
| Student accounts and saved profiles | No sign-in is needed to decide on five openings; anonymous decisions are sufficient for this experiment | Repeat visits require cross-device saving |
| Notifications, reminders, email/SMS/WhatsApp | Deadlines matter (logs 01, 03, 04, 06, 07, 08), but this sprint tests quick decisions; logs 08 and 10 describe ignored alerts | Test results show seeing the deadline alone is insufficient |
| Search, sorting and filters | Five preselected cards avoid the large-list sorting pain described in logs 01 and 07 | The weekly set becomes too large to scan easily |
| Courses, hackathons and clinics | The tested hypothesis concerns internships and entry-level openings, not the wider opportunity market | Discovery evidence establishes demand for these categories |
| In-app applications, CV builder | The experiment tests deciding, not executing employer applications; CV concerns are not the dominant pattern | New interviews/test sessions make either essential |
| AI recommendations | No personalization is necessary for a five-card decision experiment | Real skip data demonstrates an actionable matching problem |
| Employer-facing posting portal | No employer validation supports a second-sided workflow yet | Student value is confirmed and employer discovery is conducted |
| Salary fairness scoring and foreign job discovery | Neither belongs to the current card-based eligibility/decision hypothesis (`DECISIONS.md` Wk3; log 02) | Evidence changes the tested problem |

## Step to event

These names are copied exactly from `03-build/analytics/event-schema.md`.

| Step | Event (actor_verb_object) | In the schema? |
|---|---|---|
| 1 | `curator_publishes_card_set` | yes |
| 2 | `student_opens_card_set` | yes |
| 3 | `student_views_card` | yes |
| 4 | `student_decides_card` | yes |
| 5 | `student_completes_card_set` | yes |

**North star step:** **5** — count `student_completes_card_set` events with `ms_total <= 300000`, per week (`DECISIONS.md` Wk5). The event fires once after the fifth saved decision. Five decisions alone are not counted as success if the total time exceeds five minutes.

## The DECISIONS.md line

`Wk6 · MVP boundary: 5-step journey (curator publishes five cards to Nino completes five apply-or-skip decisions and sees an apply list); cut scraping, sign-in, reminders, field picker, search/filters · evidence: 03-build/mvp-boundary.md, 01-discovery/problem-statement.md, interview logs 01, 06, 07, 08, 02-design/prototype-plan.md · owner: MG`
