# Designing Data-Intensive Applications

**Martin Kleppmann — Designing Data-Intensive Applications (O'Reilly, 2017)**

The reference text for distributed systems and storage. Kleppmann is a Cambridge researcher; the book is unusually careful about the difference between marketing claims ("CP", "AP", "strong consistency") and actual guarantees.

## Core principles

- **Three concerns:** every system must be evaluated on **reliability**, **scalability**, and **maintainability**. The third is the most often neglected.
- **Reliability = continuing to work correctly in the face of adversity** (hardware faults, software bugs, human error). Fault-tolerance is essential, not optional.
- **Distinguish fault from failure.** A *fault* is one component deviating from spec; a *failure* is the system as a whole stopping. The goal of fault-tolerance is to prevent faults from cascading into failures.
- **Scalability is not a single number.** Define it against a specific load parameter (RPS, fanout, data volume) and a specific performance metric — **p95/p99 latency, not the mean**.
- **Maintainability has three sub-goals:** operability, simplicity (managing accidental complexity), and evolvability.
- **Be explicit about your consistency model.** "Strong consistency" is not one thing — *linearizability*, *sequential consistency*, *causal consistency*, *read-your-writes*, and *eventual consistency* are distinct, with very different costs.
- **CAP is misleading.** It is formally a narrow theorem about a single read-write register under total network partition. Do not classify databases as "CP" or "AP" — describe their actual guarantees instead.
- **Data outlives code.** Schema and storage format choices have a longer half-life than the application code on top of them. Design for schema evolution (backward and forward compatibility) from day one.
- **Logs are the universal primitive.** Append-only event logs unify replication, derived state, stream processing, and recovery. Treat databases as materialized views over a log when you can.
- **Idempotency is a hard requirement in distributed systems** — at-least-once delivery is the realistic default. Any operation that can be retried must be safe to retry.
- **Asynchronous replication trades durability for latency.** Know which one you chose and why.
- **Batch and stream processing are duals.** A batch job is a bounded stream; design pipelines so the same logic works for both.
- **Derived data is recoverable; source-of-truth data is not.** Keep the boundary explicit.

## Memorable quotes

- "The CAP theorem is too simplistic and too widely misunderstood to be of much use for characterizing systems."
- "Software keeps changing, but the fundamental principles remain the same."
- "Data is at the center of many challenges in system design today."
- (On CAP scope) "A single, read-write register — that's all." CAP "says nothing about latency."

## Operational heuristics

- **Before adopting a database, write down its actual consistency, durability, and partition behavior.** Never accept "it's CP" as an answer.
- **For any cross-service write, assume at-least-once delivery** and design the receiver to be idempotent (dedupe key, conditional write, or natural idempotency).
- **Quote latency as p95/p99 under target load**, never as an average.
- **When in doubt about coupling between services, prefer an append-only event log** as the integration contract over synchronous RPC.
- **Treat the schema as a long-lived API** — every change must be backward- and forward-compatible, or it is a migration with a plan.

## Sources

- <https://martin.kleppmann.com/2017/03/27/designing-data-intensive-applications.html> — author announcement
- <https://dataintensive.net/> — book site
- <https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/> — O'Reilly listing
- <https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html> — author's CAP critique
- <https://www.cl.cam.ac.uk/research/dtg/archived/files/publications/public/mk428/cap-critique.pdf> — Cambridge paper, CAP critique
