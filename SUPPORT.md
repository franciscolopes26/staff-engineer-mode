# Getting Help

Where to ask for what.

## Before opening an issue

1. Check the [README](README.md) install section — most setup problems are a misread instruction.
2. Read [CHANGELOG.md](CHANGELOG.md) — your problem may be a known limitation or fixed in `Unreleased`.
3. Search existing [issues](https://github.com/franciscolopes26/staff-engineer-mode/issues?q=) and [closed issues](https://github.com/franciscolopes26/staff-engineer-mode/issues?q=is%3Aclosed) — your problem may already be tracked.

## Where each kind of question goes

| You have… | Open… |
|-----------|-------|
| The skill should have fired but didn't | [Issue: skill-didnt-fire](https://github.com/franciscolopes26/staff-engineer-mode/issues/new?template=skill-didnt-fire.md) |
| The skill fired for a trivial task (ceremony where none was needed) | [Issue: skill-over-fired](https://github.com/franciscolopes26/staff-engineer-mode/issues/new?template=skill-over-fired.md) |
| A chapter / tip citation is wrong | [Issue: citation-error](https://github.com/franciscolopes26/staff-engineer-mode/issues/new?template=citation-error.md) |
| A script is broken, a cross-reference is rotten | [Issue: bug](https://github.com/franciscolopes26/staff-engineer-mode/issues/new?template=bug_report.md) |
| A proposal for a new red flag / playbook / anti-pattern | [Issue: improvement](https://github.com/franciscolopes26/staff-engineer-mode/issues/new?template=improvement.md) |
| An open-ended discussion about the skill's design | [Discussions](https://github.com/franciscolopes26/staff-engineer-mode/discussions) |
| A suspected vulnerability in the skill's scripts or manifests | [Security advisory](https://github.com/franciscolopes26/staff-engineer-mode/security/advisories/new) (private) |
| A question about Claude Code itself, not this skill | [docs.claude.com/en/docs/claude-code](https://docs.claude.com/en/docs/claude-code) |
| A question about the `skills` CLI (`npx skills add`) | [skills.sh documentation](https://skills.sh) |

## Response times

This is a solo-maintainer project. Best-effort response targets:

- **Security advisory:** within 7 days (see [.github/SECURITY.md](.github/SECURITY.md)).
- **Skill-didnt-fire / over-fired bugs with a clear repro:** within 14 days.
- **Citation errors with a verification source:** within 14 days.
- **General bugs / improvements:** when I can.
- **Discussion threads:** not actively monitored; reply when something jumps out.

## What to include for a fast triage

For any skill behavior issue:

- **The prompt verbatim** — the most important field. Without it, the issue cannot be reproduced.
- **Claude model** (e.g. opus-4.7, sonnet-4.6).
- **Skill version** — `cat VERSION` in your install, or the `git log -1 --oneline` of your cloned copy.
- **Install path** — `/plugin install` / `npx skills add` / manual clone.
- **Which bench eval (B-01 to B-18) is closest** — `bench.md` is the spec for expected behavior; if your issue maps to one of those evals, name it.

## Not in scope for this repo

- Generic Claude Code / Anthropic SDK questions — see Anthropic docs.
- Questions about other people's skills — see their repos.
- Code review of your codebase — that's what the skill itself helps with; use it.
- Personal coaching on becoming a staff engineer — see the 10 source books in `NOTICE`.
