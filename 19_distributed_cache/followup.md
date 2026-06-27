# Follow-up — Sharded KV Store with Quorum (Dynamo-lite)

**Mirrors:** Problem 19 (consistent hashing, replication, Strategy, Facade) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design an in-process distributed key-value store in the Dynamo style: keys sharded across nodes by consistent hashing, replicated to R nodes, with **tunable quorum** reads and writes and conflict handling. (Simulate nodes as in-memory objects; no real network.)

## Functional requirements
1. A **ring** of N nodes via consistent hashing with **virtual nodes**.
2. Each key's **preference list** = its primary + next R-1 distinct nodes clockwise (replication factor R).
3. **Tunable consistency**: `put(key, value)` succeeds when **W** replicas ack; `get(key)` reads from **R_read** replicas and returns the reconciled value. Configurable `W`, `R_read` (classic `W + R_read > R` for strong consistency).
4. **Versioning**: each write carries a version (counter or vector clock); `get` reconciles replica responses, returning the latest (and detecting conflicts).
5. **Node add/remove** moves only the affected keys (minimal remap); preference lists update.
6. **Simulated node failure**: a down node doesn't ack; show that with `W < R` writes still succeed, and reads still return data from live replicas. (Bonus) hinted handoff.

## Non-functional / constraints
- Add/remove a node remaps O(keys/nodes), not all keys — verify in the driver.
- Strategies (hash fn, conflict resolution) pluggable without touching routing.
- State your consistency guarantee for each W / R_read combo.

## Driver scenario
1. Ring of 4 nodes (vnodes), R=3, W=2, R_read=2.
2. `put` 8 keys → print each key's preference list; show balanced distribution.
3. Mark one replica of a key as **down** → `put` still succeeds (W=2 acks from live nodes).
4. `get` that key from R_read replicas → returns the latest version despite the stale/down one.
5. Add a 5th node → report how many keys remapped (≈ 1/5, not all).

## Edge cases
- R greater than node count (clamp). · W or R_read greater than R (reject/clamp). · All replicas of a key down (read/write fails cleanly). · Conflicting versions on read (resolution rule). · Remove a node holding a primary (next replica serves).
