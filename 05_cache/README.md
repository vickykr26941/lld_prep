# 05 — In-Memory Cache (LRU / LFU)

**Difficulty:** ★★☆ · **Asked at:** Amazon, Google, Microsoft, Atlassian · **Patterns:** Strategy (eviction), data-structure design

## Problem
Design a fixed-capacity in-memory cache with **O(1)** get/put and a **pluggable eviction policy**.

## Functional requirements
1. API: `get(key) -> value | None`, `put(key, value)`.
2. Fixed **capacity**; when full, evict one entry per the policy to make room.
3. Eviction policies behind one interface — implement at least:
   - **LRU** (least-recently-used), and
   - **LFU** (least-frequently-used; tie-break by least-recently-used).
4. **`get` and `put` must be O(1)** for LRU (doubly-linked list + hashmap). LFU should be O(1) too (freq buckets) — or document your complexity if not.
5. Optional but nice: per-entry **TTL** (expired entries are misses and get evicted lazily).
6. Optional: hit/miss **stats**.

## Non-functional / constraints
- Swapping the eviction policy must not change the cache's public API (Strategy).
- **Thread-safe** `get`/`put` (a lock is fine; note where it lives).
- No O(n) scans on the hot path — that's the whole point of the question.

## Driver scenario (your `main()` should show this)
1. LRU cache, capacity 2. `put(1,1); put(2,2); get(1) -> 1; put(3,3)` evicts key 2; `get(2) -> None`.
2. LFU cache, capacity 2. Show that a frequently-`get`'d key survives while a rarely-used one is evicted.
3. (If you did TTL) put a key with short TTL, advance the injected clock, `get` → miss.
4. Print hit/miss stats at the end.

## Edge cases to handle
- `put` on an existing key (update value + recency/frequency, no size growth). · Capacity 0/1. · Evicting the just-inserted key. · LFU tie-break correctness.

## TODO checklist
- [ ] `EvictionPolicy` interface (record access, choose victim)
- [ ] LRU via doubly-linked list + dict (O(1))
- [ ] LFU via frequency buckets (document complexity)
- [ ] `Cache` facade wiring capacity + policy + storage
- [ ] Thread-safety + (optional) TTL with injectable clock
- [ ] `main()` driver covering the scenario above
