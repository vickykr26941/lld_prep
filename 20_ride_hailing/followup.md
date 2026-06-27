# Follow-up — Food Delivery System (Swiggy-lite)

**Mirrors:** Problem 20 (State machine, Strategy, spatial index, concurrency) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design the core of a food-delivery service: customers order from restaurants; the system assigns a nearby **delivery partner**, manages the order lifecycle, and prices the order — safely under concurrency.

## Functional requirements
1. Entities: **Customer**, **Restaurant** (menu, location, open/closed), **DeliveryPartner** (live location + status `AVAILABLE`/`ASSIGNED`/`DELIVERING`/`OFFLINE`), **Order**, **Location**.
2. `place_order(customer, restaurant, items)` → validate items/availability, compute bill, create an order.
3. **Order state machine**: `PLACED → ACCEPTED → PREPARING → READY → PICKED_UP → DELIVERED` (+ `CANCELLED`/`REJECTED` from valid states). Enforce transitions.
4. **Partner assignment strategy** (Strategy): nearest available partner (by distance) or fewest-active-deliveries — pluggable. When an order is READY, assign a partner.
5. **Pricing strategy**: item subtotal + delivery fee (distance-based) + **surge** by area demand — pluggable.
6. **Spatial index** for nearby-partner queries — grid/geohash buckets, not an O(partners) scan.
7. Notify customer + partner on state changes (Observer).

## Non-functional / constraints
- **No double-assignment** of a partner under concurrent READY orders — assignment is atomic (lock / CAS on partner status).
- Nearby lookup sub-linear.
- Matching/pricing strategies pluggable without touching the order lifecycle.
- Deterministic time/movement via an **injectable clock**.

## Driver scenario
1. Register a restaurant + 5 partners at known locations (AVAILABLE); a customer places an order.
2. Drive PLACED → ACCEPTED → PREPARING → READY; on READY, nearest available partner is assigned (that partner no longer AVAILABLE).
3. Two orders become READY **simultaneously** (threads) near the same single free partner → exactly one gets it; the other waits / picks the next-nearest.
4. Continue PICKED_UP → DELIVERED; compute the bill (show surge applied).
5. Attempt an illegal transition (e.g. PICKED_UP before READY) → rejected.

## Edge cases
- No available partner in range. · Concurrent assignment of the same partner. · Customer cancels after ACCEPTED (free resources). · Restaurant closed / item unavailable. · Partner goes offline mid-search. · Invalid state transition.
