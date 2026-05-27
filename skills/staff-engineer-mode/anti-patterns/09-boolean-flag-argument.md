# RF-15: Boolean Flag Argument

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-15

## Detection

A function takes a `bool` parameter (often the last one) that switches its behavior between two distinct code paths. Grep for signatures like `(..., bool)`, `is*`, `should*`, `force`, `dryRun`, `urgent`. Call sites read as `doThing(x, true)` with no clue at the callsite what `true` means. The function body usually contains an `if flag { ... } else { ... }` that splits cleanly into two algorithms.

## Smell

```go
// notifications.go
func SendEmail(ctx context.Context, user User, subject, body string, urgent bool) error {
    if urgent {
        // Different sender pool, different template wrapper, different retry policy,
        // and a Slack page on failure.
        if err := sesUrgentPool.Send(ctx, user.Email, subject, wrapUrgent(body)); err != nil {
            slack.Page(ctx, "urgent email failed", err, user.ID)
            return retryWithBackoff(ctx, 5, func() error {
                return sesUrgentPool.Send(ctx, user.Email, subject, wrapUrgent(body))
            })
        }
        return nil
    }
    // Standard path — best-effort, no paging, single attempt.
    return sesStandardPool.Send(ctx, user.Email, subject, wrapStandard(body))
}

// Caller — what does `true` mean here? You have to open the function to find out.
if err := SendEmail(ctx, user, "Your invoice", body, true); err != nil {
    return err
}

// And here, a tired engineer at 2am copies the line above for a password reset:
SendEmail(ctx, user, "Password reset", body, true) // pages on-call for every reset
```

## Why this fails in production

The flag turns one function name into two algorithms that share nothing but a signature, and the call site loses the intent — `true` is just a magic literal. The 2am copy-paste above pages on-call for every password reset until someone notices the alert volume; meanwhile a different caller passes `false` for a genuinely urgent compliance email and the team misses an SLA because there's no retry. Boolean flags hide the fact that the caller is choosing between distinct operations, and they make grep useless — you can't find "all the urgent sends" without reading every callsite.

## Fix

```go
// notifications.go — two functions, two intentions, no flag.
func SendStandardEmail(ctx context.Context, user User, subject, body string) error {
    return sesStandardPool.Send(ctx, user.Email, subject, wrapStandard(body))
}

func SendUrgentEmail(ctx context.Context, user User, subject, body string) error {
    if err := sesUrgentPool.Send(ctx, user.Email, subject, wrapUrgent(body)); err != nil {
        slack.Page(ctx, "urgent email failed", err, user.ID)
        return retryWithBackoff(ctx, 5, func() error {
            return sesUrgentPool.Send(ctx, user.Email, subject, wrapUrgent(body))
        })
    }
    return nil
}

// Callers now say what they mean — and grep finds them.
if err := SendUrgentEmail(ctx, user, "Your invoice", body); err != nil {
    return err
}

// The password reset caller can't accidentally page on-call — there's no flag to flip.
if err := SendStandardEmail(ctx, user, "Password reset", body); err != nil {
    return err
}
```

## Reasoning

Martin states it plainly: "Flag arguments are ugly. Passing a boolean into a function is a truly terrible practice. It immediately complicates the signature of the method, loudly proclaiming that this function does more than one thing." A function should do one thing; if it does two, give them two names. The split also restores discoverability — `grep SendUrgentEmail` finds every urgent send, where `grep "SendEmail.*true"` is brittle and misses variables.

## Citation

- *Clean Code*, Robert C. Martin (2008), ch. 3 "Functions" — "Flag Arguments" / "Do One Thing".

## See also

- @references/clean-code.md
