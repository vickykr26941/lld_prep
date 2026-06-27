# 19 — Distributed Cache (Consistent Hashing)

**Difficulty:** ★★★★★ · **Asked at:** Amazon, Uber, Netflix (senior/staff) · **Patterns:** Strategy (hashing, write policy, eviction), Facade

## Problem
Design a distributed cache modelled in a single process: keys are sharded across multiple cache **nodes** via **consistent hashing**, with replication and configurable write policies. (No real network — simulate nodes as in-memory objects.)

## Functional requirements
1. A **ring** of N cache nodes using **consistent hashing** with **virtual nodes** for balanced distribution.
2. `get(key)` / `put(key, value)` route to the node(s) that own the key's hash position (clockwise on the ring).
3. **Add / remove a node** → only the keys in the affected arc move (the whole point of consistent hashing). Demonstrate **minimal key remapping**.
4. **Replication factor R**: each key stored on its primary + next R-1 distinct nodes clockwise. `get` can read from any replica.
5. **Write policy** (Strategy): **write-through** (write cache + backing store synchronously) vs **write-back/cache-aside** — pluggable. A `BackingStore` (simulated DB) sits behind the cache.
6. Each node has a bounded capacity with an **eviction policy** (reuse Problem 05's LRU/LFU).

## Non-functional / constraints
- Key distribution should be reasonably balanced (virtual nodes); show the distribution.
- Adding/removing a node must remap **O(keys/nodes)** keys, not all of them — verify in the driver.
- Strategies (hash fn, write policy, eviction) pluggable without touching routing.
- (Senior) Note read/write consistency under replication (read-repair? quorum?) — at least in comments.

## Driver scenario (your `main()` should show this)
1. Ring with 3 nodes (× virtual nodes), replication factor 2, LRU eviction, write-through to a backing store.
2. `put` 12 keys → print which node(s) hold each; show balance across nodes.
3. `get` a key → served from a replica; show it also persisted in the backing store.
4. **Add a 4th node** → print how many keys remapped (should be ≈ 1/4, not all 12).
5. **Remove a node** → its keys served from replicas; show no data loss for replicated keys.

## Edge cases to handle
- Single node (R > node count → clamp). · Hash collisions on the ring (tie-break). · Removing a node that holds a primary (promote replica). · get for a missing key (miss → backing store load on cache-aside). · Even key distribution with few virtual nodes (show why vnodes matter).

## TODO checklist
- [ ] `HashRing` with virtual nodes: `add_node`, `remove_node`, `get_nodes(key, r)`
- [ ] `CacheNode` (bounded, with eviction policy)
- [ ] `BackingStore` (simulated DB)
- [ ] `WritePolicy` Strategy: write-through / cache-aside
- [ ] `DistributedCache` facade: get/put routing + replication
- [ ] Remap-count instrumentation for add/remove node
- [ ] `main()` driver covering the scenario above
