"""
Problem 04: Elevator System
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Drive the sim with tick() — no wall-clock sleeps.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum

# ============================================================
# TODO 1: Enums — Direction (UP/DOWN/IDLE), ElevatorState
# ============================================================


# ============================================================
# TODO 2: Request modelling — hall call (floor, direction) vs car call (target floor)
# ============================================================


# ============================================================
# TODO 3: Elevator — holds current floor + state + pending stops.
#         step()/move() advances one floor; manages DOORS_OPEN; serves stops
#         ordered by current direction (not naive FCFS).
# ============================================================
class Elevator:
    def __init__(self, elevator_id: int, num_floors: int) -> None:
        raise NotImplementedError


# ============================================================
# TODO 4: DispatchStrategy interface + Nearest and SCAN/LOOK implementations.
# ============================================================
class DispatchStrategy(ABC):
    @abstractmethod
    def select_elevator(self, elevators, hall_call):  # -> Elevator
        ...


# ============================================================
# TODO 5: ElevatorController — registers hall/car calls, runs dispatch,
#         and exposes tick() to advance the whole simulation one unit.
# ============================================================
class ElevatorController:
    def __init__(self, num_floors: int, num_elevators: int, strategy: DispatchStrategy) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement the per-tick trace."""
    raise NotImplementedError("Run the 10-floor / 2-elevator scenario, printing each tick.")


if __name__ == "__main__":
    main()
