# A Philosophy of Software Design

**John Ousterhout — A Philosophy of Software Design, 2nd Edition (Yaknyam Press, 2021)**

A short, opinionated book from the Stanford professor who shipped Tcl/Tk and Log-Structured File Systems. Its thesis: **complexity is the central enemy of software design**, and most "good practice" should be evaluated by whether it actually reduces complexity for callers.

## Core principles

- **Complexity is what makes software hard.** The goal of design is to reduce it.
- **Complexity shows up as three symptoms:**
  - **Change amplification** — a small conceptual change requires touching many places.
  - **Cognitive load** — how much you must know to make a change.
  - **Unknown unknowns** — what you have to discover to make a change correctly.
- **Modules should be deep.** A *deep module* has a simple interface and a powerful implementation. Shallow modules add interface cost without hiding much.
- **Information hiding is the single most important technique.** Hide as much knowledge inside a module as you can.
- **Information leakage is the worst design smell.** When the same fact (file format, protocol field, units) lives in multiple modules, changing it requires changing all of them.
- **General-purpose modules are deeper.** Design somewhat-general APIs even when solving a specific problem; the discipline tends to produce cleaner interfaces.
- **Different is dangerous.** Things that look similar but mean different things mislead readers; things that mean the same should look the same.
- **Design it twice.** Produce two structurally different designs before committing. If you only have one, you don't know whether it's good.
- **Define errors out of existence.** Where possible, reshape the API so the error can't be expressed (e.g., a Unicode substring function that never throws on out-of-range indices).
- **Strategic beats tactical.** Invest ~10–20% extra now to keep the system healthy long-term. *Tactical tornadoes* (developers who optimize for short-term feature output) destroy systems.
- **Comments capture what was in the designer's head** — things not obvious from the code. Write the interface comment *before* the implementation; if it's hard to write, the interface is wrong.
- **Pull complexity downward.** The implementer absorbs pain so callers don't.
- **Decide what matters.** Make important things obvious; suppress the unimportant.

## Catalogued red flags

Ousterhout names specific design smells:
- **Shallow Module** — interface as complex as the implementation; no real abstraction.
- **Information Leakage** — the same fact lives in multiple modules.
- **Temporal Decomposition** — code organized by *when* things happen instead of *what they do*.
- **Overexposure** — internal complexity bleeds through the interface.
- **Pass-Through Method** — a method that only calls another method with the same args (no value added).
- **Repetition** — same code, multiple places.
- **Special-General Mixture** — general-purpose code with embedded special cases.
- **Conjoined Methods** — methods that can only be understood together.
- **Vague Name** — name doesn't tell you what the thing does.
- **Hard to Describe** — if you can't describe it cleanly in a comment, the abstraction is wrong.
- **Non-Obvious Code** — the reader can't predict what it does.

## Memorable quotes

- "Dealing with complexity is the most important challenge in software design."
- "It's more important for a module to have a simple interface than a simple implementation."
- "Comments should describe things that are not obvious from the code."
- "The overall idea behind comments is to capture information that was in the mind of the designer but couldn't be represented in the code."
- "If you want to maintain a clean design for a system, you must take a strategic approach when modifying existing code."

## Operational heuristics

- **Before adding a class, ask: does this make the interface smaller for callers?** If not, it's probably shallow — inline or merge.
- **If two modules share a fact (format, units, schema), that's information leakage** — extract or co-locate.
- **If a method just forwards args to another, collapse it.** Pass-throughs add interface noise without value.
- **Sketch a second, structurally different design** before committing to the first.
- **Write the interface comment first.** If you can't, the interface is wrong; rework it before implementing.

## Sources

- <https://web.stanford.edu/~ouster/cgi-bin/book.php> — author's Stanford book page
- <https://en.wikipedia.org/wiki/John_Ousterhout> — author bio
- <https://www.youtube.com/watch?v=bmSAYlu0NcY> — Talks at Google (2018), full lecture
- <https://newsletter.pragmaticengineer.com/p/the-philosophy-of-software-design> — Pragmatic Engineer interview
- <https://sportebois.medium.com/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-8a9b0045e2bb> — red-flags summary
