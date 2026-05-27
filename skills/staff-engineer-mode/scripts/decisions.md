# Decision record template

Use when a choice between two or more reasonable approaches is being made — and the rationale needs to outlive the conversation. Paste this into a PR description, a doc, or a comment. Five lines is enough; longer is allowed only when reversibility cost is high.

```
DECISION:     <one-line statement of what was decided>

CONTEXT:      <what forced this decision; what changed>
              <1-3 sentences. Include constraints (deadline, team size,
              dependency, regulation) that narrowed the option space.>

OPTIONS:      A. <option>  — pro: ___; con: ___
              B. <option>  — pro: ___; con: ___
              C. <option>  — pro: ___; con: ___ (or rejected because ___)

CHOICE:       <A / B / C> — chosen because <one or two reasons>

TRADE-OFF:    we accept <cost X> in exchange for <benefit Y>
              (named the thing we are knowingly giving up)

REVERSIBLE?   <yes / partially / no>
              If "no" — what's the migration cost if we are wrong?
              If "partially" — what's the back-out path?

REVISIT:      <date or condition under which we should re-open this>
              (e.g., "if RPS > 5k", "after Q3 retro", "if vendor X ships Y")
```

## When to use this

- Any non-trivial design choice (library selection, schema shape, sync vs async, build vs buy).
- Any irreversible or partially-reversible action (data migration, public API decision, vendor lock-in).
- Any time you find yourself about to write "we should..." in code instead of the decision record.

## When NOT to use it

- Truly local choices (variable name, helper extraction, file location).
- Anything fully covered by an existing convention or style guide.

## The C-level discipline

The thing that separates senior from staff/principal/CTO is not the code quality — it's the **named trade-off**. "I chose X over Y because Z, the cost is W" beats "I chose X" every time. The record is the artifact; the discipline is the framing.

References:
- @references/software-engineering-at-google.md — every decision is an evidence-based trade-off
- @references/mythical-man-month.md — conceptual integrity through documented decisions
