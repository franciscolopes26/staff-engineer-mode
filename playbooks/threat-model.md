# Playbook: Threat-Model a Change Before Building It

**When:** designing anything that touches auth, money, PII, external input, file I/O, or admin actions.
**Goal:** identify the attack surface and the controls *before* code exists; cheaper than retrofitting.

This playbook is the bridge between "I want to build X" and "I've designed X safely." Use `@scripts/threat-model.md` for the paste-able template; this playbook is the workflow around it.

## Phase 1 — read first

- Existing authentication and authorization patterns in this codebase. What's the convention for the new code to inherit?
- Recent security incidents in this area — `git log --grep=CVE\|security\|breach` and the ticket tracker. Bug clusters reveal weak spots.
- Whose data, money, or access does this change touch? (Find at least one downstream consumer or owner who must approve.)
- `@SECURITY.md` if you haven't internalized the 15 mental moves yet.

## Phase 2 — STRIDE the design

Run the full STRIDE walkthrough from `@scripts/threat-model.md`. For each category, answer:

- **What is the specific threat in THIS change?** (Not generic — concrete.)
- **What control mitigates it?**
- **What's the failure mode if the control fails?** (Defense in depth: name the second line.)

Three categories deserve special focus on most changes:

- **I — Information disclosure** — does an unauthorized caller learn anything? Through the response body, the error message, the response time, the cache hit ratio?
- **E — Elevation of privilege** — can a less-privileged actor cause a more-privileged action? (IDOR, mass assignment, missed AuthZ check, race between role check and action.)
- **D — Denial of service** — is there a per-actor rate limit? a cost-per-request cap? a max-input-size?

## Phase 3 — pre-mortem the security failure modes

Beyond the regular failure modes in `@scripts/pre-mortem.md`, enumerate the *adversarial* ones:

- **Replay attack** — request captured and re-sent. Idempotency key + nonce + short-lived tokens.
- **Credential stuffing** — bot iterates known username/password pairs. Rate limit + lockout + breach-list check.
- **IDOR** — attacker changes `?id=123` to `?id=124` and reads someone else's data. Authorization check on every resource fetch.
- **Mass assignment** — attacker adds `is_admin: true` to a POST body. Explicit allow-list of writable fields.
- **TOCTOU race** — state changes between permission check and action. Re-check inside the transaction; or lock.
- **SSRF** — user supplies a URL; server fetches it. Allow-list of destinations; block private IP ranges.
- **Injection** — string concat with user input (SQL, shell, LDAP, XPath). Parameterized queries; never concat.
- **Open redirect** — `?next=` parameter used as redirect target. Allow-list of paths.

## Phase 4 — change strategy

- **Default deny.** Write the rule that rejects everything first; add explicit allows.
- **Two layers, minimum.** Auth at the edge + AuthZ in the service. Crypto + audit. Rate limit + monitoring. Single layer = single point of compromise.
- **No secrets in code, logs, or errors.** Use the platform's secret manager. Add a CI check for committed secrets.
- **Lockfile / pinned deps.** Run `npm audit` / `pip-audit` / `cargo audit` before merge.
- **Reversibility:** security-relevant changes are usually **partially reversible** — a leaked secret cannot be un-leaked; a shipped vulnerability cannot be un-exploited if it was exploited before patch. Treat with extra care.

## Phase 5 — verification

- **Send the attacker request, not the happy path.** What does the endpoint return for unauthorized? Spoofed? Malformed? Oversized? Concurrent-with-permission-revoke?
- **Read your own logs.** Are secrets, tokens, full PII appearing? If yes — fix before merge, not after.
- **Run the dependency audit.** New deps reviewed for maintainer health, transitive count, license?
- **STRIDE answers documented?** They go in the PR description so reviewers see them.

## Red flags most common in this situation

- **RF-23 SQL Injection** — string-concat'd queries.
- **RF-24 Secret in Code/Log/Error** — API key or token visible anywhere except the secret manager.
- **RF-25 Broken Authorization** — endpoint missing AuthZ, or inconsistent across paths to the same resource.
- **RF-26 IDOR** — resource fetched by user-supplied ID with no ownership check.
- **RF-27 Mass Assignment** — `User.update(req.body)` without an explicit allow-list.
- **RF-28 SSRF** — server fetches a URL the user controls.
- **RF-30 Missing Rate Limit** — auth or expensive endpoint with no per-actor cap.
- **RF-01 Silent Swallow** — `catch (e) { return null }` in security-critical code path = the breach you'll never see.

## Refusal scripts for common bad framings

- "We'll add auth later" → "An endpoint shipped without auth IS the breach. Auth before merge, or feature-flag off until auth ships."
- "It's an internal-only endpoint" → "Every internal endpoint is public from the right network position. AuthN+AuthZ regardless."
- "Users don't know about this URL" → "Security by obscurity. Assume the attacker has the source. Replace with a real control."
- "We can trust this internal service" → "Trust is enforced by crypto (mTLS, signed tokens), not by network position. What's the cryptographic basis?"
- "We can't slow down for security on this sprint" → "We can ship vulnerable in this sprint or remediate for the next two. Which is cheaper?"

## When this playbook is wrong

- Pure refactor with no change to inputs, outputs, auth, or data flow — security is unchanged; skip the formal threat model.
- Trivial change to a well-modeled area (e.g., adding a field to an existing well-secured endpoint where the new field follows the existing validation pattern) — apply judgment, not the full ceremony.
- Anything in PCI, HIPAA, or other regulated scope — this playbook is NOT sufficient. Pair with formal `security-review` and the relevant compliance team.

## Escalation

Hand off to formal security review when:
- Touching authentication, session, password handling.
- Crypto, signing, or key management changes.
- New broad-scope external integration.
- This playbook's STRIDE answers are uncertain — uncertainty is the signal to escalate, not to guess.
