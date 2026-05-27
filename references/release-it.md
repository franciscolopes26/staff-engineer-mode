# Release It!

**Michael Nygard — Release It!: Design and Deploy Production-Ready Software, 2nd Edition (Pragmatic Bookshelf, 2018)**

Nygard's catalog of stability patterns and anti-patterns, learned the hard way in real production failures. The book reframes resilience as a design concern, not an operations afterthought.

## Core principles

- **Integration points are the #1 killer of system stability.** Every remote call is a hazard.
- **Failures propagate.** A single slow dependency starves threads, which starves the caller, which collapses the cluster (cascading failure).
- **Cracks accelerate.** Small problems amplify across tiers under load (chain reactions).
- **Users are the antagonist.** Real traffic exposes failure modes no test suite reproduces.
- **Design for production, not for QA.** Most systems are designed for the lab; production is where the real cost lives.
- **Bugs will happen, so they must be survived.** Resilience matters more than prevention.

## Stability patterns (the resilience toolkit)

- **Circuit Breaker** — stop calling a dependency that is already failing; let it recover.
- **Bulkhead** — partition resources (threads, pools, instances) so one failure cannot consume the whole system.
- **Timeouts** — every remote call has a deadline; an unbounded wait is an outage in slow motion.
- **Fail Fast** — detect impossibility early and return; don't hold resources for doomed work.
- **Steady State** — every accumulation (logs, sessions, caches, DB rows) must have a purge, or it will end you.
- **Handshaking & Back-Pressure** — let callees tell callers to slow down; don't accept work you cannot finish.
- **Shed Load** — when saturated, reject — degraded service beats total collapse.
- **Decoupling Middleware** — async/queue boundaries contain blast radius.
- **Test Harness** — simulate the *nasty* failure modes (slow, partial, byzantine), not just the happy errors.
- **Governor / Steady Pace** — rate-limit actions that have unbounded resource consumption.

## Stability anti-patterns

Integration Points, Chain Reactions, Cascading Failures, Users, Blocked Threads, Self-Denial Attacks, Unbalanced Capacities, Slow Responses, Unbounded Result Sets.

## Memorable quotes

- "Integration points are the number-one killer of systems. Every single one of those feeds presents a stability risk."
- "Most software is designed for the development lab or the testers in the Quality Assurance (QA) department."
- "Bugs will happen. They cannot be eliminated, so they must be survived instead."
- "Design with skepticism, and you will achieve resilience."
- "Hope is not a design method."
- "Release is the beginning of the software's true life; everything before that release is gestation."

## Operational heuristics

- **Every remote call gets a timeout AND a circuit breaker.** No exceptions, including "internal" services.
- **Pool isolation per dependency.** A flaky downstream cannot exhaust the thread pool used by healthy ones.
- **Cap and purge everything that grows.** Sessions, logs, caches, queues, DB tables — no unbounded data structures in production.
- **When overloaded, shed before you fail.** Return 503 to a fraction of traffic rather than collapse all of it.
- **Run a failure drill before launch.** Kill the DB, add 5s latency to a dependency, fill the disk — if you don't know what happens, you're not production-ready.

## Sources

- <https://pragprog.com/titles/mnee2/release-it-second-edition/> — publisher page
- <https://www.oreilly.com/library/view/release-it-2nd/9781680504552/f_0047.xhtml> — Chapter 5: Stability Patterns (O'Reilly)
- <https://media.pragprog.com/titles/mnee/mnee-antipatterns.pdf> — Anti-patterns sample PDF
- <https://sookocheff.com/post/architecture/stability-antipatterns/> — Kevin Sookocheff's stability anti-patterns summary
- <https://www.goodreads.com/work/quotes/1056502-release-it-design-and-deploy-production-ready-software-pragmatic-prog> — sourced quotes
