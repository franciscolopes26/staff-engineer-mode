# Security — How a C-Level Engineer Thinks About Attack Surface

The cognitive layer for security. Pairs with `MINDSET.md` (general thinking) and `SKILL.md` (operating loop). Security is **not** a review afterthought — it is woven into Phase 2 (contracts) and Phase 3 (pre-mortem) of every non-trivial change.

This file does NOT replace `security-review`, `core:security-review`, or formal pen-testing. It makes security a **design** concern so the review finds fewer surprises.

## The summary in one sentence

> A senior engineer asks "is this code correct?" — a C-level engineer also asks "**who would attack this, what would they want, and what stops them if my first defense fails?**"

---

## STRIDE — the threat-modeling vocabulary

Six categories every non-trivial change should be checked against:

| Letter | Threat | Example | First defense |
|--------|--------|---------|---------------|
| **S** | Spoofing | impersonating a user, system, or sender | strong authentication |
| **T** | Tampering | modifying data in transit / at rest | integrity controls (TLS, MAC, signatures) |
| **R** | Repudiation | denying an action was performed | tamper-evident audit logs |
| **I** | Information disclosure | leaking data the user shouldn't see | authorization, encryption, error redaction |
| **D** | Denial of service | making the system unavailable | rate limits, timeouts, shed-load |
| **E** | Elevation of privilege | gaining permissions you shouldn't have | least privilege, default-deny |

Walk STRIDE during Phase 2 of any change that touches: authentication, authorization, user input, file/path handling, external requests, money, PII, or production data. Five-minute check; catches most categories of issue before code is written.

---

## 15 security mental moves

### 1. Default deny, not default allow

**Senior:** "let me list what users can do."
**C-level adds:** "let me deny everything by default, then explicitly enable."

Allow-lists fail safe; deny-lists fail open. A new feature, a new role, a new endpoint inherits "denied" until someone consciously enables it — which means a missing permission check is a *broken feature*, not a *broken security control*. The bug becomes obvious instead of invisible.

**Trigger:** When designing a permission model, write the "deny everything" rule first; add explicit allows as the only way to grant access.

### 2. Assume the attacker has your source code

**Senior:** "this code is private."
**C-level adds:** "every defense must work even if the attacker reads the source."

Open-source the codebase mentally. Security through obscurity (hidden URLs, magic header values, "no one will guess this") is no security at all — leaks happen via former employees, GitHub mistakes, decompilation, or vendor breaches.

**Trigger:** If your defense rests on "they don't know about it", it isn't a defense. Replace with a control that survives full disclosure.

### 3. Authentication ≠ Authorization

**Senior:** "the user is logged in, so they can do this."
**C-level adds:** "they're logged in as *someone* — is that someone allowed to do *this* to *this resource*?"

AuthN = who you are. AuthZ = what you can do. They are not the same check, and they fail in different ways. Most "broken access control" bugs (OWASP A01) are conflating the two: assuming that because a user is authenticated, they are authorized.

**Trigger:** On every endpoint, name the two checks separately. "Authenticated as user U" and "U is allowed to do action A on resource R." If you can't name both, the endpoint is unsafe.

### 4. Time-of-check ≠ Time-of-use

**Senior:** "I checked the permission at the start of the function."
**C-level adds:** "state can change between check and use. Re-check at use, or hold a lock."

The classic TOCTOU race. Check that a file is safe, then open it — but between the check and the open, an attacker swaps it for a symlink. Check that a user has balance, then debit — but between the check and the debit, a parallel request already debited. Check, hold, use.

**Trigger:** Any sequence "check X → act on X" — assume X changes between the steps unless you hold a lock, use an atomic operation, or validate at the point of action.

### 5. Trust boundaries are the only place validation matters

**Senior:** "validate inputs everywhere — defensive coding."
**C-level adds:** "validate at the **trust boundary**; trust within it; over-validation inside is noise that hides the real checks."

The trust boundary is where data crosses from less-trusted to more-trusted (network → process, user → admin, public API → internal call). Validation belongs there. Internal callers — your own code — are trusted; re-validating their arguments adds noise and hides the validations that matter. *(McConnell's barricade.)*

**Trigger:** Draw the trust boundary explicitly. Inside the barricade is trusted; outside is hostile. Put all validation at the barricade — never inside.

### 6. Logs are data

**Senior:** "log everything for debuggability."
**C-level adds:** "secrets, PII, and tokens in logs are leaks. The log infrastructure becomes part of the attack surface."

The most common breach class isn't fancy exploits — it's a developer logging an `Authorization` header for debugging, then forgetting. Logs replicate to S3, get archived, get read by ten support engineers, get exported for an investigation. Anything in a log is effectively public to the org.

**Trigger:** Before logging an object, ask: would I email this dump to a stranger? If no, redact (passwords, tokens, full credit cards, full email, biometric, health, legal).

### 7. Defense in depth — single point of failure is single point of compromise

**Senior:** "we have auth, so we're secure."
**C-level adds:** "if auth fails, what else stops the attacker? If nothing — single point of compromise."

A single broken control should not equal full breach. Layer controls: auth at the edge AND authorization in the service AND least-privilege DB credentials AND audit at the storage layer. Each layer is cheap; together they multiply.

**Trigger:** For any sensitive operation, name three independent controls. If you can only name one, you have a single-point-of-compromise system.

### 8. Errors are information disclosure

**Senior:** "useful error messages help debugging."
**C-level adds:** "useful externally → useful to attackers. Generic outside, specific in internal logs."

Stack traces in API responses reveal framework versions and code structure. "User not found" vs "wrong password" reveals which usernames exist (enumeration). "Database error: relation `users_payment_methods` not found" leaks the schema. External errors should be uniform; specifics go to internal logs with a request ID the user can reference for support.

**Trigger:** Read every error message your code emits. Would an attacker learn anything useful from it that a legitimate user wouldn't already know?

### 9. Supply chain IS your attack surface

**Senior:** "this library does what we need."
**C-level adds:** "every dependency is a trust delegation."

`package.json` is a list of trust grants — each transitive dep has full code-execution authority over your process. Pin versions (lockfile). Review what new deps bring in (transitive count, maintainer health, last-publish date). Watch for typosquats (`reqeusts`, `cross-env-shell`). Snyk/Dependabot is necessary, not sufficient.

**Trigger:** Before adding a new dependency, check: maintainer activity, transitive dep count, GitHub stars vs npm downloads sanity check, license, whether it's pinned in the lockfile.

### 10. The most expensive bug is the one users tell you about

**Senior:** "we'll fix it when we find it."
**C-level adds:** "defense in depth, monitoring, red-team thinking — **we** find it first, not the attacker."

If a user (or worse, the press) tells you about your security bug, the cost is regulatory, reputational, and remedial — orders of magnitude more than the cost of finding it yourself. Pen-tests, audit logs, anomaly alerts, bug bounties — these exist to make you the first to know.

**Trigger:** For every sensitive operation, ask: how would I detect this being abused, before the user noticed? If you can't answer, add the monitoring before shipping.

### 11. Idempotency keys are security primitives

**Senior:** "idempotency is for retries."
**C-level adds:** "they also prevent replay attacks — same primitive, two purposes."

A request with a unique idempotency key, once processed, cannot be replayed for a duplicate effect — whether the duplicate comes from a flaky network (stability) or from an attacker capturing the request (security). Design for replay safety; you get both for one cost.

**Trigger:** Any state-changing operation that an attacker could replay (financial, permission grant, send a message) — require an idempotency token and reject reuse.

### 12. Rate limiting is fundamental

**Senior:** "we'll add a rate limit if it becomes a problem."
**C-level adds:** "every authenticated endpoint — especially auth itself — needs per-actor rate limiting from day 1."

Auth endpoints without rate limiting enable credential stuffing. Expensive endpoints without rate limits enable DoS-via-cost. The default for any endpoint is "rate-limited"; "unlimited" is the exception that requires justification.

**Trigger:** Every new endpoint gets a rate-limit budget (per IP, per user, per token). Auth endpoints get an aggressive one + lockout after N failures.

### 13. Encryption ≠ confidentiality of access patterns

**Senior:** "the data is encrypted at rest."
**C-level adds:** "encrypted, yes — but access pattern, size, and timing can still leak."

Encryption protects content, not metadata. Knowing *that* user X accessed *something* in a "medical-conditions" table at 3 a.m. leaks a lot even if the content is encrypted. Side channels — query latency, response size, cache hits — leak independently. Real privacy needs more than encryption.

**Trigger:** For sensitive data, ask: what does an observer learn from the access pattern, response timing, or response size? If non-trivial, design to obscure the metadata too (constant-time, padding, decoy queries).

### 14. Audit logs are append-only and themselves the attack target

**Senior:** "we log audit events."
**C-level adds:** "if an attacker can modify the audit log, the attack is invisible. Audit infrastructure is itself security-critical."

The first thing a competent attacker does is delete the trace. Audit logs must be: append-only, off-host (so compromising one machine doesn't lose them), tamper-evident (signed or hash-chained), and monitored for *gaps* (missing entries are themselves an alert).

**Trigger:** If your audit log lives on the same DB as the audited data, the attacker who reads the data can edit the audit. Move the audit somewhere they cannot reach with the same credentials.

### 15. Threat modeling is product design, not security review

**Senior:** "security review happens at the end."
**C-level adds:** "the threat model shapes the design — STRIDE during Phase 2 of the loop, not after Phase 5."

If threat modeling happens at the end, the design is already locked in and the only options are expensive retrofits or known-unsafe ships. Threat modeling during design is cheap; threat modeling after is rework. STRIDE the design *before* writing code. *(See `@scripts/threat-model.md`.)*

**Trigger:** For any change involving auth, money, PII, or external input — run STRIDE before Phase 4 (CHANGE). Five minutes during design saves weeks of remediation later.

---

## Where security threads into the operating loop

| Phase | Security thread |
|-------|-----------------|
| Phase 1 (UNDERSTAND) | Read who is authorized to call this code today; who isn't. Read auth-related git blame — the bugs cluster here. |
| Phase 2 (SPECIFY) | Run STRIDE. Name the threat actors. Name the authorization check. Name what's in the audit log. |
| Phase 3 (PRE-MORTEM) | Add hostile input, replay, credential stuffing, IDOR, TOCTOU to the failure mode list. |
| Phase 4 (CHANGE) | Default deny. Pin dependencies. No secrets in code. Errors generic externally. |
| Phase 5 (VERIFY) | Send the *attacker* request, not just the happy-path. Read your own logs — are secrets leaking? |

---

## When to escalate to formal security review

This skill makes security a design concern. It does NOT replace formal security review when the change is:

- Touching authentication, session, or password handling.
- Storing or transmitting payment data (PCI scope).
- Storing or processing PII/PHI (GDPR/HIPAA scope).
- Changing crypto, signing, or key management.
- Adding a new external integration with broad scope.
- Public-facing endpoint with no rate limit yet.

For these — invoke `security-review` (formal) or pair with a security engineer. This skill is the upstream design discipline; security-review is the downstream audit.

---

## The shortest version

> Default deny. Assume the attacker has the source. AuthN ≠ AuthZ. Validate at the boundary, trust within. Logs are data. Defense in depth. Errors disclose. Threat-model in Phase 2, not after Phase 5.

If you remember nothing else, remember those eight sentences. The 15 moves above are the elaboration; STRIDE is the vocabulary.
