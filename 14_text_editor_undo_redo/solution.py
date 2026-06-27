"""
Problem 14: Text Editor with Undo / Redo
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Store INVERSE operations (Command), not whole-document snapshots, for O(edit-size) undo.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# TODO 1: Document — text buffer + cursor (+ optional selection). Keep cursor valid.
# ============================================================
class Document:
    def __init__(self) -> None:
        raise NotImplementedError


# ============================================================
# TODO 2: Command interface — execute(doc) / undo(doc).
#         Concrete: InsertCommand, DeleteCommand, ReplaceCommand.
#         Each captures enough state to invert itself.
# ============================================================
class Command(ABC):
    @abstractmethod
    def execute(self, doc) -> None:
        ...
    @abstractmethod
    def undo(self, doc) -> None:
        ...


# ============================================================
# TODO 3: Editor — runs commands, maintains undo + redo stacks.
#         A new edit after undo CLEARS the redo stack.
#         (Bonus) coalesce consecutive single-char inserts into one undo unit.
# ============================================================
class Editor:
    def __init__(self) -> None:
        raise NotImplementedError

    def insert(self, text: str) -> None:
        raise NotImplementedError

    def delete(self, n: int) -> None:
        raise NotImplementedError

    def undo(self) -> None:
        raise NotImplementedError

    def redo(self) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Show insert/delete/undo/redo and redo-cleared-by-new-edit.")


if __name__ == "__main__":
    main()
