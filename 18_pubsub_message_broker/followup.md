# Follow-up — Message Broker with Exchanges & Routing (RabbitMQ-lite)

**Mirrors:** Problem 18 (Observer, Producer-Consumer, Strategy routing, concurrency) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design an in-process message broker in the RabbitMQ style: producers publish to **exchanges**, which route messages to bound **queues** by routing rules; consumers pull from queues with acknowledgements and requeue.

## Functional requirements
1. **Queues**: durable, ordered FIFO buffers consumers read from.
2. **Exchanges** with a **routing type** (Strategy):
   - `DIRECT` — deliver to queues whose binding key **equals** the message routing key.
   - `FANOUT` — deliver to **all** bound queues (ignore key).
   - `TOPIC` — wildcard match (`*` = one word, `#` = zero+ words) of routing key vs binding pattern.
3. `bind(queue, exchange, binding_key)` / `unbind(...)`.
4. `publish(exchange, routing_key, message)` → routed to **0+ queues**; a message matching multiple queues is copied to each.
5. **Consume**: `consume(queue) -> (message, delivery_tag)`; `ack(tag)` removes it; `nack(tag, requeue=True)` puts it back (at-least-once).
6. **Unrouted messages** (no matching queue) → optionally to an alternate/dead-letter exchange (state your rule).

## Non-functional / constraints
- **Thread-safe**: concurrent publishers and consumers; an unacked in-flight message isn't delivered to another consumer.
- Per-queue FIFO ordering preserved under concurrency.
- Adding a new exchange/routing type must not touch queue or broker core (Open/Closed).
- No busy-wait consumers.

## Driver scenario
1. Declare queues Qa, Qb, Qc. Direct exchange "ex.d": bind Qa key="info", Qb key="error".
2. `publish("ex.d","error",m)` → only Qb gets it; `publish("ex.d","info",m)` → only Qa.
3. Topic exchange "ex.t": bind Qc pattern="logs.*.eu"; publish key "logs.app.eu" → Qc; "logs.app.us" → not.
4. Fanout exchange → a publish reaches all bound queues.
5. Consume from Qb, `nack(requeue=True)` → message reappears for redelivery; then `ack` removes it.

## Edge cases
- Publish to an exchange with no bindings (unrouted). · Topic `#` matching zero words. · Same message to multiple queues. · Ack/nack with an invalid tag. · Two consumers on one queue (each message to exactly one). · Unbind mid-flight.
