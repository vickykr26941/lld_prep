"""
Problem 02: Splitwise / Expense Sharing
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Tip: store money as integer cents to avoid float drift.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List

# ============================================================
# TODO 1: Entities — User, Group, Expense
# ============================================================


# ============================================================
# TODO 2: SplitStrategy interface + EQUAL / EXACT / PERCENT impls.
#         Each computes per-participant owed amounts (in cents) and VALIDATES input.
#         Decide deterministically who absorbs the leftover cent on uneven splits.
# ============================================================
class SplitStrategy(ABC):
    @abstractmethod
    def compute_shares(self, amount_cents: int, participants, params) -> Dict[str, int]:
        """Return {user_id: owed_cents}. Must sum to amount_cents."""
        ...


# ============================================================
# TODO 3: Balance sheet — track net pairwise balances (who owes whom).
#         Adding an expense updates balances; settling reduces them.
# ============================================================


# ============================================================
# TODO 4: ExpenseManager orchestrator
#         - add_expense(paid_by, amount, participants, strategy, params)
#         - show_balances(user) / show_balances_all()
#         - settle(from_user, to_user, amount)
# ============================================================
class ExpenseManager:
    def __init__(self) -> None:
        raise NotImplementedError


# ============================================================
# TODO 5: Debt simplification — given net balances, return the MINIMAL
#         list of (debtor, creditor, amount) transactions that settle everyone.
# ============================================================
def simplify_debts(net_balances) -> List:
    raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Run the 6-step expense + simplify scenario from the README.")


if __name__ == "__main__":
    main()
