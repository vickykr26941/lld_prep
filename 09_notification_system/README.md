# 09 — Notification System

**Difficulty:** ★★★ · **Asked at:** Amazon, Uber, Swiggy, Razorpay · **Patterns:** Observer, Strategy, Decorator, Factory

## Problem
Design a notification service: the app raises events; the system delivers messages to users over multiple **channels** (email, SMS, push), honouring user **preferences**, with retries and pluggable formatting.

## Functional requirements
1. **Channels** behind one interface — at least **Email**, **SMS**, **Push** (simulate actual sending with a log/print + a stored "sent" record).
2. Send a notification to a user across **one or more channels**.
3. **User preferences**: each user opts into a subset of channels (and can mute). Respect them when dispatching.
4. **Observer / pub-sub**: components **subscribe** to event types (e.g. `ORDER_SHIPPED`); when an event is **published**, all interested subscribers are notified. Decouple producers from the dispatcher.
5. **Templates / formatting** per channel (a template strategy): the same event renders differently for email vs SMS.
6. **Retry with backoff** on channel failure, up to N attempts; mark `FAILED` after exhausting retries. (Use an injectable clock; don't really sleep.)
7. (Decorator bonus) Cross-cutting add-ons — e.g. wrap a channel to add **rate-limiting** or **audit-logging** without modifying it.

## Non-functional / constraints
- Adding a new channel must require **zero changes** to the dispatcher or event producers (Factory + interface, Open/Closed).
- The event publisher must not know who the subscribers are (Observer).
- Delivery should be resilient: one channel failing must not block the others.

## Driver scenario (your `main()` should show this)
1. Register users with different channel preferences (U1: email+push, U2: SMS only, U3: muted).
2. Publish an `ORDER_SHIPPED` event for an order belonging to U1 and U2.
3. Show U1 gets email+push, U2 gets SMS (channel-specific template), U3 gets nothing.
4. Make the SMS channel **fail twice then succeed** → show retry/backoff producing eventual success.
5. Wrap the email channel in an **audit-logging decorator** → show the audit entries without changing EmailChannel.

## Edge cases to handle
- User with no enabled channels. · All channels fail (final FAILED status). · Duplicate subscription. · Unknown event type (no subscribers). · Template missing for a channel.

## TODO checklist
- [ ] `NotificationChannel` interface + Email / SMS / Push impls
- [ ] `ChannelFactory` to create channels by type
- [ ] User + preferences model
- [ ] Observer: `EventBus`/`Subject` with subscribe/publish, decoupled from producers
- [ ] `TemplateStrategy` per channel/event
- [ ] Retry-with-backoff (injectable clock) + delivery status tracking
- [ ] A `Decorator` adding a cross-cutting concern to a channel
- [ ] `main()` driver covering the scenario above
