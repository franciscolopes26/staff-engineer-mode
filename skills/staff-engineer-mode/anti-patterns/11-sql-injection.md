# RF-23: SQL Injection

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-23

## Detection

String-concatenated or f-string SQL where any operand traces back to a request, header, query param, form field, or upstream service response. Grep for `f"SELECT`, `f"INSERT`, `"SELECT .* " +`, `format("UPDATE`, `%-formatted` SQL, or any `execute(` whose argument is built with `+`, `.format()`, or template literals. Code review red flag: a query string assembled before `cursor.execute` instead of being passed alongside a params tuple.

## Smell

```python
from fastapi import APIRouter, Request
import psycopg2

router = APIRouter()
conn = psycopg2.connect(DSN)

@router.get("/invoices/search")
def search_invoices(request: Request):
    q = request.query_params.get("q", "")
    company_id = request.query_params.get("company_id", "")

    sql = (
        f"SELECT id, number, total_cents, issued_at "
        f"FROM invoices "
        f"WHERE company_id = '{company_id}' "
        f"  AND (number ILIKE '%{q}%' OR customer_name ILIKE '%{q}%') "
        f"ORDER BY issued_at DESC LIMIT 50"
    )

    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    return [{"id": r[0], "number": r[1], "total": r[2], "at": r[3]} for r in rows]
```

## Why this fails in production

A request with `?q=%25%27%29%20UNION%20SELECT%20id%2C%20token%2C%200%2C%20now%28%29%20FROM%20api_keys--` returns every API key in the table, scoped to nothing, in the same JSON shape the frontend already renders. The `company_id` param is equally exploitable — `' OR '1'='1` walks the entire multi-tenant invoice table. This is the canonical full-database breach: one curl, every customer's data, GDPR Article 33 72-hour notification clock starts the moment the WAF logs surface the payload. SQL injection remains the single most damaging web vulnerability class precisely because the blast radius is "every row the DB role can see".

## Fix

```python
from fastapi import APIRouter, Request, HTTPException
import psycopg2

router = APIRouter()
conn = psycopg2.connect(DSN)

@router.get("/invoices/search")
def search_invoices(request: Request):
    q = request.query_params.get("q", "")
    company_id = request.query_params.get("company_id", "")

    if not company_id.isdigit():  # barricade — reject obviously malformed input early
        raise HTTPException(status_code=400, detail="company_id must be numeric")

    sql = (
        "SELECT id, number, total_cents, issued_at "
        "FROM invoices "
        "WHERE company_id = %s "
        "  AND (number ILIKE %s OR customer_name ILIKE %s) "
        "ORDER BY issued_at DESC LIMIT 50"
    )
    like = f"%{q}%"  # the % wildcards are part of the *value*, not the SQL

    with conn.cursor() as cur:
        cur.execute(sql, (int(company_id), like, like))
        rows = cur.fetchall()

    return [{"id": r[0], "number": r[1], "total": r[2], "at": r[3]} for r in rows]
```

## Reasoning

Treat any boundary between trusted and untrusted code as a barricade: validate and parameterize at the perimeter, then trust the value inside. Parameterized queries are not a stylistic choice — they are the only mechanism that lets the database distinguish *code* from *data*. Concatenation hands that distinction to the attacker.

## Citation

- OWASP Top 10 (2021), A03:2021 — Injection.
- *Code Complete*, Steve McConnell (2nd ed., 2004), ch. 8 "Defensive Programming" — barricades and isolating bad input at the perimeter.

## See also

- @scripts/threat-model.md
- @SECURITY.md
- @references/code-complete.md
