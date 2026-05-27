# The Mythical Man-Month

**Fred Brooks — The Mythical Man-Month: Essays on Software Engineering, Anniversary Edition (Addison-Wesley, 1995; original 1975)**

Brooks's reflections on the IBM OS/360 project. The anniversary edition adds "No Silver Bullet" (1986) and a retrospective ("'No Silver Bullet' Refired"). The book is a series of essays; the principles below are the ones that have held up across five decades of software.

## Core principles

- **Brooks's Law.** "Adding manpower to a late software project makes it later." New people impose ramp-up and communication cost that exceeds the throughput they add.
- **The man-month is a myth.** Effort and progress are not interchangeable; sequentially-constrained tasks cannot be parallelized by piling on people. ("Nine women cannot make a baby in one month.")
- **Communication overhead grows as n(n−1)/2.** Coordination cost is quadratic in team size, not linear.
- **No Silver Bullet.** No single technology or technique will yield a tenfold productivity improvement within a decade. The reason is the next principle.
- **Essential vs. accidental complexity.** *Accidental* complexity comes from our tools, languages, environment — we created it and can remove it. *Essential* complexity is inherent to the problem domain and cannot be wished away. Most remaining productivity gains must attack essence, which is hard.
- **Conceptual integrity is *the* most important consideration in system design.** A coherent, opinionated design used by many is better than a feature-rich design assembled by committee.
- **Architecture must be separated from implementation,** and entrusted to one chief architect (or a very small team) acting as the user's agent — to preserve conceptual integrity.
- **Second-System Effect.** A designer's second system is the most dangerous they will ever build — they over-generalize, add every feature cut from the first, and lose the disciplined constraints that made the first one work.
- **Plan to throw one away — you will anyway.** The first build teaches you the problem; ship the second. (Brooks later softened this in favor of incremental/iterative growth.)
- **The Surgical Team.** Organize around one outstanding programmer (the "surgeon") supported by specialists. Productivity differences between individuals are 10:1; structure around that fact.
- **The Tar Pit.** Large-system programming is a tar pit; the more it struggles, the more it sinks. Recognize the trap rather than wish it away.
- **Build pilots, prototypes, and incremental releases.** Organic growth beats big-bang delivery.
- **Schedules slip "one day at a time."** Integration and testing always take longer than planned.

## Memorable quotes

- "Adding manpower to a late software project makes it later." (Brooks's Law)
- "The bearing of a child takes nine months, no matter how many women are assigned." (paraphrased)
- "Conceptual integrity is *the* most important consideration in system design."
- "Plan to throw one away; you will, anyhow."
- "The second system is the most dangerous system a man ever designs."
- "If users want a program to do 30 different things, then those 30 things are essential, and the program must do those 30 different things." (No Silver Bullet)

## Operational heuristics

- **Don't add people to a late project.** Cut scope, extend the date, or improve the team you have. Adding heads almost always makes it worse.
- **Protect conceptual integrity — designate one architect.** When a design decision is contested, the architect decides; democratic design produces incoherent systems.
- **Before optimizing, ask: essential or accidental?** Spend effort on essence (the problem); only spend on accident (tools/process) when it's clearly the bottleneck.
- **Beware your second system.** When tempted to "do it right this time," cut the wishlist in half — twice.
- **Estimate communication cost explicitly.** Every new team member adds n−1 new channels; price that into the plan.

## Sources

- <https://en.wikipedia.org/wiki/The_Mythical_Man-Month> — Wikipedia overview
- <https://en.wikipedia.org/wiki/No_Silver_Bullet> — No Silver Bullet (Brooks, 1986)
- <https://en.wikipedia.org/wiki/Brooks%27s_law> — Brooks's Law
- <https://en.wikipedia.org/wiki/Second-system_effect> — Second-system effect
- <https://www.informit.com/store/mythical-man-month-essays-on-software-engineering-anniversary-9780201835953> — publisher page
