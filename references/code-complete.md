# Code Complete

**Steve McConnell — Code Complete: A Practical Handbook of Software Construction, 2nd Edition (Microsoft Press, 2004)**

A construction-focused encyclopedia: every chapter ends with a checklist that operationalizes the principles. The book treats "construction" (detailed design + coding + debugging + unit test + integration) as a first-class engineering activity.

## Core principles

- **Software's Primary Technical Imperative is managing complexity.** Every other practice serves this.
- **Construction is engineering, not typing.** It spans detailed design, coding, debugging, unit testing, and integration.
- **Metaphors shape behavior.** "Building" beats "writing" — the bigger the system, the more planning, scaffolding, and inspection pay off.
- **Upstream prerequisites determine downstream cost.** Skipping problem definition, requirements, or architecture is the most expensive defect of all. ("Measure twice, cut once.")
- **Key construction decisions are conscious.** Language, conventions, technology-wave position, choice of practices — pick deliberately, not by default.
- **Design is heuristic, iterative, and "wicked."** Manage it with information hiding, loose coupling, strong cohesion, and abstraction.
- **Routines exist to reduce complexity, not to save lines.** Create a routine even for a one-liner if it hides a decision.
- **Defensive programming has three modes:**
  - **Validate** inputs at the *boundary* (system or module edge).
  - **Assert** programmer-error invariants (should-never-happen).
  - **Catch/exception** for expected-but-rare runtime conditions.
  - **Barricade** untrusted data behind a known-safe zone.
- **Pseudocode Programming Process (PPP).** Write the routine in precise prose first; refine each line until it maps to code. If you can't write the prose, you don't understand the problem yet.
- **Table-driven methods replace complex conditional logic.** When `if/else` chains hit ~3 branches or repeat shape, convert to a lookup table.
- **Variable scope and live time should be minimized.** Names encode purpose, not type.
- **Integration is planned, not hoped for.** Prefer incremental + daily build + smoke test over big-bang integration.
- **Code tuning only after measurement.** Most "optimizations" are folklore. Correctness and clarity first.
- **Write for the reader, not the compiler.** Programmers spend most of their time reading code.
- **Checklists are the operational form of the book.** Use them like a pilot's preflight.

## Memorable quotes

- "Managing complexity is the most important technical topic in software development."
- "The single most important reason to create a routine is to reduce a program's complexity."
- "The goal is to minimize the amount of a program you have to think about at any one time."
- "Measure twice, cut once." (chapter title, used as the upstream-prerequisites maxim)
- Subtitle: "A Practical Handbook of Software Construction."

## Operational heuristics

- **Pseudocode before code.** Before coding a routine, write its intent in prose. If you can't, you don't understand it — go back.
- **Tables over chained conditionals.** When `if/else` hits three branches or starts repeating shape, convert to a lookup table.
- **Barricade untrusted data.** Validate at the boundary; trust inside. Assertions guard programmer errors; exceptions handle environment errors.
- **Continuous integration with smoke tests.** Never let the build stay broken overnight.
- **Use the checklists.** Run the chapter checklist (defensive programming, variables, routines, integration) as a self-review before opening the PR.

## Sources

- <https://en.wikipedia.org/wiki/Code_Complete> — Wikipedia overview
- <https://www.microsoftpressstore.com/store/code-complete-9780735619678> — publisher (Microsoft Press)
- <https://www.oreilly.com/library/view/code-complete-2nd/0735619670/> — O'Reilly listing with full table of contents
- <https://www.matthewjmiller.net/files/cc2e_checklists.pdf> — official chapter checklists PDF (the operational form of the book)
- <https://ptgmedia.pearsoncmg.com/images/9780735619678/samplepages/9780735619678a.pdf> — Pearson sample chapters
