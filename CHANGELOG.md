# Changelog

All notable changes to this skill follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Notes

- `bench.md` evals have NOT yet been executed end-to-end. The expected behaviors are designed; actual skill firing has not been measured against them.
- Chapter citations across `references/` and inline in `SKILL.md` have been pulled from source-research agents and not independently verified line-by-line. Some chapter numbers may be approximate.
- `/plugin marketplace add franciscolopes26/staff-engineer-mode` install path follows the Claude Code docs but has not been tested in a fresh session.
- No external user feedback yet — this is an unbroken solo author release.

## [1.0.0] — 2026-05-27

### Added

- **`SKILL.md`** — Operating mode with 5-phase loop (UNDERSTAND, SPECIFY, PRE-MORTEM, CHANGE, VERIFY), Iron Laws, 30-item red-flag detection catalog with restart actions, 3-strike rule, Two Hats discipline, reversibility classification, complexity budget check, Common Rationalizations table, Signals from the human, Closing Gate checklist.
- **`MINDSET.md`** — 15 cognitive moves on software thinking (time horizons, compound cost, trust as currency, reversibility as risk dial, etc.).
- **`SECURITY.md`** — 15 cognitive moves on attack surface, STRIDE walkthrough, integration with the operating loop.
- **`bench.md`** — 15 eval prompts with expected vs failure-mode behavior for skill verification.
- **`references/`** — 10 per-book digests grounded in: The Pragmatic Programmer, Clean Code, Code Complete, A Philosophy of Software Design, Refactoring, The Mythical Man-Month, Designing Data-Intensive Applications, Working Effectively with Legacy Code, Release It!, Software Engineering at Google.
- **`scripts/`** — 10 helpers: `phase-checklist`, `contracts`, `pre-mortem`, `verify`, `find-callers.sh`, `decisions`, `calibrate`, `refusal-scripts`, `communication`, `threat-model`.
- **`anti-patterns/`** — 10 real code examples in TypeScript / Python / Go (RF-01 through RF-22 representative subset).
- **`playbooks/`** — 7 situation recipes: `incident-response`, `pr-review`, `new-endpoint-design`, `flaky-test`, `schema-migration`, `debugging-marathon`, `threat-model`.
- **`examples/`** — 1 worked walkthrough of the full 5-phase loop on a representative refactor.
- **Distribution** — MIT License, NOTICE with ISBN attributions to the 10 source books, README, CONTRIBUTING, VERSION.
- **Claude Code plugin format** — `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` for one-line install via `/plugin marketplace add` or `npx skills add`.

### Known issues at v1.0.0

- `find-callers.sh` initial release lacked `coverage/` exclusion → false-positive matches in repos with lcov HTML reports. Fixed in unreleased.
- No usage data yet. Skill is theoretically grounded but empirically unproven.
