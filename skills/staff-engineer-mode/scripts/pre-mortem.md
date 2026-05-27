# Pre-mortem template (Phase 3)

Paste this into your working notes before writing the happy path. For each failure mode, mark **H** (handle), **F** (fail fast), or **A** (knowingly accept). Mark **?** if you don't know — that's a Phase 1 gap.

```
FAILURE MODE                                            MODE     NOTES
═══════════════════════════════════════════════════════════════════════
Bad input                                               [ ]
  nil/null                                              [ ]
  empty                                                 [ ]
  malformed                                             [ ]
  hostile                                               [ ]
  oversized                                             [ ]

Bad state
  row/record missing                                    [ ]
  lock already held                                     [ ]
  cache stale                                           [ ]
  connection dropped                                    [ ]
  disk full                                             [ ]
  upstream unavailable                                  [ ]

Partial failure (step N of M fails)
  is the system recoverable?                            [ ]
  is there orphan state left behind?                    [ ]
  is the audit/log entry written before or after?       [ ]

Retry behavior (caller retries)
  is the operation idempotent?                          [ ]
  is there a dedupe key?                                [ ]
  what timeout does the caller use?                     [ ]

Concurrent caller (two callers, same moment)
  race on the same row?                                 [ ]
  double-charge / double-credit?                        [ ]
  lock ordering / deadlock?                             [ ]

Slow dependency (10ms expected → 30s actual)
  thread starvation                                     [ ]
  timeout configured?                                   [ ]
  circuit breaker around it?                            [ ]

Time-of-check / time-of-use (TOCTOU)
  did X change between when we checked and when we used? [ ]

Trust boundary
  input from internal code (trust)?                     [ ]
  input from network/user/file (validate)?              [ ]

Resource growth
  is there an unbounded queue/log/cache/table?          [ ]
  is there a cap and a purge?                           [ ]

Authorization
  is the check on every entry point?                    [ ]
  what happens on a permission throw?                   [ ]
```

## The three modes

- **H — Handle.** Recover and continue. Log it. (Retry with backoff, fall back, return default, surface a user-facing error.)
- **F — Fail fast.** Throw, exit, abort. Loud, immediate, debuggable. (Hunt & Thomas, Tip 38 — "Crash early.")
- **A — Accept.** Knowingly skip. Comment why. ("Two concurrent callers can both win; the merge step deduplicates.")

The mode forbidden by default: **swallow**. Empty catch blocks, ignored errors, "this can't happen" without proof. The most expensive bugs in production are not crashes — they are silent corruption.

## Stability primitives for remote calls

If any failure mode involves a network or process boundary, the default surface is:
- **Timeout** — every remote call has a deadline.
- **Circuit Breaker** — stop calling a failing dependency.
- **Bulkhead** — partition resources so one failure can't consume all.
- **Steady State** — cap and purge anything that accumulates.
- **Shed Load / Back-Pressure** — reject before you collapse.

References:
- @references/release-it.md — stability patterns and anti-patterns
- @references/designing-data-intensive-applications.md — at-least-once, idempotency
- @references/pragmatic-programmer.md — Tip 38 (crash early), Tip 34 (prove it)
