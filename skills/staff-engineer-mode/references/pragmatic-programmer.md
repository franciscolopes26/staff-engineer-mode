# The Pragmatic Programmer

**Hunt & Thomas — 20th Anniversary Edition (Addison-Wesley, 2019)**

The book is organized around 100 numbered tips. The full official list is at <https://pragprog.com/tips/>. The principles below are the highest-leverage ones for working engineers.

## Core principles

- **Tip 1 — Care about your craft.** Don't write software unless you care about doing it well.
- **Tip 5 — Don't live with broken windows.** Fix bad code, bad designs, and wrong decisions when you see them. Decay accelerates; one ignored broken window invites the next.
- **Tip 8 — Make quality a requirements issue.** Quality is a non-negotiable constraint, not a deliverable layered on at the end.
- **Tip 14 — Good design is easier to change than bad design.** ETC ("Easier To Change") is the underlying value of every principle. When choosing between two designs, pick the one that costs less to change.
- **Tip 15 — DRY: Don't Repeat Yourself.** "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system." DRY is about *knowledge*, not lines of code that happen to look the same.
- **Tip 17 — Eliminate effects between unrelated things (orthogonality).** Each module owns one concern; changing one should not ripple into others.
- **Tip 20 — Use tracer bullets to find the target.** In unfamiliar territory, build the thinnest end-to-end vertical slice that reaches the target, then iterate. Better than building each layer in isolation and praying they integrate.
- **Tip 34 — Don't assume it — prove it.** Reproduce against real data in the real environment before "fixing" or "explaining" a bug.
- **Tip 38 — Crash early.** A dead program does less damage than a crippled one running on bad state.
- **Tip 42 — Take small steps — always.** Get feedback after each step before taking the next.
- **Tip 44 — Decoupled code is easier to change.** Coupling is the tax you pay every time you want to evolve a system.
- **Tip 45 — Tell, Don't Ask.** Don't extract data from an object to operate on it; ask the object to do the work. Reduces coupling, hides invariants.
- **Tip 62 — Don't program by coincidence.** Rely on reliable things. If your code works and you don't know why, you have a bug waiting to surface.
- **Tip 65 — Refactor early, refactor often.** Refactoring is gardening, not surgery.
- **Tip 74 — Name well; rename when needed.** Names are load-bearing; investing in them is not optional.

## Memorable quotes

- "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system." (Tip 15, DRY)
- "One broken window, left unrepaired for any substantial length of time, instills in the inhabitants of the building a sense of abandonment… So another window gets broken."
- "Tracer bullets let you home in on your target by trying things and seeing how close they land."
- "Don't program by coincidence — rely only on reliable things."
- "Care about your craft."

## Operational heuristics

- **DRY check.** Before writing, ask "is this knowledge represented elsewhere?" If yes, reference; don't duplicate. Don't conflate accidental similarity with knowledge duplication.
- **Tell, Don't Ask.** If you find yourself reading `x.foo` then `x.bar` then writing logic, push the logic into `x`.
- **Crash early.** Fail loudly at the first sign of an inconsistent state; never let bad data propagate.
- **Tracer bullets for unknowns.** When the territory is unfamiliar, ship a thin vertical slice end-to-end before deepening any layer.
- **Prove, don't assume.** Reproduce the bug against real data in a real environment before "explaining" it.

## Sources

- <https://pragprog.com/tips/> — official 100 Tips card
- <https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/> — publisher page, 20th anniversary edition
- <https://www.artima.com/articles/dont-live-with-broken-windows> — "Don't Live with Broken Windows" essay by Hunt & Thomas
- <https://www.oreilly.com/library/view/the-pragmatic-programmer/9780135956977/> — O'Reilly title page
