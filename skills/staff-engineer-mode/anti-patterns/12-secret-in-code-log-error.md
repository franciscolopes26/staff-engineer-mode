# RF-24: Secret in Code / Log / Error

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-24

## Detection

Hard-coded API keys, tokens, OAuth client secrets, or DB passwords in committed source; logger calls that dump full request/response objects (headers, cookies, bodies); error responses that echo internal messages or stack traces to the client. Grep for `sk_live_`, `AKIA`, `Bearer `, `password\s*[:=]\s*['"]`, `console.log(req`, `logger.*(req\.headers`, `JSON.stringify(err)` in a response body. Code review red flag: any string literal that looks like base64 of 32+ bytes.

## Smell

```typescript
import express, { Request, Response, NextFunction } from 'express'
import axios from 'axios'

const STRIPE_KEY = 'sk_live_51N8xQzL3kP9mF2vB7tH4jR6yE0wA'
const app = express()

app.post('/charges', async (req: Request, res: Response) => {
  const charge = await axios.post(
    'https://api.stripe.com/v1/charges',
    req.body,
    { headers: { Authorization: `Bearer ${STRIPE_KEY}` } },
  )
  res.json(charge.data)
})

app.use((err: Error, req: Request, res: Response, _next: NextFunction) => {
  console.error('request failed', {
    url: req.url,
    headers: req.headers, // includes Authorization, Cookie, x-api-key
    body: req.body,       // includes card.number, cvc
    error: err.stack,
  })
  res.status(500).json({ error: err.message, stack: err.stack })
})

app.listen(3000)
```

## Why this fails in production

The literal `sk_live_...` is now in git history forever — rotating it requires revoking, reissuing, and redeploying before the next `git clone` reaches a contractor's laptop or a public fork. The middleware writes cardholder PAN and CVV to CloudWatch in plaintext, instantly converting a routine logging setup into a PCI-DSS scope violation with mandatory forensic audit. The error handler returns the stack trace — including file paths, library versions, and ORM-generated SQL — to any client, handing attackers a free reconnaissance endpoint. One leaked key here is a six-figure incident: chargebacks, fraud, mandatory breach disclosure, and the auditor's report blocks the next SOC 2 renewal.

## Fix

```typescript
import express, { Request, Response, NextFunction } from 'express'
import axios from 'axios'
import { randomUUID } from 'crypto'
import pino from 'pino'

const STRIPE_KEY = process.env.STRIPE_SECRET_KEY
if (!STRIPE_KEY) throw new Error('STRIPE_SECRET_KEY not configured')

const logger = pino({
  redact: {
    paths: ['req.headers.authorization', 'req.headers.cookie', 'body.card', 'body.cvc'],
    censor: '[REDACTED]',
  },
})

const app = express()

app.post('/charges', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const charge = await axios.post(
      'https://api.stripe.com/v1/charges',
      req.body,
      { headers: { Authorization: `Bearer ${STRIPE_KEY}` } },
    )
    res.json({ id: charge.data.id, status: charge.data.status }) // never echo the full upstream payload
  } catch (e) {
    next(e)
  }
})

app.use((err: Error, req: Request, res: Response, _next: NextFunction) => {
  const requestId = randomUUID()
  logger.error({ requestId, url: req.url, err }, 'request failed') // redactor strips secrets
  res.status(500).json({ error: 'internal_error', requestId }) // client gets a correlator, nothing more
})

app.listen(3000)
```

## Reasoning

Secrets belong in a secret manager (env via dotenv for local, Vault/SSM/Secrets Manager for prod) and never cross the source-control boundary. Logs and external error responses serve different audiences: operators need correlation IDs and redacted detail; clients need a generic failure plus the same correlator so support can join the two. Conflating them — by dumping internals to the wire or secrets to the log — turns observability into an attack surface.

## Citation

- OWASP Top 10 (2021), A02:2021 — Cryptographic Failures, and A05:2021 — Security Misconfiguration.
- *Release It!*, Michael Nygard (2nd ed., 2018), ch. 5 "Stability Patterns" — handshaking and generic external messages with internal correlation IDs.

## See also

- @scripts/threat-model.md
- @SECURITY.md
- @references/release-it.md
