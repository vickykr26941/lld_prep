"""
Problem 09: Notification System
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# TODO 1: NotificationChannel interface + Email / SMS / Push impls.
#         Simulate sending (log + store a "sent" record). send() may fail.
# ============================================================
class NotificationChannel(ABC):
    @abstractmethod
    def send(self, user, content) -> bool:
        ...


# ============================================================
# TODO 2: ChannelFactory — create a channel by type (no caller `new`s concretes).
# ============================================================


# ============================================================
# TODO 3: User + preferences (which channels each user accepts; muted).
# ============================================================


# ============================================================
# TODO 4: TemplateStrategy — render an event into channel-specific content.
# ============================================================
class TemplateStrategy(ABC):
    @abstractmethod
    def render(self, event, channel_type) -> str:
        ...


# ============================================================
# TODO 5: Observer — EventBus/Subject with subscribe(event_type, handler) and
#         publish(event). Producers don't know subscribers.
# ============================================================
class EventBus:
    def subscribe(self, event_type, handler) -> None:
        raise NotImplementedError
    def publish(self, event) -> None:
        raise NotImplementedError


# ============================================================
# TODO 6: Dispatcher — on event, pick users' enabled channels, render template,
#         send with RETRY + BACKOFF (injectable clock), track delivery status.
# ============================================================


# ============================================================
# TODO 7: Decorator — wrap a channel to add a cross-cutting concern
#         (audit log / rate limit) WITHOUT modifying the channel class.
# ============================================================


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Publish ORDER_SHIPPED; show prefs, retry, and decorator.")


if __name__ == "__main__":
    main()
