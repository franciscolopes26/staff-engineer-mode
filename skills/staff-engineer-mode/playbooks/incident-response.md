# Playbook: Production Incident Response

**When:** prod is broken or degraded, users are affected, time pressure is real.
**Goal:** restore service first; learn second; preserve evidence throughout.

The 5-phase loop **does not disappear** under pressure — it compresses. Skipping a phase under time pressure is how a 5-minute outage becomes a 5-day cascade.

## Crisis-mode loop (compressed, in this order)

1. **STABILIZE** — restore service. Roll back, disable feature flag, scale up, shed load. **Do not investigate root cause yet.**
2. **CONTAIN** — limit blast radius. Stop the bleeding even if you don't yet know the cause.
3. **PRESERVE EVIDENCE** — snapshot logs, save the bad data sample, capture metrics over the incident window. *Before* anything mutates.
4. **THEN apply Phases 1–5** to the actual fix.

## Phase 1 — read first (5 minutes max)

- Last 3 deploys / config changes in the affected service — `git log --since="2 hours ago"`.
- Recent alerts: which fired, when, what changed in their values.
- The error itself: not just the message, the **trace + the input that triggered it**.
- One log line of a passing request next to one of a failing — diff them.

## Phase 2 — contracts to surface

- What promise is broken right now? (200 → 500, 1s → 30s, success → silent skip.)
- What's downstream relying on it? (Hyrum's Law applies under fire too.)
- Is the failure binary (everything broken) or partial (1% / one tenant)?

## Phase 3 — failure modes specific to incidents

- **Cascading**: integration point failure starves a thread pool → upstream service collapses. Stop the chain. *(Release It! — Chain Reaction.)*
- **Retry storm**: clients retry, multiplying load on a struggling service. Shed load BEFORE adding capacity.
- **Caching staleness**: a deploy invalidated a cache but downstream still hits the bad keys. Flush carefully — flush can amplify load.
- **Migration in flight**: a partial schema migration left rows in an inconsistent state. Halt the migration before fixing.

## Phase 4 — change strategy (in priority order)

1. **Rollback** if the cause is the most recent deploy. Always cheaper than a forward fix.
2. **Feature flag off** if you can disable the bad code path without rolling back.
3. **Configuration mitigation** — raise a timeout, lower a rate, increase a pool size — *if* you understand the trade-off.
4. **Forward fix** — only if the above don't apply.

**Reversibility:** every incident action is HARD-TO-REVERSE under time pressure (you may not have the cycles to undo a wrong move). Treat with disproportionate care. Have a peer confirm before the irreversible step.

## Phase 5 — verification

- Watch the same dashboards that showed the failure return to baseline.
- Issue a synthetic test (curl, replay) against the recovered path.
- Wait **at least one full failure interval** before declaring "resolved" — premature all-clears are the second-most-common incident failure.

## Red flags most common in incidents

- **RF-05** (Patch-and-Hope) — under pressure, the temptation to "just make the error go away" without root cause is overwhelming.
- **RF-18** (Authorization Drift) — "we approved a hotfix path, so I'll use it for the next thing too". No — every irreversible action is its own approval.
- **RF-08** (It Compiles, Ship It) — under pressure, "tests pass" gets accepted as "feature works". Don't.
- **RF-22** (Third-Strike Loop) — three failed mitigations in a row means the model is wrong. Stop and re-investigate, even mid-incident.

## Refusal scripts for common bad framings

- "Just deploy the fix to prod" → "What's the rollback if this is wrong? If you can't answer in one sentence, we ship to a canary first."
- "We don't have time to write a test" → "We have time to roll back twice or write the test once. Which is cheaper this hour?"
- "Skip the review, it's urgent" → "Send the diff to one person for a 60-second sanity check while you prep the deploy. Costs nothing; catches the obvious."
- "Trust me, it's the same as last time" → "What's the one thing that's different? If it's truly the same, the same fix is a 30-second confirmation."

## After the incident

Use `@scripts/communication.md` post-mortem skeleton. Capture in writing (within 24h):
- The proximate cause (the change that triggered it).
- The **root cause** (the gap that allowed the proximate change to have this effect — usually a missing test, alarm, or review).
- What went well, what didn't, three action items with owners and dates.

Blameless — the question is "what made this failure mode possible?", not "whose fault was it?"

## When this playbook is wrong

- The "incident" is a non-urgent bug report — use the normal 5-phase loop, not crisis mode.
- The system is fundamentally untrustworthy and rollback is risky — escalate to senior on-call before acting.
