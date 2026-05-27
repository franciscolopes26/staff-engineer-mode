# Confidence calibration — how to report "done"

The difference between a senior engineer and a junior is not what they verified — it's how honestly they report what they didn't.

When declaring a change done, classify each claim into one of four levels. State the level explicitly. Never collapse the levels — "tested and working" is a lie when only `tsc` ran.

## The four levels

| Level | Meaning | Example phrasing |
|-------|---------|------------------|
| **Verified** | I exercised this behavior end-to-end and observed it work | "Verified — clicked the button in dev, saw the email in mailhog, audit row written" |
| **Tested** | The unit/integration test I wrote passes — but I did not exercise the surface myself | "Tested — unit tests green; did not exercise the HTTP endpoint directly" |
| **Assumed** | I followed a pattern I trust, but did not verify this specific instance | "Assumed — followed the existing pattern in `BillingService`; not specifically verified" |
| **Not-checked** | I did not look at this; it might be broken | "Not-checked — admin permission path not exercised; please verify before merging" |

A complete "done" report names where each level applies. Skipping the not-checked line is the dishonest move.

## The four-level template

```
DONE REPORT — <feature / fix>

VERIFIED:     [thing 1 — how I verified]
              [thing 2 — how I verified]

TESTED:       [thing — what tests; what was NOT covered]

ASSUMED:      [thing — based on what assumption]

NOT-CHECKED:  [thing — why; who should verify]

REVERSIBILITY: <if shipping is reversible, say so; if not, name the back-out>
```

## When everything is verified

State that explicitly. "All four surfaces verified end-to-end (UI, DB, audit, email)" — three words. Calibration is not pessimism; it's accuracy.

## When you cannot verify a surface

Say so up-front, not after the fact. "I cannot reach the admin UI from this environment, so the admin-permission path is **not-checked**. Recommend a manual smoke test before merge."

## Why this matters

The team's trust in your "done" reports is a finite resource. Every false positive ("I tested it" → it was broken) drains the budget faster than you think. Calibrated reports earn the right to ship faster next time, because they are believed.

This is what makes a C-level engineer different from a competent one: **the senior makes others' decisions easier by accurately reporting what they know and don't know.** A vague "looks good" forces the reviewer to redo the work; a calibrated report tells them exactly where to look.

References:
- @references/pragmatic-programmer.md — Tip 34 (prove it), Tip 62 (don't program by coincidence)
- @references/working-effectively-with-legacy-code.md — what counts as a unit test
- @references/software-engineering-at-google.md — evidence-based reporting
