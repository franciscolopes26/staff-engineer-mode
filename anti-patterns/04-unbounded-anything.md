# RF-04: Unbounded Anything (no Steady State)

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-04

## Detection

Any in-memory collection, DB table, log file, or session store that only ever grows. Grep for `Map[`, `sync.Map`, `make(map`, or DB tables without a `created_at` index plus a documented purge job. Red flag: a cache with `Put` but no eviction, a `events` or `audit_log` table with no archival, a session store with no TTL.

## Smell

```go
// pricing/cache.go — "temporary" memoization shipped 18 months ago.

package pricing

import "sync"

type Cache struct {
    mu sync.RWMutex
    m  map[string]*Quote // keyed by hash(symbol, ts, payload)
}

func New() *Cache { return &Cache{m: map[string]*Quote{}} }

func (c *Cache) Get(key string) (*Quote, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    q, ok := c.m[key]
    return q, ok
}

func (c *Cache) Put(key string, q *Quote) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.m[key] = q // grows forever
}
```

## Why this fails in production

Each pod accretes a few hundred MB of `Quote` entries per day. Day 30: GC pause times cross 200ms and p99 latency on the pricing endpoint breaches SLO. Day 45: pods OOM-kill on weekends when the market is closed but background reconciliation still writes keys. The "fix" of bumping the memory limit just delays the next OOM. There is no eviction path because the cache was never designed to reach steady state — Nygard's rule is that every accumulating resource needs a purge counterpart at design time, not as a follow-up ticket.

## Fix

```go
package pricing

import (
    "time"
    lru "github.com/hashicorp/golang-lru/v2/expirable"
)

const (
    maxEntries = 50_000
    entryTTL   = 10 * time.Minute
)

type Cache struct {
    c *lru.LRU[string, *Quote]
}

func New() *Cache {
    // Bounded by count AND time — two independent ceilings.
    return &Cache{c: lru.NewLRU[string, *Quote](maxEntries, nil, entryTTL)}
}

func (c *Cache) Get(key string) (*Quote, bool) {
    return c.c.Get(key)
}

func (c *Cache) Put(key string, q *Quote) {
    c.c.Add(key, q) // oldest evicted when full; expired entries reaped on access
}
```

## Reasoning

Every long-lived process accumulates state — connections, sessions, log lines, cache entries, audit rows. If the accumulation has no bound and no purge, the system cannot reach steady state and is guaranteed to fail; the only question is when. Steady State demands that for every mechanism that adds, there exists a mechanism that removes.

## Citation

- *Release It!*, Michael Nygard (2nd ed., 2018), ch. 5 "Stability Patterns" — Steady State.
- *Designing Data-Intensive Applications*, Martin Kleppmann (2017), ch. 3 — storage growth and compaction.

## See also

- @references/release-it.md
- @references/ddia.md
