# RF-27: Mass Assignment

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-27

## Detection

Grep for `update(req.body)`, `Object.assign(entity, req.body)`, `findOneAndUpdate(_, req.body)`, `Model(**request.json)`, or any ORM call whose payload comes directly from the request without an intermediate allow-list. Code review red flag: an endpoint handler whose update line has no DTO, no `pick`, no destructure — just a raw spread of user input into a persisted entity.

## Smell

```typescript
// PATCH /api/users/me — "let users edit their own profile"
async function updateProfile(req: FastifyRequest, reply: FastifyReply) {
  const userId = req.user.id

  // Hand the request body straight to the ORM. What could go wrong?
  const updated = await User.findByIdAndUpdate(userId, req.body, {
    new: true,
  })

  return reply.send(updated)
}

// Attacker sends:
//   PATCH /api/users/me
//   { "displayName": "alice", "isAdmin": true, "stripeCustomerId": "cus_victim" }
//
// The schema has `isAdmin: Boolean` and `stripeCustomerId: String`,
// so Mongoose happily writes both. Alice is now an admin and her
// invoices bill another customer's card.
```

## Why this fails in production

This is the canonical privilege escalation bug — GitHub shipped it in 2012 and any attacker on the public internet who guesses your field names can grant themselves admin, swap billing identifiers, mark accounts as verified, bypass tenant isolation, or change the `userId` foreign key on a record they don't own. The damage is silent because the request looks legitimate in access logs (`200 PATCH /api/users/me`), and you only discover it when someone wires the new `isPaidTier` column the same week the breach happens. Every field you ever add to that model becomes retroactively writable by every existing endpoint that spreads `req.body`.

## Fix

```typescript
// Explicit allow-list — a DTO that names every writable field.
const UpdateProfileDto = z.object({
  displayName: z.string().min(1).max(80),
  locale: z.enum(['pt-PT', 'en-US']).optional(),
  avatarUrl: z.string().url().optional(),
})

async function updateProfile(req: FastifyRequest, reply: FastifyReply) {
  const userId = req.user.id

  // Parse strips unknown keys; safeParse surfaces validation errors as 400.
  const parsed = UpdateProfileDto.safeParse(req.body)
  if (!parsed.success) {
    return reply.code(400).send({ errors: parsed.error.issues })
  }

  // Only the three named fields can ever reach the ORM. Adding a new
  // sensitive column (isAdmin, tenantId) to the schema does NOT widen
  // this endpoint's blast radius — you'd have to extend the DTO.
  const updated = await User.findByIdAndUpdate(userId, parsed.data, {
    new: true,
    runValidators: true,
  })

  return reply.send(updated)
}
```

## Reasoning

A function should accept only what it needs — applying Interface Segregation to the input boundary closes the gap between "what the user is allowed to change" and "what the ORM is willing to write". Trust boundaries belong at the edge of the system, not in the persistence layer; the DTO is the boundary made executable.

## Citation

- OWASP Top 10 (2021), A04 Insecure Design + A05 Security Misconfiguration; OWASP API Security Top 10 (2023), API6 Mass Assignment.
- *Clean Code*, Robert C. Martin (2008), ch. 3 "Functions" — "Function Arguments" / Interface Segregation applied to inputs.

## See also

- @scripts/threat-model.md
- @SECURITY.md
- @references/clean-code.md
