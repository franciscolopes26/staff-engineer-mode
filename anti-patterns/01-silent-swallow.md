# RF-01: Silent Swallow

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-01

## Detection

Catch blocks that discard the exception, return a falsy sentinel on error, or log to a sink no one reads. Grep for `catch.*{\s*}`, `except.*:\s*pass`, `catch.*return null`, or `_ =` on Go error returns. Code review red flag: a `try` whose `catch` has fewer lines than the `try` body.

## Smell

```typescript
async function getUserPreferences(userId: string): Promise<UserPreferences | null> {
  try {
    const row = await db.query(
      'SELECT prefs FROM user_preferences WHERE user_id = $1',
      [userId],
    )
    return row?.prefs ?? null
  } catch (e) {
    // swallow — caller will just use defaults
    return null
  }
}

// Caller, three layers up:
async function renderDashboard(userId: string) {
  const prefs = await getUserPreferences(userId)
  const theme = prefs?.theme ?? 'light'
  const locale = prefs?.locale ?? 'en-US'
  return buildDashboard({ theme, locale })
}
```

## Why this fails in production

The `catch` collapses three distinct failures — "row not found", "DB connection refused", and "query timed out" — into the same `null`. When the primary RDS fails over, every user sees their dashboard silently reset to English light-mode for 90 seconds; support tickets blame "the redesign" and no log line ever fired. The same swallow hides a SQL injection regression for six weeks because the malformed query throws, returns null, and the caller cheerfully renders defaults. Silent swallows convert outages into mysteries.

## Fix

```typescript
async function getUserPreferences(userId: string): Promise<UserPreferences | null> {
  try {
    const row = await db.query(
      'SELECT prefs FROM user_preferences WHERE user_id = $1',
      [userId],
    )
    return row?.prefs ?? null // genuine absence — caller decides
  } catch (e) {
    if (e instanceof QueryTimeoutError || e instanceof ConnectionError) {
      // Infra failure: fail fast so upstream can return 503 instead of fake defaults.
      logger.error({ err: e, userId }, 'prefs lookup failed — infra')
      throw new DependencyUnavailableError('user_preferences', { cause: e })
    }
    // Unknown error class — never silently swallow.
    logger.error({ err: e, userId }, 'prefs lookup failed — unknown')
    throw e
  }
}
```

## Reasoning

Error handling is a first-class design concern, not boilerplate. Every catch block must choose one of three responses — handle locally, translate to a domain error, or rethrow — and "do nothing" is never a fourth option. Swallowing exceptions violates the Stability anti-pattern Nygard calls "Cascading Failures hidden by error eating".

## Citation

- *Clean Code*, Robert C. Martin (2008), ch. 7 "Error Handling" — "Don't Return Null" / "Don't Pass Null".
- *Release It!*, Michael Nygard (2nd ed., 2018), ch. 4 "Stability Anti-Patterns".

## See also

- @references/clean-code.md
- @references/release-it.md
