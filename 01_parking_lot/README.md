# 01 — Parking Lot System

**Difficulty:** ★★☆ · **Asked at:** Amazon, Google, Uber, Swiggy, almost everyone · **Patterns:** Strategy, Factory, Singleton

## Problem
Design the software for a multi-floor parking lot. Vehicles enter, are assigned a spot, get a ticket, and pay a fee on exit based on duration and vehicle type.

## Functional requirements
1. The lot has **multiple floors**; each floor has multiple **spots**.
2. Spot types: `MOTORCYCLE`, `COMPACT`, `LARGE` (size-tiered). Vehicle types: `MOTORCYCLE`, `CAR`, `TRUCK`.
3. A vehicle can park in its own size or larger (e.g. a car fits COMPACT or LARGE, not MOTORCYCLE).
4. On entry: find the **nearest available** compatible spot, mark it occupied, issue a **Ticket** (id, vehicle, spot, entry time).
5. On exit: free the spot, compute the **fee**, and return it.
6. **Pricing is pluggable** — support at least: per-hour flat rate, and a tiered rate (first hour X, each extra hour Y). Different vehicle types may have different rates.
7. Query: how many free spots remain (overall and per floor / per spot-type).
8. Reject entry gracefully when the lot (or compatible spots) is **full**.

## Non-functional / constraints
- The `ParkingLot` should be a **single shared instance** (think Singleton — but make it testable, not a hard global).
- Adding a **new pricing strategy** or a **new vehicle/spot type** must not require editing existing spot-assignment logic (Open/Closed).
- Fee calculation must use an **injectable clock** so tests are deterministic (don't call `time.time()` deep inside).

## Driver scenario (your `main()` should show this)
1. Build a lot: 2 floors × {2 motorcycle, 3 compact, 1 large} spots.
2. Park a motorcycle, two cars, a truck → print issued tickets + spot ids.
3. Try to park a second truck when no LARGE spot is free → show graceful rejection.
4. Exit one car after a simulated 2h15m → print computed fee (use the tiered strategy).
5. Print remaining-capacity summary.

## Edge cases to handle
- Full lot / no compatible spot. · Exit with an invalid/used ticket. · Duration rounding (do you round up partial hours?). · Concurrent entries grabbing the same spot (note your assumption even if single-threaded).

## TODO checklist
- [ ] `VehicleType` / `SpotType` enums + compatibility rule
- [ ] `Vehicle`, `ParkingSpot`, `ParkingFloor`, `Ticket` entities
- [ ] `SpotAssignmentStrategy` (nearest-first) behind an interface
- [ ] `PricingStrategy` interface + ≥2 implementations
- [ ] `ParkingLot` orchestrator (park / unpark / availability)
- [ ] Injectable clock for entry/exit timing
- [ ] `main()` driver covering the scenario above
