# Working Effectively with Legacy Code

**Michael Feathers — Working Effectively with Legacy Code (Prentice Hall, 2004)**

The canonical text for changing code that has no tests. Feathers reframes "legacy" not as "old" but as "without tests" — which makes the title apply to most code written this morning.

## Core principles

- **Legacy code is code without tests.** Age, language, and style are irrelevant; the absence of tests is what makes change dangerous.
- **The legacy dilemma:** you need tests to change safely, but you must change the code to make it testable. Resolve it with the smallest, safest dependency-breaking step.
- **Seams are the central concept.** A *seam* is "a place where you can alter behavior in your program without editing in that place."
- **Three kinds of seam:**
  - **Preprocessing seams** — macros / build-time substitution (mostly C/C++).
  - **Link seams** — swap the linked library/binary at build time.
  - **Object seams** — subclass / interface substitution at runtime (the most useful in OO languages).
- **Characterization tests pin down current behavior**, not intended behavior. They capture what the code actually does so you have a safety net before you change it.
- **The change algorithm:**
  1. Identify change points.
  2. Find test points.
  3. Break dependencies.
  4. Write tests.
  5. Make changes and refactor.
- **Sprout method / sprout class.** When adding new behavior, write it as a new, fully tested method (or class) and call it from the legacy code — instead of editing the messy code in place.
- **Wrap method / wrap class.** Rename the old method, create a new one with the original name that calls the old one plus the new behavior — used when you must augment an existing call.
- **A unit test is fast and isolated.** "If it talks to a database, the network, or the file system, or requires environment config, it's not a unit test." Sub-100ms, in-process.
- **Don't scatter third-party APIs through your code.** Wrap them behind an abstraction you own, so the dependency cannot spread.
- **Prefer the smallest reversible refactor** (lean on the compiler, extract method, extract interface) over big rewrites. Every step must keep the system green.
- **Effect sketches and feature/effect analysis.** Before changing code, map what calls what and what is affected, so you know the blast radius.
- **Tests are documentation that cannot lie.** Adding them is not overhead; it is the only way to learn the system.

## Memorable quotes

- "To me, legacy code is simply code without tests."
- "A seam is a place where you can alter behavior in your program without editing in that place."
- "A characterization test … characterizes the actual behavior of a piece of code."
- "If it talks to a database, the network, or the file system, or requires environment config, it's not a unit test."

## Operational heuristics

- **Before changing legacy code, write a characterization test.** If you can't get the code under test, that is the first task — not the feature.
- **If you can't test it, find the seam.** Ask: where can I alter behavior without editing this code? (Subclass, interface, link substitution, DI.)
- **Default to sprout, not surgery.** New behavior goes in a new, tested method/class. Only edit the legacy body when you must.
- **Define "done" by the green bar.** Every dependency-breaking step compiles and the existing tests still pass before you move to the next.
- **Wrap every third-party SDK** behind an interface you own so it has exactly one seam.

## Sources

- <https://michaelfeathers.silvrback.com/> — author's blog
- <https://understandlegacycode.com/blog/key-points-of-working-effectively-with-legacy-code/> — comprehensive summary
- <https://www.infoq.com/podcasts/working-effectively-legacy-code/> — InfoQ interview with Feathers
- <https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052> — publisher (Pearson, Robert C. Martin Series)
- <https://en.wikipedia.org/wiki/Michael_Feathers> — Wikipedia
