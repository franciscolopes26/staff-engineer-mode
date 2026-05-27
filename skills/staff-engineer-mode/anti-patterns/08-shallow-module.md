# RF-12: Shallow Module

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-12

## Detection

A class, service, or wrapper whose public interface is roughly the same size as its implementation — every method is a one-line forward to the underlying primitive. Grep for classes where most methods are a single `return` statement, repositories that wrap a single ORM call per method, or "services" that exist only to inject something the caller could have asked for directly. The module adds a name and a file but hides no complexity.

## Smell

```typescript
// users.service.ts — looks like an abstraction, isn't one.
@Injectable()
export class UserService {
  constructor(@InjectKnex() private readonly db: Knex) {}

  async getUser(id: string) {
    return this.db('users').where({ id }).first()
  }

  async getUserByEmail(email: string) {
    return this.db('users').where({ email }).first()
  }

  async createUser(data: { email: string; name: string }) {
    return this.db('users').insert(data).returning('*')
  }

  async updateUser(id: string, data: Partial<{ email: string; name: string }>) {
    return this.db('users').where({ id }).update(data).returning('*')
  }

  async deleteUser(id: string) {
    return this.db('users').where({ id }).delete()
  }
}

// Caller — has to know the same things it would have known without the wrapper.
const user = await this.users.getUser(id)
if (!user) throw new NotFoundException()
if (user.deleted_at) throw new GoneException()
if (user.tenant_id !== ctx.tenantId) throw new ForbiddenException()
```

## Why this fails in production

Every caller still has to know about soft-deletes, tenant scoping, the difference between "not found" and "deleted", and the raw row shape — because the wrapper hid none of that. The team pays the cost of an abstraction (extra file, extra DI registration, extra mock in every test) and gets none of the benefit. Worse, when a tenant-isolation bug ships because one caller forgot the `tenant_id` check, the post-mortem reveals the rule was never centralized — `UserService` looked like the place but enforced nothing. Shallow modules are interface tax with no abstraction payoff.

## Fix

```typescript
// Option A — go DEEP. The module now hides real complexity:
// tenant scoping, soft-delete semantics, audit logging, cache invalidation.
@Injectable()
export class UserRepository {
  constructor(
    @InjectKnex() private readonly db: Knex,
    private readonly audit: AuditLog,
    private readonly cache: UserCache,
  ) {}

  // Callers never have to think about tenants or soft-deletes again.
  async findActive(id: string, ctx: RequestContext): Promise<User> {
    const cached = await this.cache.get(id, ctx.tenantId)
    if (cached) return cached
    const row = await this.db('users')
      .where({ id, tenant_id: ctx.tenantId })
      .whereNull('deleted_at')
      .first()
    if (!row) throw new UserNotFoundError(id)
    await this.cache.set(row)
    return row
  }

  async softDelete(id: string, ctx: RequestContext): Promise<void> {
    await this.db.transaction(async trx => {
      const [row] = await trx('users')
        .where({ id, tenant_id: ctx.tenantId })
        .update({ deleted_at: trx.fn.now() })
        .returning('*')
      if (!row) throw new UserNotFoundError(id)
      await this.audit.record(trx, 'user.deleted', { id, actor: ctx.userId })
      await this.cache.invalidate(id, ctx.tenantId)
    })
  }
}

// Option B — COLLAPSE. If there's no real complexity to hide, just use Knex
// directly in the handler and delete UserService. One fewer file, one fewer mock.
```

## Reasoning

Ousterhout's central thesis: modules should be deep — a simple interface hiding substantial implementation. The cost of a module is its interface (what every caller must learn); the benefit is the complexity it hides. A shallow module inverts this: all cost, no benefit. The correct response is binary — either deepen the module so it earns its interface, or delete it and let callers use the primitive directly. "Classitis" — making everything a class for its own sake — is the canonical symptom.

## Citation

- *A Philosophy of Software Design*, John Ousterhout (2nd ed., 2021), ch. 4 "Modules Should Be Deep" and ch. 5 "Information Hiding (and Leakage)".

## See also

- @references/philosophy-of-software-design.md
