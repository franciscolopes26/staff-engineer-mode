# Playbook: Diagnose and Fix a Flaky Test

**When:** A test passes most of the time but fails intermittently; prior "fixes" added retries, `sleep`, timeout bumps, or `@flaky` markers.
**Goal:** Identify the underlying race / shared state / missing wait and remove it. Test runs green 100/100 times unattended.

## Phase 1 — read first
- Read the test top-to-bottom and the system-under-test entry point it calls. Note every `await`, timer, mock, and global it touches.
- Run the test in isolation 50 times: `pnpm test -- path/to/file.spec.ts --testNamePattern "<name>" --runInBand` then repeat in a loop. Capture failure rate.
- Run it with random test order and with `--runInBand` vs parallel. If it only fails in one mode, suspect shared state / ordering.
- `git log -p` the test file and the SUT — when did flakiness start? What landed near that commit?
- Grep for shared singletons, module-level caches, static maps, global timers, and DB/Redis state the test touches without a per-test reset.

## Phase 2 — contracts to surface
- What does the test *claim*? Restate as a single pre/post/invariant — often the test asserts on a side-effect that is eventually-consistent, not synchronous.
- Identify the actual happens-before edge the assertion depends on (DB write committed? event handler ran? cache invalidated?). If you cannot name it, the test is asserting on luck.
- Ordering: does the assertion run before, during, or after the async work completes? `await` returning is not the same as "side effect visible".
- See `@scripts/contracts.md` for the template.

## Phase 3 — failure modes specific to this situation
- Shared singleton / module-cache state leaking across tests: fail-fast — reset in `beforeEach`, not patch with retries.
- Missed `await` or fire-and-forget promise: handle — await it; if intentional fire-and-forget in prod, use a deterministic test hook.
- Time-of-check race (assert reads state before writer commits): handle — wait on the actual condition, not a `sleep`.
- Test-ordering dependency (passes alone, fails in suite): fail-fast — find the leaking test, fix isolation.
- Hidden filesystem / DB / Redis state across runs: handle — truncate or use a fresh schema/namespace per test.
- Network / RabbitMQ / gRPC mock gap: handle — assert the mock was called, don't poll.
- Clock / `Date.now()` / timezone: handle — inject a clock, never rely on wall time.
- Full enumeration: `@scripts/pre-mortem.md`.

## Phase 4 — change strategy
- Reproduce deterministically *before* changing anything. A characterization test (Feathers, *Working Effectively with Legacy Code*) that pins the current broken behavior makes the race observable.
- Remove every previously-added `setTimeout`, `sleep`, retry wrapper, and timeout bump. They are camouflage (RF-05).
- Replace polling with a deterministic wait: an event, a promise, a `waitFor(condition)` with a tight bound and a clear error.
- If shared state is the cause, isolate it (per-test container, fresh module via `jest.isolateModules`, transactional rollback) — do not "clean up after".
- One change at a time. If you fix two suspected causes in one commit and it passes, you don't know which one mattered (RF-02).
- Reversibility: local — contained to the test file plus possibly a small SUT fix. Easy to revert.

## Phase 5 — verification
- Run the test 100 times consecutively in CI parity mode (same node version, same parallelism). All green = fixed. Any red = not fixed.
- Run the full suite 10 times to confirm no cross-test regression.
- Observe: no new `sleep`, no new retry, no new `@flaky` annotation in the diff.
- See `@scripts/verify.md` for the surface checklist.

## Red flags most common in this situation
- **RF-05 Patch-and-Hope** — retries, sleeps, and timeout bumps are the canonical symptoms; if they're in the diff, the bug is still there.
- **RF-22 Third-Strike Loop** — three failed "fixes" on the same test means stop guessing and reproduce deterministically.
- **RF-09 Test-Driven False Positive** — green CI after adding a retry is not a passing test, it's a silenced one.

## Refusal scripts for common bad framings here
- "Just add `@flaky` / `test.retry(3)` and move on" → "That hides the race; it will fire in prod where there is no retry. What's the actual happens-before edge being violated?"
- "Bump the timeout from 5s to 30s" → "A correct test does not need 30s. What is it waiting for, and why isn't it observing that condition directly?"
- "Add a `setTimeout(100)` before the assertion" → "That is a guess about scheduler timing. Wait on the condition, not the clock."
- See `@scripts/refusal-scripts.md` for more.

## When this playbook is wrong
- The test is genuinely time-bound (asserting a 5-second debounce, a TTL expiry, a rate-limit window). Use a clock-injection playbook instead.
- The flakiness is in infrastructure (CI runner, container pull, external API), not the test logic — escalate to platform, do not "fix" the test.

