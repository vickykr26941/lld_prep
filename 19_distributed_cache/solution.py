"""
Problem 19: Distributed Cache (Consistent Hashing)
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Adding/removing a node must remap O(keys/nodes) keys, not all of them. Use virtual nodes.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

# ============================================================
# TODO 1: HashRing with virtual nodes.
#         - add_node(node) / remove_node(node)
#         - get_nodes(key, r) -> the primary + next r-1 distinct nodes clockwise
#         Use a sorted structure of ring positions + bisect for lookup.
# ============================================================
class HashRing:
    def __init__(self, vnodes_per_node: int = 100) -> None:
        raise NotImplementedError

    def add_node(self, node) -> None:
        raise NotImplementedError

    def get_nodes(self, key, r: int) -> List:
        raise NotImplementedError


# ============================================================
# TODO 2: CacheNode (bounded; reuse an eviction policy) + BackingStore (sim DB).
# ============================================================


# ============================================================
# TODO 3: WritePolicy Strategy — write-through vs cache-aside.
# ============================================================
class WritePolicy(ABC):
    @abstractmethod
    def write(self, cache, store, key, value) -> None:
        ...


# ============================================================
# TODO 4: DistributedCache facade — get/put routing via the ring + replication.
#         Instrument add/remove-node to report how many keys remapped.
# ============================================================
class DistributedCache:
    def __init__(self, ring: HashRing, replication: int, write_policy: WritePolicy) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Show distribution, replication, and minimal remap on add/remove.")


if __name__ == "__main__":
    main()
