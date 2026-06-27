"""
Problem 03: Rate Limiter
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Use an injectable clock (no real time.sleep in tests) and per-client locking.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# TODO 1: Clock abstraction — a real monotonic clock + a fake clock you can advance.
# ============================================================
class Clock(ABC):
    @abstractmethod
    def now(self) -> float:
        ...


# ============================================================
# TODO 2: RateLimiter interface
# ============================================================
class RateLimiter(ABC):
    @abstractmethod
    def allow_request(self, client_id: str) -> bool:
        ...


# ============================================================
# TODO 3: Implementations — FixedWindowCounter, SlidingWindowLog, TokenBucket.
#         Each keeps PER-CLIENT state and is thread-safe (per-client lock).
#         SlidingWindowLog must evict timestamps outside the window.
# ============================================================


# ============================================================
# TODO 4: RateLimiterConfig + RateLimiterFactory
#         Factory builds the right limiter from (algorithm, params).
# ============================================================
class RateLimiterFactory:
    @staticmethod
    def create(config) -> RateLimiter:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement (use the fake clock)."""
    raise NotImplementedError("Run the token-bucket + fixed-window burst scenarios.")


if __name__ == "__main__":
    main()
