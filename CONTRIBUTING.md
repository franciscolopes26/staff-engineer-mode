# Contributing to staff-engineer-mode

Contributions are welcome. The goals of this skill are:

1. **Operational over academic.** Every principle should change behavior mid-work, not just describe a concept.
2. **Grounded over invented.** Every claim cites a canonical source — typically one of the 10 books in `references/`.
3. **Universal over local.** Language-agnostic in `SKILL.md`; language-specific application in `languages/`.
4. **Tight over comprehensive.** A short principle that lands beats a long one that doesn't.

## Ways to contribute

### Add a scenario (proposed extension: `scenarios/`)

A *scenario* is a worked example showing the five-phase loop applied to a common engineering situation. Good scenarios:

- Pick a situation engineers face regularly (debugging a flaky test, adding a feature to legacy code, designing a new public API).
- Show the WRONG approach briefly, then walk through the FIVE PHASES with concrete code.
- Cite which books inform each phase's discipline.
- Stay under ~150 lines.

### Add a language application note (proposed extension: `languages/`)

A *language* file translates the universal principles into idiomatic practice for one language. Good language notes:

- Map each phase or cross-cutting principle to language-specific tools and idioms.
- Include short code snippets in that language.
- Avoid framework lock-in — keep them about the *language*, not the framework.
- Stay under ~250 lines.

### Add an anti-pattern (proposed extension: `anti-patterns/`)

An *anti-pattern* file shows: the smell (real code), the fix (real code), and the reasoning (why the fix is better, with a citation). Good anti-pattern files:

- Use real-looking code, not pseudocode.
- Show the smallest meaningful example — 10–30 lines, not a full module.
- Cite which book or principle calls out this anti-pattern.
- Stay under ~80 lines.

### Add a helper script (`scripts/`)

A *script* is either an executable (`.sh`, `.py`) for a deterministic operation Claude shouldn't generate fresh each time, OR a paste-able template (`.md`) that Claude can drop into its working notes. Good helpers:

- Solve one specific Phase-1 to Phase-5 sub-step that recurs across many tasks.
- For executables: stay <100 lines, work cross-platform when possible.
- For templates: fillable with `_____` blanks; one section per concern.

See `scripts/contracts.md` and `scripts/find-callers.sh` as references.

### Improve the operating mode

If you find a principle missing from `SKILL.md`, propose it with:

- The principle, in one sentence.
- The canonical source (book + page or section).
- A short justification of why it belongs.
- Optionally, an example of the failure mode it prevents.

### Translations

Translations of `SKILL.md` to other languages are welcome. The references and citations stay in English (because the books are English) but the operating mode can be translated.

## Style guide

- **Tone:** declarative, terse, second-person imperative. "Read before writing." not "It is recommended that one read..."
- **No emojis** in skill content. (They distract from the signal.)
- **Citations:** parenthetical with book name in italics — `(Ousterhout, *A Philosophy of Software Design*)`.
- **Code samples:** real-looking, idiomatic in the target language, with the smell and the fix clearly labeled.
- **Headers:** sentence case for body content; title case only for top-level book titles.
- **No emoji icons in headers or tables.**
- **Markdown:** standard CommonMark. Tables and fenced code blocks fine; HTML inside Markdown discouraged.

## What we don't accept

- **New principles without citations.** This skill is the canon, not original philosophy. If a principle isn't in one of the 10 books (or another well-attested source), it doesn't belong here.
- **Framework-specific rules.** Those go in framework-specific skills (`nestjs-standards`, `shadcn-nextjs`, etc.).
- **Length for its own sake.** A 30-line scenario that lands beats a 300-line one that doesn't.
- **Personal opinion sections.** "I think..." doesn't appear in this skill. The skill speaks with the books' authority, or it doesn't speak.

## Submitting changes

If the skill is hosted in a Git repository:

1. Fork the repository.
2. Create a feature branch (`scenario/flaky-test`, `language/kotlin`, `anti-pattern/cargo-cult`, etc.).
3. Write the addition following the templates above.
4. Open a pull request with a one-paragraph description of what the addition adds and which gap it fills.

## License

By contributing, you agree that your contribution is licensed under the same MIT License as the rest of the skill.
