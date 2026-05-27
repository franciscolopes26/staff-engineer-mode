# Security Policy

This is the **vulnerability reporting policy** for the `staff-engineer-mode` repository itself. The skill's *content* on attack-surface thinking lives in `skills/staff-engineer-mode/SECURITY.md`.

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |
| < 1.0   | No        |

## What counts as a vulnerability in this repo

This skill ships pure Markdown plus one shell script (`scripts/find-callers.sh`). The realistic risk surface is small but non-zero:

- **Shell-script issues in `find-callers.sh`** — argument-injection, path-traversal-via-symbol, unsafe glob expansion, or unintended file writes.
- **Manifest-file issues** — malformed `.claude-plugin/plugin.json` / `marketplace.json` that causes Claude Code to misbehave at install time.
- **Documented-but-unsafe patterns in `scripts/*.md`** — paste-able templates that would mislead a user into shipping unsafe code if followed verbatim.
- **Citation-driven misinformation** — a citation to an authoritative source that, if followed, would actively harm security posture.

What does NOT count as a vulnerability:

- Disagreement with the skill's design opinions or anti-pattern coverage (open a regular issue or PR).
- Citation chapter-number errors (open a `[citation]` issue).
- Skill firing in cases you don't want (open a `[over-fire]` issue).

## Reporting a vulnerability

Email: open a private security advisory via **GitHub Security Advisories** (Repo → Security tab → Report a vulnerability).

Do NOT open a public issue for suspected security vulnerabilities.

### What to include

- The file path and line numbers involved.
- The behavior you observed.
- A proof-of-concept if applicable (e.g. a `find-callers.sh` invocation that misbehaves).
- The impact: who is affected, how, what an attacker could achieve.
- Whether the vulnerability is currently public anywhere (CVE, blog, social).

### Response timeline

This is a solo-author project; response is best-effort:

- **Acknowledgement:** within 7 days.
- **Triage:** within 14 days.
- **Fix or mitigation:** depends on severity; high-severity issues prioritized.
- **Disclosure:** coordinated. Will work with the reporter on a disclosure timeline; default 90 days from report.

## Credit

Reporters who follow this policy and want public credit will be acknowledged in the `NOTICE` file and the GitHub Security Advisory.
