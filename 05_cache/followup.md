# Follow-up — Database Connection Pool

**Mirrors:** Problem 05 (Strategy eviction + bounded resource + concurrency) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design a thread-safe pool of reusable database connections: callers borrow a connection, use it, and return it; the pool bounds the total and reclaims idle ones.

## Functional requirements
1. Construct with a **max pool size** and a connection **factory** (creates a simulated `Connection`).
2. `acquire(timeout) -> Connection` — return an idle connection, or create one if under max, or **block** up to `timeout` until one is returned (then raise on timeout).
3. `release(conn)` — return a connection to the pool for reuse.
4. **Idle eviction policy** (Strategy): close connections idle longer than a TTL, keeping a configurable **min idle**. Reuse order is pluggable (LIFO for warmth vs FIFO for fairness).
5. **Health check**: validate a connection on borrow; if broken, discard and create a fresh one.
6. Metrics: total / in-use / idle counts.
7. `shutdown()` — close all connections; reject further `acquire`.

## Non-functional / constraints
- **Thread-safe**: many threads acquire/release concurrently; never hand the same connection to two callers; never exceed max.
- No busy-wait — block on a condition for an available connection.
- Idle eviction and TTL use an **injectable clock**.
- Adding a new reuse/eviction policy must not touch acquire/release core.

## Driver scenario
1. Pool max 2, min idle 1.
2. Two threads acquire both connections; a third `acquire(timeout=short)` blocks then times out.
3. One thread releases → the waiting third acquirer (in a retry) gets it.
4. Advance the clock past idle-TTL → an idle connection beyond min-idle is evicted/closed.
5. Mark a connection unhealthy → on next acquire it's discarded and replaced. Print metrics.

## Edge cases
- Release a connection not from this pool / double-release. · Acquire after shutdown. · All connections in use + timeout. · Min-idle vs TTL eviction conflict. · Concurrent acquire of the last connection.
