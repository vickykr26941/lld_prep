"""
Problem 08: Vending Machine
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Model states explicitly (State pattern or transition table) — no if-spaghetti.
Money in integer cents.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# TODO 1: Product, Slot/inventory, denomination model (integer cents).
# ============================================================


# ============================================================
# TODO 2: State interface — each state implements the allowed actions
#         (select_product, insert_money, dispense, cancel) and rejects the rest.
# ============================================================
class VendingMachineState(ABC):
    @abstractmethod
    def select_product(self, machine, slot_id): ...
    @abstractmethod
    def insert_money(self, machine, amount_cents): ...
    @abstractmethod
    def dispense(self, machine): ...
    @abstractmethod
    def cancel(self, machine): ...


# ============================================================
# TODO 3: Concrete states — IdleState, CollectingMoneyState, DispensingState.
# ============================================================


# ============================================================
# TODO 4: Change-making — return change from available denominations;
#         detect "exact change impossible" BEFORE dispensing.
# ============================================================


# ============================================================
# TODO 5: VendingMachine context — holds current state + inventory + coin bank,
#         delegates actions to the state, and exposes admin refill/collect.
# ============================================================
class VendingMachine:
    def __init__(self) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Run buy, out-of-stock, cancel/refund, and no-change cases.")


if __name__ == "__main__":
    main()
