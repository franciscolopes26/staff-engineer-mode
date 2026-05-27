# STRIDE threat model template

Paste this into your design notes before writing code that touches auth, money, PII, file I/O, external requests, or admin actions. Five minutes during design saves weeks of remediation.

```
CHANGE:           <one-line description of what's being designed>

ASSETS AT RISK:   <data, money, availability, reputation that could be harmed>
                  ____________________________________

THREAT ACTORS:    [ ] external opportunistic (script kiddies, bots)
                  [ ] external targeted (skilled, motivated)
                  [ ] authenticated user (escalation, IDOR)
                  [ ] insider (employee, contractor)
                  [ ] supply chain (compromised dep, vendor)

ATTACK SURFACE:   what entry points does this change add/modify?
                  - endpoint(s):  ____________________
                  - inputs:       ____________________
                  - integrations: ____________________
```

## STRIDE walkthrough

For each row, name the specific threat in YOUR change and the control. "N/A" is a valid answer if the category genuinely doesn't apply — but say so explicitly.

```
S — SPOOFING
  Threat:    can someone claim to be a user/service they aren't?
  Control:   strong auth at boundary (TLS + OAuth/JWT + scope check)
  In MY change: ____________________

T — TAMPERING
  Threat:    can data in transit / at rest be modified?
  Control:   TLS + integrity (MAC/signature/hash) + immutable audit
  In MY change: ____________________

R — REPUDIATION
  Threat:    can an action be performed and then denied?
  Control:   tamper-evident audit log, signed/append-only, with actor ID + timestamp
  In MY change: ____________________

I — INFORMATION DISCLOSURE
  Threat:    can someone read data they shouldn't?
  Control:   AuthZ check at every entry path, errors generic externally,
             encrypt at rest, redact in logs, no PII in error responses
  In MY change: ____________________

D — DENIAL OF SERVICE
  Threat:    can someone make the system unavailable to others?
  Control:   per-actor rate limit, timeout on every remote call,
             input size caps, query cost limits, shed-load under pressure
  In MY change: ____________________

E — ELEVATION OF PRIVILEGE
  Threat:    can a user gain permissions they shouldn't have?
  Control:   default-deny, least-privilege credentials, separation of duties,
             distinct AuthZ check per resource (not per role alone)
  In MY change: ____________________
```

## Specific checks (almost always relevant)

```
[ ] AUTHENTICATION:  what proves the caller is who they claim?
[ ] AUTHORIZATION:   what proves they can do THIS to THIS resource?
                     (separate check from auth, on EVERY entry path)
[ ] RATE LIMITING:   what's the per-actor cap? what about auth endpoints?
[ ] INPUT VALIDATION at the trust boundary; nowhere else
[ ] OUTPUT ESCAPING in the right context (HTML / SQL / shell / URL)
[ ] SECRETS:         where do they live? not in code, not in logs, not in errors
[ ] IDEMPOTENCY:     replay-safe? required key for state-changing ops
[ ] AUDIT:           who did what, when, from where — append-only, off-host
[ ] DEPENDENCIES:    new deps reviewed (maintainer, license, transitive count)?
[ ] LEAST PRIV:      does this code need the credentials it has, or less?
```

## Common framings → the right question

- "We'll add auth later." → No. Endpoint shipped without auth IS the breach; retrofit is harder than ship-with.
- "It's an internal endpoint." → All internal endpoints are public from the right network position. AuthN+AuthZ regardless.
- "Users don't know about this URL." → Security through obscurity. Replace.
- "We trust our own services." → Service-to-service auth (mTLS, signed tokens). The trust is enforced by crypto, not assumption.
- "It's just a debug endpoint." → Debug endpoints in prod are the most common silent root-cause of breach.

## Escalation criteria

Hand off to formal `security-review` when the change touches:
- Authentication, session, password, MFA, account recovery.
- Crypto / signing / key management.
- Payment data (PCI scope).
- PII / PHI (GDPR / HIPAA scope).
- New broad-scope external integration.
- Anything where this template's STRIDE answers are uncertain.

## References

- @references/release-it.md — Nygard on integration points as the #1 stability AND security risk
- @references/code-complete.md — McConnell on barricades and trust boundaries
- @SECURITY.md — full 15 security cognitive moves
- OWASP Top 10 (2021): A01 Broken Access Control, A02 Crypto Failures, A03 Injection, A04 Insecure Design, A05 Misconfig, A06 Vulnerable Components, A07 Auth Failures, A08 Integrity Failures, A09 Logging Failures, A10 SSRF.
