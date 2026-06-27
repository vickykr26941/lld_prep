# 20 — Ride-Hailing / Cab Booking (Uber)

**Difficulty:** ★★★★★ · **Asked at:** Uber, Lyft, Ola, Grab (senior/staff) · **Patterns:** Strategy (matching, pricing), State, Observer, concurrency

## Problem
Design the core of a ride-hailing service: riders request rides, the system **matches** a nearby available driver, manages the **trip lifecycle**, and prices the fare — safely under concurrency.

## Functional requirements
1. Entities: **Rider**, **Driver** (with live location + status: `AVAILABLE`/`EN_ROUTE`/`ON_TRIP`/`OFFLINE`), **Trip**, **Location** (lat/lng or grid).
2. `request_ride(rider, pickup, drop)` → find nearby available drivers and **match** one.
3. **Matching strategy** (Strategy): nearest-driver (by distance), or shortest-ETA — pluggable. Drivers update location over time.
4. **Trip state machine**: `REQUESTED → DRIVER_ASSIGNED → DRIVER_ARRIVED → IN_PROGRESS → COMPLETED` (+ `CANCELLED` from several states). Enforce valid transitions.
5. **Pricing strategy**: base + per-km + per-min, with **surge multiplier** by area demand — pluggable.
6. **Driver location index** for efficient "nearby" queries — a grid / geohash bucket, not an O(drivers) scan per request.
7. **Concurrency**: two riders must not be matched to the **same** driver. Assignment is atomic.
8. Notify rider + driver on state changes (Observer).

## Non-functional / constraints
- **No double-assignment** of a driver under concurrent requests — the crux (lock or atomic compare-and-set on driver status).
- Nearby lookup should be sub-linear (spatial bucketing).
- Matching/pricing strategies pluggable without touching the trip lifecycle.
- Deterministic time/movement via an injectable clock so tests don't depend on wall-clock.

## Driver scenario (your `main()` should show this)
1. Register 5 drivers at known locations (AVAILABLE); a rider requests a ride at a pickup point.
2. Matching picks the nearest available driver → trip enters `DRIVER_ASSIGNED`; that driver is no longer AVAILABLE.
3. Two riders request **simultaneously** (threads) near the same single available driver → exactly one is matched; the other gets "no driver available" or the next-nearest.
4. Drive the trip through arrived → in-progress → completed; compute the fare (show surge applied).
5. Attempt an illegal transition (e.g. complete a trip that never started) → rejected.

## Edge cases to handle
- No available drivers in range. · Concurrent match for the same driver. · Rider cancels after assignment (free the driver). · Driver goes offline mid-search. · Surge area with zero supply. · Invalid state transition.

## TODO checklist
- [ ] Entities: Rider, Driver(+status), Trip, Location
- [ ] `TripState` machine with enforced transitions
- [ ] Spatial index (grid/geohash) for nearby-driver queries
- [ ] `MatchingStrategy` (nearest / ETA) + `PricingStrategy` (base+distance+time+surge)
- [ ] Atomic driver assignment (no double-booking) under concurrency
- [ ] Observer notifications on state changes; injectable clock
- [ ] `main()` driver covering the scenario above (with the concurrent-match test)
