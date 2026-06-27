"""
Problem 05: In-Memory Cache (LRU / LFU)
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Hot path must be O(1) — no linear scans.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

# ============================================================
# TODO 1: EvictionPolicy interface
#         e.g. record_access(key), record_insert(key), evict() -> key, remove(key)
# ============================================================
class EvictionPolicy(ABC):
    @abstractmethod
    def evict(self):  # -> key to remove
        ...


# ============================================================
# TODO 2: LRU policy — doubly-linked list + dict for O(1) move-to-front + pop-tail.
# ============================================================


# ============================================================
# TODO 3: LFU policy — frequency buckets; tie-break by least-recently-used.
# ============================================================


# ============================================================
# TODO 4: Cache facade — get(key)/put(key, value), capacity, delegates eviction
#         to the policy. Thread-safe. (Optional: TTL via injectable clock + stats.)
# ============================================================
class Cache:
    def __init__(self, capacity: int, policy: EvictionPolicy) -> None:
        raise NotImplementedError

    def get(self, key) -> Optional[object]:
        raise NotImplementedError

    def put(self, key, value) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Show LRU eviction, LFU survival, and stats.")


if __name__ == "__main__":
    main()
