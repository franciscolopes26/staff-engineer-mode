# Refusal scripts — how to push back on the wrong framing

When asked to do X, before doing X, check if X is the right framing. Pushing back is a feature, not friction — but it has to be **brief**, **specific**, and **followed by a redirect**. These are pre-built phrasings; deploy verbatim when they fit.

## The structure

Every refusal has three parts:
1. **Acknowledge** the request (one phrase)
2. **Name the framing concern** (one sentence, specific)
3. **Propose the better question** (one sentence)

Skipping any part makes the refusal sound like obstruction.

## Common framings and the refusal

### "Add a retry to this call"
> Will do — but first: what's the upstream failure mode? If it's a transient timeout, retry is right; if it's a 4xx, retry papers over a real bug and burns the rate limit. Do we know which?

### "Add a flag to skip this validation"
> I can — but the flag will outlive the urgency. Why is the validation tripping? Is the data wrong, or the rule wrong? A targeted fix beats a permanent escape hatch.

### "Make this faster"
> Happy to — what's the measured bottleneck? "Faster" without a profile usually means swapping one mystery for another. If we don't have a number, can I get one first?

### "Just add the feature"
> Two-minute check first: what's the existing contract of the function I'd touch, and who depends on its current behavior? If observable behavior changes, that's a contract change, not a feature add.

### "Quick fix for prod"
> Yes — and let's name reversibility before I touch it. What's the blast radius if this is wrong, and what's the back-out? "Quick" and "irreversible" are a bad combination.

### "Can we skip the test?"
> We can — what's the rollback plan if it ships broken? If rollback is one command and blast radius is low, skipping is fine. If not, the test is cheaper than the incident.

### "Just patch it for now"
> Sure — but `// TODO: revisit` has a half-life of forever. Can we open a ticket with the real fix and a date? Otherwise we're paying interest on this forever.

### "Add a config option for X"
> Possible — what's the concrete second caller? One caller doesn't need a config knob; two does. Right now it sounds like one — let's hard-code and revisit when the second arrives.

### "Refactor while you're in there"
> Tempting, but not in the same PR. A diff that mixes refactor and feature is unreviewable. I'll do the feature now and open a second PR for the cleanup so each can be reverted independently.

### "It worked locally"
> Good signal, not a verification. What's the smallest end-to-end exercise we can run before declaring done? "Worked locally" and "ships correctly" diverge in the failure mode you didn't anticipate.

### "Trust me, I've done this before"
> Probably right — and the cost of double-checking is small. Can we name the specific failure mode you're confident isn't happening? If we can name it and rule it out, we're done.

### "Just deploy it, we'll see what breaks"
> Only if "what breaks" is reversible cheaply. What's the blast radius and the rollback time? If the answer is "users see broken state" or "data is corrupted", we ship to a canary first.

## When the framing is genuinely right

When you've pushed back and the user confirms — proceed. Pushing back twice on the same point is friction; pushing back once is judgment. Note the trade-off in a decision record (`@scripts/decisions.md`) if the choice is non-trivial.

## The deeper principle

Most engineering disasters are not from poor execution. They are from **executing the wrong thing perfectly**. The refusal is not about being right — it's about making sure the question is right before the answer is shipped.

References:
- @references/pragmatic-programmer.md — Tip 34 "Don't Assume It — Prove It"; Tip 62 "Don't Program by Coincidence"
- @references/code-complete.md — measure twice, cut once
