# RF-02: Mixed Diff (Two-Hats violation)

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-02

## Detection

A single commit (or PR) that combines a refactor, a behavior change, and incidental cleanup. Look for diffs where a function is renamed, its logic altered, and unrelated imports reordered. `git log --stat` showing a high file count with one-line edits across many files alongside a substantive logic change is a strong signal.

## Smell

```python
# Single commit: "fix invoice rounding + cleanup"
# Diff touches 14 files. Tests pass. Reviewer LGTMs in 90 seconds.

# invoicing/service.py
- def calc_invoice_total(line_items, vat_rate):
-     subtotal = sum(item.price * item.qty for item in line_items)
-     vat = subtotal * vat_rate
-     return subtotal + vat
+ def compute_invoice_total(items, vat):
+     # fixed: round each line BEFORE summing, not after
+     subtotal = sum(round(i.price * i.qty, 2) for i in items)
+     return subtotal + round(subtotal * vat, 2)

# invoicing/api.py — rename propagated
- from .service import calc_invoice_total
+ from .service import compute_invoice_total

# invoicing/api.py — unrelated import reorder (12 lines moved)
- from datetime import datetime
- import logging
- from .models import Invoice
+ import logging
+ from .models import Invoice
+ from datetime import datetime

# invoicing/api.py — and a silent behavior tweak slipped in
- total = calc_invoice_total(invoice.lines, 0.23)
+ total = compute_invoice_total(invoice.lines, invoice.vat_rate)  # was hardcoded
```

## Why this fails in production

Two weeks later finance reports that Q3 invoices for non-PT customers are short by exactly the difference between 23% and their local VAT — the hardcoded `0.23` removal was the actual bug fix, but it was hidden inside a rename and import shuffle, so the rollback strategy is "revert and break the rounding fix too". Bisecting is useless because every commit in the range mixes concerns. Code review missed the VAT change entirely because the reviewer was tracking the rename. Kent Beck's "Two Hats" rule exists precisely to prevent this: when you change behavior, do not also refactor; when you refactor, do not also change behavior.

## Fix

```python
# Commit 1: pure refactor — rename only, behavior identical.
- def calc_invoice_total(line_items, vat_rate):
+ def compute_invoice_total(line_items, vat_rate):
      subtotal = sum(item.price * item.qty for item in line_items)
      vat = subtotal * vat_rate
      return subtotal + vat

# Commit 2: behavior change — per-line rounding. Tests updated to assert new contract.
  def compute_invoice_total(line_items, vat_rate):
-     subtotal = sum(item.price * item.qty for item in line_items)
-     vat = subtotal * vat_rate
-     return subtotal + vat
+     subtotal = sum(round(i.price * i.qty, 2) for i in line_items)
+     return subtotal + round(subtotal * vat_rate, 2)

# Commit 3: bug fix — stop hardcoding VAT, use invoice's own rate. Single-line diff.
- total = compute_invoice_total(invoice.lines, 0.23)
+ total = compute_invoice_total(invoice.lines, invoice.vat_rate)
```

## Reasoning

Each commit must answer exactly one question: "what did this change?". Mixing concerns destroys bisectability, hides intent from reviewers, and couples revertable fixes to non-revertable refactors. Fowler's Two Hats principle: at any moment you are either refactoring (preserving behavior) or adding function (changing behavior), never both.

## Citation

- *Refactoring*, Martin Fowler (2nd ed., 2018), ch. 2 "Principles in Refactoring" — the formal Two Hats statement. The worked example demonstrating the discipline is in ch. 1 "A First Example".
- *Software Engineering at Google*, Winters/Manshreck/Wright (2020), ch. 9 "Code Review" — small-CL discipline.

## See also

- @references/refactoring.md
- @references/sweg.md
