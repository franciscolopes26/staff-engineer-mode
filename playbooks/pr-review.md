# Playbook: Reviewing Someone Else's PR

**When:** asked to review a non-trivial PR.
**Goal:** catch what would page someone at 3 a.m.; teach where you can; do not nitpick.

A review is not "find every flaw". It is **make the change safer to ship** by sharing what the author may not have seen. Three categories of finding: blocker, suggestion, nitpick — and you label which is which.

## Phase 1 — read first

- The PR description. If it doesn't tell you *what* and *why*, ask for it before reading the diff.
- The diff, end to end, before commenting on anything. Note: never review one file in isolation — the bug is usually in the seam between files.
- The tests. What behavior is locked in? What's *not* tested?
- The linked ticket / design doc, if any. The diff should match the stated intent.
- `git blame` on the touched lines — what was there before? Why did it look like that?

## Phase 2 — contracts the PR may have changed

- Did any public function / endpoint / event change its observable behavior? (Hyrum's Law — even "internal" code has de-facto consumers.)
- Did any error message, status code, ordering, or timing change? These are contracts too.
- If yes → is the contract change intended? Is it documented in the PR description?

## Phase 3 — failure modes to scan for

Walk the red-flag catalog (`SKILL.md` → Red Flag Detection Catalog). The high-frequency ones in PR review:

- **RF-01 Silent Swallow** — every new catch block, every `?? null`, every `try {} catch (_) {}`.
- **RF-02 Mixed Diff** — does this PR do one thing? If it's "fix bug + rename + reformat", ask to split.
- **RF-03 Naked Remote Call** — any new outbound HTTP/gRPC/DB call: where's the timeout? circuit breaker?
- **RF-08 It Compiles, Ship It** — does the description say *how* the author verified, not just "tested"?
- **RF-15 Boolean Flag Argument** — any new `bool` parameter that switches behavior.
- **RF-13 Information Leakage** — does this PR put the same fact in two places?
- **RF-11 Pass-Through** — new methods that just forward args.

## Phase 4 — comment strategy

For each finding, label and limit:

- **[BLOCKER]** — must change before merge. Use sparingly. A blocker is "this will cause a production failure or contract violation". Not "I'd write this differently."
- **[SUGGESTION]** — would improve the PR; author can take or leave. Most findings should be these.
- **[NITPICK]** — stylistic preference; mark optional explicitly. If you have more than 3 nits, group into one comment.

**The sandwich rule for difficult feedback:** specific praise → specific concern → specific suggestion. Not generic — generic praise reads as condescension.

Use `@scripts/communication.md` PR-review section for phrasing templates.

## Phase 5 — verification before approving

- Does the PR description's "Verification" section list end-to-end exercises? If not, ask.
- Pull the branch locally and run the test suite if the change is non-trivial.
- For schema / config / migration changes: did the author rehearse the rollback?

## Red flags in YOUR OWN review behavior

- **You commented on every file equally.** Either you read carelessly or you over-reviewed. Re-prioritize.
- **You marked everything as blocker.** You are training the author to ignore your blockers. Save the label.
- **You have no questions.** Either the PR is exceptional or you skimmed. Both deserve scrutiny.
- **You approved in under 60 seconds on a non-trivial PR.** That's a rubber stamp, not a review.

## Refusal scripts for common bad framings

- "It's just a small refactor" → "Small refactor in one PR; one behavior change at a time. The diff says behavior changed too — let's split."
- "Tests are flaky, ignore the failing CI" → "If CI is flaky we fix CI in a separate PR. Merging on broken CI burns the signal."
- "I'll add tests in a follow-up" → "Follow-ups for tests have a half-life of forever. Either tests now or document why they aren't needed."
- "It works in my testing" → "What did you exercise? Specifically, which surface? `@scripts/calibrate.md` for the levels."

## When this playbook is wrong

- A trivial PR (one-line fix, dependency bump, typo) — apply 60 seconds of judgment, not the full playbook.
- A PR you authored — different discipline applies; use the self-review checklist in `@scripts/phase-checklist.md`.
- A design-doc review — different artifact, different playbook (read the design doc skeleton in `@scripts/communication.md`).
