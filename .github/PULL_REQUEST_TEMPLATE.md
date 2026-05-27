## What

<one or two sentences of what THIS PR does>

## Why

<the problem / motivation; link to issue if any>

## How

<short tour of the approach — key decisions, not every file>

## Verification

Following `@scripts/calibrate.md` — classify each claim:

- **VERIFIED:** <thing — how I verified>
- **TESTED:** <thing — what tests; what was NOT covered>
- **ASSUMED:** <thing — based on what assumption>
- **NOT-CHECKED:** <thing — why; who should verify>

## Reversibility

- [ ] Reversible — can be reverted with a normal `git revert` and no migration
- [ ] Partially reversible — back-out plan: _________________________________
- [ ] Hard to reverse — explicitly authorized for this exact change

## Bench impact

Did any of the following change?

- [ ] `SKILL.md` (re-run bench.md mentally; note PASS/FAIL deltas)
- [ ] An entry in the Red Flag Detection Catalog
- [ ] A `scripts/` template
- [ ] A `playbooks/` recipe
- [ ] A `references/` digest

If yes, document expected bench delta in this PR description.

## Two Hats check

- [ ] This PR does ONE thing (refactor OR feature OR bug fix), not multiple
- [ ] Imports / formatting cleanup is NOT mixed with substantive changes

## Citation

If you added or modified a citation: source URL or book chapter you verified against.
