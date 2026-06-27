# Follow-up — Doctor Appointment Booking

**Mirrors:** Problem 06 (concurrency, locking, hold/expire) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design an appointment booking system for a clinic: patients book time **slots** with doctors; no slot is ever double-booked under concurrency.

## Functional requirements
1. Entities: **Specialty → Doctor → Day → Slot** (fixed-length, e.g. 30 min). A slot is AVAILABLE / HELD / BOOKED.
2. Search: list doctors by specialty; list a doctor's **available** slots for a date.
3. **Book**: a patient selects an available slot → it becomes booked, an **Appointment** is created.
4. **Hold then confirm**: selecting a slot **temporarily locks** it (e.g. 5 min) during payment; if not confirmed, the hold **expires** and the slot frees.
5. **Cancel** an appointment → slot becomes available again.
6. **Reschedule**: move an appointment to another available slot atomically (old freed only if new succeeds).

## Non-functional / constraints
- **The crux: concurrency** — two patients must never book the same slot. Lock at slot-or-doctor granularity, not one global lock; selection is atomic.
- Holds time out via an **injectable clock** (tests don't sleep for real).
- Adding a new slot-search or pricing rule shouldn't touch booking logic.

## Driver scenario
1. One specialty, one doctor, a day with 4 slots.
2. Print available slots.
3. Two threads try to book the **same slot** concurrently → exactly one wins; the other gets "slot unavailable".
4. A patient holds a slot but never confirms → advance the clock past the hold → slot is free again.
5. Reschedule a booked appointment to another slot; then cancel it → print final availability.

## Edge cases
- Concurrent booking race (must be prevented). · Booking an already-held/booked slot. · Hold expiry mid-flow. · Reschedule to an unavailable slot (must keep the original). · Cancel an already-cancelled appointment.
