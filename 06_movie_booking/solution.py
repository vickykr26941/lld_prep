"""
Problem 06: Movie Ticket Booking (BookMyShow)
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

The crux is concurrency: no double-booking. Pick your lock granularity deliberately.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum

# ============================================================
# TODO 1: Catalog entities — City, Cinema, Screen, Seat (+ SeatType), Movie, Show.
# ============================================================


# ============================================================
# TODO 2: Seat state machine — AVAILABLE / HELD / BOOKED, with transitions.
# ============================================================
class SeatStatus(Enum):
    pass  # TODO


# ============================================================
# TODO 3: PricingStrategy — fee per seat-type / show.
# ============================================================
class PricingStrategy(ABC):
    @abstractmethod
    def price(self, show, seat) -> float:
        ...


# ============================================================
# TODO 4: BookingService — the orchestrator. THREAD-SAFE.
#         - search shows by city/movie/cinema
#         - hold(show, seats, user) -> Hold (temporary, expires)
#         - confirm(hold) -> Booking
#         - cancel(booking)
#         Make seat selection atomic; lock per-show or per-seat, not globally.
#         Holds expire via an injectable clock.
# ============================================================
class BookingService:
    def __init__(self, clock=None) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README. TODO: spawn 2 threads booking the same seats; prove one wins."""
    raise NotImplementedError("Demonstrate no double-booking under concurrency.")


if __name__ == "__main__":
    main()
