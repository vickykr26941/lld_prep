"""
Problem 15: Chess Game Engine
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Per-piece move rules (polymorphism), NOT a switch(pieceType) inside the board.
Reuse legal-move generation for both validation and checkmate detection.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum

# ============================================================
# TODO 1: Color enum, Position/Square (file,rank), Move value object.
# ============================================================
class Color(Enum):
    pass  # TODO: WHITE / BLACK


# ============================================================
# TODO 2: Piece base + subclasses King/Queen/Rook/Bishop/Knight/Pawn.
#         Each generates its candidate moves from a square given the board.
# ============================================================
class Piece(ABC):
    @abstractmethod
    def candidate_moves(self, board, frm):  # -> list[Move]
        ...


# ============================================================
# TODO 3: Board — 8x8 state, starting position, apply_move/undo_move,
#         path-blocking, and "is square attacked by color?" query.
# ============================================================
class Board:
    def __init__(self) -> None:
        raise NotImplementedError


# ============================================================
# TODO 4: Legal-move generation — filter candidate moves that would leave own
#         king in check. Reuse this for check / checkmate / stalemate detection.
# ============================================================


# ============================================================
# TODO 5: Game — turn order, move(from,to) with validation, history, result.
#         Plus special moves: promotion + castling (+ en-passant if you can).
# ============================================================
class Game:
    def __init__(self) -> None:
        raise NotImplementedError

    def move(self, frm, to):
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement (drive a checkmate)."""
    raise NotImplementedError("Play legal moves, reject illegal ones, reach checkmate.")


if __name__ == "__main__":
    main()
