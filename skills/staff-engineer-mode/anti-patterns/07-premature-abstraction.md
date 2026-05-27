# RF-10: Premature Abstraction

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-10

## Detection

An interface, abstract base class, or generic helper appears in a PR that introduces only ONE concrete implementation — often with a comment like "in case we need more later" or "to make it pluggable". Grep for interfaces with a single `implements` site, factories that always return the same class, and config keys that are never set to anything but the default. The abstraction's shape was guessed, not discovered.

## Smell

```python
# notifications/notifier.py
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def notify(self, user_id: str, message: str) -> None: ...

class EmailNotifier(Notifier):
    def notify(self, user_id: str, message: str) -> None:
        email = users.get_email(user_id)
        ses.send_email(to=email, subject="Notification", body=message)

# notifications/factory.py
def make_notifier() -> Notifier:
    # "Pluggable" — but only ever returns EmailNotifier.
    return EmailNotifier()

# Six months later, product asks for SMS for 2FA codes.
# SMS needs: phone number lookup, country-code routing, a different
# template engine, delivery-receipt callbacks, and per-region carriers.
# `notify(user_id, message)` is the wrong shape for ALL of it.
class SmsNotifier(Notifier):
    def notify(self, user_id: str, message: str) -> None:
        # Now what? We need a phone, not a user_id. We need a template id,
        # not a rendered message. We need a callback URL. The interface lies.
        raise NotImplementedError
```

## Why this fails in production

The interface was designed against imagined requirements and locked in the wrong vocabulary (`user_id`, `message`) before the second use case existed. When the real second case arrives, the team faces three bad choices: bend SMS into the email-shaped hole (lose delivery receipts, lose template variables), widen `notify` with optional params until the signature is meaningless, or rip the abstraction out and pay the migration cost in every caller. Speculative generality always extracts a tax — you pay the indirection cost forever to handle a future that arrives in a different shape than you guessed.

## Fix

```python
# notifications/email.py — just the concrete thing, no interface yet.
def send_email_notification(user_id: str, message: str) -> None:
    email = users.get_email(user_id)
    ses.send_email(to=email, subject="Notification", body=message)

# Six months later: SMS arrives. Now we have TWO real shapes. Still don't
# abstract — let them live side by side and observe what's actually common.
def send_sms_2fa(user_id: str, code: str, template_id: str) -> str:
    phone = users.get_phone(user_id)
    region = phone_routing.region_for(phone)
    return twilio.send(to=phone, template=template_id, vars={"code": code}, region=region)

# After the THIRD channel (push notifications) lands and we can see the
# real seams — delivery confirmation, retry policy, audit logging — THEN
# extract whatever genuinely repeats. The abstraction's shape is now
# discovered from three data points, not guessed from one.
```

## Reasoning

The term "speculative generality" is Fowler's, from the *Refactoring* smell catalog — adding flexibility for hypothetical future needs that adds interface cost (more to read, more to mock, more to navigate) for zero present benefit. Ousterhout's parallel framing is that *somewhat-general* APIs are deeper than special-purpose ones, but designing for the imagined fourth caller before it exists almost always picks the wrong axis of variation. The Pragmatic Programmer's rule of three says: write it once, duplicate it the second time, extract on the third — because only at three cases can you see which parts genuinely vary and which are coincidence. Inheritance and interfaces are the most expensive coupling in the codebase; spend them on patterns that have proved themselves, not on guesses.

## Citation

- *Refactoring*, Martin Fowler (2nd ed., 2018), Smell Catalog: "Speculative Generality" — the canonical name for this anti-pattern.
- *A Philosophy of Software Design*, John Ousterhout (2nd ed., 2021), ch. 6 "General-Purpose Modules are Deeper" — the case for *somewhat* general, with warnings against over-generalization.
- *The Pragmatic Programmer*, Hunt & Thomas (20th Anniversary ed., 2019) — the "rule of three" discussion (DRY tempered by waiting for real duplication).

## See also

- @references/philosophy-of-software-design.md
- @references/pragmatic-programmer.md
