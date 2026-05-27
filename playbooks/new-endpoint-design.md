# Playbook: Designing a New Public Endpoint

**When:** adding a new HTTP / gRPC / event-based endpoint that other systems (or other teams) will consume.
**Goal:** make the contract right the first time, because changing it later is expensive in direct proportion to the number of consumers.

A public endpoint is a **long-lived API**. Hyrum's Law applies from the moment the second consumer integrates. Most of the cost of an endpoint is in changing it, not in writing it.

## Phase 1 — read first

- Existing endpoints in the same service: naming, error shapes, status codes, auth model. **Conceptual integrity** (Brooks) — your new endpoint should look like its neighbors.
- The would-be consumer's perspective. Sketch the call site they'll write. If it's awkward to call, the endpoint is wrong.
- Any prior design doc or ticket. If none exists for a non-trivial endpoint, **stop and write one** using `@scripts/communication.md` design doc skeleton.

## Phase 2 — contracts to surface

Use `@scripts/contracts.md`. For a new endpoint, especially fill:

- **Inputs:** types, shapes, validation, max sizes, encoding, null/optional semantics.
- **Outputs:** shape on success; **every error case** with status code and body shape.
- **Idempotency:** is this endpoint safe to retry? If yes, how (request ID? natural key?).
- **Authorization:** who can call it? Where is the check enforced? Is it the same on every entry path?
- **Versioning:** is this `v1`? what's the deprecation path?
- **Observable contract:** error message format, response ordering, timing — once a consumer ships, these are de-facto contracts (Hyrum's Law).

## Phase 3 — failure modes specific to public endpoints

- **Bad input** — what's the response for malformed / oversized / hostile input? (400 with a useful message; never 500.)
- **Auth failure** — 401 (not authenticated) vs 403 (not authorized) — distinguish.
- **Rate / abuse** — what's the per-caller limit? what's the response when exceeded? (429 with `Retry-After`.)
- **Downstream failure** — what does this endpoint do when its dependency is slow / down? (Don't propagate a 30s wait — fail fast or fall back.)
- **Partial result** — can this endpoint return success with a missing field? If yes, document it.
- **Schema evolution** — adding a new optional field is safe; removing one breaks. Default to additive change only.

## Phase 4 — change strategy

- **Sketch the request/response in the spec FIRST** (OpenAPI, .proto, Pydantic, Zod — whatever your stack uses). Compile/lint it.
- **Implement the failure paths before the happy path.** They're harder and more important.
- **Add the test for at least one consumer call site.** Not just unit tests — a test that calls the endpoint exactly as a consumer would.
- **Documentation in the same PR** (or it doesn't ship). Includes: purpose, auth, request, response, errors, examples, versioning policy.
- **Reversibility:** publishing a new endpoint is **partially reversible** — once a consumer integrates, you cannot remove it without their cooperation. Treat with care.

## Phase 5 — verification

- Hit the endpoint with curl / Postman / grpcurl. Read the response. Is it what a stranger would expect?
- Trigger each documented error case at least once. Are the status codes and messages right?
- Run the consumer test (the one you wrote in Phase 4). Does it pass without you tweaking the consumer code?
- **Complexity budget**: is this endpoint *deep* (does real work, hides complexity from caller) or *shallow* (thin wrapper over a DB query the caller could do themselves)? If shallow — reconsider whether it should exist (Ousterhout).

## Red flags most common in new endpoints

- **RF-13 Information Leakage** — does the response leak the internal DB schema verbatim? If yes, model a response DTO instead.
- **RF-12 Shallow Module** — the endpoint is one SQL query forwarded; just expose a query interface or do real work.
- **RF-03 Naked Remote Call** — if the endpoint calls a downstream, where's the timeout and circuit breaker?
- **RF-14 Just-In-Case** — every "what if" validation should map to a stated failure mode in Phase 3; if it doesn't, delete.
- **RF-15 Boolean Flag Argument** — a `bool` in the request payload that switches behavior usually means you wanted two endpoints.

## Refusal scripts for common bad framings

- "We'll figure out the response shape in v2" → "v2 requires every v1 consumer to migrate. What's the shape that won't need a v2?"
- "Just expose the DB column names directly" → "DB columns are an internal contract. Once a consumer reads them, you can't rename. Model a response DTO."
- "Make it return 200 with `error: true` on failure" → "HTTP has status codes for a reason. 4xx/5xx is the contract intermediaries (caches, retries, logs) act on. Use them."
- "We don't need versioning yet" → "When you add the first breaking change, you'll wish you had. Pick a versioning policy now even if you never bump it."
- "I'll add a flag to support both old and new behavior" → "RF-15. Two endpoints (one new, one deprecated) is clearer than one with a mode switch."

## When this playbook is wrong

- An internal-only endpoint with one trusted caller in the same codebase — apply judgment, not the full ceremony.
- A truly throwaway prototype — use the regular 5-phase loop, label the endpoint `experimental/`, set an expiration date.
- A migration endpoint that's deliberately one-shot — different lifecycle, different rules.
