# Five-phase checklist

Paste this into your working notes. Check off as you go. Do not skip — when you find yourself wanting to, that's the signal you most need to slow down.

```
PHASE 1 — UNDERSTAND
  [ ] Read the function itself, every line
  [ ] Found all callers (grep / find references)
  [ ] Read at least 3 callers — how do they use the result?
  [ ] Read the tests for it — what behavior is locked in?
  [ ] Read git blame on the lines I'd touch
  [ ] I can describe what this code does in one sentence
  [ ] Chesterton's Fence: I understand why every check / branch exists
       (if not — investigate before removing)

PHASE 2 — SPECIFY (see @scripts/contracts.md for the template)
  [ ] Precondition stated
  [ ] Postcondition stated
  [ ] Invariant stated
  [ ] Idempotency considered
  [ ] Concurrency considered
  [ ] Ordering considered
  [ ] Atomicity considered
  [ ] Authorization considered
  [ ] Hyrum's Law: I know which observable behaviors are de-facto contract

PHASE 3 — PRE-MORTEM (see @scripts/pre-mortem.md)
  [ ] Failure modes enumerated
  [ ] Each failure mode classified: handle / fail-fast / accept
  [ ] No "swallow" mode used
  [ ] Every remote call has timeout AND circuit breaker
  [ ] Every accumulating resource has a cap AND a purge

PHASE 4 — CHANGE
  [ ] One concern per commit (no mixed diff)
  [ ] Two Hats: I am adding function OR refactoring — not both
  [ ] Refactored first if needed (prepare ground, then drop change)
  [ ] Each step compiles + tests green before the next
  [ ] Reversibility classified (see table in SKILL.md):
       local-reversible / shared-reversible / hard-to-reverse / irreversible
  [ ] Hard-to-reverse + irreversible: confirmed with user before acting

PHASE 5 — VERIFY (see @scripts/verify.md for surface-by-surface)
  [ ] Exercised the actual behavior end-to-end
  [ ] Tried at least one edge case
  [ ] Watched logs / network / DB for the side effect
  [ ] If I cannot verify, I said so out loud (did not claim done)
  [ ] Complexity budget: this change made the affected module deeper,
       not shallower (Ousterhout — simple interface, powerful inside)
  [ ] No silent catches, no unrelated TODOs, no dead code I introduced

FINAL
  [ ] No mixed diff
  [ ] Comments explain WHY, not WHAT
  [ ] Names tell the reader what / are search-friendly
  [ ] If I am about to declare done — am I willing to be paged for this at 3am?
```

## The 3-strike rule

After **three failed attempts** at the same fix, stop. The bug is not where you think it is. The framing is wrong.

- Strike 1: try the fix.
- Strike 2: re-read; try a different fix.
- Strike 3: re-read more; try a third fix.
- After strike 3: **stop fixing, return to Phase 1**. Re-investigate. State the problem back. Often the actual bug is two layers up from where the symptom appears.

Most "hard bugs" are hard because the model of the system was wrong, not because the fix is hard to write. (Hunt & Thomas — *Don't program by coincidence*.)
