# RF-05: Patch-and-Hope (symptom fix without root cause)

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-05

## Detection

A change whose justification is "the test/alert stopped firing" rather than "the underlying invariant is restored". Grep for `@pytest.mark.flaky`, `retry=`, `try: ... except: pass # intermittent`, `sleep(2) # race`. Code review smell: PR description says "fixes flake" or "makes CI green" without naming the actual race / ordering / state bug.

## Smell

```python
# tests/test_checkout.py — was failing ~1 in 8 runs on CI.

import pytest
from .helpers import place_order, get_order_status

@pytest.mark.flaky(reruns=3, reruns_delay=2)  # added because "CI keeps going red"
def test_order_status_after_payment():
    order = place_order(user_id="u1", items=[("sku-1", 1)])
    pay(order.id, amount=order.total)
    # Sometimes status is still PENDING here. Add a sleep just in case.
    import time; time.sleep(1)
    assert get_order_status(order.id) == "PAID"
```

```python
# checkout/service.py — what the test was actually catching.

def pay(order_id: str, amount: Decimal) -> None:
    charge_id = payment_gateway.charge(order_id, amount)  # 1
    publish_event("payment.captured", order_id, charge_id) # 2 — async consumer flips status
    # returns before consumer has processed; caller sees PENDING for ~200-1500ms
```

## Why this fails in production

The flake was a real race: `pay()` returns before the payment-captured event is processed, so any caller — test, frontend, partner API — can observe a paid order still marked `PENDING`. The `@flaky` annotation and `sleep(1)` hide the bug from CI but ship the race to production. Two months later, a customer's mobile app retries an order it believes is `PENDING`, the idempotency window has already expired on the payment gateway, and the customer is charged twice. The on-call engineer finds the original "fix this flake" PR and realizes the team has been patching the symptom for a quarter. Hunt & Thomas call this "Programming by Coincidence" — code that happens to work without anyone understanding why.

## Fix

```python
# checkout/service.py — make the contract synchronous from the caller's POV.

def pay(order_id: str, amount: Decimal) -> PaymentResult:
    charge_id = payment_gateway.charge(order_id, amount)
    # Update order state in the SAME transaction as recording the charge.
    # Event publication moves to an outbox row consumed by a separate worker;
    # the order's status is authoritative the instant pay() returns.
    with db.transaction():
        db.execute(
            "UPDATE orders SET status = 'PAID', charge_id = $1 WHERE id = $2 AND status = 'PENDING'",
            charge_id, order_id,
        )
        db.execute(
            "INSERT INTO event_outbox(topic, payload) VALUES ('payment.captured', $1)",
            {"order_id": order_id, "charge_id": charge_id},
        )
    return PaymentResult(charge_id=charge_id, status="PAID")
```

```python
# tests/test_checkout.py — no sleep, no flake annotation, asserts the real contract.

def test_order_status_after_payment():
    order = place_order(user_id="u1", items=[("sku-1", 1)])
    pay(order.id, amount=order.total)
    assert get_order_status(order.id) == "PAID"  # holds synchronously now
```

## Reasoning

A fix that silences the symptom without identifying the cause is a debt instrument issued against future on-call shifts. The Pragmatic Programmer's discipline — "prove it" before assuming, never "program by coincidence" — applies most sharply to flaky tests, intermittent alerts, and "retry until it works" patches. If you cannot state the invariant that was being violated, you have not fixed anything.

## Citation

- *The Pragmatic Programmer*, Hunt & Thomas (20th Anniv. ed., 2019), Tip 34 "Don't Assume It — Prove It"; Tip 62 "Don't Program by Coincidence".
- *Debugging*, David J. Agans (2002), Rule 3 "Quit Thinking and Look".

## See also

- @references/pragmatic-programmer.md
- @scripts/pre-mortem.md
