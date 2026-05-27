# RF-26: IDOR (Insecure Direct Object Reference)

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-26

## Detection

Any handler that accepts a resource ID from the URL, query, or body and fetches by ID alone — where the only guard upstream is "is the JWT valid". Grep for `@Param('id')` / `req.params.id` / `pathParam("id")` followed by `repo.findById(`, `findOne({ id })`, `Get(id)` with no second predicate naming the actor. Code review red flag: the repository method is named `findById` and the route is per-tenant — the names alone tell you ownership was never modelled.

## Smell

```typescript
import { Controller, Get, Param, Patch, Body, UseGuards, Req } from '@nestjs/common'
import { JwtAuthGuard } from '../auth/jwt.guard'
import { InvoiceRepository } from './invoice.repository'
import { UpdateInvoiceDto } from './dto/update-invoice.dto'

@Controller('invoices')
@UseGuards(JwtAuthGuard)
export class InvoiceController {
  constructor(private readonly repo: InvoiceRepository) {}

  @Get(':id')
  async findOne(@Param('id') id: string) {
    const invoice = await this.repo.findById(id)
    if (!invoice) throw new NotFoundException()
    return invoice
  }

  @Patch(':id')
  async update(@Param('id') id: string, @Body() dto: UpdateInvoiceDto) {
    return this.repo.update(id, dto)
  }
}
```

## Why this fails in production

`JwtAuthGuard` proves the caller is *some* user; it proves nothing about *which* invoice they should see. Any logged-in account — a 30-second free signup — can curl `GET /invoices/<other-tenant-uuid>` and read another company's billing data, or `PATCH` it to zero out the total. Sequential IDs make this trivial; UUIDs only slow it down (HTTP referer leaks, browser history, error pages, support screenshots all expose them). This is the precise pattern behind dozens of public breaches: Bumble (100M users), USPS Informed Visibility (60M), Parler's entire post archive. The fix is one line per query; the breach is unbounded.

## Fix

```typescript
import { Controller, Get, Param, Patch, Body, UseGuards, Req, NotFoundException } from '@nestjs/common'
import { JwtAuthGuard } from '../auth/jwt.guard'
import { InvoiceRepository } from './invoice.repository'
import { UpdateInvoiceDto } from './dto/update-invoice.dto'
import { AuthedRequest } from '../auth/authed-request'

@Controller('invoices')
@UseGuards(JwtAuthGuard)
export class InvoiceController {
  constructor(private readonly repo: InvoiceRepository) {}

  @Get(':id')
  async findOne(@Param('id') id: string, @Req() req: AuthedRequest) {
    // Ownership is part of the query, not an afterthought.
    // A non-owner literally cannot construct a result row → 404, not 403,
    // so we don't even leak existence.
    const invoice = await this.repo.findByIdForCompany(id, req.user.companyId)
    if (!invoice) throw new NotFoundException()
    return invoice
  }

  @Patch(':id')
  async update(
    @Param('id') id: string,
    @Body() dto: UpdateInvoiceDto,
    @Req() req: AuthedRequest,
  ) {
    const updated = await this.repo.updateForCompany(id, req.user.companyId, dto)
    if (!updated) throw new NotFoundException()
    return updated
  }
}

// invoice.repository.ts
export class InvoiceRepository {
  // Note: no plain `findById` is exported. The unsafe shape doesn't exist in the API surface.
  async findByIdForCompany(id: string, companyId: string) {
    return this.em.findOne(Invoice, { id, company: companyId })
  }
  async updateForCompany(id: string, companyId: string, patch: Partial<Invoice>) {
    const inv = await this.findByIdForCompany(id, companyId)
    if (!inv) return null
    Object.assign(inv, patch)
    await this.em.flush()
    return inv
  }
}
```

## Reasoning

Define the error out of existence: an ownership-scoped query has no representation for "wrong owner" — the row simply isn't in the result set, and there is no boolean for a future maintainer to forget. This is preferable to a separate `if (invoice.companyId !== user.companyId) throw` because the check cannot be omitted; it is the query. Returning 404 instead of 403 also avoids the side-channel that confirms a resource exists for another tenant.

## Citation

- OWASP Top 10 (2021), A01:2021 — Broken Access Control. IDOR is the canonical instance.
- *A Philosophy of Software Design*, John Ousterhout (2nd ed., 2021), ch. 10 "Define Errors Out of Existence".

## See also

- @scripts/threat-model.md
- @SECURITY.md
- @references/philosophy-of-software-design.md
