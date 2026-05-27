# RF-08: It Compiles, Ship It

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-08

## Detection

A change is declared "done" because the type-checker passes and the unit tests are green — but the actual behavior was never exercised against a real HTTP request, a real DB row, or a real consumer. Look for PR descriptions that say "tested" with only `*.spec.ts` / `test_*.py` evidence and no curl, no screenshot, no log line from a running process. Grep for tests that mock the very boundary the change touches.

## Smell

```typescript
// New endpoint added to the orders service.
@Controller('orders')
export class OrdersController {
  constructor(private readonly orders: OrdersService) {}

  @Post('cancel')
  async cancel(@Body() dto: CancelOrderDto) {
    return this.orders.cancel(dto.orderId, dto.reason)
  }
}

// orders.controller.spec.ts
describe('OrdersController', () => {
  it('cancels an order', async () => {
    const orders = { cancel: jest.fn().mockResolvedValue({ ok: true }) }
    const ctrl = new OrdersController(orders as any)
    await expect(ctrl.cancel({ orderId: 'o1', reason: 'x' })).resolves.toEqual({ ok: true })
  })
})

// PR description: "Adds POST /orders/cancel. Tested and working."
// Reality: OrdersController was never added to OrdersModule.controllers[],
// so Nest never registers the route. Every production call returns 404.
```

## Why this fails in production

Instantiating a controller with `new` in a test bypasses the framework's wiring — DI, route registration, guards, pipes, interceptors. The unit test happily exercises a class that the running process will never see. The first real customer to click "Cancel" gets a 404, the order stays in `PENDING_SHIPMENT`, the warehouse ships it anyway, and finance issues a refund three days later because the cancel button "didn't do anything". The test was green; the feature was never alive.

## Fix

```typescript
// 1. Wire it.
@Module({
  controllers: [OrdersController],
  providers: [OrdersService],
})
export class OrdersModule {}

// 2. Exercise the real boundary — at least once — before claiming done.
describe('POST /orders/cancel (e2e)', () => {
  let app: INestApplication
  beforeAll(async () => {
    const mod = await Test.createTestingModule({ imports: [OrdersModule] }).compile()
    app = mod.createNestApplication()
    await app.init()
  })
  afterAll(() => app.close())

  it('returns 200 and persists the cancellation', async () => {
    const res = await request(app.getHttpServer())
      .post('/orders/cancel')
      .send({ orderId: 'o1', reason: 'customer_request' })
    expect(res.status).toBe(200)
    // And confirm the side effect actually happened in the test DB.
    expect(await ordersRepo.findOne('o1')).toMatchObject({ status: 'CANCELLED' })
  })
})
```

## Reasoning

A unit test that mocks the boundary the change touches proves only that the mock matches the mock. Feathers' definition is unambiguous: if it talks to a database, the network, the filesystem, or requires environment configuration to run, it is not a unit test — and you need that exercise before claiming the behavior works. "It compiles" and "the types line up" are necessary but never sufficient.

## Citation

- *Working Effectively with Legacy Code*, Michael Feathers (2004), ch. 1 — "A unit test that talks to a database is not a unit test".
- *The Pragmatic Programmer*, Hunt & Thomas (20th Anniversary ed., 2019), Tip 34 "Test Your Software, or Your Users Will".

## See also

- @scripts/phase-5-verify.md
- @references/working-effectively-with-legacy-code.md
- @references/pragmatic-programmer.md
