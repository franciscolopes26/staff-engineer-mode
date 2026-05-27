# Playbook: Zero-Downtime Schema Migration

**When:** Adding, renaming, retyping, or dropping a column / table / index on a database under live traffic.
**Goal:** Schema evolves with no dropped writes, no extended lock, no broken readers, and each step independently reversible.

## Phase 1 — read first
- Enumerate every consumer of the table: services, batch jobs, replicas, BI / SAF-T exports, ad-hoc scripts. `grep` repo-wide for the table name and every column you intend to touch (`@scripts/find-callers.sh`).
- Read the existing migration tool's conventions (MikroORM / `pg-migrate` / Flyway). Check the project's rule for "never edit existing migrations — always create new ones".
- Measure the table: row count, average row width, indexes, current write RPS, slowest query. Without these numbers you cannot predict lock duration.
- Check the DB engine's lock semantics for the operation you plan (Postgres `ADD COLUMN` with default, `ALTER TYPE`, `DROP COLUMN`, `CREATE INDEX` vs `CREATE INDEX CONCURRENTLY`).
- Confirm the migration role / user (e.g., `manager` vs `app_user_*`) and that rollback path is reachable from the same role.

## Phase 2 — contracts to surface
- "Data outlives code" (Kleppmann, *Designing Data-Intensive Applications*). The schema is a long-lived API; both backward and forward compatibility are mandatory for the duration of the rollout.
- Pre-condition: every running version of every consumer can read AND write the table at every intermediate state.
- Invariant: no row may be written that any concurrently-running consumer cannot read without erroring.
- Idempotency: every migration step must be safe to re-run (deploys retry, pods restart mid-batch).
- Concurrency: backfills must be bounded in batch size and rate; never `UPDATE` the whole table in one statement.
- See `@scripts/contracts.md`.

## Phase 3 — failure modes specific to this situation
- `ALTER TABLE` taking an `ACCESS EXCLUSIVE` lock for longer than the statement timeout, blocking all reads/writes: fail-fast — pre-measure, use `CONCURRENTLY` / nullable-add patterns.
- Old code reading a column that no longer exists (or new code reading a column not yet backfilled): handle — expand-and-contract enforces ordering.
- Backfill crashes halfway, leaving rows partially migrated: handle — make every batch idempotent and resumable via a watermark column or `WHERE new_col IS NULL`.
- Rollback under load: a deploy that worked forward may not work backward if old code can't read new schema; verify both directions before merging.
- Replica lag during long migration: writes succeed on primary, reads from replica see stale schema. Accept only if reads are eventually-consistent already; otherwise pause replica-routed reads.
- Foreign keys / triggers / generated columns silently amplifying lock scope: fail-fast — list them before running.
- Hyrum's Law (SWE@Google): some consumer depends on column ordering, default value, or null behavior you don't know about — grep wider than you think necessary.
- Full enumeration: `@scripts/pre-mortem.md`.

## Phase 4 — change strategy
Expand-and-contract, one PR per step. Never combine.
1. **Add** the new column nullable, no default that rewrites the table. Deploy.
2. **Dual-write** from application code: write to old and new column. Deploy. Verify in logs.
3. **Backfill** in bounded batches (e.g., 1000 rows, `WHERE new IS NULL`, sleep between batches). Track progress. Resumable.
4. **Dual-read**: code reads new column, falls back to old. Deploy. Verify metrics.
5. **Read-new-only**: drop the fallback. Deploy.
6. **Stop dual-write**: write only the new column. Deploy.
7. **Drop** the old column (or keep for N days as a safety net). Separate PR.

Rules:
- Each step ships independently and is reversible on its own.
- The drop step (7) is irreversible without a backup — treat it as such; require a pre-drop snapshot and a waiting period.
- For renames, use the same pattern — never `ALTER COLUMN RENAME` on a live table consumed by N services.
- Reversibility: steps 1–6 are local-to-shared (reversible by deploying the previous version + a small revert migration). Step 7 is **irreversible**.

## Phase 5 — verification
- Rehearse the migration on a restored copy of production data at production size. Measure lock time, batch duration, total runtime. If you have not measured on real data volume, you have not tested.
- Run the migration with a synthetic write load against the rehearsal DB. Confirm no dropped writes.
- Test the rollback path on the same rehearsal DB — deploy step N, then deploy step N-1, confirm both directions work.
- Observe in stage / canary: error rate on the table's consumers, replica lag, lock waits, slow query log. Bake for at least one full traffic cycle (peak hour) before advancing.
- See `@scripts/verify.md`.

## Red flags most common in this situation
- **RF-02 Mixed Diff** — combining "add column" + "backfill" + "switch reads" in one PR. Each must be its own deploy.
- **RF-04 Unbounded Anything** — `UPDATE table SET new = old` with no `LIMIT` / batching will lock the table and time out.
- **RF-18 Authorization Drift** — running migrations as `app_user_*` instead of the `manager` role, or vice versa, often surfaces here because the app user lacks DDL grants.

## Refusal scripts for common bad framings here
- "Just run `ALTER TABLE`, it's a small table" → "What is the row count and write RPS in production? `Small` in dev is not small in prod."
- "Combine the migration and the code change in one PR, it's atomic" → "It is not atomic — the migration and the deploy land at different times. Old pods will see new schema or new pods will see old schema. Split it."
- "Skip the dual-write step, we'll backfill once at the end" → "Then every row written between backfill and cutover is missing the new column. Dual-write is not optional."
- "We don't need to test rollback, we won't roll back" → "You roll back when you must, not when you plan to."
- See `@scripts/refusal-scripts.md`.

## When this playbook is wrong
- Brand-new table with zero consumers — ship the schema in one migration, no expand-and-contract needed.
- Table is small (< ~10k rows) AND the operation is fast AND a brief planned maintenance window is acceptable — a single locked migration may be simpler. Decide explicitly, do not default to it.
- The change is additive and read-only (a new index built `CONCURRENTLY`) with no application code change — most steps collapse; still measure.

