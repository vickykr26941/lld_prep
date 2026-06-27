"""
Problem 20: Ride-Hailing / Cab Booking (Uber)
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Crux: atomic driver assignment (no double-booking) + sub-linear nearby lookup.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum

# ============================================================
# TODO 1: Entities — Location, Rider, Driver(+DriverStatus), Trip.
# ============================================================
class DriverStatus(Enum):
    pass  # TODO: AVAILABLE / EN_ROUTE / ON_TRIP / OFFLINE


# ============================================================
# TODO 2: TripState machine — REQUESTED -> DRIVER_ASSIGNED -> DRIVER_ARRIVED
#         -> IN_PROGRESS -> COMPLETED (+ CANCELLED). Enforce valid transitions.
# ============================================================


# ============================================================
# TODO 3: Spatial index — grid/geohash buckets for nearby-driver queries
#         (NOT an O(drivers) scan). update_location / nearby(point, radius).
# ============================================================


# ============================================================
# TODO 4: MatchingStrategy (nearest / ETA) + PricingStrategy (base+km+min+surge).
# ============================================================
class MatchingStrategy(ABC):
    @abstractmethod
    def select(self, candidates, pickup):  # -> Driver or None
        ...

class PricingStrategy(ABC):
    @abstractmethod
    def fare(self, trip) -> float:
        ...


# ============================================================
# TODO 5: RideService — request_ride (ATOMIC driver assignment, no double-book),
#         trip lifecycle transitions, Observer notifications, injectable clock.
# ============================================================
class RideService:
    def __init__(self, matching: MatchingStrategy, pricing: PricingStrategy, clock=None) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement (concurrent match test)."""
    raise NotImplementedError("Match nearest driver; prove no double-assignment under threads.")


if __name__ == "__main__":
    main()
