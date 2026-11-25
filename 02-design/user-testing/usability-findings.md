
# Usability Findings — Prometheus / CareerCards

## 1. Testing goal

We want to understand whether students can review five job opportunities and make Apply/Skip decisions quickly, without repeatedly opening the original job advertisements.

Our assumption is that short, relevant job cards help students decide faster.

The target users are students looking for internships or entry-level opportunities.

## 2. Frozen testing task

The task comes from `02-design/user-testing/test-plan.md`:

> Here are five job posts on paper cards. For each one, tell me out loud whether you would apply or skip it, and why. Use only the cards. The envelope has the full post, but you can only open it if you really need it.

For the clickable prototype, requesting the original job advertisement counts as opening the envelope.

### PASS criteria

A participant passes only if all three conditions are met:

1. They finish all five decisions within five minutes.
2. They request the original job post for no more than one card.
3. They say they would still need to check the original post before deciding for no more than one card.

Otherwise, the session is marked FAIL.

If at least three of five completed sessions fail, the team should reconsider the assumption and investigate removing irrelevant or duplicate opportunities.

## 3. Session records

The team identified three participants for usability testing. The records below preserve the planned participants and testing responsibilities.

### Session 1 — T1

**Participant:** Third-year student and job seeker  
**Source:** Interview 07  
**Planned runner:** AP  
**Planned logger:** MG

| Measurement | Result |
|---|---|
| Actual testing date | Not documented |
| Device / prototype | Not documented |
| Actual runner and logger | Not documented |
| Time to first interaction | Not documented |
| Time to five decisions | Not documented |
| Original job posts requested | Not documented |
| Posts they would still check | Not documented |
| Predicted mistake observed | Not documented |
| PASS / FAIL | Not assessed |

**Observed behavior:** Original session notes are required.

**Participant feedback:** No verified quotation is available.

**What we learned:** Cannot draw a participant-specific conclusion without the actual observations.

### Session 2 — T2

**Participant:** Second-year student and job seeker  
**Source:** Interview 08  
**Planned runner:** AP  
**Planned logger:** AS

| Measurement | Result |
|---|---|
| Actual testing date | Not documented |
| Device / prototype | Not documented |
| Actual runner and logger | Not documented |
| Time to first interaction | Not documented |
| Time to five decisions | Not documented |
| Original job posts requested | Not documented |
| Posts they would still check | Not documented |
| Predicted mistake observed | Not documented |
| PASS / FAIL | Not assessed |

**Observed behavior:** Original session notes are required.

**Participant feedback:** No verified quotation is available.

**What we learned:** Cannot draw a participant-specific conclusion without the actual observations.

### Session 3 — T3

**Participant:** Management student and job seeker  
**Source:** Interview 01  
**Planned runner:** AS  
**Planned logger:** AP

| Measurement | Result |
|---|---|
| Actual testing date | Not documented |
| Device / prototype | Not documented |
| Actual runner and logger | Not documented |
| Time to first interaction | Not documented |
| Time to five decisions | Not documented |
| Original job posts requested | Not documented |
| Posts they would still check | Not documented |
| Predicted mistake observed | Not documented |
| PASS / FAIL | Not assessed |

**Observed behavior:** Original session notes are required.

**Participant feedback:** No verified quotation is available.

**What we learned:** Cannot draw a participant-specific conclusion without the actual observations.

## 4. Additional evidence — Production walkthrough

A separate production walkthrough was documented by teammate ST in his individual Homework 2.

**Date:** November 24, 2026  
**Tester:** ST  
**Environment:** Railway production deployment

The teammate reported that:

- The production URL loaded.
- Five job cards appeared.
- Apply/Skip interactions worked.
- The student journey reached the final apply list.
- Five deadlines appeared in the resulting list.

This supports the team's claim that the deployed product can complete its primary journey.

However, this was an internal teammate walkthrough, not one of the three required participant usability sessions.

It also does not establish whether browser analytics events were captured in PostHog.

**Evidence source:** `members/tabukashvilisaba/hw2.md` (or the teammate's submitted HW2 file).

## 5. Findings and limitations

### Finding 1 — The production journey was demonstrated

The teammate walkthrough provides evidence that the live product was able to display opportunities and complete the Apply/Skip journey.

### Finding 2 — Usability remains unverified

The repository does not yet contain participant timings, observed difficulties, original-post request counts, or verified PASS/FAIL results.

We therefore cannot determine whether students can reliably complete the five decisions within five minutes.

### Finding 3 — Analytics require separate verification

The team must confirm whether production events are arriving in PostHog, particularly:

- `student_opens_card_set`
- `student_views_card`
- `student_decides_card`
- `student_completes_card_set`

Production functionality alone does not establish successful event tracking.

## 6. Decision against the frozen rule

| Measure | Current evidence |
|---|---|
| Required documented sessions | 3 |
| Completed session records | 0 |
| Verified PASS results | 0 |
| Verified FAIL results | 0 |
| Five-person decision threshold | 3 FAIL out of 5 |

**Decision:** Insufficient participant evidence to accept or reject the assumption.

The team should recover its original testing notes or conduct the missing sessions using the frozen task and criteria.

After recording the results, the team should update this file and append the corresponding evidence-based decision to `DECISIONS.md`.

## 7. Next actions

1. AP and MG: recover or conduct T1's session and record actual measurements.
2. AP and AS: recover or conduct T2's session and record actual measurements.
3. AS and AP: recover or conduct T3's session and record actual measurements.
4. Evaluate each documented session against the frozen PASS/FAIL criteria.
5. Check the final decision against the five-person rule when five sessions are available.
6. Record the resulting decision and evidence in `DECISIONS.md`.

**Current status:** Prototype testing is planned, the production journey has been demonstrated internally, and participant usability evidence is still incomplete.
