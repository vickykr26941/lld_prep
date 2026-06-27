"""
Problem 18: Pub/Sub Message Broker (Kafka-lite)
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Ordering is per-PARTITION. Same key -> same partition. Per-group offsets. Thread-safe.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# TODO 1: Message (key, value, offset, ts) + Partition (append-only ordered log).
#         Append assigns a monotonic offset; reads start from a given offset.
# ============================================================


# ============================================================
# TODO 2: PartitioningStrategy interface + HashByKey and RoundRobin impls.
# ============================================================
class PartitioningStrategy(ABC):
    @abstractmethod
    def partition_for(self, key, num_partitions: int) -> int:
        ...


# ============================================================
# TODO 3: Topic (P partitions) + ConsumerGroup (committed offset per partition).
# ============================================================


# ============================================================
# TODO 4: Assignor — assign partitions to consumers in a group (range / round-robin)
#         and REBALANCE when a consumer joins/leaves.
# ============================================================
class Assignor(ABC):
    @abstractmethod
    def assign(self, partitions, consumers):  # -> {consumer: [partitions]}
        ...


# ============================================================
# TODO 5: Broker — create_topic, publish, subscribe(group, consumer),
#         poll(consumer), commit(consumer). Thread-safe per-partition.
#         At-least-once: uncommitted messages redeliver after rebalance.
# ============================================================
class Broker:
    def __init__(self) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Show partitioning, group load-balancing, fan-out, redelivery.")


if __name__ == "__main__":
    main()
