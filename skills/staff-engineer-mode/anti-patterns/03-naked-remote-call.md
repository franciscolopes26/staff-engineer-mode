# RF-03: Naked Remote Call

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-03

## Detection

Any outbound HTTP, gRPC, or DB call without an explicit timeout, retry policy, or circuit breaker. Grep for `fetch(`, `axios.`, `requests.get(`, `http.Get(` and inspect the call site. Red flag: no `AbortController`, no `timeout:`, no wrapper around the client. Default timeouts in many HTTP libraries are infinity or several minutes.

## Smell

```typescript
// notifications.service.ts — fans out per user on every order event.

import { fetch } from 'undici'

export class PushService {
  async notify(userId: string, payload: NotifyPayload): Promise<void> {
    const res = await fetch('https://push.vendor.example/v1/send', {
      method: 'POST',
      headers: { 'content-type': 'application/json', authorization: this.token },
      body: JSON.stringify({ userId, payload }),
    })
    if (!res.ok) throw new Error(`push failed: ${res.status}`)
  }
}

// orders.service.ts
async function onOrderPlaced(order: Order) {
  for (const userId of order.watchers) {
    await pushService.notify(userId, { kind: 'ORDER_PLACED', orderId: order.id })
  }
}
```

## Why this fails in production

The push vendor's TLS terminator hangs — accepts the TCP connection, never sends a response byte. With no timeout, every `fetch` sits open for the OS-level default (often 2+ minutes). Each blocked `onOrderPlaced` holds an event-loop slot, a DB connection from the surrounding transaction, and a Node worker. Within 90 seconds the order service's connection pool is exhausted, healthchecks fail, the LB pulls the pod, and the cascade kills the cluster — the vendor's brown-out has become your full outage. Nygard's term for this exact failure mode is "Chain Reaction via Integration Point" and the only defense is bulkheads at every remote boundary.

## Fix

```typescript
import { fetch } from 'undici'
import CircuitBreaker from 'opossum'

const PUSH_TIMEOUT_MS = 800

async function rawPush(userId: string, payload: NotifyPayload, token: string) {
  const ctrl = new AbortController()
  const t = setTimeout(() => ctrl.abort(), PUSH_TIMEOUT_MS)
  try {
    const res = await fetch('https://push.vendor.example/v1/send', {
      method: 'POST',
      headers: { 'content-type': 'application/json', authorization: token },
      body: JSON.stringify({ userId, payload }),
      signal: ctrl.signal,
    })
    if (!res.ok) throw new Error(`push ${res.status}`)
  } finally {
    clearTimeout(t)
  }
}

// Circuit breaks after 50% failures over 10s; half-opens after 30s.
export const pushBreaker = new CircuitBreaker(rawPush, {
  timeout: PUSH_TIMEOUT_MS,
  errorThresholdPercentage: 50,
  resetTimeout: 30_000,
})
pushBreaker.fallback(() => { /* enqueue for async retry, do NOT block caller */ })
```

## Reasoning

Every integration point is a failure point. The defenses — Timeout, Circuit Breaker, Bulkhead, Steady State — are non-optional at any remote boundary, regardless of how reliable the upstream "usually" is. The rule is: if the call leaves your process, it has a timeout and a fallback.

## Citation

- *Release It!*, Michael Nygard (2nd ed., 2018), ch. 5 "Stability Patterns" — Timeout, Circuit Breaker, Bulkhead.
- *Designing Data-Intensive Applications*, Martin Kleppmann (2017), ch. 8 — "The Trouble with Distributed Systems".

## See also

- @references/release-it.md
- @references/ddia.md
