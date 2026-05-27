# Software Engineering at Google

**Titus Winters, Tom Manshreck, Hyrum Wright (eds.) — Software Engineering at Google: Lessons Learned from Programming Over Time (O'Reilly, 2020)**

A distillation of what Google's engineering culture optimizes for. The book is **freely available online** at <https://abseil.io/resources/swe-book> — all quotes below are sourced from that text and can be verified.

## Core principles

- **Software engineering = programming integrated over time.** Code that has to live and change is a different discipline from code that just runs once.
- **The three axes that distinguish engineering from programming: Time, Scale, Trade-offs.**
- **Hyrum's Law:** "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." The contract is what users *observe*, not what you *documented*.
- **Sustainability over cleverness.** "Clever" is a compliment in programming and an accusation in software engineering.
- **A project is sustainable** if, for the expected lifespan of the software, you can adopt any necessary change.
- **The half-life of code varies by ~100,000×.** A throwaway shell script and a ten-year API are not the same problem; pick rigor by lifespan.
- **Decisions are evidence-based trade-offs**, not absolutes. Document the trade-off so it can be revisited.
- **Nothing is free; everything is a trade-off** — including "best practices."
- **Code review is primarily a teaching and consistency tool**, not a gatekeeping ritual.
- **Style guides exist to optimize for the reader**, not the writer. Readability scales; cleverness does not.
- **Changing a public API is expensive in direct proportion to its number of consumers** (Hyrum's Law in action).
- **Expect to deprecate.** Every API will eventually need to be migrated; design migration paths in.
- **Knowledge sharing scales the org**, not just the codebase — documentation, mentoring, code review.
- **Automate the boring, hard-to-be-consistent parts** — testing, formatting, large-scale change.
- **Policies that don't scale will break first.** Design rules that survive 10× engineers and 10× code.

## Memorable quotes (verbatim from the free online text)

- "Software engineering is programming integrated over time."
- "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." (Hyrum's Law)
- "It's programming if 'clever' is a compliment, but it's software engineering if 'clever' is an accusation."
- "Your project is sustainable if, for the expected life span of your software, you are capable of reacting to whatever valuable change comes along."
- "We are doing this because it is the best option we can see at the time, based on current evidence."
- "Cubes aren't squares, distance isn't velocity. Software engineering isn't programming."

## Operational heuristics

- **Treat every observable behavior as part of the contract** — timing, error messages, ordering, byte layout. If you don't want it depended on, hide it.
- **Ask: what's the expected lifetime of this code?** before choosing how much rigor to invest. A one-week script and a ten-year API are not the same problem.
- **Frame every decision as a trade-off with evidence.** "We chose X because, given Y, the cost of Z is lower." Avoid absolute rules.
- **In code review, optimize for the reader six months from now.** Leave the code clearer than you found it; use the review to teach.
- **Before adding a public API, plan its deprecation path** — who migrates callers, how you detect remaining users, what the timeline looks like.

## Sources

- <https://abseil.io/resources/swe-book> — full book, free online (authoritative)
- <https://abseil.io/resources/swe-book/html/ch01.html> — Chapter 1: What Is Software Engineering?
- <https://www.hyrumslaw.com/> — canonical statement of Hyrum's Law
- <https://www.oreilly.com/library/view/software-engineering-at/9781492082781/ch01.html> — O'Reilly Chapter 1
- <https://books.google.com/books?id=V3TTDwAAQBAJ> — Google Books listing
