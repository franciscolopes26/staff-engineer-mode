# Verification checklist by surface (Phase 5)

`tsc` says "the types fit". `jest` says "the assertions I wrote pass". **Neither says "the feature works."** Pick the row that matches what you changed and execute it.

## UI change

```
[ ] Dev server running, app loads
[ ] Open the page I changed; perform the new action
[ ] Watch the Network tab — request fires? response shape correct?
[ ] Watch the console — no errors, no warnings I introduced
[ ] Happy path works
[ ] Try at least ONE edge case (empty state, error state, slow network)
[ ] Adjacent feature still works (smoke test for regressions)
[ ] Mobile / responsive checked if applicable
[ ] Keyboard navigation / accessibility unbroken
```

## HTTP endpoint

```
[ ] Hit it with curl (or equivalent)
[ ] Status code correct
[ ] Response body shape correct
[ ] Response headers correct (content-type, caching, CORS)
[ ] Auth failure path returns the right status (401 / 403, not 500)
[ ] Validation failure returns 400 with a useful message
[ ] One error path actually exercised (don't just trust the happy path)
```

## Background job / queue handler

```
[ ] Publish a real message (or trigger the local equivalent)
[ ] Confirm the handler ran (log line, DB row, side effect)
[ ] Confirm idempotency: publish the same message TWICE; same outcome?
[ ] Confirm retry behavior: simulate a failure mid-way; does the system recover?
[ ] Confirm the dead-letter / error path if the handler raises
```

## Library / pure function

```
[ ] Wrote the smallest possible CALLER that exercises the new behavior
[ ] Caller compiles AND produces the expected output
[ ] Tested at least one edge case the unit tests don't cover
[ ] Public API I just added is described in one sentence
  (if I can't describe it, the interface is wrong — Ousterhout)
```

## Migration / schema change

```
[ ] Applied on a copy of representative data (not just empty schema)
[ ] Rolled it back; rollback works
[ ] Re-applied; idempotent
[ ] Forward + backward compatibility: old code can still read new schema,
  new code can still read old schema (Kleppmann — data outlives code)
[ ] Time estimated on production-sized data
[ ] Online vs blocking checked (does it lock the table?)
```

## Config / infra change

```
[ ] Applied in a staging-equivalent environment first
[ ] Actual behavior observed, not just "plan looked OK"
[ ] Rollback path verified (can I undo this in <5 min?)
[ ] Blast radius understood (which services / users affected if wrong)
[ ] Monitored for at least one full failure interval after applying
```

## When you cannot verify

```
[ ] Said so explicitly to the user
[ ] Listed which surfaces are unverified and why
[ ] Did NOT claim "tested and working"
```

"I implemented and ran type-check + tests" is honest.
"I implemented and tested" — when you only ran `tsc` — is dishonest.

References:
- @references/working-effectively-with-legacy-code.md — "if it talks to a DB / network / file, it's not a unit test"
- @references/pragmatic-programmer.md — Tip 34 ("Prove it")
- @references/release-it.md — design for production, not for QA
