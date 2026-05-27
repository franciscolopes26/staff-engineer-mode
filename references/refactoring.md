# Refactoring

**Martin Fowler — Refactoring: Improving the Design of Existing Code, 2nd Edition (Addison-Wesley, 2018)**

Fowler's catalog of code smells and behavior-preserving transformations. The 2nd edition rewrites examples in JavaScript; the principles are language-agnostic. Companion site: <https://refactoring.com/>.

## Core principles

- **Refactoring (noun):** "A change made to the internal structure of software to make it easier to understand and cheaper to modify without changing its observable behavior."
- **Refactoring (verb):** "To restructure software by applying a series of refactorings without changing its observable behavior."
- **Behavior preservation is the invariant.** Tests must stay green after every step. If they don't, the refactor was incorrect.
- **Many small steps, not big ones.** Each individual change is intentionally tiny so the system is always shippable.
- **The Two Hats** (Kent Beck, via Fowler). At any moment you wear *exactly one* hat: "adding function" or "refactoring." When adding function you don't change existing code; when refactoring you add no behavior. Never both at once.
- **Refactor opportunistically, not as a separate ticket.** Refactor *before* a change to make it easy, then make the easy change. ("Make the change easy, then make the easy change." — Kent Beck.)
- **Code smells are heuristics, not proofs.** A smell is "a surface indication that usually corresponds to a deeper problem" — a flag to investigate, not a verdict.
- **Extract Function is the workhorse.** The trigger is intent: if you can name the new function better than the inline code reads, extract it.
- **Rename ruthlessly.** A bad name is a refactor you owe yourself; good names eliminate most of the need for comments.
- **Comments are often a smell.** Frequently signal code that should have been extracted and named instead.
- **Tests are a prerequisite, not an afterthought.** Without fast, reliable tests you cannot refactor — you can only hope.

## The smell catalog (2nd edition — 24 smells)

Mysterious Name, Duplicated Code, Long Function, Long Parameter List, Global Data, Mutable Data, Divergent Change, Shotgun Surgery, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Loops, Lazy Element, Speculative Generality, Temporary Field, Message Chains, Middle Man, Insider Trading, Large Class, Alternative Classes with Different Interfaces, Data Class, Refused Bequest, Comments.

For each smell, the book maps to specific refactorings. The catalog is at <https://refactoring.com/catalog/>.

## Most-used refactorings

Extract Function, Inline Function, Extract Variable, Rename Variable, Change Function Declaration, Move Function, Move Field, Encapsulate Variable, Replace Conditional with Polymorphism.

## Memorable quotes

- "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."
- "If it stinks, change it." (Grandma Beck, quoted by Kent Beck in Refactoring, ch. 3)
- "When you have to add a feature to a program but the code is not structured in a convenient way, first refactor the program to make it easy to add the feature, then add the feature." (Kent Beck, via Fowler)
- "When you add function, you shouldn't be changing existing code." (Two Hats)
- "By continuously improving the design of code, we make it easier and easier to work with."

## Operational heuristics

- **Never mix a refactor and a feature in one diff.** If you find yourself doing both, split the commit/PR.
- **Extract Function the moment you can name it.** The name justifies the extraction; if you can't name it, don't extract.
- **Refactor before the change, not after.** Prepare the ground, then drop the feature in cleanly (preparatory refactoring).
- **Run tests after every micro-step.** If a step is so large you fear it, decompose it further.
- **Treat comments-that-explain-what as an Extract Function trigger.** The comment becomes the function name.

## Sources

- <https://refactoring.com/> — Fowler's canonical site
- <https://refactoring.com/catalog/> — full refactoring catalog
- <https://martinfowler.com/bliki/CodeSmell.html> — code smell definition
- <https://martinfowler.com/articles/refactoring-2nd-ed.html> — what changed in the 2nd edition
- <https://martinfowler.com/articles/preparatory-refactoring-example.html> — preparatory refactoring
- <https://en.wikipedia.org/wiki/Code_refactoring> — Wikipedia
