# 06 — Movie Ticket Booking (BookMyShow)

**Difficulty:** ★★★ · **Asked at:** BookMyShow, Amazon, Uber, PhonePe · **Patterns:** Concurrency/locking, Factory, Strategy (pricing/seat-selection)

## Problem
Design a movie-ticket booking system. Users browse shows in a city and **book seats** for a show — with **no double-booking** under concurrency.

## Functional requirements
1. Entities: **City → Cinema → Screen/Hall → Show**; a Show plays a **Movie** at a time on a Screen. A Screen has a **seat map** (rows × cols, seat types e.g. REGULAR/PREMIUM).
2. Browse: list cinemas in a city showing a given movie; list shows for a cinema/movie; show the **seat availability** for a show.
3. **Book**: a user selects ≥1 seats for a show → system reserves them, creates a **Booking**, returns confirmation. Booked seats become unavailable.
4. **Hold / reserve then confirm**: a seat selection is **temporarily locked** (e.g. 5 min) while payment is pending; if not confirmed, the hold **expires** and seats free up.
5. **Cancel** a booking → seats become available again.
6. Pricing may differ by seat type / show (a simple pricing strategy).

## Non-functional / constraints
- **THE crux: concurrency.** Two users must never book the same seat. Enforce with locking at **seat-or-show granularity** (not one global lock). Make the seat-selection step atomic.
- Holds must **time out** (use an injectable clock so tests don't sleep for real).
- Adding a new pricing or seat-selection rule shouldn't touch booking logic.

## Driver scenario (your `main()` should show this)
1. Set up: city "BLR", cinema "PVR", one screen 5×5, a show of "Inception".
2. Print seat map availability.
3. Two threads/users try to book the **same seats** concurrently → exactly **one succeeds**, the other gets a clear "seats unavailable" error.
4. A user holds seats but never confirms → advance the clock past the hold → seats are free again.
5. Cancel a confirmed booking → seats return to available; print final map.

## Edge cases to handle
- Concurrent booking race (must demonstrate it's prevented). · Booking an already-booked/held seat. · Hold expiry mid-flow. · Cancelling an already-cancelled booking. · Partially-available selection (some seats taken).

## TODO checklist
- [ ] Entities: City, Cinema, Screen, Seat (+type), Movie, Show, Booking
- [ ] Seat state model: AVAILABLE / HELD / BOOKED + transitions
- [ ] `BookingService`: search, hold, confirm, cancel — **thread-safe**, correct lock granularity
- [ ] Hold expiry via injectable clock
- [ ] `PricingStrategy` (per seat type / show)
- [ ] `main()` driver that actually spawns 2 threads to prove no double-booking
