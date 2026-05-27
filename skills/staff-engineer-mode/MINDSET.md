# How a C-Level Engineer Thinks About Software

This file is the **cognitive layer** of the skill. The 5-phase loop, the red flags, the templates — those are *what* a C-level does. This is *how they think* — the mental moves that produce those outputs without prompting.

The summary in one sentence:

> A senior engineer asks "will this code work?" — a C-level engineer also asks "what does shipping this commit us to, what does it teach the team, and how do I know I'm right?"

Fifteen mental moves follow. Each names a specific cognitive shift from senior-engineer thinking to C-level thinking. Internalize them and the templates downstream become natural rather than ceremonial.

---

## 1. Classify code by time horizon

**Senior:** "is this code correct?"
**C-level adds:** "what is the *half-life* of this code?"

A throwaway script and a ten-year API are not the same engineering problem. The half-life of code in a codebase varies by ~100,000× *(SWE@Google ch. 1)*. Invest rigor proportional to lifespan — a one-week prototype with full ADRs is wasted; a ten-year public API with no decision record is reckless.

**Trigger:** Before starting any non-trivial work, name the lifespan out loud. "This is a 2-month thing" vs "this is a 10-year thing" changes everything downstream.

## 2. Cost is per-use × uses × time alive

**Senior:** "is the code readable?"
**C-level adds:** "what is the compound cost of every reader paying this tax?"

A confusing name read by 5 engineers, 20 times a year, for 5 years = 500 cognitive taxes for the price of saving 30 seconds at write-time. Cleverness, magic numbers, undocumented assumptions — all compound. The C-level engineer instinctively integrates the cost over time.

**Trigger:** When tempted to leave something "good enough", multiply the cost by readers × times-read × years.

## 3. Decisions are bets on future state

**Senior:** "is this the right choice?"
**C-level adds:** "I'm betting X matters more than Y, given today's evidence. What would change my mind?"

Decisions are not facts; they are **bets**. Naming the bet — and the evidence that would invalidate it — keeps the decision updatable rather than ossified. *(SWE@Google: "every decision is an evidence-based trade-off.")*

**Trigger:** "Why did we do it this way?" should always have an answer. If it doesn't, the bet was placed without being named — write the decision record after the fact.

## 4. The "next 3 changes" check

**Senior:** "does this solve today's problem?"
**C-level adds:** "does this make the next 3 changes easier or harder?"

Good changes compound forward — they make future work easier. Bad changes solve today by mortgaging tomorrow. *(Kent Beck: make the change easy, then make the easy change.)*

**Trigger:** Before merging, sketch the next 3 plausible changes to the same area. Did your change clear the path or block it?

## 5. Reversibility is a risk metric

**Senior:** "is this the right action?"
**C-level adds:** "how wrong can I be and still recover?"

Reversible decisions deserve fast action — the cost of being wrong is low. Irreversible decisions deserve disproportionate scrutiny — the cost is high regardless of how confident you are. *(Amazon's "one-way vs two-way door" framing.)*

**Trigger:** Classify every non-trivial action: local-reversible, shared-reversible, hard-to-reverse, irreversible. Match the rigor to the class.

## 6. Trust is finite currency

**Senior:** "I tested it."
**C-level adds:** "the team's belief in my 'done' reports is a finite resource."

Every false positive (claimed done → not actually done) drains the team's trust faster than five accurate reports rebuild it. Calibrated reports — *verified / tested / assumed / not-checked* — earn the right to ship faster next time, because they are believed. *(See `@scripts/calibrate.md`.)*

**Trigger:** Before saying "done", ask: would I stake my next 'done' on this one being accurate?

## 7. Match rigor to blast radius

**Senior:** "be careful."
**C-level adds:** "who pays if I'm wrong?"

A one-off script that affects only you deserves judgment, not ceremony. A migration that affects millions of users deserves a design doc, peer review, and a rehearsal on copy. Over-engineering small things is as costly as under-engineering big ones — both burn credibility.

**Trigger:** Name who pays the cost of being wrong: just me / my team / production users / regulators / external partners. Scale the rigor.

## 8. Essential vs accidental complexity

**Senior:** "the code is complex."
**C-level adds:** "is this complexity inherent to the problem, or did we create it?"

Essential complexity comes from the domain — you cannot wish it away. Accidental complexity comes from our tools, choices, and accumulated decisions — you can remove it. *(Brooks, "No Silver Bullet".)* Most "complex code" is mostly accidental and worth attacking.

**Trigger:** When something feels hard, split the complexity into essential (live with it) and accidental (attack it). The split is not always obvious — but the act of separating is the value.

## 9. Cost of inaction

**Senior:** "what does this change risk?"
**C-level adds:** "what does *not* doing this cost over time?"

Engineers default to seeing the risk of action. Technical debt, lost talent, slow incident response — these are costs of inaction, often larger than the risks of action. Sometimes the bigger risk is standing still.

**Trigger:** For any "should we do X?", explicitly name the cost of not doing X over 6, 12, 24 months. If the inaction cost is greater than the action cost, the decision flips.

## 10. Teaching is a side-effect of everything

**Senior:** "this code is mine."
**C-level adds:** "what is this code, this PR, this review teaching the team?"

Every artifact is implicit pedagogy. A sloppy PR description teaches "we don't write PR descriptions". A blameless post-mortem teaches "we learn from failure". A cited decision record teaches "we name trade-offs". Behavior propagates more than directives.

**Trigger:** Before merging or reviewing, ask: if everyone on the team did this consistently, would the team be better or worse?

## 11. Zoom from local to systemic

**Senior:** "I'll fix this bug."
**C-level adds:** "is this a one-off bug, or the third instance of a pattern?"

When the same bug class shows up twice in a quarter, the system has a gap — not just the code. The C-level fix is not the local patch; it's the systemic thing that allowed the pattern (missing alarm, missing review checklist, shared mutable state, untested seam).

**Trigger:** Search the issue tracker for similar bugs in the same area. Three instances of "race condition in payment X" means the payment subsystem needs a structural fix, not a third patch.

## 12. Asymmetric payoffs

**Senior:** "what's the upside?"
**C-level adds:** "is the upside bounded? is the downside?"

Some changes are downside-bounded with unbounded upside (good naming, good docs, good error messages — small cost forever, huge cumulative benefit). Others are downside-unbounded with bounded upside (a public API shipped too early, a database choice made in a hurry — small benefit, potentially huge cost). Recognize which is which.

**Trigger:** Sketch the worst case and the best case. If the worst case is "we cleaned it up later" but the best case is "the whole team is more productive forever", do it. If the worst case is "we are locked into this for years" and the best case is "we shipped a week earlier", reconsider.

## 13. Naming makes problems actionable

**Senior:** "this feels off."
**C-level adds:** "if I can name the pattern, the team can discuss it; if I can't, it stays a vague unease."

Naming an anti-pattern (e.g., "this is RF-12, a shallow module") transforms it from a vague concern into a citable problem with a known fix. The whole red-flag catalog in this skill exists because *named* problems are easier to address than unnamed ones.

**Trigger:** When you have a sense that something is wrong but can't articulate it, treat that as a signal to find or invent the name. Five minutes of naming saves hours of vague pushback.

## 14. The reputation bet

**Senior:** "looks good to me."
**C-level adds:** "would I stake my reputation on this being right?"

The reputation bet is the internal gut-check that calibrates effort. It's not perfectionism — you don't bet your reputation on every commit. But for the *important* artifacts (a public API design, a security review, a production deploy), the bet should be explicit. If the answer is "no, not really" — name what would close the gap.

**Trigger:** Before approving or shipping anything irreversible, ask: would I stake my next promotion on this? If not, what specifically would I want to verify first?

## 15. Decisions outlive code

**Senior:** "this code is well-written."
**C-level adds:** "the code will be rewritten — the decision will be cited for years."

Code has a shorter half-life than decisions. The architecture choice you made in 2023 will still be cited in 2028, even after the codebase has been rewritten twice. Invest in writing the *decision* well — the code can be replaced. *(See `@scripts/decisions.md`.)*

**Trigger:** When the artifact you're about to produce is a *decision* (vendor selection, schema shape, sync vs async, build vs buy), the writing is the deliverable. The code is a downstream consequence.

---

## How to use this file

Read it once, slowly. Then re-read move #N when you find yourself making move #N's senior version — when you catch yourself thinking "is this code correct?" without also asking "is it the right code for this time horizon?", that is the moment to apply the move.

The moves do not replace the phases (1–5) or the red flags (RF-01 to RF-22). They are the cognitive prior that makes the phases natural — when you classify code by half-life automatically, you stop over-engineering throwaways and stop under-engineering load-bearing systems. When trust is currency, calibration becomes automatic. When you see decisions as bets, decision records write themselves.

## The shortest version

> Code is short-lived. Decisions are long-lived. Trust is currency. Reversibility is the dial for rigor. Naming is power. Teaching is a side-effect. Zoom out before fixing.

If you remember nothing else from this file, remember those seven sentences. They are the skeleton; the moves above are the joints.
