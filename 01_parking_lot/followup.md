# Follow-up — Bike-Sharing Dock System

**Mirrors:** Problem 01 (Strategy, Factory, Singleton) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design the software for a city bike-sharing service: docking stations hold bikes; users pick up a bike at one station and return it at another; the system charges by duration and bike type.

## Functional requirements
1. The city has multiple **stations**; each station has a fixed number of **docks**. A dock is empty or holds a bike.
2. Bike types: `STANDARD`, `ELECTRIC`, `CARGO` — each with its own rate.
3. **Rent**: a user unlocks a compatible available bike at a station → dock becomes empty, a **Trip** is started (id, bike, start station, start time).
4. **Return**: user docks the bike at any station with a free dock → dock fills, the trip ends, and a **fare** is computed.
5. **Pricing is pluggable**: at least a flat per-minute rate and a tiered rate (free first N minutes, then per-minute). Electric/cargo may price differently.
6. A **station-selection strategy** for "where can I return?": nearest station with a free dock (Strategy).
7. Queries: bikes available at a station (by type), free docks at a station, system-wide availability.
8. Reject gracefully: no compatible bike to rent, or no free dock to return.

## Non-functional / constraints
- The system manager is a single shared instance, but keep it testable (inject dependencies, no hard global).
- Adding a new bike type or pricing/selection strategy must not edit rental logic (Open/Closed).
- Duration/fare must use an injectable clock (no deep `time.time()`).

## Driver scenario
1. Build 3 stations with mixed docks/bikes.
2. Rent a standard bike at station A; rent an electric at station B → print trips.
3. Try to rent when no compatible bike is free → graceful rejection.
4. Return the standard bike at station C after a simulated 22 min → print fare (tiered).
5. Print system-wide availability summary.

## Edge cases
- Full station on return (no free dock). · Empty station on rent. · Return to the same station. · Partial-minute rounding. · Concurrent rent of the last bike (state your assumption).
