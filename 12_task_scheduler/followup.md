# Follow-up — Delayed Message Queue (SQS-lite)

**Mirrors:** Problem 12 (min-heap by time, Producer-Consumer, concurrency, retries) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design an in-process delayed/visibility-timeout message queue like Amazon SQS: producers enqueue messages (optionally delayed); consumers receive them, process, and delete; un-deleted messages reappear after a visibility timeout, with retries and a dead-letter queue.

## Functional requirements
1. `send(message, delay=0)` — message becomes **visible** at `now + delay`.
2. `receive(count, visibility_timeout) -> [messages]` — returns up to `count` currently-visible messages and makes them **invisible** (in-flight) for `visibility_timeout`.
3. `delete(receipt)` — permanently remove a successfully-processed message.
4. If a received message is **not deleted** before its visibility timeout expires, it becomes **visible again** (at-least-once delivery) and its **receive count** increments.
5. After **max receives**, route the message to a **dead-letter queue** instead of redelivering.
6. A single dispatcher tracks the **earliest** become-visible time via a min-heap (sleep-until-due with early wakeup on new/earlier message); not a busy poll, not a thread per message.

## Non-functional / constraints
- **Thread-safe**: concurrent producers and consumers; a message in-flight is never handed to a second consumer.
- Deterministic via an **injectable clock** + controllable time advance (no real waits).
- Ordering is best-effort by visibility time (state your guarantee).

## Driver scenario
1. `send(A)`, `send(B, delay=50)`, `send(C)`.
2. `receive(10, vt=30)` → returns A and C (B not yet visible); they go in-flight.
3. Advance clock past 30 without deleting A → A becomes visible again, receive-count 2.
4. Advance clock to 50 → B visible.
5. Receive a message past its max-receive limit → it lands in the DLQ.

## Edge cases
- Receive on an empty/all-in-flight queue (returns empty, no spin). · Delete with an expired/invalid receipt. · Two consumers racing for the same message. · Delay added while dispatcher sleeps (early wakeup). · Max-receive boundary → DLQ.
