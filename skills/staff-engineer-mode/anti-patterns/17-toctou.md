# RF-29: TOCTOU (Time-of-Check / Time-of-Use)

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-29

## Detection

Look for any `if check(x) { act(x) }` sequence where `check` and `act` hit shared state (DB row, file, lock, balance, quota, permission) and nothing serializes the gap between them. Grep for `SELECT … then UPDATE` pairs without `FOR UPDATE`, `os.path.exists` followed by `open`, or "read balance / compare / write balance" patterns that aren't inside a transaction with the row locked.

## Smell

```go
// POST /wallet/debit  { "amount": 30 }
func (h *WalletHandler) Debit(w http.ResponseWriter, r *http.Request) {
    userID := r.Context().Value("userID").(string)
    amount := parseAmount(r)

    balance, err := h.db.GetBalance(r.Context(), userID)
    if err != nil {
        http.Error(w, "lookup failed", http.StatusInternalServerError)
        return
    }

    if balance < amount {
        http.Error(w, "insufficient funds", http.StatusPaymentRequired)
        return
    }

    // GAP: another request for the same user can land here between the
    // check above and the debit below. Both see balance=100, both pass
    // the guard, both call Debit(100, 80). Final balance: -60.
    if err := h.db.Debit(r.Context(), userID, amount); err != nil {
        http.Error(w, "debit failed", http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusNoContent)
}
```

## Why this fails in production

Two concurrent debits worth $80 each against a $100 wallet both pass the check and both commit — the user spends $160 of someone else's money and the ledger goes negative. The window is microseconds wide on a quiet system and seconds wide under load, which is exactly when fraud rings hammer it; the 2014 Mt. Gox transaction-malleability losses, every duplicate-coupon redemption, and most "I got charged for an item that was out of stock" bugs are TOCTOU. Worse, the bug is invisible in single-request tests and only surfaces with concurrent load, so it ships, sits dormant, and detonates on Black Friday.

## Fix

```go
func (h *WalletHandler) Debit(w http.ResponseWriter, r *http.Request) {
    userID := r.Context().Value("userID").(string)
    amount := parseAmount(r)

    // Single atomic statement: the WHERE clause is the guard, so the
    // database (not the application) serializes concurrent debits.
    // RowsAffected==0 means the guard failed AT COMMIT TIME, not at
    // read time, so two racing requests cannot both succeed.
    res, err := h.db.ExecContext(r.Context(), `
        UPDATE wallets
           SET balance = balance - $1,
               updated_at = NOW()
         WHERE user_id = $2
           AND balance >= $1
    `, amount, userID)
    if err != nil {
        http.Error(w, "debit failed", http.StatusInternalServerError)
        return
    }

    rows, _ := res.RowsAffected()
    if rows == 0 {
        http.Error(w, "insufficient funds", http.StatusPaymentRequired)
        return
    }

    w.WriteHeader(http.StatusNoContent)
}

// When you genuinely need the read-then-write shape (e.g. compute a
// fee from the current balance), wrap it in a transaction with an
// explicit row lock:
//   BEGIN; SELECT balance FROM wallets WHERE user_id=$1 FOR UPDATE;
//   ... compute ... UPDATE wallets SET balance = $new WHERE user_id=$1; COMMIT;
```

## Reasoning

The check and the act must happen under the same isolation boundary, or the gap is a race. Either collapse them into one atomic statement (the conditional UPDATE), or take a lock that holds across both (`SELECT … FOR UPDATE` inside a transaction); under Read Committed isolation, a bare `SELECT` followed by an `UPDATE` is the textbook lost-update anomaly.

## Citation

- *Designing Data-Intensive Applications*, Martin Kleppmann (2017), ch. 7 "Transactions" — "Preventing Lost Updates" and "Write Skew and Phantoms".
- OWASP Top 10 (2021), A04 Insecure Design; CWE-367 "Time-of-check Time-of-use (TOCTOU) Race Condition".

## See also

- @scripts/threat-model.md
- @SECURITY.md
- @references/designing-data-intensive-applications.md
