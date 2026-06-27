# 13 — In-Memory Key-Value Store with Transactions

**Difficulty:** ★★★★ · **Asked at:** Amazon, Google, Databricks (senior) · **Patterns:** Command/Memento, Composite (nested txns)

## Problem
Design an in-memory key-value store (like a tiny Redis) that supports **nested transactions** with commit/rollback.

## Functional requirements
1. Basic ops: `set(key, value)`, `get(key) -> value | None`, `delete(key)`, `count(value)` (how many keys hold a given value).
2. **Transactions**:
   - `begin()` — start a transaction (transactions can be **nested**).
   - `commit()` — apply the **innermost open** transaction's changes to its parent (or to the store if outermost). Be explicit about whether `commit` collapses all or one level.
   - `rollback()` — discard the innermost open transaction's changes; error if none open.
3. Reads inside a transaction see that transaction's **uncommitted** writes layered over parent/store state.
4. Writes inside a transaction are **isolated** — invisible to the base store until committed.
5. `count(value)` must reflect the current transactional view efficiently (ideally not O(n) per call — maintain a value→count index per layer).

## Non-functional / constraints
- Nested begin/rollback must be correct to arbitrary depth (Composite/stack of layers).
- Decide and document **isolation**: this is single-connection (no concurrent txns) unless you add locking — state your scope.
- Prefer O(1) `set/get/delete` and amortised efficient `count`.
- (Senior bonus) Sketch how you'd extend to multiple concurrent clients (per-key locks / MVCC) — at least in comments.

## Driver scenario (your `main()` should show this)
```
set(a,1); get(a) -> 1
begin; set(a,2); get(a) -> 2
begin; set(a,3); get(a) -> 3
rollback; get(a) -> 2          # inner txn discarded
commit; get(a) -> 2            # outer txn applied to store
rollback -> error (no open txn)
```
Also demonstrate `count`: set two keys to value "x" across nested txns and show `count("x")` tracking through commit/rollback.

## Edge cases to handle
- `commit`/`rollback` with no open transaction → error. · `delete` of a key set in a parent layer (tombstone vs absent). · `get` of a deleted-in-txn key → None even if base has it. · `count` after deletes. · Deeply nested begin then a single rollback.

## TODO checklist
- [ ] Base store (dict) + a value→count index
- [ ] Transaction layer (a stack of diff-layers, each with writes + tombstones + count deltas)
- [ ] `set/get/delete/count` resolving through the layer stack
- [ ] `begin/commit/rollback` over the stack (commit merges into parent layer)
- [ ] Tombstone handling for deletes inside a txn
- [ ] `main()` driver covering the scenario above
