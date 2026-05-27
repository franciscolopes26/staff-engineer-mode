# Contract template (Phase 2)

Paste this into your working notes before changing a non-trivial function. Fill it in. If you can't fill a row, you don't know enough yet — return to Phase 1.

```
FUNCTION / OPERATION:  ______________________________________________

INPUTS:                what types, what shapes, what invariants must hold
                       ______________________________________________

OUTPUTS:               what is returned on success
                       ______________________________________________

PRECONDITION:          what must be true on entry
                       (locks held? transaction open? user authenticated?
                       inputs validated? upstream healthy?)
                       ______________________________________________

POSTCONDITION:         what must be true on success
                       (row written? event published? response returned?
                       audit log entry exists?)
                       ______________________________________________

INVARIANT:             what must remain true throughout, even on failure
                       (no partial writes? no leaked locks?
                       no dangling state? caller's references still valid?)
                       ______________________________________________

IDEMPOTENCY:           if this runs twice, what happens?
                       (queue handlers, webhook receivers,
                       retried HTTP requests are at-least-once)
                       ______________________________________________

CONCURRENCY:           if two callers run this at once, what happens?
                       (race on the same row, double-credit, double-charge)
                       ______________________________________________

ORDERING:              does the order of internal operations matter?
                       can they be reordered or parallelized?
                       ______________________________________________

ATOMICITY:             is the operation all-or-nothing?
                       if it fails mid-way, what state is left behind?
                       ______________________________________________

AUTHORIZATION:         who is allowed to call this?
                       where is the check?
                       is it present on every entry point?
                       ______________________________________________

OBSERVABLE BEHAVIOR    timing? error messages? ordering? byte layout?
THAT IS A CONTRACT     (Hyrum's Law — what users observe IS the contract)
(EVEN IF UNDOCUMENTED):
                       ______________________________________________
```

If any field reads "I don't know" — read more before changing.

If any field reveals a contract you're about to *break* — that's the contract change. Decide explicitly whether it is intended; if so, document it in the commit message; if not, redesign.

References:
- @references/code-complete.md — defensive programming, barricade pattern
- @references/designing-data-intensive-applications.md — idempotency, consistency models
- @references/software-engineering-at-google.md — Hyrum's Law
- @references/philosophy-of-software-design.md — define errors out of existence
