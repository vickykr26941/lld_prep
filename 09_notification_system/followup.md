# Follow-up — Stock Price Alert System

**Mirrors:** Problem 09 (Observer, Strategy, Decorator, Factory) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design a system where users subscribe to **price alerts** on stock symbols; when the market price crosses a user's condition, they're notified across their chosen channels.

## Functional requirements
1. A **price feed** publishes `(symbol, price)` ticks. The alert engine subscribes (Observer) — producers don't know who listens.
2. Users create **alerts**: `symbol` + a **condition** (Strategy): price `>`, `<`, crosses a target, or % change from a reference. Pluggable condition types.
3. When a tick satisfies an alert, notify the user over their enabled **channels** (Email, SMS, Push) — channel created via a **Factory**, each with a per-channel **template**.
4. **One-shot vs recurring** alerts: a one-shot alert disarms after firing; recurring re-arms.
5. **Throttling / cooldown** per alert so a noisy symbol doesn't spam (e.g. at most once per minute) — model with a **Decorator** wrapping the channel (audit/rate-limit) without modifying it.
6. Per-channel **retry with backoff** on delivery failure; track delivery status.

## Non-functional / constraints
- Adding a new condition type or channel requires zero changes to the engine (Open/Closed + Factory).
- Thread-safe: concurrent ticks and subscription changes.
- Time-based cooldown/retry via an **injectable clock** (no real sleeps).
- One channel failing must not block the others.

## Driver scenario
1. Users: U1 (AAPL > 200, email+push), U2 (AAPL < 150, SMS), U3 (TSLA crosses 250, muted).
2. Feed AAPL ticks rising past 200 → U1 notified on both channels; U2 not.
3. Re-fire within the cooldown → suppressed by the rate-limit decorator.
4. SMS channel fails twice then succeeds → retry/backoff eventually delivers.
5. A one-shot alert disarms after firing; a recurring one fires again on the next qualifying tick.

## Edge cases
- User with no enabled channels. · Condition exactly at the boundary. · Duplicate subscription. · Tick for a symbol with no alerts. · All channels fail (final FAILED). · Throttled vs disarmed distinction.
