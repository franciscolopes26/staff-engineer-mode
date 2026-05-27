# Communication templates

Code is half the work. The artifacts around it — commit messages, PR descriptions, design docs, incident reports — are where the team's shared understanding lives. Tight templates, used consistently, are a multiplier; absent or sloppy ones are a tax.

## Commit message

```
<verb-tense subject, ≤72 chars, no trailing period>

<one paragraph WHY this change exists. NOT what changed — the
diff shows what. Why was it necessary? What user-visible problem
does it solve? What constraint forced this shape?>

<optional: trade-offs the change accepts, if non-trivial>
<optional: ticket / issue reference>
```

**Good:**

```
fix: resend-invoice endpoint loses audit row on SMTP failure

The previous implementation called mailer.send() inside the DB
transaction. When SMTP timed out (~5s), the transaction also
rolled back — the email was dispatched but no audit row existed.
On the next reconciliation pass, the system thought the resend
never happened and dispatched again, double-mailing the customer.

This moves the dispatch to an after-commit hook. The audit row
is now written atomically; the email is dispatched best-effort
with retry. Cost: a small window where the audit says "initiated"
but no email arrives — reconciliation handles it.

Closes BILL-1423.
```

**Bad:**

```
Fix bug in invoice resend
```

(Says nothing future-you can use. Forces the next reader to read the diff to learn the intent.)

## PR description

```
## What
<one or two sentences of what THIS PR does — not background>

## Why
<the problem / motivation; link to ticket if any>

## How
<short tour of the approach — key decisions, not every file>
<if a decision record exists, link it: see scripts/decisions.md>

## Verification
<DONE REPORT format from scripts/calibrate.md>
<list of: VERIFIED / TESTED / ASSUMED / NOT-CHECKED>

## Reversibility
<reversible / partially / no — and the back-out plan if relevant>

## Risk
<one paragraph: how could this break in production?>
<what's the blast radius? who's on call this week?>
```

## Design doc skeleton

```
# <feature / system> — Design

## Problem
<the user-visible / business problem in one paragraph>

## Constraints
<deadline, team size, dependencies, regulations, performance budget>

## Goals & non-goals
GOALS:
  - <thing this design must achieve>
NON-GOALS:
  - <thing this design explicitly DOES NOT solve — to bound scope>

## Options considered
A. <approach>  — pros / cons / cost estimate
B. <approach>  — pros / cons / cost estimate
C. <do nothing>  — what's the cost of NOT solving this?

## Recommended choice
<A / B / C> — because <evidence-based reasoning>

## Trade-offs accepted
<the costs we are knowingly taking on>

## Risks & failure modes
<from scripts/pre-mortem.md — failure modes and how we handle them>

## Reversibility / migration
<if we ship this and it's wrong, what's the cost to back out?>

## Open questions
<things we don't know yet; what's needed to resolve each>
```

## Incident / post-mortem skeleton

Blameless — the question is "what made this failure mode possible?" not "whose fault was it?"

```
# <date> — <one-line summary of the incident>

## Impact
<user-visible: how many users / requests / how long / what failed>

## Timeline (UTC)
HH:MM — <event>
HH:MM — <event>
HH:MM — <detected by ___>
HH:MM — <mitigated>
HH:MM — <resolved>

## What happened
<3-5 sentences. The actual mechanism. No blame; just the chain
of events that produced the failure.>

## Root cause
<the underlying condition that made this possible — usually NOT
the proximate change, but the gap that let the proximate change
have this effect (missing test, missing alarm, missing review,
shared mutable state, etc.)>

## What went well
<detection? mitigation? response coordination? — name it so we
keep doing it>

## What didn't
<the friction; the things that slowed detection or mitigation>

## Action items
- [ ] <fix the root cause, not just the proximate symptom>  (owner, date)
- [ ] <add the alarm / test that would have caught this>     (owner, date)
- [ ] <document the surprise so the next person knows>       (owner, date)

## Lessons
<what this incident teaches about how the system fails>
```

## The principle

Bad writing is a tax on every future reader. Good writing is leverage — a senior engineer's PR description saves the reviewer 20 minutes; a thousand reviews compound. The template costs you 3 minutes once.

References:
- @references/software-engineering-at-google.md — knowledge sharing scales the org
- @references/pragmatic-programmer.md — Tip 1 (care about your craft)
