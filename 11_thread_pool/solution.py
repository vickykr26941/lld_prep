"""
Problem 11: Thread Pool / Executor Service
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Correctness over cleverness: no lost tasks, no deadlock on shutdown, no busy-wait.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# TODO 1: Future — holds result OR exception, a 'done' event;
#         result(timeout) blocks until set and re-raises any captured exception.
# ============================================================
class Future:
    def result(self, timeout=None):
        raise NotImplementedError
    def is_done(self) -> bool:
        raise NotImplementedError


# ============================================================
# TODO 2: RejectionPolicy interface + ABORT / DISCARD / CALLER_RUNS impls.
#         Invoked when the bounded queue is full.
# ============================================================
class RejectionPolicy(ABC):
    @abstractmethod
    def reject(self, task, pool):
        ...


# ============================================================
# TODO 3: ThreadPool
#         - __init__(num_workers, queue_capacity, rejection_policy)
#         - submit(fn, *args) -> Future
#         - worker loop: block on queue, run task, set future result/exception
#         - shutdown(): no new tasks, drain queue, exit workers
#         - shutdown_now(): stop ASAP, return un-run tasks
#         - await_termination(timeout)
#         A task raising must NOT kill its worker.
# ============================================================
class ThreadPool:
    def __init__(self, num_workers: int, queue_capacity: int, rejection_policy: RejectionPolicy) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Show bounded concurrency, futures, rejection, clean shutdown.")


if __name__ == "__main__":
    main()
