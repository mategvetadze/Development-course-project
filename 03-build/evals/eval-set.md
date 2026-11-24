# Eval set (starter)

## The feature, in four lines

**Input:** the full text of one job or internship post, in English, Georgian or Russian, pasted by the curator
**Grounded in:** only that post text
**Output:** the card fields (role, company, field, students_ok, experience, hours, pay, deadline) plus a list of fields the model was unsure about
**Approved by:** the curator (AS), who checks and edits every field before the card is published; nothing reaches a student without that

**The number from our readout that should move if it works:** minutes for the curator to publish five cards, and student_completes_card_set once real students use the page. We do not have a baseline for either yet: AS times the next five cards by hand before the model is used.

**Version zero lives at:** 03-build/evals/prompt-v0.md

## Cases

Sources: where a case comes from an interview log, the input is rebuilt from what the participant described, because we did not save the original post. Before Lab 9, each of these is replaced with a real post of the same kind copied from jobs.ge, hr.ge or LinkedIn, and the Source column says so.

| # | Source | Input, exactly as it would arrive | Facts that were true at the time | A good output must |
|---|---|---|---|---|
| 01 | Log 06 | "Junior Legal Assistant. Requirements: law degree, 3 years of experience in a law firm, English B2." | 3 years required; nothing about students | experience "3 years"; students_ok "not stated" or "no"; never "none" |
| 02 | Log 07 | "We are hiring a Junior Developer! Send your CV." | Post gives no experience; the employer later said experience was needed | experience "not stated"; never "none"; "experience" in unclear |
| 03 | Log 10 | "Junior Java Developer. 2+ years of commercial experience with Spring." | 2+ years required | experience "2+ years" |
| 04 | Log 11 | "Junior Backend Engineer: Kubernetes, Kafka, microservices, 1–2 years of experience." | 1–2 years required | experience "1–2 years"; role kept as written |
| 05 | Log 09 | "Office manager. 6 days a week in the office, Georgian, English and Russian, 5+ years of experience, leadership skills. Salary 1500 GEL." | Pay stated; 5+ years | pay "1500 GEL"; experience "5+ years"; hours mention 6 days |
| 06 | Log 08 | "Marketing intern wanted! Write to us on Facebook for details." | No pay, no hours | pay "not stated"; hours "not stated"; never invent either |
| 07 | Log 10 | "Internship (unpaid), full-time, 3 months." | Unpaid, full-time | pay "unpaid"; hours "full-time"; never a number for pay |
| 08 | Log 04 | "TBC IT Academy: free 3-month course. Best graduates get a job offer. Apply by 10 December." | It is a course, not a job | role keeps the word "course"; deadline "2026-12-10"; never call it a paid job |
| 09 | Edge | "სტაჟიორი მარკეტინგში. სტუდენტებს შეუძლიათ განაცხადის გაკეთება. ნახევარი განაკვეთი. ანაზღაურება 600 ლარი." (Georgian: marketing intern; students can apply; part-time; pay 600 GEL) | Students OK; part-time; 600 GEL | fields in English; students_ok "yes"; pay "600 GEL"; hours "part-time" |
| 10 | Edge | "Requirements: completed bachelor's degree. Final-year students will not be considered. Junior Analyst." | Students cannot apply | students_ok "no" |

**The worst thing this feature could say confidently and wrongly, and the case numbers that test it:** students_ok "yes" or experience "none" when the post requires years of experience or a finished degree. A student would apply and be rejected, which is exactly what happened to log 07. Cases 01, 02, 03, 04 and 10.

## Checks (drafted in the Week 9 session, finished in Lab 9)

| Check | Kind | Passes when |
|---|---|---|
| No false "none" | code | experience is not "none" whenever the post contains a number followed by "year" |
| No invented pay | code | pay is "not stated" whenever the post contains no number and no "unpaid" |
| Fields match the post | judge, spot-checked by AS | every field value can be pointed to in the post text |

## The DECISIONS.md line

Wk8 · AI feature: fill the card fields (students OK, experience, hours, pay, deadline) from a pasted job post, so hidden requirements in "junior" posts show on the card; the curator approves every card before it is published · evidence: 03-build/evals/eval-set.md, logs 06, 07, 08, 10, 11 · owner: ST
