# Playbook: You're 3 Hours into a Bug and Stuck

**When:** Multiple attempted fixes have failed. The "obvious" cause turned out wrong. You feel pressure to try one more thing. The three-strike threshold has been crossed but you have not noticed.
**Goal:** Stop guessing. Get a deterministic reproducer. Then — and only then — fix the real cause.

## Phase 1 — read first
- STOP editing code. Close the editor tab where you were about to type another `console.log`.
- Write the symptom in one sentence: *what input produces what observed output, and what was expected*. If you cannot write this in one sentence, you do not understand the bug yet.
- List every hypothesis you have tried, what change you made for each, and what happened. Mark each as: **verified-wrong**, **verified-right**, or **guessed**. Use `@scripts/calibrate.md`.
- Count the **guessed** entries. If three or more, you are in RF-22; this playbook is mandatory, not optional.
- Re-read the failing code AND its callers AND `git log -p` for the last 30 days on the file and its immediate neighbors. Bugs are usually two layers up from the symptom (Hunt & Thomas, *The Pragmatic Programmer*).
- Read the logs from a *failing* invocation in full. Not the line you grepped — the whole request lifecycle.

## Phase 2 — contracts to surface
- Re-derive the contract of the function at the symptom site from its callers, not from its name. What do callers assume? What does the function actually guarantee?
- Identify the gap between assumed and actual contract — bugs live in that gap.
- Note every assumption you have been making implicitly: "this runs in one process", "the cache is fresh", "the user is authenticated", "this is called once per request". Mark each as verified or guessed.
- See `@scripts/contracts.md`.

## Phase 3 — failure modes you have not considered
- Caching layer (Redis, in-process LRU, HTTP cache, CDN) returning stale data — invisible in code review.
- Time zone / DST / `Date` parsing — especially around midnight UTC and quarter boundaries.
- Retry amplification: client retries × server retries × queue redelivery → N-fold side effects.
- Race between **cron jobs / scheduled tasks / consumers**, not just request handlers. The bug may only fire when two non-request workers overlap.
- Shared singleton / module-level state across requests in a long-lived Node process.
- At-least-once delivery (Rabbit, SQS) producing duplicate processing — idempotency assumed but not enforced.
- Connection pool exhaustion / slow query / replica lag causing a different code path to win.
- A feature flag, env var, or config row differing between environments. Diff the config, do not assume parity.
- Full enumeration: `@scripts/pre-mortem.md`.

## Phase 4 — change strategy
- **Minimal reproducer first.** Write the smallest test, script, or curl that reproduces the bug deterministically. Do not write another fix until you have one.
- If you cannot reproduce it, you cannot fix it — you can only hope. Spend the next hour on reproduction, not on guessing.
- Once reproduced: add a characterization test (Feathers, *Working Effectively with Legacy Code*) that pins the broken behavior in code. This is the test that turns red, then green.
- Revert every speculative "fix" still in your branch. They are noise and may be hiding the real bug (RF-05, RF-06).
- Change one variable at a time against the reproducer. Bisect.
- Reversibility: depends on the underlying fix; the *process* of this playbook is fully reversible — you have added only a test and reverted noise.

## Phase 5 — verification
- Run the reproducer 20 times after the fix. All green = real fix. Intermittent green = race still there (see `flaky-test.md`).
- Run the full test suite to confirm no regression elsewhere.
- Write one paragraph: *what the cause was, why earlier fixes missed it, what would have surfaced it sooner*. If you cannot, you do not understand the fix and may have patched a symptom (RF-06).
- Have a teammate read the paragraph and the diff, or rubber-duck it out loud. If the explanation doesn't survive a fresh listener, restart.
- See `@scripts/verify.md`.

## Red flags most common in this situation
- **RF-22 Third-Strike Loop** — this playbook exists because of RF-22. If you have failed three times, the next attempt without a reproducer will also fail.
- **RF-05 Patch-and-Hope** — adding null checks, try/catch swallows, and retries near the symptom site instead of finding the cause.
- **RF-06 Lookalike Fix** — applying a fix that resembles last week's fix because the stack trace looks similar; symptoms repeat, causes vary.

## Refusal scripts for common bad framings here
- "I just need to try ONE more thing" → "Have you reproduced it deterministically yet? If not, the next attempt is also a guess."
- "Let me add a try/catch around it and ship" → "That hides the bug from logs but it still fires in production. What is the actual cause?"
- "It works on my machine now" → "What changed between the failing run and this one? If you cannot name it, it is not fixed."
- "Customer is waiting, just ship the workaround" → "Ship a documented, time-boxed workaround with a ticket for the root cause. Do not call the workaround a fix."
- See `@scripts/refusal-scripts.md`.

## When this playbook is wrong
- The bug is a shallow logic error visible in the diff (off-by-one, wrong operator, swapped arguments) and you spot it on a fresh read — fix it directly, no marathon needed.
- The bug is a known infra incident affecting many services — escalate, do not debug in isolation.
- You are within the first 30 minutes and have not yet tried the obvious hypothesis once — finish a normal debugging pass before invoking this.

