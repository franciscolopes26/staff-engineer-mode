# Governance

How decisions are made in this project.

## Model

**Solo-maintainer (BDFL).** All commits to `main` go through a pull request reviewed by the maintainer. The maintainer has final say on what merges and what does not. This is a deliberate choice — a small skill curated by one person, not a sprawling project assembled by committee. *Conceptual integrity* (Brooks, *The Mythical Man-Month*) is the design principle.

Maintainer: [@franciscolopes26](https://github.com/franciscolopes26).

## What gets merged

A pull request is merged when ALL of these hold:

1. **CI is green.** All four required checks pass — see `.github/workflows/ci.yml`.
2. **Conversations are resolved.** No unresolved review threads.
3. **Linear history is preserved.** The branch is squashed into a single commit on merge; branch is auto-deleted.
4. **The skill's own bar is met.** Specifically:
   - Citations are accurate and verifiable (the `[citation]` issue template exists for the cases where we missed).
   - New red flags, anti-patterns, or playbooks cite a canonical source.
   - No mixed diffs (Two Hats: one PR does one thing).
   - No silent failures introduced (RF-01).
   - The Closing Gate checklist in `SKILL.md` would pass for the change.

## What gets deferred

Proposals that don't get merged are not always wrong — they are often out of scope. Common deferral reasons:

- **No canonical citation.** The skill is grounded in cited literature. New principles without a defensible source citation are deferred until one exists.
- **Doesn't fit the operating-mode framing.** Language-specific style rules belong in `coding-standards`, `nestjs-standards`, etc. Framework-specific rules in their respective skills. This skill is the *operating mode* on top.
- **Over-bloats SKILL.md.** The skill follows progressive disclosure: SKILL.md stays under 500 lines; depth goes in `references/`, `scripts/`, `playbooks/`, `anti-patterns/`, `examples/`. Proposals that inflate SKILL.md without removing equivalent fat get deferred.
- **Duplicates existing content.** Before opening, search the catalog (`SKILL.md` → Red Flag Detection Catalog, `playbooks/`, etc.) to see if the concept is already covered.

Deferrals are documented in the PR/issue close comment. A deferred proposal can be re-opened later with new evidence.

## How decisions are documented

Material decisions are captured in commit messages, PR descriptions, or `CHANGELOG.md`. Particularly:

- **Citation corrections** — the corrected reference and the verification source.
- **Red flag additions/removals** — the canonical source and the failure mode the red flag prevents.
- **Bench eval changes** — the rationale and the before/after PASS/FAIL behavior.
- **Architecture changes** to the skill (e.g. solo-skill vs collection, restructure as plugin) — captured in `CHANGELOG.md` and referenced commit.

Substantial design decisions follow the `@scripts/decisions.md` template from the skill itself (context, options, choice, trade-off accepted, reversibility, revisit).

## How to escalate a disagreement

If a deferral or close decision feels wrong:

1. Re-read the deferral reason; check the specific bar that wasn't met.
2. Open a calm issue with a single specific question: "Re-considering deferral of #N because [new evidence]."
3. Keep it technical and concise. The skill's `signals from the human` guidance applies in both directions.

The maintainer commits to actually re-reading new evidence — not just rubber-stamping the previous decision.

## When this governance model changes

If the project grows to the point where solo-maintainer is no longer right (e.g. 10+ active contributors, >1 maintainer-day per week of triage), this file gets rewritten. The trigger condition is documented now to avoid the trap of "we've always done it this way" *(Hyrum's Law applied to governance)*.

Current state (v1.0.0): zero external contributors, near-zero triage load. Solo-maintainer is appropriate.

## Inspiration

Influences:
- Linux kernel maintainer model (subsystem maintainers + Linus)
- Python BDFL model (Guido era)
- *The Mythical Man-Month* (Brooks) — conceptual integrity through small designer teams
- *Software Engineering at Google* (Winters/Manshreck/Wright) — code review as teaching + ownership boundaries
