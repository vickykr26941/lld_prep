"""
Problem 12: Task / Job Scheduler
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

One dispatcher thread + min-heap + early-wakeup. NOT one thread per job, NOT a busy poll.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# TODO 1: ScheduleStrategy interface — next_run(after_time) -> next time or None.
#         Impls: OneShot, FixedRate(interval), Cron(simple).
# ============================================================
class ScheduleStrategy(ABC):
    @abstractmethod
    def next_run(self, after_time):  # -> time or None (None = no more runs)
        ...


# ============================================================
# TODO 2: ScheduledTask — id, callable, schedule strategy, next-run time.
#         Make it heap-orderable by next-run (with a stable tie-break).
# ============================================================


# ============================================================
# TODO 3: Scheduler
#         - schedule / schedule_after / schedule_recurring / cancel
#         - min-heap of tasks by next-run time (thread-safe)
#         - ONE dispatcher thread: wait until earliest due; wake EARLY if a
#           sooner task is added (use a Condition, not fixed polling)
#         - hand due tasks to a worker pool; re-enqueue recurring tasks
#         - injectable clock; retry on failure
# ============================================================
class Scheduler:
    def __init__(self, clock=None, num_workers: int = 4) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement (deterministic clock)."""
    raise NotImplementedError("Show fire-order, early wakeup, recurring, and cancel.")


if __name__ == "__main__":
    main()
