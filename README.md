# staff-engineer-mode

> An operating-mode skill for Claude Code that activates staff/principal engineer thinking on any non-trivial coding task. Grounded in the canonical software engineering literature.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What it is

A Claude Code skill that changes *how* the assistant approaches non-trivial engineering work. When loaded, it enforces a five-phase loop on every change:

```
UNDERSTAND   → read the code and its callers before writing
SPECIFY      → name pre/post/invariants before changing
PRE-MORTEM   → list failure modes; decide handle / fail-fast / accept
CHANGE       → small reversible steps; never mix refactor and feature
VERIFY       → exercise behavior, not the build
```

Every principle is cited to a canonical source. The skill is the operating mode; the reasoning lives in 10 reference files distilled from the engineering canon.

## What it is *not*

- It is not a language-specific style guide. (Pair with `coding-standards`, `nestjs-standards`, `python-patterns`, etc.)
- It is not a code-review checklist. (Pair with `code-reviewer` and `security-review`.)
- It does not enforce specific line counts, naming conventions, or file structures.
- It does not replace human judgment — it makes the judgment more deliberate.

## Why this skill exists

Most engineering mistakes are not from lack of knowledge. They are from skipping steps that competent engineers know they should take. The skill exists to make those steps the default:

- **Read before writing** — most bugs introduced by competent engineers are from changing code they didn't fully understand. (Feathers, *Working Effectively with Legacy Code*.)
- **Surface contracts** — observable behavior is the contract, regardless of the docstring. (Hyrum's Law, via *Software Engineering at Google*.)
- **Pre-mortem failure modes** — bugs cannot be eliminated, only survived. (Nygard, *Release It!*.)
- **Small reversible steps** — Two Hats: refactor *or* add function, never both. (Beck, via Fowler's *Refactoring*.)
- **Verify behavior, not the build** — `tsc` passing is not the feature working.

## Installation

1. Clone or copy this directory to `~/.claude/skills/staff-engineer-mode/`:

   ```bash
   git clone <repo-url> ~/.claude/skills/staff-engineer-mode
   ```

   Or download the latest release and extract into `~/.claude/skills/`.

2. Restart your Claude Code session. The skill will appear in the available-skills list.

3. Optionally, add an automatic-load rule to your `~/.claude/CLAUDE.md`:

   ```markdown
   For any non-trivial coding task (debug, refactor, design, review),
   load the `staff-engineer-mode` skill before starting.
   ```

That's it. The skill is plain Markdown — no dependencies, no installation step.

## Usage

### Automatic activation

By design, the skill's description matches a broad set of triggers — debugging, refactoring, design, review, "do this properly". Claude Code's skill router will load it without explicit invocation when those signals are present.

### Explicit invocation

```text
/staff-engineer-mode
```

You can also reference it in a prompt:

> "Apply staff-engineer-mode to this PR review."

> "Use staff-engineer-mode and walk through your reasoning before changing the migration."

### Pair with other skills

The skill is intentionally additive. Load it alongside:

- `coding-standards` — language-agnostic rules (SOLID, smells, naming).
- Language skills (`typescript`, `python-patterns`, `golang-patterns`, etc.).
- `code-reviewer` / `security-review` for review contexts.
- `git-operations` for any commit / PR work.

Multiple skills compose; you do not have to choose.

## Repository structure

```
staff-engineer-mode/
├── SKILL.md                          The operating mode (the skill itself).
├── README.md                         This file.
├── LICENSE                           MIT License.
├── NOTICE                            Source-book attributions.
├── CONTRIBUTING.md                   How to extend or contribute.
├── VERSION                           Semantic version.
├── references/                       One file per canonical book — loaded on demand.
│   ├── pragmatic-programmer.md
│   ├── clean-code.md
│   ├── code-complete.md
│   ├── philosophy-of-software-design.md
│   ├── refactoring.md
│   ├── mythical-man-month.md
│   ├── designing-data-intensive-applications.md
│   ├── working-effectively-with-legacy-code.md
│   ├── release-it.md
│   └── software-engineering-at-google.md
└── scripts/                          Paste-able templates and helpers.
    ├── phase-checklist.md            Five-phase checklist + 3-strike rule.
    ├── contracts.md                  Phase 2 template (pre/post/invariants).
    ├── pre-mortem.md                 Phase 3 failure-mode enumeration.
    ├── verify.md                     Phase 5 surface-by-surface verification.
    └── find-callers.sh               Phase 1 helper — find callers of a symbol.
```

The skill follows the **progressive disclosure** pattern: only `SKILL.md`'s metadata (~100 tokens) loads at startup; the body loads when triggered; `references/` and `scripts/` load only when referenced. Total cost when idle is negligible.

Possible future additions (welcomed via `CONTRIBUTING.md`): `scenarios/` (worked examples), `languages/` (per-language application), `anti-patterns/` (anti-patterns with code).

## Canonical sources

Every principle is grounded in one of these ten books. Full citations in `NOTICE`. Per-book digests in `references/`.

| # | Book | Author |
|---|------|--------|
| 1 | The Pragmatic Programmer (20th Anniv.) | Hunt & Thomas |
| 2 | Clean Code | Robert C. Martin |
| 3 | Code Complete (2nd ed.) | Steve McConnell |
| 4 | A Philosophy of Software Design (2nd ed.) | John Ousterhout |
| 5 | Refactoring (2nd ed.) | Martin Fowler |
| 6 | The Mythical Man-Month | Fred Brooks |
| 7 | Designing Data-Intensive Applications | Martin Kleppmann |
| 8 | Working Effectively with Legacy Code | Michael Feathers |
| 9 | Release It! (2nd ed.) | Michael Nygard |
| 10 | Software Engineering at Google | Winters, Manshreck, Wright (eds.) |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests welcome — particularly additional scenarios, language application notes, and translations.

## License

MIT — see [LICENSE](LICENSE). Cite the underlying books when you use a principle; they did the original work.
