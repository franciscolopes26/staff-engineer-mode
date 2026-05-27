# Clean Code

**Robert C. Martin — Clean Code: A Handbook of Agile Software Craftsmanship (Prentice Hall, 2008)**

The book is opinionated and not universally loved; some specific rules (function size targets, comment guidance) are debated. The principles distilled here are the durable ones — naming, single-purpose functions, comment discipline, SOLID, the Boy Scout Rule.

## Core principles

### Chapter 2 — Meaningful Names
- Use **intention-revealing names** — the name answers *why* it exists, *what* it does, *how* it's used.
- **Avoid disinformation.** Don't call a thing `accountList` if it isn't a `List`.
- **Make meaningful distinctions.** No `a1, a2, a3…`. No `ProductInfo` vs `ProductData` without a real semantic difference.
- **Use pronounceable, searchable names.** Single-letter names only inside tight scopes.
- **Class names are nouns; method names are verbs.**
- **Avoid encodings.** No Hungarian notation; no type prefixes.

### Chapter 3 — Functions
- **Functions should be small.** "The second rule of functions is that they should be smaller than that."
- **Do One Thing.** Do it well. Do it only.
- **One level of abstraction per function** (the Stepdown Rule — reading a class should feel like reading a top-down narrative).
- **Prefer fewer arguments** (0 > 1 > 2 > 3). Three or more arguments deserve a parameter object.
- **Avoid flag arguments.** A boolean parameter that switches behavior is proof the function does two things; split it.
- **Have no side effects.** A function should do what its name says, nothing else.
- **Command-Query Separation.** A function either *does* something or *answers* something — never both.

### Chapter 4 — Comments
- **"Don't comment bad code — rewrite it."** Comments are usually a failure to express intent in the code itself.
- **Explain *why*, not *what*.** Remove redundant, misleading, and commented-out code.
- A comment that restates the code is noise; delete it. Keep comments that explain rationale, trade-offs, hidden constraints, or warnings.

### Chapter 10 — SOLID (single-sentence summaries)
- **SRP — Single Responsibility:** a class has one, and only one, reason to change.
- **OCP — Open/Closed:** open for extension, closed for modification.
- **LSP — Liskov Substitution:** subtypes must be substitutable for their base types.
- **ISP — Interface Segregation:** many small, client-specific interfaces beat one fat interface.
- **DIP — Dependency Inversion:** depend on abstractions, not concretions.

### Chapter 1 — The Boy Scout Rule
- **"Leave the campground cleaner than you found it."** Every time you touch the codebase, leave it slightly better than you found it — a name, a smell, a duplicated block.

## Memorable quotes

- "The only way to go fast, is to go well." (Martin)
- "The first rule of functions is that they should be small. The second rule of functions is that they should be smaller than that." (Ch. 3)
- "Clean code always looks like it was written by someone who cares." (Ch. 1)
- "Leave the campground cleaner than you found it." (Ch. 1, the Boy Scout Rule)

## Operational heuristics

- **Rename until it reads.** If a teammate has to ask what a name means, rename it before merging.
- **Function size budget.** If a function exceeds ~20 lines or two levels of indentation, look for an extraction.
- **No flag arguments.** A boolean parameter is a smell — split into two functions with intention-revealing names.
- **Why-not-what comments.** If a comment restates what the code does, delete it. Keep comments that explain rationale, trade-offs, or non-obvious context.
- **Boy Scout rule per PR.** Every PR leaves at least one thing in the touched files cleaner — a name improved, a duplicate removed, a stale comment deleted.

## Caveats

Clean Code is a strong-opinion book. Several of its prescriptions are debated:
- The 4-line / 20-line function targets are not universally accepted; many production codebases ship 50-line functions that read well.
- The "comments are usually a failure" rule, applied too dogmatically, deletes the *why* alongside the *what*.

Use the principles; don't enforce the line-count rules as law.

## Sources

- <https://catdir.loc.gov/catdir/toc/ecip0820/2008024750.html> — Library of Congress table of contents
- <https://www.informit.com/articles/article.aspx?p=1235624&seqNum=6> — InformIT (Pearson) excerpt: "The Boy Scout Rule"
- <https://gist.github.com/wojteklu/73c6914cc446146b8b533c0988cf8d29> — widely-referenced rule-by-rule summary
- <https://deviq.com/principles/boy-scout-rule/> — Boy Scout Rule reference
