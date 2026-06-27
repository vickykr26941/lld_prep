# 18 — Pub/Sub Message Broker (Kafka-lite)

**Difficulty:** ★★★★★ · **Asked at:** Amazon, Uber, Confluent, LinkedIn (senior/staff) · **Patterns:** Observer, Producer-Consumer, Strategy (partitioning)

## Problem
Design an in-process publish/subscribe message broker with **topics, partitions, consumer groups, and offsets** — a single-process Kafka model.

## Functional requirements
1. **Topics**, each split into **P partitions**. Messages have an optional key.
2. **Producer**: `publish(topic, key, value)`. A **partitioning strategy** (Strategy) maps key→partition (hash by key, or round-robin when no key). Same key ⇒ same partition (ordering guarantee per key).
3. Each partition is an **ordered, append-only log**; every message gets a monotonic **offset** within its partition.
4. **Consumer groups**:
   - Multiple consumers in a group **share** the topic's partitions (each partition consumed by **at most one** consumer in the group → load balancing).
   - Different groups consume the **same** messages independently (fan-out).
   - Each group tracks its **committed offset per partition**; a consumer reads from its offset forward.
5. `poll()` returns the next batch for a consumer; `commit()` advances its offset.
6. **Partition assignment / rebalancing** when consumers join/leave a group (a simple range or round-robin assignor).
7. (Senior) **At-least-once** delivery semantics: redelivery if not committed before crash/leave. State your guarantee.

## Non-functional / constraints
- **Thread-safe**: concurrent producers and consumers. Per-partition locking; appends are atomic and ordered.
- Ordering is guaranteed **per partition** (and thus per key), not globally — state this.
- No busy-wait consumers (block/notify on new messages or return empty).
- Adding a new partitioning or assignment strategy must not touch the log/broker core.

## Driver scenario (your `main()` should show this)
1. Create topic "orders" with 3 partitions.
2. Producer publishes 9 messages with keys → show same key lands in the same partition.
3. Group "G1" with 2 consumers → partitions split across them; together they receive all 9, each partition to exactly one consumer, in-order within a partition.
4. Group "G2" with 1 consumer → independently receives all 9 (fan-out).
5. A consumer in G1 polls but doesn't commit, then "leaves"; rebalance reassigns its partition and the uncommitted messages are redelivered (at-least-once).

## Edge cases to handle
- Publish to a topic/partition count mismatch. · Consumer polling an empty partition (returns empty, no spin). · More consumers than partitions (some idle). · Commit beyond current offset. · Rebalance mid-consumption. · Ordering preserved per partition under concurrency.

## TODO checklist
- [ ] `Message` (key, value, offset, timestamp); `Partition` append-only log
- [ ] `Topic` (list of partitions); `PartitioningStrategy` (hash / round-robin)
- [ ] `Broker`: create_topic, publish, register consumer group/consumer
- [ ] Consumer group offset tracking (committed offset per partition)
- [ ] Partition `Assignor` (range / round-robin) + rebalance on join/leave
- [ ] Thread-safe per-partition access; `poll()` / `commit()`
- [ ] `main()` driver covering the scenario above
