"""
Problem 13: In-Memory Key-Value Store with Transactions
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Nested transactions = a STACK of diff-layers. Keep count(value) efficient, not O(n).
"""
from __future__ import annotations

from typing import Optional

# ============================================================
# TODO 1: A transaction layer — pending writes, tombstones (for deletes),
#         and a value->count delta so count() stays efficient.
# ============================================================


# ============================================================
# TODO 2: KeyValueStore
#         - set(key, value) / get(key) / delete(key) / count(value)
#           resolving through base store + the stack of open txn layers
#         - begin(): push a new layer
#         - commit(): merge innermost layer into its parent (or base)
#         - rollback(): discard innermost layer; error if none open
# ============================================================
class KeyValueStore:
    def __init__(self) -> None:
        raise NotImplementedError

    def set(self, key, value) -> None:
        raise NotImplementedError

    def get(self, key) -> Optional[object]:
        raise NotImplementedError

    def delete(self, key) -> None:
        raise NotImplementedError

    def count(self, value) -> int:
        raise NotImplementedError

    def begin(self) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Run the nested set/begin/rollback/commit + count walkthrough.")


if __name__ == "__main__":
    main()
