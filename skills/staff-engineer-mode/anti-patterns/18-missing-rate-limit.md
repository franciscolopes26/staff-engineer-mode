# RF-30: Missing Rate Limit

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-30

## Detection

Grep for route definitions matching `/login`, `/signin`, `/reset-password`, `/forgot`, `/verify`, `/otp`, `/mfa`, `/register`, plus any handler that calls an LLM, runs an unbounded query, or processes large uploads — and check whether the file imports a rate-limit middleware (`express-rate-limit`, `@fastify/rate-limit`, `slowapi`, a Redis token-bucket helper). No import = no limit. Code review red flag: an auth handler whose only failure response is "401 invalid credentials" with no counter, no lockout, no Retry-After.

## Smell

```typescript
// POST /api/auth/login
export async function login(req: FastifyRequest, reply: FastifyReply) {
  const { email, password } = req.body as { email: string; password: string }

  const user = await db.user.findUnique({ where: { email } })
  if (!user) {
    return reply.code(401).send({ error: 'invalid credentials' })
  }

  const ok = await bcrypt.compare(password, user.passwordHash)
  if (!ok) {
    return reply.code(401).send({ error: 'invalid credentials' })
  }

  const token = await issueJwt({ sub: user.id })
  return reply.send({ token })
}

// app.ts — the entire rate-limit story:
//   app.post('/api/auth/login', login)
//
// Attacker buys a $40 credential-stuffing list (Collection #1, 770M
// email/password pairs leaked from other breaches) and replays it at
// 5,000 req/s from a residential proxy network. Within an hour they
// have valid sessions for every user who reused a password — and your
// access logs show 200s, not 401s, so nothing alerts.
```

## Why this fails in production

Credential stuffing is the #1 cause of account takeover in 2025: attackers know 60-70% of users reuse passwords across sites, so an unrated login endpoint is a free oracle to validate a leaked list against your user base. Beyond logins, an unrated password-reset endpoint lets attackers enumerate which emails are registered (a privacy violation under GDPR Art. 32) and exhaust your transactional email quota; an unrated LLM proxy hands an attacker a $40,000 OpenAI bill overnight; an unrated OTP-send endpoint becomes a free SMS pump that routes traffic to premium-rate numbers the attacker owns ("SMS toll fraud"). The cost of adding a rate limit is one middleware line; the cost of omitting it is measured in breach disclosures and AWS invoices.

## Fix

```typescript
import rateLimit from '@fastify/rate-limit'
import { isPwnedPassword } from 'hibp' // Have I Been Pwned k-anonymity API

await app.register(rateLimit, {
  global: false,
  redis: redisClient, // shared across pods — per-IP, not per-process
})

// Per-IP burst guard: stops volumetric credential stuffing.
const ipLimit = {
  max: 10,
  timeWindow: '1 minute',
  keyGenerator: (req: FastifyRequest) => req.ip,
}

// Per-account guard: stops slow stuffing that rotates IPs but targets
// one inbox. Counter keyed by the email being tried, not the requester.
const accountLimit = {
  max: 5,
  timeWindow: '15 minutes',
  keyGenerator: (req: FastifyRequest) => `login:${(req.body as any)?.email ?? ''}`,
}

app.post(
  '/api/auth/login',
  { config: { rateLimit: ipLimit }, preHandler: app.rateLimit(accountLimit) },
  async (req, reply) => {
    const { email, password } = req.body as { email: string; password: string }
    const user = await db.user.findUnique({ where: { email } })

    // bcrypt.compare on a dummy hash equalises timing — prevents user enumeration.
    const ok = user
      ? await bcrypt.compare(password, user.passwordHash)
      : await bcrypt.compare(password, DUMMY_HASH)
    if (!user || !ok) {
      await recordFailure(req.ip, email) // feeds exponential backoff
      return reply.code(401).send({ error: 'invalid credentials' })
    }

    const token = await issueJwt({ sub: user.id })
    return reply.send({ token })
  },
)

// On password set / reset, refuse known-breached passwords:
//   if (await isPwnedPassword(newPassword)) throw new BadRequest('password appears in a known breach')
```

## Reasoning

A rate limit is the security application of Nygard's stability primitives Shed Load and Back-Pressure — without it, the system has no way to distinguish a legitimate burst from an adversarial one, so every expensive endpoint becomes both a DoS vector and a brute-force oracle. The principle generalises: any operation whose cost (CPU, money, sent SMS, downstream quota) exceeds the cost of the request itself must be rate-limited per actor, or an attacker will arbitrage the gap.

## Citation

- OWASP Top 10 (2021), A07 Identification and Authentication Failures; OWASP ASVS v4.0 §2.2 "General Authenticator Requirements".
- *Release It!*, Michael Nygard (2nd ed., 2018), ch. 5 "Stability Patterns" — Shed Load, Back-Pressure, Bulkheads.

## See also

- @scripts/threat-model.md
- @SECURITY.md
- @references/release-it.md
