# Follow-up — Circuit Breaker

**Mirrors:** Problem 03 (Strategy, State, concurrency) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design a circuit breaker that protects a flaky downstream dependency: it monitors failures and **trips open** to fail fast, then probes for recovery — like Hystrix/resilience4j.

## Functional requirements
1. Wrap a call: `execute(callable) -> result` (or raises if the breaker is open / the call fails).
2. **Three states** (state machine): `CLOSED` (calls pass), `OPEN` (calls rejected immediately), `HALF_OPEN` (a limited number of trial calls allowed).
3. **Trip rule (pluggable Strategy)**: open when failures exceed a threshold — support at least a consecutive-failure count and a failure-rate-over-window rule.
4. From OPEN, after a **cooldown**, move to HALF_OPEN and allow N trial calls: if they succeed → CLOSED; if any fail → back to OPEN (reset cooldown).
5. Per-dependency breakers, each with independent state and config.
6. Expose metrics: current state, recent success/failure counts, last state-change time.

## Non-functional / constraints
- **Thread-safe**: concurrent calls update counts/state without races; state transitions are atomic.
- Time-based transitions use an **injectable clock** (no real sleeps in tests).
- Adding a new trip strategy must not touch the state-machine code (Open/Closed).
- A rejected (fast-fail) call must be cheap — no downstream invocation.

## Driver scenario
1. Breaker: open after 3 consecutive failures, cooldown 5s, 2 trial calls in half-open.
2. 3 failing calls → breaker trips OPEN; next call fast-fails without invoking downstream.
3. Advance clock past cooldown → HALF_OPEN; one trial succeeds, second succeeds → CLOSED.
4. Repeat trip, but a half-open trial fails → back to OPEN with cooldown reset.
5. Show two dependencies have independent breaker states.

## Edge cases
- Concurrent calls during the OPEN→HALF_OPEN transition (only N trials get through). · Success in CLOSED resets the failure counter. · Clock going backwards (guard). · Exactly-at-threshold failure count.
