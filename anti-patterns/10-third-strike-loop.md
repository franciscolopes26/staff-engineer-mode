# RF-22: Third-Strike Loop (the bug is not where you think)

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-22

## Detection

The same bug has been "fixed" three times with variations of the same approach — add a retry, bump a timeout, sleep a little longer, mock one more thing — and the symptom keeps coming back. Git log shows a cluster of commits with messages like "fix flaky test", "really fix flaky test", "actually fix flaky test this time". The next commit is about to be a fourth variant of the same idea. You are programming by coincidence: trying things until the symptom hides, without a model of why.

## Smell

```python
# tests/test_billing.py — flaky for three weeks.

# Attempt 1 (commit a1b2c3d): "fix flaky billing test — add retry"
@pytest.mark.flaky(reruns=3)
def test_invoice_totals():
    invoice = create_invoice(customer_id="c1", lines=[(SKU_A, 2), (SKU_B, 1)])
    assert invoice.total_cents == 4500

# Attempt 2 (commit e4f5g6h): "still flaky — bump rerun count"
@pytest.mark.flaky(reruns=5)
def test_invoice_totals():
    invoice = create_invoice(customer_id="c1", lines=[(SKU_A, 2), (SKU_B, 1)])
    assert invoice.total_cents == 4500

# Attempt 3 (commit i7j8k9l): "ugh — add sleep before assert, must be timing"
@pytest.mark.flaky(reruns=5)
def test_invoice_totals():
    invoice = create_invoice(customer_id="c1", lines=[(SKU_A, 2), (SKU_B, 1)])
    time.sleep(0.5)
    assert invoice.total_cents == 4500

# Attempt 4 about to land: "increase sleep to 2s and add another retry layer"
# CI is now 40% slower. The test still flakes once a week.
# Nobody has asked: why does the SAME inputs produce a different total?
```

## Why this fails in production

Each "fix" treats the symptom (the assert fails sometimes) without naming the cause (the same inputs produce different totals). The actual bug is two layers up: `PricingEngine` is instantiated as a module-level singleton, it caches the tax rate from whichever test ran first, and `test_invoice_totals` happens to run after a test that mutates the tax table — sometimes. Retries and sleeps mask this in CI for weeks; then the same singleton ships to production, where one pod boots after a tax-table migration and quietly bills every customer in that pod at the old rate. The "flaky test" was a real bug the whole time.

## Fix

```python
# STOP fixing. Re-read the symptom literally:
# "Given identical inputs, total_cents is sometimes 4500 and sometimes not."
# That sentence rules out timing, network, and flakiness. The function is
# not deterministic in its inputs — so it has hidden inputs. Find them.

# Investigation, not a fourth patch:
#   1. Print invoice.total_cents and the breakdown on failure.
#   2. Discover: tax_cents differs between runs. Tax rate is the hidden input.
#   3. Trace tax rate source -> PricingEngine._cached_rate -> set at import time.
#   4. Root cause: module-level singleton bleeds state across tests.

# Real fix — at the actual layer of the bug:
@pytest.fixture(autouse=True)
def fresh_pricing_engine(monkeypatch):
    # Each test gets its own engine; no shared cache, no order dependency.
    engine = PricingEngine(tax_provider=TaxProvider.from_db())
    monkeypatch.setattr("billing.pricing.engine", engine)
    yield engine

def test_invoice_totals(fresh_pricing_engine):
    invoice = create_invoice(customer_id="c1", lines=[(SKU_A, 2), (SKU_B, 1)])
    assert invoice.total_cents == 4500  # deterministic now; no retry, no sleep

# And — because this was a real production bug — fix the singleton itself:
# inject PricingEngine per-request instead of caching at module scope.
```

## Reasoning

Programming by coincidence is the canonical failure mode here: you observe that something works (or stops failing) without understanding why, and you build on that. Three failed attempts at the same layer is the signal to stop and return to investigation — restate the problem literally, list what you actually know vs. what you assumed, and look one or two layers above the symptom. The bug is almost never where the symptom appears; the symptom is where the bug becomes visible. The 3-Strike rule formalizes this: at strike three, the next action is never another variant of strikes one and two.

## Citation

- *The Pragmatic Programmer*, Hunt & Thomas (20th Anniversary ed., 2019), Tip 62 "Don't Program by Coincidence" / ch. 5 §27.
- "3-Strike Architectural Rule" — widely-adopted community pattern for systematic debugging (obra/superpowers `systematic-debugging`).

## See also

- @scripts/phase-1-investigate.md
- @references/pragmatic-programmer.md
