# Example: Adding a feature to a 600-line legacy function

A worked example showing the five-phase loop applied to a concrete situation. The scenario is invented; the patterns are real.

## The task

Product wants a "Resend invoice" button in the billing dashboard. When clicked, it should re-send the invoice email for an existing invoice. The relevant code lives inside `BillingService.processBilling()` — a 612-line method that handles invoice creation, payment retry, email dispatch, and analytics. Zero tests. Last meaningful commit 18 months ago.

## The wrong way (the ~30-second answer)

```typescript
// In BillingService.processBilling(), line 384 — somewhere in the middle.
if (sendEmail) {
  await this.mailer.send(invoice.customerEmail, this.buildInvoiceEmail(invoice))
}

// And a new method bolted on at the bottom of the class:
async resend(invoiceId: string) {
  const invoice = await this.repo.findById(invoiceId)
  await this.mailer.send(invoice.customerEmail, this.buildInvoiceEmail(invoice))
}
```

**Why it's wrong** — even though it "works":

- The new code path doesn't go through `processBilling`'s logic (idempotency check, audit log, throttle).
- `buildInvoiceEmail` is now called from two places; behavior diverges silently if anyone changes the inline version.
- No test covers either the old or new path.
- The PR diff also "while we're here" reformats 14 lines (mixed diff — RF-02).
- No timeout on `mailer.send`; the new button can hang for 30 seconds on a flaky SMTP day (RF-03).

This is the diff a junior ships. A staff engineer's path looks different.

## Phase 1 — UNDERSTAND

```bash
# Find every place the old behavior is invoked.
$ scripts/find-callers.sh processBilling apps/billing/
apps/billing/src/jobs/nightly.ts:42:  await billingService.processBilling(...)
apps/billing/src/api/billing.controller.ts:88:  return this.svc.processBilling(...)
apps/billing/src/admin/replay.ts:17:  await svc.processBilling(..., { sendEmail: false })
```

Three callers. Two pass `sendEmail: true`; one passes `false`. The boolean is a flag argument (RF-15) — already a smell.

Read each caller:

- `nightly.ts` — cron job, runs at 02:00, retries on failure with backoff. **Idempotency matters.**
- `billing.controller.ts` — synchronous HTTP, user-initiated. **Latency matters.**
- `replay.ts` — admin reprocessing tool. **No email.**

Read the function itself — line by line. Note the implicit invariant: every successful path writes to `BillingAudit`. The proposed "Resend" path bypasses this. That alone is the contract change the wrong way ships without noticing.

`git blame` reveals: line 384's `if (sendEmail)` was added in PR #2103 with the message *"hot-fix: don't email on replay"*. The flag was meant for **one** caller (replay), but its presence reshaped the whole function.

## Phase 2 — SPECIFY the contracts

Filling in `@scripts/contracts.md` for the new "resend" operation:

```
FUNCTION:        BillingService.resendInvoice(invoiceId)
INPUTS:          invoiceId — UUID of an existing invoice
PRECONDITION:    invoice exists; caller is authorized for this customer;
                 invoice is in a state where resend is meaningful
                 (issued / pending — NOT cancelled or draft)
POSTCONDITION:   one email dispatched; one BillingAudit row written;
                 invoice.lastEmailedAt updated
INVARIANT:       AT MOST ONE email per invoice per minute (throttle),
                 even if the user clicks the button twice
IDEMPOTENCY:     two clicks within the throttle window → one email, not two
CONCURRENCY:     two admins clicking simultaneously → still one email
ORDERING:        audit row MUST be written before the email is dispatched
                 (so a crash mid-send leaves a trail)
ATOMICITY:       audit-write and mark-as-sent are one DB transaction;
                 email dispatch happens AFTER commit (otherwise rollback
                 leaves a sent email with no audit)
AUTHORIZATION:   admin role OR the customer themselves (self-service)
HYRUM'S LAW:     callers of the existing processBilling() rely on the
                 BillingAudit row being written. Don't break that.
```

The filled-in template surfaced four invariants the wrong way violated. Worth more than the writing time.

## Phase 3 — PRE-MORTEM the failure modes

From `@scripts/pre-mortem.md`:

| Failure | Mode | How |
|---------|------|-----|
| Invoice doesn't exist | **Fail-fast** | 404 + log |
| Caller unauthorized | **Fail-fast** | 403 + log + alert if repeated |
| Invoice in wrong state | **Fail-fast** | 422 with explanation |
| Two clicks within 1 min | **Handle** | throttle: second click returns "already sent X seconds ago", same response |
| Two admins, same moment | **Handle** | DB row-lock during audit write |
| SMTP down | **Handle** | retry with backoff; after 3 fails → fail with retry-after; do NOT mark as sent |
| SMTP slow (>5s) | **Fail-fast** | timeout 5s; mark as transient; queue for retry |
| Audit row written, dispatch fails | **Accept** | the audit row says "attempted"; reconciliation job retries; documented |

The dispatch-fails-after-audit-write case is the one most engineers don't think about. Naming it explicitly turned a "bug in 6 months" into a "design decision in 5 minutes."

## Phase 4 — CHANGE in small reversible steps

Three commits. Each one is independently revert-able and shippable.

### Commit 1: Characterization test (no behavior change)

```typescript
// apps/billing/test/processBilling.characterization.spec.ts
describe('processBilling — characterization', () => {
  it('writes a BillingAudit row on success when sendEmail=true', async () => {
    const svc = makeService()
    await svc.processBilling(invoiceFixture(), { sendEmail: true })
    expect(await auditRepo.findByInvoiceId(invoiceFixture().id)).toBeDefined()
  })
  it('still writes the audit row when sendEmail=false', async () => {
    const svc = makeService()
    await svc.processBilling(invoiceFixture(), { sendEmail: false })
    expect(await auditRepo.findByInvoiceId(invoiceFixture().id)).toBeDefined()
  })
})
```

Two tests pinning down the current behavior. They give a safety net for the refactor in Commit 2. (Feathers — characterization tests come *before* changes, not after.)

### Commit 2: Refactor — extract `sendInvoiceEmail` and `recordBillingAudit` (no behavior change)

```typescript
// Before: 612 lines, lines 380–410 inlined inside processBilling.
// After: two well-named private methods, processBilling now reads as
// a 30-line orchestration of named steps.

private async sendInvoiceEmail(invoice: Invoice): Promise<void> {
  await this.mailer.send(invoice.customerEmail, this.buildInvoiceEmail(invoice), {
    timeoutMs: 5_000,
    retry: { attempts: 3, backoffMs: 1_000 },
  })
}

private async recordBillingAudit(invoice: Invoice, action: BillingAuditAction): Promise<void> {
  await this.auditRepo.insert({
    invoiceId: invoice.id,
    customerId: invoice.customerId,
    action,
    occurredAt: new Date(),
  })
}
```

Characterization tests stay green. PR is mechanical — easy to review. (Fowler's *Two Hats*: this is the refactor hat.)

### Commit 3: Add `resendInvoice` (behavior change)

```typescript
async resendInvoice(invoiceId: string, actor: Actor): Promise<ResendResult> {
  const invoice = await this.repo.findById(invoiceId)
  if (!invoice) throw new InvoiceNotFoundError(invoiceId)
  if (!actor.canResend(invoice)) throw new UnauthorizedError()
  if (!RESENDABLE_STATES.has(invoice.state)) {
    throw new InvalidStateError(`invoice ${invoiceId} is in state ${invoice.state}`)
  }

  // Throttle — Hyrum's Law: existing callers rely on lastEmailedAt being
  // truthful, so we enforce the window at the boundary, not inside the
  // mailer.
  const since = Date.now() - (invoice.lastEmailedAt?.getTime() ?? 0)
  if (since < THROTTLE_MS) {
    return { status: 'throttled', secondsAgo: Math.round(since / 1000) }
  }

  return this.db.transaction(async (tx) => {
    await this.recordBillingAudit(invoice, 'resend_initiated', tx)
    await this.repo.markEmailed(invoice.id, new Date(), tx)
    // Dispatch AFTER tx commits — otherwise rollback leaves a sent email
    // with no audit. The audit says "initiated"; reconciliation handles
    // failed dispatches.
    tx.afterCommit(() => this.sendInvoiceEmail(invoice))
    return { status: 'sent' }
  })
}
```

Three explicit guards, one transaction, one post-commit hook. Each piece is named in the spec from Phase 2.

## Phase 5 — VERIFY the behavior

Type-check passes. Unit tests pass. None of that is the verification.

Surface checklist from `@scripts/verify.md`:

```
[x] Started dev server; opened the billing dashboard
[x] Clicked "Resend invoice" on a valid invoice — email arrived in mailhog
[x] Clicked twice within 1 minute — second click returned "throttled"
[x] Clicked on a cancelled invoice — got the 422 error with explanation
[x] Logged in as a different customer's user — got 403
[x] Stopped mailhog; clicked resend — audit row written, dispatch fails,
    invoice.lastEmailedAt SET (so the retry job picks it up), no crash
[x] Restarted mailhog; verified the reconciliation job re-dispatches
[x] Complexity budget: BillingService is now 530 lines, down from 612.
    Two extracted methods both have simple interfaces and do real work
    (deep modules — Ousterhout). resendInvoice has one job, named after it.
```

Five surfaces exercised, including two non-happy paths. If the dev environment couldn't reach one of these surfaces, the right answer is to *say so*, not to claim it works.

## Books invoked

| Phase | Discipline | Source |
|-------|------------|--------|
| 1 | Characterization tests, read callers, Chesterton's Fence | Feathers, *Working Effectively with Legacy Code*, ch. 13 "Characterization Tests" |
| 2 | Contract specification; Hyrum's Law on existing callers | *Software Engineering at Google*, ch. 1 |
| 3 | Failure-mode enumeration; timeout + retry on remote calls | Nygard, *Release It!*, ch. 5 |
| 4 | Two Hats; Extract Function; Sprout | Fowler, *Refactoring*, ch. 2 "Principles in Refactoring"; Feathers, *WEwLC*, ch. 6 |
| 4 | Boolean flag argument as smell (`sendEmail`) | Martin, *Clean Code*, ch. 3 |
| 5 | "If it talks to the DB / network, it's not a unit test" | Feathers, *WEwLC*, ch. 2 "Working with Feedback" |
| 5 | Deep modules check | Ousterhout, *A Philosophy of Software Design*, ch. 4 |

## The takeaway

The wrong way is faster by maybe 30 minutes. The right way prevents:

- one silent audit-row gap (no one would notice for months),
- one race on double-resend,
- one bug from the inlined `buildInvoiceEmail` diverging,
- one hung-button on a slow SMTP day.

The skill is not the writing speed. It's the failure-mode catalog you ran past first.
