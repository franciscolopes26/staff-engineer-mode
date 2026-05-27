---
name: Skill over-fired (ceremony where none was needed)
about: Report a case where staff-engineer-mode activated for a trivial task and added unwanted ceremony.
title: "[over-fire] "
labels: ["over-fire", "bug"]
assignees: []
---

## What you asked Claude

Paste the prompt verbatim. Trivial-task prompts especially — renames, typo fixes, one-line config changes, single-question lookups.

```
<your prompt>
```

## What ceremony fired that you didn't want

E.g. "asked me to write contracts for a one-line rename", "ran a pre-mortem for a typo fix", "wanted to write a decision record for a variable rename".

## Why you consider this a false positive

The skill's `Activation` section and Decision Tree explicitly list trivial cases that should be SKIPPED. Tell us which case yours falls into (or if it's a new one we should add to the skip list).

## Environment

- Claude model: (e.g. opus-4.7)
- Skill version: (see `VERSION`)

## Which bench eval (B-15 to B-18) is closest?

The negative-case evals exist exactly to catch over-firing. If your prompt is similar to one of them, the eval may be regressing.

## Anything else

Logs, screenshots, conversation transcript link.
