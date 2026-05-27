---
name: Skill did not fire when it should have
about: Report a case where staff-engineer-mode should have activated but didn't, or activated without producing the expected behavior.
title: "[under-fire] "
labels: ["under-fire", "bug"]
assignees: []
---

## What you asked Claude

Paste the prompt verbatim. The prompt is the most important field here — without it the issue cannot be reproduced.

```
<your prompt>
```

## What you expected staff-engineer-mode to do

Reference the relevant section of SKILL.md if you know it (e.g. "Phase 3 should have run", "RF-22 should have fired", "the Decision Tree should have routed to incident-response").

## What actually happened

Paste Claude's response, OR describe the gap (e.g. "it dove straight into writing code without reading the callers").

## Environment

- Claude model: (e.g. opus-4.7, sonnet-4.6)
- Skill version: (see `VERSION` file or `git log -1` in the cloned repo)
- Install path: `/plugin install` / `npx skills add` / manual clone
- Was `staff-engineer-mode` in the active-skills list at the time? (`/skills` to check)

## Which bench eval (B-01 to B-18) is closest to your prompt?

If you can map your prompt to a `bench.md` entry, name it — this helps triage and may indicate a regression in that specific eval.

## Anything else

Logs, screenshots, conversation transcript link, other context.
