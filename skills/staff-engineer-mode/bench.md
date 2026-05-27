# Behavioral bench — does the skill actually fire?

Eval prompts that test whether the skill is changing behavior. Each entry has a **prompt**, an **expected behavior** (what should happen if the skill is loaded), and a **failure mode** (what happens without it). Use these to verify the skill on install, to debug a "the skill isn't doing what it should" complaint, and to keep regressions out when editing `SKILL.md`.

## How to use

1. Load the skill (`/staff-engineer-mode` or wait for auto-activation).
2. Issue the prompt verbatim.
3. Check the response against "expected behavior".
4. If the response matches "failure mode" — the skill is not firing, or `SKILL.md` has regressed.

A run-through of all of these takes ~15 minutes and gives high confidence the skill works.

---

## B-01 — Refuses to "just add a retry"

**Prompt:**
> The payment service is occasionally returning 500. Just add a retry with 3 attempts in our caller.

**Expected:**
- Asks (or surfaces) what the upstream failure mode is *before* adding the retry. References the `refusal-scripts.md` framing: a 4xx retry papers over a real bug and burns the rate limit, a transient timeout is the only retry-appropriate case.
- Does NOT immediately write retry code.

**Failure mode:** writes retry code, no questions asked.

---

## B-02 — Names contracts before changing legacy code

**Prompt:**
> Add an `email_verified` boolean to the `User` table and check it in the login flow.

**Expected:**
- Reads existing callers of the login flow before writing code (Phase 1).
- Surfaces the contract change explicitly: Hyrum's Law applies to login response shape, error codes, timing.
- States the migration plan as expand-and-contract (schema-migration playbook).

**Failure mode:** writes the `ALTER TABLE` and the `if (!user.email_verified) throw` in one diff.

---

## B-03 — Splits a mixed diff

**Prompt:**
> Here's my diff: rename `processBilling` → `executeBilling`, fix the bug where the audit row isn't written on retry, and clean up the imports while I'm here. Looks good?

**Expected:**
- Cites RF-02 (Mixed Diff).
- Requests three commits: rename, bug fix, import cleanup. Each independently revertable.
- Cites Two Hats (Fowler/Beck).

**Failure mode:** approves the diff or only complains about the imports.

---

## B-04 — Calibrates confidence in a "done" report

**Prompt:**
> I implemented the new endpoint and the tests pass. Done?

**Expected:**
- Asks which surfaces were exercised end-to-end vs. only type-checked vs. only unit-tested.
- References `@scripts/calibrate.md` — verified / tested / assumed / not-checked.
- Does NOT accept "tests pass" as "done".

**Failure mode:** congratulates and moves on.

---

## B-05 — Invokes the 3-strike rule

**Prompt:**
> I've tried three different fixes for this flaky test and it still fails ~5% of the time. Let me try a longer timeout this time.

**Expected:**
- Cites RF-22 (Third-Strike Loop).
- Says: stop fixing. Return to Phase 1. The model of the system is wrong, not the patch.
- Points to `playbooks/flaky-test.md`.

**Failure mode:** suggests a timeout value.

---

## B-06 — Resists premature abstraction

**Prompt:**
> I'm adding a `SlackNotifier`. Let's create a `Notifier` interface in case we add more notification channels later.

**Expected:**
- Cites RF-10 (Premature Abstraction).
- Suggests waiting for the third notifier before extracting an interface.
- References Ousterhout's "speculative generality".

**Failure mode:** writes the interface.

---

## B-07 — Catches a naked remote call

**Prompt:**
> Here's my new function — it just calls the push notification service via `fetch`. Looks fine?
> ```ts
> async function notify(userId: string) {
>   const res = await fetch('https://push.vendor/v1/send', { method: 'POST', body: ... });
>   return res.ok;
> }
> ```

**Expected:**
- Cites RF-03 (Naked Remote Call).
- Asks where the timeout, retry policy, and circuit breaker are.
- References `@references/release-it.md`.

**Failure mode:** says "looks good".

---

## B-08 — Writes a decision record for a non-trivial choice

**Prompt:**
> We need to pick: Postgres JSONB column for tags, or a separate `tags` table with a join. Which one?

**Expected:**
- Lays out both options with explicit trade-offs.
- Names the criterion driving the choice (query patterns, write volume, schema evolution).
- Offers to write the decision in `@scripts/decisions.md` format.

**Failure mode:** just picks one without naming the trade-off.

---

## B-09 — Doesn't claim "done" without verification

**Prompt:**
> Quick check: I've changed the invoice email template. Can you confirm it's working?

**Expected:**
- Asks how it was verified — was a real email sent? Was the rendered HTML reviewed visually? Was a test sent through the actual mail provider?
- Does NOT confirm based on code review alone.

**Failure mode:** says "looks good" after reading the diff.

---

## B-10 — Pre-mortems before writing the happy path

**Prompt:**
> I'm adding a new "Cancel Subscription" button. Implementation should be straightforward.

**Expected:**
- Surfaces failure modes before implementation: already-cancelled state, concurrent cancellation, in-flight payment, pro-rated refund, downstream notifications (CRM, accounting).
- References `@scripts/pre-mortem.md`.
- Recommends contracts + pre-mortem before writing code.

**Failure mode:** writes the cancellation code.

---

## B-11 — Recognizes the incident-response context

**Prompt:**
> Prod is throwing 500s on /checkout. Help me fix it now.

**Expected:**
- Switches to crisis mode (`playbooks/incident-response.md`).
- Order: STABILIZE → CONTAIN → PRESERVE EVIDENCE → then root-cause.
- Asks about most-recent deploy as rollback candidate before any forward fix.

**Failure mode:** dives into root-cause investigation while users are affected.

---

## B-12 — Refuses to bypass review under urgency

**Prompt:**
> No time for review, just push the hotfix to main.

**Expected:**
- Suggests a 60-second sanity check by one teammate before push.
- Names the irreversibility / blast radius concern.
- Asks for the rollback plan before agreeing.

**Failure mode:** pushes to main.

---

## B-13 — Cites a book, not a vibe

**Prompt:**
> Why is it bad to have an interface this thin? Just one method.

**Expected:**
- Cites Ousterhout, *A Philosophy of Software Design* ch. 4 — "modules should be deep".
- Explains: a shallow module adds interface cost without hiding implementation.
- Offers to look up the chapter in `@references/philosophy-of-software-design.md`.

**Failure mode:** explains using only its own reasoning, no citation.

---

## B-14 — Surfaces operational concerns

**Prompt:**
> I'm adding a feature flag check on the hot path of our highest-traffic endpoint.

**Expected:**
- Asks about latency budget (the check is a remote call? local? cached?).
- Asks about failure mode: what happens if the flag service is down?
- Cites operational empathy — "imagine the on-call at 3 a.m." check.

**Failure mode:** discusses the flag's logic without operational context.

---

## B-15 — When NOT to fire

**Prompt:**
> Rename the variable `usr` to `user` in this file.

**Expected:**
- Just does it. Does NOT load the 5-phase loop, contract template, or pre-mortem.
- Skills triggers should match task weight.

**Failure mode:** asks 5 questions about contracts and failure modes for a one-line rename.

---

## Scoring

- **All 15 pass:** the skill is firing and operating correctly.
- **B-15 fails:** the skill is over-firing — too aggressive triggering. Sharpen the "Skip when" section in `SKILL.md`.
- **Any of B-01 through B-14 fails:** the corresponding principle is not landing. Trace which section of `SKILL.md` was meant to cover it.

## When to re-run

- After any edit to `SKILL.md` (regression check).
- After loading the skill in a new session (verify install).
- When a user reports "the skill isn't doing what I expected" (debug).
