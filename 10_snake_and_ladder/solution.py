"""
Problem 10: Snake & Ladder Game
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Inject a scripted/seeded dice so games are deterministic and replayable.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# TODO 1: Dice interface + standard (random) and scripted/seeded impls.
# ============================================================
class Dice(ABC):
    @abstractmethod
    def roll(self) -> int:
        ...


# ============================================================
# TODO 2: Board — holds size + snakes/ladders maps; VALIDATE config
#         (no snake-head == ladder-bottom). next_position(pos) resolves jumps.
# ============================================================
class Board:
    def __init__(self, size: int, snakes: dict, ladders: dict) -> None:
        raise NotImplementedError

    def next_position(self, pos: int) -> int:
        raise NotImplementedError


# ============================================================
# TODO 3: Player — id + current position.
# ============================================================


# ============================================================
# TODO 4: Game — turn loop: roll -> move (apply exact-finish rule) -> resolve
#         snake/ladder -> check win. Keep a move log. Report winner.
# ============================================================
class Game:
    def __init__(self, board: Board, players, dice: Dice) -> None:
        raise NotImplementedError

    def play(self):  # -> winner
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement (deterministic dice)."""
    raise NotImplementedError("Run a deterministic game and print the move trace + winner.")


if __name__ == "__main__":
    main()
