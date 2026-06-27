# 03 — Rate Limiter

**Difficulty:** ★★★ · **Asked at:** Atlassian, Stripe, Amazon, Razorpay · **Patterns:** Strategy, Factory, concurrency

## Problem
Design a rate limiter that decides whether an incoming request from a client should be **allowed** or **throttled**, configurable per client.

## Functional requirements
1. Core API: `allow_request(client_id) -> bool` (True = allow, False = reject).
2. Implement **3 algorithms** behind a common interface:
   - **Fixed Window Counter** — N requests per fixed window (note the boundary burst problem).
   - **Sliding Window Log** — precise; keep timestamps within the trailing window.
   - **Token Bucket** — capacity + refill rate; allows controlled bursts.
3. **Per-client** limits: each `client_id` has its own independent counter/bucket. Support different limits per client (a `RateLimiterConfig`).
4. A **factory** creates the right limiter from config (algorithm + params) so callers don't `new` concrete classes.
5. Limits are time-based — use an **injectable clock** (don't hard-call `time.monotonic()` inside the algorithm) so behaviour is testable.

## Non-functional / constraints
- **Thread-safe**: many threads may call `allow_request` for the same client concurrently. Lock at the **right granularity** (per-client, not one global lock for everything).
- Memory: sliding-window log must **evict** old timestamps, not grow unbounded.
- Adding a **4th algorithm** must require zero changes to existing limiters or the caller (Open/Closed via the factory + interface).

## Driver scenario (your `main()` should show this)
1. Configure a token-bucket limiter: capacity 5, refill 1 token/sec, for `client_A`.
2. Fire 8 requests back-to-back → first 5 allowed, next 3 rejected (print allow/deny).
3. Advance the injected clock by 3s → 3 tokens refilled → next 3 allowed.
4. Repeat the burst test with the **fixed-window** limiter and show the boundary-burst weakness.
5. Show two clients (`A`, `B`) are limited **independently**.

## Edge cases to handle
- First-ever request for a client (lazy init). · Clock going backwards (guard). · Exactly-at-boundary timestamps. · Concurrent refill + consume on the same bucket.

## TODO checklist
- [ ] `RateLimiter` interface: `allow_request(client_id) -> bool`
- [ ] `FixedWindowCounter`, `SlidingWindowLog`, `TokenBucket` implementations
- [ ] Per-client state isolation + per-client locking
- [ ] Injectable clock abstraction
- [ ] `RateLimiterFactory` + a `RateLimiterConfig`
- [ ] `main()` driver covering the scenario above (use the fake clock, no real sleeps)
